"""
IC Registry and Configuration
Manages all available IC classes and their categorization
"""

# Import IC classes
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from IC.ic_7400 import IC7400
from IC.ic_7402 import IC7402
from IC.ic_7404 import IC7404
from IC.ic_7408 import IC7408
from IC.ic_7410 import IC7410
from IC.ic_7420 import IC7420
from IC.ic_7430 import IC7430
from IC.ic_7432 import IC7432
from IC.ic_7486 import IC7486
from IC.ic_74138 import IC74138
from IC.ic_74139 import IC74139
from IC.ic_74147 import IC74147
from IC.ic_74148 import IC74148
from IC.ic_74150 import IC74150
from IC.ic_74151 import IC74151
from IC.ic_74153 import IC74153
from IC.ic_74157 import IC74157

# IC Registry
IC_CLASSES = {
    '7400': IC7400,
    '7402': IC7402,
    '7404': IC7404,
    '7408': IC7408,
    '7410': IC7410,
    '7420': IC7420,
    '7430': IC7430,
    '7432': IC7432,
    '7486': IC7486,
    '74138': IC74138,
    '74139': IC74139,
    '74147': IC74147,
    '74148': IC74148,
    '74150': IC74150,
    '74151': IC74151,
    '74153': IC74153,
    '74157': IC74157,
}

# IC Categories
IC_CATEGORIES = {
    'Logic Gates': ['7400', '7402', '7404', '7408', '7410', '7420', '7430', '7432', '7486'],
    'Decoders': ['74138', '74139'],
    'Encoders': ['74147', '74148'],
    'Multiplexers': ['74150', '74151', '74153', '74157']
}

def get_ic_class(ic_type):
    """Get IC class by type"""
    return IC_CLASSES.get(ic_type)

def get_all_ic_types():
    """Get all available IC types"""
    return list(IC_CLASSES.keys())

def get_ic_categories():
    """Get IC categories"""
    return IC_CATEGORIES

def create_ic_instance(ic_type):
    """Create and power up an IC instance"""
    ic_class = get_ic_class(ic_type)
    if ic_class:
        ic = ic_class()
        ic.connect_power()
        return ic
    return None
