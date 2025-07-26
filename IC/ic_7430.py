"""
7430 IC - Single 8-Input NAND Gate
Digital Logic Design - TTL 7400 Series

The 7430 contains one 8-input NAND gate.
Pin Configuration (DIP-14):
- VCC: Pin 14
- GND: Pin 7
- 1 NAND gate with 8 inputs
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basic_gates'))
from .base_ic import BaseIC
from NAND import NANDGate

class IC7430(BaseIC):
    """
    7430 IC - Single 8-Input NAND Gate
    
    Pin Configuration:
    Pin 1: A (Input A)
    Pin 2: B (Input B)
    Pin 3: C (Input C)
    Pin 4: D (Input D)
    Pin 5: E (Input E)
    Pin 6: F (Input F)
    Pin 7: GND
    Pin 8: Y (Output)
    Pin 9: NC (Not Connected)
    Pin 10: NC (Not Connected)
    Pin 11: G (Input G)
    Pin 12: H (Input H)
    Pin 13: NC (Not Connected)
    Pin 14: VCC
    """
    
    def __init__(self):
        super().__init__("7430", "DIP-14", "Single 8-Input NAND Gate")
        
        # Create one NAND gate instance (modified to handle 8 inputs)
        self.gates = {
            'gate1': NANDGate()
        }
        
        # Pin mapping for 7430
        self.pin_mapping = {
            1: "A (Input A)",
            2: "B (Input B)",
            3: "C (Input C)",
            4: "D (Input D)",
            5: "E (Input E)",
            6: "F (Input F)",
            7: "GND",
            8: "Y (Output)",
            9: "NC (Not Connected)",
            10: "NC (Not Connected)",
            11: "G (Input G)",
            12: "H (Input H)",
            13: "NC (Not Connected)",
            14: "VCC"
        }
        
        # Gate pin assignments (8 inputs)
        self.gate_pins = {
            'gate1': {'inputs': [1, 2, 3, 4, 5, 6, 11, 12], 'output': 8}
        }
    
    def update_outputs(self):
        """Update gate output based on current inputs"""
        if not self.powered:
            # Set output to 0 when not powered
            self.pins[8] = 0
            return
        
        # Calculate output for the gate
        gate_info = self.gate_pins['gate1']
        inputs = [self.pins[pin] for pin in gate_info['inputs']]
        
        # Only calculate if all inputs are connected
        if all(inp is not None for inp in inputs):
            # For 8-input NAND: output is 0 only when all inputs are 1
            output = 0 if all(inp == 1 for inp in inputs) else 1
            self.pins[gate_info['output']] = output
        else:
            self.pins[gate_info['output']] = None
    
    def set_pin(self, pin_number, value):
        """Override to update outputs when inputs change"""
        super().set_pin(pin_number, value)
        self.update_outputs()
    
    def get_gate_output(self, a, b, c, d, e, f, g, h):
        """
        Get output of the gate for given inputs
        
        Args:
            a through h (int): Eight inputs (0 or 1)
            
        Returns:
            int: Gate output (0 or 1)
        """
        if not self.powered:
            return 0
        
        # 8-input NAND: output is 0 only when all inputs are 1
        inputs = [a, b, c, d, e, f, g, h]
        return 0 if all(inp == 1 for inp in inputs) else 1
    
    def test_ic(self):
        """
        Test gate with key test cases
        
        Returns:
            bool: True if all tests pass
        """
        if not self.powered:
            print("IC must be powered for testing")
            return False
        
        # Key test cases for 8-input NAND
        test_cases = [
            # All zeros -> 1
            (0, 0, 0, 0, 0, 0, 0, 0, 1),
            # One 1 -> 1
            (1, 0, 0, 0, 0, 0, 0, 0, 1),
            # Half 1s -> 1
            (1, 1, 1, 1, 0, 0, 0, 0, 1),
            # Seven 1s -> 1
            (1, 1, 1, 1, 1, 1, 1, 0, 1),
            # All 1s -> 0
            (1, 1, 1, 1, 1, 1, 1, 1, 0)
        ]
        
        print(f"\nTesting {self.ic_number} - {self.description}")
        print("=" * 70)
        print("A B C D E F G H | Y | Expected | Pass")
        print("-" * 31)
        
        all_passed = True
        
        for a, b, c, d, e, f, g, h, expected in test_cases:
            actual = self.get_gate_output(a, b, c, d, e, f, g, h)
            passed = actual == expected
            all_passed &= passed
            status = "✓" if passed else "✗"
            
            print(f"{a} {b} {c} {d} {e} {f} {g} {h} | {actual} |    {expected}     | {status}")
        
        print(f"\nOverall IC Test: {'PASS ✓' if all_passed else 'FAIL ✗'}")
        return all_passed
    
    def get_truth_table(self):
        """Generate partial truth table for the IC (key cases)"""
        if not self.powered:
            return "IC must be powered to generate truth table"
        
        table = f"\n{self.ic_number} Truth Table - 8-Input NAND Gate (Key Cases)\n"
        table += "=" * 65 + "\n"
        table += "A B C D E F G H | Y\n"
        table += "-" * 21 + "\n"
        
        # Show key test cases
        key_cases = [
            (0, 0, 0, 0, 0, 0, 0, 0),  # All 0
            (1, 0, 0, 0, 0, 0, 0, 0),  # One 1
            (1, 1, 0, 0, 0, 0, 0, 0),  # Two 1s
            (1, 1, 1, 1, 0, 0, 0, 0),  # Four 1s
            (1, 1, 1, 1, 1, 1, 1, 0),  # Seven 1s
            (1, 1, 1, 1, 1, 1, 1, 1)   # All 1s
        ]
        
        for inputs in key_cases:
            output = self.get_gate_output(*inputs)
            inputs_str = ' '.join(str(inp) for inp in inputs)
            table += f"{inputs_str} | {output}\n"
        
        table += "\nNote: Only key cases shown. Full truth table has 256 combinations.\n"
        return table
    
    def set_all_inputs(self, inputs):
        """
        Set all 8 inputs at once
        
        Args:
            inputs (list): List of 8 inputs (0 or 1)
            
        Returns:
            int: Gate output
        """
        if len(inputs) != 8:
            raise ValueError("Must provide exactly 8 inputs")
        
        if not self.powered:
            return 0
        
        return self.get_gate_output(*inputs)

def main():
    """Demonstration of 7430 IC"""
    print("7430 IC Demonstration")
    print("=" * 30)
    
    # Create IC instance
    ic = IC7430()
    
    # Show pinout
    print(ic.get_pinout_diagram())
    
    # Connect power
    print("Connecting power...")
    ic.connect_power()
    
    # Test the IC
    ic.test_ic()
    
    # Show truth table
    print(ic.get_truth_table())
    
    # Test with different input patterns
    print("\nTesting different input patterns:")
    print(f"All 0s: {ic.set_all_inputs([0,0,0,0,0,0,0,0])}")
    print(f"All 1s: {ic.set_all_inputs([1,1,1,1,1,1,1,1])}")
    print(f"Alternating: {ic.set_all_inputs([1,0,1,0,1,0,1,0])}")
    print(f"Binary 85 (01010101): {ic.set_all_inputs([0,1,0,1,0,1,0,1])}")
    print(f"Binary 255 (11111111): {ic.set_all_inputs([1,1,1,1,1,1,1,1])}")

if __name__ == "__main__":
    main()
