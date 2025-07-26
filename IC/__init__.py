"""
IC Package - Digital Logic Design
TTL 7400 Series Integrated Circuits

This package contains implementations of common 7400 series TTL logic ICs
using object-oriented programming and modular design.

Available ICs:

Basic Logic Gates:
- 7400: Quad 2-Input NAND Gates
- 7402: Quad 2-Input NOR Gates  
- 7404: Hex Inverter (NOT Gates)
- 7408: Quad 2-Input AND Gates
- 7432: Quad 2-Input OR Gates
- 7486: Quad 2-Input XOR Gates
- 7410: Triple 3-Input NAND Gates
- 7420: Dual 4-Input NAND Gates
- 7430: Single 8-Input NAND Gate

Advanced Data Processing ICs:
- 74138: 3-to-8 Line Decoder/Demultiplexer
- 74139: Dual 2-to-4 Line Decoder/Demultiplexer
- 74147: 10-to-4 Line Priority Encoder (Decimal to BCD)
- 74148: 8-to-3 Line Priority Encoder with Cascade
- 74150: 16-to-1 Line Data Selector/Multiplexer
- 74151: 8-to-1 Line Data Selector/Multiplexer
- 74153: Dual 4-to-1 Line Data Selector/Multiplexer
- 74157: Quad 2-to-1 Line Data Selector/Multiplexer

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
from .ic_74138 import IC74138
from .ic_74139 import IC74139
from .ic_74147 import IC74147
from .ic_74148 import IC74148
from .ic_74150 import IC74150
from .ic_74151 import IC74151
from .ic_74153 import IC74153
from .ic_74157 import IC74157
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
    'IC74138',
    'IC74139',
    'IC74147',
    'IC74148',
    'IC74150',
    'IC74151',
    'IC74153',
    'IC74157',
    'ICTestSuite'
]

# Package metadata
__version__ = "1.0.0"
__author__ = "Digital Logic Design Library"
__description__ = "TTL 7400 Series IC Implementations"

# IC catalog for easy reference
IC_CATALOG = {
    # Basic Logic Gates
    '7400': {
        'class': IC7400,
        'description': 'Quad 2-Input NAND Gates',
        'category': 'Logic Gates',
        'gates': 4,
        'inputs_per_gate': 2,
        'logic': 'NAND'
    },
    '7402': {
        'class': IC7402,
        'description': 'Quad 2-Input NOR Gates',
        'category': 'Logic Gates',
        'gates': 4,
        'inputs_per_gate': 2,
        'logic': 'NOR'
    },
    '7404': {
        'class': IC7404,
        'description': 'Hex Inverter (NOT Gates)',
        'category': 'Logic Gates',
        'gates': 6,
        'inputs_per_gate': 1,
        'logic': 'NOT'
    },
    '7408': {
        'class': IC7408,
        'description': 'Quad 2-Input AND Gates',
        'category': 'Logic Gates',
        'gates': 4,
        'inputs_per_gate': 2,
        'logic': 'AND'
    },
    '7432': {
        'class': IC7432,
        'description': 'Quad 2-Input OR Gates',
        'category': 'Logic Gates',
        'gates': 4,
        'inputs_per_gate': 2,
        'logic': 'OR'
    },
    '7486': {
        'class': IC7486,
        'description': 'Quad 2-Input XOR Gates',
        'category': 'Logic Gates',
        'gates': 4,
        'inputs_per_gate': 2,
        'logic': 'XOR'
    },
    '7410': {
        'class': IC7410,
        'description': 'Triple 3-Input NAND Gates',
        'category': 'Logic Gates',
        'gates': 3,
        'inputs_per_gate': 3,
        'logic': 'NAND'
    },
    '7420': {
        'class': IC7420,
        'description': 'Dual 4-Input NAND Gates',
        'category': 'Logic Gates',
        'gates': 2,
        'inputs_per_gate': 4,
        'logic': 'NAND'
    },
    '7430': {
        'class': IC7430,
        'description': 'Single 8-Input NAND Gate',
        'category': 'Logic Gates',
        'gates': 1,
        'inputs_per_gate': 8,
        'logic': 'NAND'
    },
    
    # Advanced Data Processing ICs
    '74138': {
        'class': IC74138,
        'description': '3-to-8 Line Decoder/Demultiplexer',
        'category': 'Decoders',
        'inputs': 3,
        'outputs': 8,
        'function': 'Binary to Decimal Decoder'
    },
    '74139': {
        'class': IC74139,
        'description': 'Dual 2-to-4 Line Decoder/Demultiplexer',
        'category': 'Decoders',
        'inputs': '2x2',
        'outputs': '2x4',
        'function': 'Dual Binary Decoder'
    },
    '74147': {
        'class': IC74147,
        'description': '10-to-4 Line Priority Encoder (Decimal to BCD)',
        'category': 'Encoders',
        'inputs': 10,
        'outputs': 4,
        'function': 'Decimal to BCD Priority Encoder'
    },
    '74148': {
        'class': IC74148,
        'description': '8-to-3 Line Priority Encoder with Cascade',
        'category': 'Encoders',
        'inputs': 8,
        'outputs': 3,
        'function': 'Octal Priority Encoder'
    },
    '74150': {
        'class': IC74150,
        'description': '16-to-1 Line Data Selector/Multiplexer',
        'category': 'Multiplexers',
        'inputs': 16,
        'outputs': 1,
        'function': '16-to-1 Data Selector'
    },
    '74151': {
        'class': IC74151,
        'description': '8-to-1 Line Data Selector/Multiplexer',
        'category': 'Multiplexers',
        'inputs': 8,
        'outputs': 1,
        'function': '8-to-1 Data Selector'
    },
    '74153': {
        'class': IC74153,
        'description': 'Dual 4-to-1 Line Data Selector/Multiplexer',
        'category': 'Multiplexers',
        'inputs': '2x4',
        'outputs': '2x1',
        'function': 'Dual 4-to-1 Data Selector'
    },
    '74157': {
        'class': IC74157,
        'description': 'Quad 2-to-1 Line Data Selector/Multiplexer',
        'category': 'Multiplexers',
        'inputs': '4x2',
        'outputs': '4x1',
        'function': 'Quad 2-to-1 Data Selector'
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
    print("=" * 50)
    
    # Group by category
    categories = {}
    for ic_num, info in IC_CATALOG.items():
        category = info.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append((ic_num, info))
    
    # Display by category
    for category, ics in categories.items():
        print(f"\n{category}:")
        print("-" * len(category))
        for ic_num, info in ics:
            print(f"{ic_num}: {info['description']}")
            if 'gates' in info:
                print(f"       Gates: {info['gates']}, Inputs per gate: {info['inputs_per_gate']}, Logic: {info['logic']}")
            elif 'function' in info:
                inputs = info.get('inputs', 'N/A')
                outputs = info.get('outputs', 'N/A')
                print(f"       Function: {info['function']}, Inputs: {inputs}, Outputs: {outputs}")
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
