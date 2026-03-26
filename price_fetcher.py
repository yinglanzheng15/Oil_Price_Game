"""
Price fetcher module for fetching real Brent crude oil prices from oilprice.com
"""

import requests
from bs4 import BeautifulSoup
import re

def fetch_brent_price():
    """
    Fetch the current Brent crude oil price from oilprice.com
    
    Returns:
        float: Current Brent price in USD per barrel, or None if fetch fails
    """
    try:
        url = "https://oilprice.com/oil-price-charts/"
        
        # Set a user agent to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for Brent price in the page
        # oilprice.com has various price displays, try multiple selectors
        
        # Try to find price in main display
        price_text = None
        
        # Method 1: Look for span with price data
        for span in soup.find_all('span'):
            text = span.get_text(strip=True)
            # Look for pattern like "$XX.XX"
            if re.search(r'\$\d+\.\d{2}', text):
                # Check if it's near "Brent" text
                parent = span.parent
                if parent and 'Brent' in parent.get_text():
                    match = re.search(r'\$(\d+\.\d{2})', text)
                    if match:
                        return float(match.group(1))
        
        # Method 2: Look for div with price class
        for div in soup.find_all('div', class_=re.compile('price', re.I)):
            text = div.get_text()
            if 'Brent' in text:
                match = re.search(r'\$?(\d+\.\d{2})', text)
                if match:
                    return float(match.group(1))
        
        # Method 3: Generic price search
        for element in soup.find_all(re.compile('^[div|span|p]')):
            text = element.get_text()
            if 'Brent' in text:
                # Extract price from text
                match = re.search(r'\$?(\d{2,3}\.\d{2})', text)
                if match:
                    price = float(match.group(1))
                    if 0 < price < 500:  # Reasonable range
                        return price
        
        print("Warning: Could not extract price from page. Trying alternative method...")
        
        # Method 4: Look at all text and find oil price pattern
        text = soup.get_text()
        matches = re.findall(r'Brent[^$]*\$?(\d{2,3}\.\d{2})', text)
        if matches:
            return float(matches[0])
        
        return None
        
    except requests.RequestException as e:
        print(f"Error fetching price: {e}")
        return None
    except Exception as e:
        print(f"Error parsing price: {e}")
        return None

if __name__ == '__main__':
    price = fetch_brent_price()
    if price:
        print(f"Current Brent crude price: ${price:.2f}")
    else:
        print("Failed to fetch price")
