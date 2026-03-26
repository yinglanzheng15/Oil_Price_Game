"""
SQLite database handler for the Oil Price Game - works well locally and in cloud.
This replaces the Excel-based storage for better multi-user support.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class DatabaseHandler:
    def __init__(self, db_path='game_data.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize_database(self):
        """Create database and tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                joined_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                week INTEGER NOT NULL,
                price_guess REAL NOT NULL,
                submitted_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username),
                UNIQUE(username, week)
            )
        ''')
        
        # Results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER UNIQUE NOT NULL,
                actual_price REAL NOT NULL,
                updated_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, username, password):
        """Add a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            conn.commit()
        finally:
            conn.close()
    
    def user_exists(self, username):
        """Check if user exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM users WHERE username = ?', (username,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return check_password_hash(row['password_hash'], password)
        return False
    
    def add_prediction(self, username, week, price_guess):
        """Add or update a prediction for the week"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT OR REPLACE INTO predictions (username, week, price_guess, submitted_date) VALUES (?, ?, ?, CURRENT_TIMESTAMP)',
                (username, week, price_guess)
            )
            conn.commit()
        finally:
            conn.close()
    
    def has_submitted_this_week(self, username, week):
        """Check if user has submitted prediction for this week"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT 1 FROM predictions WHERE username = ? AND week = ?',
            (username, week)
        )
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    def get_week_predictions(self, week):
        """Get all predictions for a week"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT username, week, price_guess, submitted_date FROM predictions WHERE week = ?',
            (week,)
        )
        predictions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return predictions
    
    def set_actual_price(self, week, actual_price):
        """Set the actual end-of-week price"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT OR REPLACE INTO results (week, actual_price, updated_date) VALUES (?, ?, CURRENT_TIMESTAMP)',
                (week, actual_price)
            )
            conn.commit()
        finally:
            conn.close()
    
    def get_actual_price(self, week):
        """Get actual price for a week"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT actual_price FROM results WHERE week = ?', (week,))
        row = cursor.fetchone()
        conn.close()
        return row['actual_price'] if row else None
    
    def get_user_stats(self, username):
        """Get user's cumulative stats"""
        from scoring import calculate_points
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get all predictions for this user
        cursor.execute(
            'SELECT week, price_guess FROM predictions WHERE username = ?',
            (username,)
        )
        predictions = cursor.fetchall()
        
        total_points = 0
        weeks_participated = 0
        
        for pred in predictions:
            week = pred['week']
            guess = pred['price_guess']
            
            cursor.execute('SELECT actual_price FROM results WHERE week = ?', (week,))
            result = cursor.fetchone()
            
            if result:
                points = calculate_points(guess, result['actual_price'])
                total_points += points
                weeks_participated += 1
        
        conn.close()
        return {
            'total_points': total_points,
            'weeks_participated': weeks_participated
        }
    
    def get_leaderboard(self):
        """Get current leaderboard"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get all users
        cursor.execute('SELECT username FROM users ORDER BY username')
        users = [row['username'] for row in cursor.fetchall()]
        
        scores = {}
        for username in users:
            stats = self.get_user_stats(username)
            scores[username] = stats['total_points']
        
        conn.close()
        
        # Sort by points
        leaderboard = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [{'rank': i+1, 'username': name, 'points': points} 
                for i, (name, points) in enumerate(leaderboard)]
