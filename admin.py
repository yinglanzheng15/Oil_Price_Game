#!/usr/bin/env python
"""
Admin script to manage the Oil Price Game.

Usage:
    python admin.py --week 13 --price 75.50          # Manually set price
    python admin.py --week 13 --fetch-price           # Fetch from oilprice.com
    python admin.py --list-all                        # Show leaderboard
"""

import argparse
from database_handler import DatabaseHandler
from price_fetcher import fetch_brent_price

def main():
    parser = argparse.ArgumentParser(description='Oil Price Game Admin')
    parser.add_argument('--week', type=int, help='Week number (ISO week)')
    parser.add_argument('--price', type=float, help='Actual Brent oil price (manual entry)')
    parser.add_argument('--fetch-price', action='store_true', help='Fetch price from oilprice.com')
    parser.add_argument('--list-all', action='store_true', help='List all data')
    
    args = parser.parse_args()
    
    handler = DatabaseHandler()
    handler.initialize_database()
    
    if args.week:
        if args.fetch_price:
            print(f"\nFetching Brent crude price from oilprice.com...")
            price = fetch_brent_price()
            if price:
                print(f"✓ Found price: ${price:.2f}")
                print(f"\nSetting actual price for week {args.week}: ${price:.2f}")
                handler.set_actual_price(args.week, price)
                print("✓ Price saved successfully!")
                print("\nResults will now be calculated automatically for all predictions.")
            else:
                print("✗ Failed to fetch price from oilprice.com")
                print("Try again or use: python admin.py --week {args.week} --price 75.50")
        elif args.price:
            print(f"\nSetting actual price for week {args.week}: ${args.price:.2f}")
            handler.set_actual_price(args.week, args.price)
            print("✓ Price saved successfully!")
            print("\nResults will now be calculated automatically for all predictions.")
        else:
            print("Please provide either --price or --fetch-price")
            
    elif args.list_all:
        print("\n=== LEADERBOARD ===")
        leaderboard = handler.get_leaderboard()
        for entry in leaderboard:
            print(f"{entry['rank']}. {entry['username']}: {entry['points']} points")
            
    else:
        print("\nUsage:")
        print("  Set price manually:  python admin.py --week 13 --price 75.50")
        print("  Fetch from web:      python admin.py --week 13 --fetch-price")
        print("  Show leaderboard:    python admin.py --list-all")

if __name__ == '__main__':
    main()
