"""
IC Test Suite and Demonstration
Digital Logic Design - TTL 7400 Series IC Collection

Comprehensive testing and demonstration of all implemented 7400 series ICs.
This module provides automated testing, interactive demos, and comparison tools.
"""

import sys
import os

# Import all IC classes
from .ic_7400 import IC7400
from .ic_7402 import IC7402
from .ic_7404 import IC7404
from .ic_7408 import IC7408
from .ic_7432 import IC7432
from .ic_7486 import IC7486
from .ic_7410 import IC7410
from .ic_7420 import IC7420
from .ic_7430 import IC7430

class ICTestSuite:
    """
    Comprehensive test suite for all 7400 series ICs
    """
    
    def __init__(self):
        """Initialize test suite with all IC types"""
        self.ics = {
            '7400': IC7400,
            '7402': IC7402,
            '7404': IC7404,
            '7408': IC7408,
            '7432': IC7432,
            '7486': IC7486,
            '7410': IC7410,
            '7420': IC7420,
            '7430': IC7430
        }
        
        self.test_results = {}
    
    def test_all_ics(self):
        """Test all ICs and return summary"""
        print("=" * 80)
        print("7400 SERIES IC TEST SUITE")
        print("=" * 80)
        
        passed_count = 0
        total_count = len(self.ics)
        
        for ic_name, ic_class in self.ics.items():
            print(f"\n{'='*20} Testing {ic_name} {'='*20}")
            
            try:
                # Create and power the IC
                ic = ic_class()
                ic.connect_power()
                
                # Run the test
                result = ic.test_ic()
                self.test_results[ic_name] = result
                
                if result:
                    passed_count += 1
                    print(f"{ic_name}: ✅ PASS")
                else:
                    print(f"{ic_name}: ❌ FAIL")
                    
            except Exception as e:
                print(f"{ic_name}: ❌ ERROR - {str(e)}")
                self.test_results[ic_name] = False
        
        # Print summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Total ICs tested: {total_count}")
        print(f"Passed: {passed_count}")
        print(f"Failed: {total_count - passed_count}")
        print(f"Success rate: {(passed_count/total_count)*100:.1f}%")
        
        # Detailed results
        print("\nDetailed Results:")
        for ic_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {ic_name}: {status}")
        
        return passed_count == total_count
    
    def demonstrate_ic(self, ic_name):
        """Demonstrate a specific IC"""
        if ic_name not in self.ics:
            print(f"IC {ic_name} not found. Available: {list(self.ics.keys())}")
            return
        
        ic_class = self.ics[ic_name]
        ic = ic_class()
        
        print(f"\n{'='*60}")
        print(f"DEMONSTRATION: {ic_name}")
        print(f"{'='*60}")
        
        # Show pinout
        print(ic.get_pinout_diagram())
        
        # Connect power
        print("Connecting power...")
        ic.connect_power()
        
        # Run tests
        ic.test_ic()
        
        # Show truth table
        print(ic.get_truth_table())
        
        return ic
    
    def compare_logic_families(self):
        """Compare different logic gate families"""
        print("\n" + "=" * 80)
        print("LOGIC GATE FAMILY COMPARISON")
        print("=" * 80)
        
        families = {
            'AND Family': ['7408'],
            'OR Family': ['7432'],
            'NOT Family': ['7404'],
            'NAND Family': ['7400', '7410', '7420', '7430'],
            'NOR Family': ['7402'],
            'XOR Family': ['7486']
        }
        
        for family_name, ic_list in families.items():
            print(f"\n{family_name}:")
            for ic_name in ic_list:
                ic_class = self.ics[ic_name]
                ic = ic_class()
                print(f"  {ic_name}: {ic.description}")
    
    def interactive_mode(self):
        """Interactive testing mode"""
        print("\n" + "=" * 60)
        print("INTERACTIVE IC TESTING MODE")
        print("=" * 60)
        print("Available ICs:", ", ".join(self.ics.keys()))
        print("Commands:")
        print("  test <ic_name>  - Test specific IC")
        print("  demo <ic_name>  - Demonstrate IC")
        print("  list           - List all ICs")
        print("  compare        - Compare logic families")
        print("  testall        - Test all ICs")
        print("  quit           - Exit")
        
        while True:
            try:
                command = input("\nEnter command: ").strip().lower()
                
                if command == 'quit':
                    break
                elif command == 'list':
                    print("Available ICs:")
                    for ic_name, ic_class in self.ics.items():
                        ic = ic_class()
                        print(f"  {ic_name}: {ic.description}")
                elif command == 'compare':
                    self.compare_logic_families()
                elif command == 'testall':
                    self.test_all_ics()
                elif command.startswith('test '):
                    ic_name = command.split()[1].upper()
                    if ic_name in self.ics:
                        ic = self.ics[ic_name]()
                        ic.connect_power()
                        ic.test_ic()
                    else:
                        print(f"IC {ic_name} not found")
                elif command.startswith('demo '):
                    ic_name = command.split()[1].upper()
                    self.demonstrate_ic(ic_name)
                else:
                    print("Unknown command. Type 'quit' to exit.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {str(e)}")

def logic_gate_showcase():
    """Showcase different logic operations using the ICs"""
    print("\n" + "=" * 80)
    print("LOGIC GATE SHOWCASE")
    print("=" * 80)
    
    # Create instances of different ICs
    nand_ic = IC7400()
    and_ic = IC7408()
    or_ic = IC7432()
    xor_ic = IC7486()
    not_ic = IC7404()
    
    # Power them all
    for ic in [nand_ic, and_ic, or_ic, xor_ic, not_ic]:
        ic.connect_power()
    
    print("\nBasic Logic Operations Comparison:")
    print("-" * 40)
    
    test_inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    print("A B | AND | OR | NAND | XOR | NOT A")
    print("-" * 35)
    
    for a, b in test_inputs:
        and_out = and_ic.get_gate_output(1, a, b)
        or_out = or_ic.get_gate_output(1, a, b)
        nand_out = nand_ic.get_gate_output(1, a, b)
        xor_out = xor_ic.get_gate_output(1, a, b)
        not_out = not_ic.get_gate_output(1, a)
        
        print(f"{a} {b} |  {and_out}  |  {or_out} |   {nand_out}  |  {xor_out}  |   {not_out}")

def digital_circuit_examples():
    """Show examples of common digital circuits using the ICs"""
    print("\n" + "=" * 80)
    print("DIGITAL CIRCUIT EXAMPLES")
    print("=" * 80)
    
    # Example 1: Half Adder using XOR and AND
    print("\nExample 1: Half Adder (Sum and Carry)")
    print("-" * 40)
    xor_ic = IC7486()  # For sum
    and_ic = IC7408()  # For carry
    xor_ic.connect_power()
    and_ic.connect_power()
    
    print("A B | Sum | Carry")
    print("-" * 16)
    for a in [0, 1]:
        for b in [0, 1]:
            sum_out = xor_ic.get_gate_output(1, a, b)  # A XOR B
            carry_out = and_ic.get_gate_output(1, a, b)  # A AND B
            print(f"{a} {b} |  {sum_out}  |   {carry_out}")
    
    # Example 2: Decoder using NAND gates
    print("\nExample 2: 2-to-4 Decoder (using NAND gates)")
    print("-" * 45)
    nand_ic = IC7400()
    not_ic = IC7404()
    nand_ic.connect_power()
    not_ic.connect_power()
    
    print("A B | Y0 | Y1 | Y2 | Y3")
    print("-" * 20)
    for a in [0, 1]:
        for b in [0, 1]:
            # Inverted inputs
            not_a = not_ic.get_gate_output(1, a)
            not_b = not_ic.get_gate_output(2, b)
            
            # Decoder outputs (active low)
            y0 = nand_ic.get_gate_output(1, not_a, not_b)  # !A AND !B
            y1 = nand_ic.get_gate_output(2, not_a, b)      # !A AND B
            y2 = nand_ic.get_gate_output(3, a, not_b)      # A AND !B
            y3 = nand_ic.get_gate_output(4, a, b)          # A AND B
            
            print(f"{a} {b} | {1-y0}  | {1-y1}  | {1-y2}  | {1-y3}")

def main():
    """Main demonstration function"""
    print("Welcome to the 7400 Series IC Test Suite!")
    print("=" * 50)
    
    # Create test suite
    test_suite = ICTestSuite()
    
    # Menu system
    while True:
        print("\nSelect an option:")
        print("1. Test all ICs")
        print("2. Demonstrate specific IC")
        print("3. Logic gate showcase")
        print("4. Digital circuit examples")
        print("5. Compare logic families")
        print("6. Interactive mode")
        print("7. Exit")
        
        try:
            choice = input("\nEnter choice (1-7): ").strip()
            
            if choice == '1':
                test_suite.test_all_ics()
            elif choice == '2':
                ic_name = input("Enter IC name (e.g., 7400): ").strip().upper()
                test_suite.demonstrate_ic(ic_name)
            elif choice == '3':
                logic_gate_showcase()
            elif choice == '4':
                digital_circuit_examples()
            elif choice == '5':
                test_suite.compare_logic_families()
            elif choice == '6':
                test_suite.interactive_mode()
            elif choice == '7':
                print("Thank you for using the IC Test Suite!")
                break
            else:
                print("Invalid choice. Please enter 1-7.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
