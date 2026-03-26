from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from database_handler import DatabaseHandler
from scoring import calculate_points
from utils import get_week_number
from price_fetcher import fetch_brent_price

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'oil-price-game-secret-key-change-in-production')
handler = DatabaseHandler()

# Home page
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('register.html', error='Username and password required')
        
        if handler.user_exists(username):
            return render_template('register.html', error='Username already exists')
        
        handler.add_user(username, password)
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if handler.verify_user(username, password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    leaderboard = handler.get_leaderboard()
    user_stats = handler.get_user_stats(user)
    week_number = get_week_number()
    
    # Check if user has already submitted for this week
    submitted = handler.has_submitted_this_week(user, week_number)
    
    return render_template('dashboard.html', 
                         user=user, 
                         leaderboard=leaderboard,
                         user_stats=user_stats,
                         week_number=week_number,
                         submitted=submitted)

# Submit prediction
@app.route('/submit-prediction', methods=['POST'])
def submit_prediction():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user = session['user']
    try:
        price_guess = float(request.form.get('price_guess'))
        week = get_week_number()
        
        if not (0 < price_guess < 500):  # Reasonable oil price range
            return jsonify({'error': 'Price must be between 0 and 500'}), 400
        
        handler.add_prediction(user, week, price_guess)
        return jsonify({'success': True, 'message': 'Prediction submitted!'})
    except ValueError:
        return jsonify({'error': 'Invalid price value'}), 400

# Get results for a week
@app.route('/results/<int:week>')
def results(week):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    actual_price = handler.get_actual_price(week)
    
    if actual_price is None:
        return render_template('results.html', week=week, error='Results not yet available')
    
    predictions = handler.get_week_predictions(week)
    scored = []
    
    for pred in predictions:
        points = calculate_points(pred['guess'], actual_price)
        scored.append({
            'username': pred['username'],
            'guess': pred['guess'],
            'points': points
        })
    
    # Sort by points descending
    scored.sort(key=lambda x: x['points'], reverse=True)
    
    return render_template('results.html', 
                         week=week, 
                         actual_price=actual_price,
                         results=scored)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# API: Fetch current price from web
@app.route('/api/fetch-price')
def api_fetch_price():
    """Fetch current Brent price from oilprice.com"""
    try:
        price = fetch_brent_price()
        if price:
            return jsonify({'success': True, 'price': price})
        else:
            return jsonify({'success': False, 'error': 'Could not fetch price'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    handler.initialize_database()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get('FLASK_ENV') == 'development', host='0.0.0.0', port=port)
