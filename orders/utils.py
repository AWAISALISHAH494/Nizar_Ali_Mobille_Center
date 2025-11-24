"""
Utility functions for order processing.
"""

from decimal import Decimal

# Delivery charges for Pakistan cities (in PKR)
# Major cities have lower charges, smaller cities/towns have higher charges
DELIVERY_CHARGES = {
    # Major cities - Lower charges (Rs. 150-200)
    'karachi': Decimal('150.00'),
    'lahore': Decimal('150.00'),
    'islamabad': Decimal('150.00'),
    'rawalpindi': Decimal('150.00'),
    'faisalabad': Decimal('180.00'),
    'multan': Decimal('180.00'),
    'peshawar': Decimal('180.00'),
    'quetta': Decimal('200.00'),
    'sialkot': Decimal('180.00'),
    'gujranwala': Decimal('180.00'),
    'hyderabad': Decimal('180.00'),
    'sargodha': Decimal('200.00'),
    
    # Medium cities - Medium charges (Rs. 200-250)
    'bahawalpur': Decimal('200.00'),
    'sukkur': Decimal('200.00'),
    'larkana': Decimal('200.00'),
    'sheikhupura': Decimal('200.00'),
    'raiwind': Decimal('200.00'),
    'gujrat': Decimal('200.00'),
    'kasur': Decimal('200.00'),
    'sahiwal': Decimal('200.00'),
    'okara': Decimal('200.00'),
    'sadiqabad': Decimal('220.00'),
    'mianwali': Decimal('220.00'),
    'burewala': Decimal('220.00'),
    
    # Default for other cities/towns - Higher charges (Rs. 250-300)
    'default': Decimal('250.00'),
}

# Free delivery threshold (if cart total exceeds this amount, delivery is free)
FREE_DELIVERY_THRESHOLD = Decimal('5000.00')


def calculate_delivery_charges(city, cart_total=Decimal('0.00')):
    """
    Calculate delivery charges based on city and cart total.
    
    Args:
        city (str): City name (case-insensitive)
        cart_total (Decimal): Total cart amount in PKR
    
    Returns:
        Decimal: Delivery charges in PKR
    """
    if cart_total >= FREE_DELIVERY_THRESHOLD:
        return Decimal('0.00')
    
    # Normalize city name (lowercase, strip whitespace)
    city_normalized = city.lower().strip() if city else ''
    
    # Check if city exists in delivery charges dictionary
    delivery_charge = DELIVERY_CHARGES.get(city_normalized, DELIVERY_CHARGES['default'])
    
    return delivery_charge


def get_pakistan_cities():
    """
    Get list of major Pakistan cities for dropdown.
    
    Returns:
        list: List of city names
    """
    return sorted([
        'Karachi', 'Lahore', 'Islamabad', 'Rawalpindi', 'Faisalabad',
        'Multan', 'Peshawar', 'Quetta', 'Sialkot', 'Gujranwala',
        'Hyderabad', 'Sargodha', 'Bahawalpur', 'Sukkur', 'Larkana',
        'Sheikhupura', 'Raiwind', 'Gujrat', 'Kasur', 'Sahiwal',
        'Okara', 'Sadiqabad', 'Mianwali', 'Burewala'
    ])




