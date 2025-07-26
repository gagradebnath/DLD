"""
IC Package - Digital Logic Design
TTL 7400 Series Integrated Circuits

This package contains implementations of common 7400 series TTL logic ICs
using object-oriented programming and modular design.

Available ICs:
- 7400: Quad 2-Input NAND Gates
- 7402: Quad 2-Input NOR Gates  
- 7404: Hex Inverter (NOT Gates)
- 7408: Quad 2-Input AND Gates
- 7432: Quad 2-Input OR Gates
- 7486: Quad 2-Input XOR Gates
- 7410: Triple 3-Input NAND Gates
- 7420: Dual 4-Input NAND Gates
- 7430: Single 8-Input NAND Gate

Usage:
    from IC.ic_7400 import IC7400
    
    # Create and power the IC
    ic = IC7400()
    ic.connect_power()
    
    # Test the IC
    ic.test_ic()
    
    # Use individual gates
    output = ic.get_gate_output(1, 1, 0)  # Gate 1: 1 NAND 0 = 1
"""

# Import all IC classes for easy access
from .base_ic import BaseIC
from .ic_7400 import IC7400
from .ic_7402 import IC7402
from .ic_7404 import IC7404
from .ic_7408 import IC7408
from .ic_7432 import IC7432
from .ic_7486 import IC7486
from .ic_7410 import IC7410
from .ic_7420 import IC7420
from .ic_7430 import IC7430
from .ic_test_suite import ICTestSuite

# Define what gets imported with "from IC import *"
__all__ = [
    'BaseIC',
    'IC7400',
    'IC7402', 
    'IC7404',
    'IC7408',
    'IC7432',
    'IC7486',
    'IC7410',
    'IC7420',
    'IC7430',
    'ICTestSuite'
]

# Package metadata
__version__ = "1.0.0"
__author__ = "Digital Logic Design Library"
__description__ = "TTL 7400 Series IC Implementations"

# IC catalog for easy reference
IC_CATALOG = {
    '7400': {
        'class': IC7400,
        'description': 'Quad 2-Input NAND Gates',
        'gates': 4,
        'inputs_per_gate': 2,
        'logic': 'NAND'
    },
    '7402': {
        'class': IC7402,
        'description': 'Quad 2-Input NOR Gates',
        'gates': 4,
        'inputs_per_gate': 2,
        'logic': 'NOR'
    },
    '7404': {
        'class': IC7404,
        'description': 'Hex Inverter (NOT Gates)',
        'gates': 6,
        'inputs_per_gate': 1,
        'logic': 'NOT'
    },
    '7408': {
        'class': IC7408,
        'description': 'Quad 2-Input AND Gates',
        'gates': 4,
        'inputs_per_gate': 2,
        'logic': 'AND'
    },
    '7432': {
        'class': IC7432,
        'description': 'Quad 2-Input OR Gates',
        'gates': 4,
        'inputs_per_gate': 2,
        'logic': 'OR'
    },
    '7486': {
        'class': IC7486,
        'description': 'Quad 2-Input XOR Gates',
        'gates': 4,
        'inputs_per_gate': 2,
        'logic': 'XOR'
    },
    '7410': {
        'class': IC7410,
        'description': 'Triple 3-Input NAND Gates',
        'gates': 3,
        'inputs_per_gate': 3,
        'logic': 'NAND'
    },
    '7420': {
        'class': IC7420,
        'description': 'Dual 4-Input NAND Gates',
        'gates': 2,
        'inputs_per_gate': 4,
        'logic': 'NAND'
    },
    '7430': {
        'class': IC7430,
        'description': 'Single 8-Input NAND Gate',
        'gates': 1,
        'inputs_per_gate': 8,
        'logic': 'NAND'
    }
}

def get_ic(ic_number):
    """
    Factory function to create IC instances
    
    Args:
        ic_number (str): IC part number (e.g., "7400")
        
    Returns:
        BaseIC: IC instance
    """
    if ic_number in IC_CATALOG:
        ic_class = IC_CATALOG[ic_number]['class']
        return ic_class()
    else:
        raise ValueError(f"IC {ic_number} not available. Available: {list(IC_CATALOG.keys())}")

def list_ics():
    """List all available ICs with descriptions"""
    print("Available 7400 Series ICs:")
    print("=" * 40)
    for ic_num, info in IC_CATALOG.items():
        print(f"{ic_num}: {info['description']}")
        print(f"       Gates: {info['gates']}, Inputs per gate: {info['inputs_per_gate']}, Logic: {info['logic']}")
        print()

def quick_test():
    """Quick test of all ICs"""
    print("Quick Test of All ICs")
    print("=" * 30)
    
    for ic_num in IC_CATALOG.keys():
        try:
            ic = get_ic(ic_num)
            ic.connect_power()
            result = ic.test_ic()
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{ic_num}: {status}")
        except Exception as e:
            print(f"{ic_num}: ❌ ERROR - {str(e)}")

if __name__ == "__main__":
    print(__doc__)
    list_ics()
