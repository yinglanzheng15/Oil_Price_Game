# Oil Price Game

A weekly oil price prediction game with a point-scoring system. Players estimate the weekly Brent crude oil price and compete on accuracy.

> **🚀 Want to deploy online?** See [DEPLOY.md](DEPLOY.md) to put this on the web and share a link!

## Features

- **User Registration & Login**: Simple authentication stored in Excel
- **Weekly Predictions**: Submit price estimates each week
- **Automated Scoring**: Points awarded based on guess accuracy
  - Perfect (within $0.01): 1000 points
  - Within $1: 500 - (100 * distance)
  - Within $5: 250 - (50 * distance)
  - Within $10: 100 - (10 * distance)
  - Beyond $10: 0 points
- **Leaderboard**: See cumulative scores and rankings
- **Local Storage**: All data stored in Excel (game_data.xlsx)

## Setup & Installation

### Prerequisites
- Python 3.8+ installed on your computer

### Steps

1. **Clone/Download the project** to `c:\code\Oil_Price_Game`

2. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run the app**:
   ```
   python app.py
   ```

5. **Open in browser**:
   - Visit `http://localhost:5000`
   - Register a new account
   - Submit weekly predictions

## Managing Weekly Prices

You can set the actual end-of-week oil price in two ways:

**Option 1: Fetch automatically from oilprice.com**
```
python admin.py --week 13 --fetch-price
```

**Option 2: Enter price manually**
```
python admin.py --week 13 --price 75.50
```

Once the price is set:
- Results become available
- All players' scores are automatically calculated
- Scores appear on the leaderboard

## File Structure

```
Oil_Price_Game/
├── app.py                  # Main Flask application
├── database_handler.py     # SQLite database management
├── scoring.py              # Point calculation logic
├── admin.py               # Admin CLI for setting prices
├── price_fetcher.py       # Fetches live prices from oilprice.com
├── utils.py               # Helper functions
├── requirements.txt       # Python dependencies
├── Procfile               # Railway deployment config
├── runtime.txt            # Python version
├── README.md              # This file
├── DEPLOY.md              # Deployment instructions
├── templates/             # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── results.html
├── static/                # CSS and JS
│   └── style.css
└── game_data.db          # SQLite database (auto-created)
```

## How It Works

1. Users register with a username/password
2. Each week, users submit their oil price estimate
3. At end of week, admin fetches the actual price from oilprice.com using `admin.py --week 13 --fetch-price`
4. System calculates points for each player automatically
5. Results show on the leaderboard
6. Cumulative scores display based on performance

## Troubleshooting

**Port already in use**: Edit `app.py` line 93 to change the port:
```python
app.run(debug=True, port=5001)  # Use 5001 instead of 5000
```

**Excel file locked**: Close any Excel applications that have `game_data.xlsx` open

**ModuleNotFoundError**: Make sure you've installed requirements: `pip install -r requirements.txt`
