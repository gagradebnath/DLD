"""
Quick test for K-Map fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from combinational_circuits.karnaugh_map import KarnaughMap

def test_kmap_fix():
    print("Testing K-Map with Full Adder Sum function...")
    print("Minterms: [1, 2, 4, 7]")
    
    try:
        kmap = KarnaughMap(3)
        kmap.variables = ['A', 'B', 'Cin']
        kmap.set_function_from_minterms([1, 2, 4, 7])
        
        print("K-Map created successfully")
        print(kmap.display_kmap())
        
        print("Finding prime implicants...")
        prime_implicants = kmap.find_prime_implicants()
        print(f"Prime implicants found: {len(prime_implicants)}")
        for pi in prime_implicants:
            print(f"  {pi}")
        
        print("Minimizing expression...")
        result = kmap.minimize_expression()
        print(f"✅ Success! Simplified Expression: {result['simplified_expression']}")
        print(f"Cost: {result['cost']} terms")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_kmap_fix()
