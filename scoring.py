def calculate_points(guess, actual_price):
    """
    Calculate points based on accuracy of guess.
    
    Scoring system:
    - Perfect (within $0.01): 1000 points
    - Within $1: 500 - (100 * distance)
    - Within $5: 250 - (50 * distance)
    - Within $10: 100 - (10 * distance)
    - Beyond $10: 0 points
    """
    difference = abs(guess - actual_price)
    
    if difference <= 0.01:
        return 1000
    elif difference <= 1:
        return max(0, int(500 - (100 * difference)))
    elif difference <= 5:
        return max(0, int(250 - (50 * difference)))
    elif difference <= 10:
        return max(0, int(100 - (10 * difference)))
    else:
        return 0
