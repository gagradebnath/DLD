"""
7420 IC - Dual 4-Input NAND Gates
Digital Logic Design - TTL 7400 Series

The 7420 contains two independent 4-input NAND gates.
Pin Configuration (DIP-14):
- VCC: Pin 14
- GND: Pin 7
- 2 NAND gates with 4 inputs each
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basic_gates'))
from base_ic import BaseIC
from NAND import NANDGate

class IC7420(BaseIC):
    """
    7420 IC - Dual 4-Input NAND Gates
    
    Pin Configuration:
    Pin 1: 1A (Gate 1 Input A)
    Pin 2: 1B (Gate 1 Input B)
    Pin 3: NC (Not Connected)
    Pin 4: 1C (Gate 1 Input C)
    Pin 5: 1D (Gate 1 Input D)
    Pin 6: 1Y (Gate 1 Output)
    Pin 7: GND
    Pin 8: 2Y (Gate 2 Output)
    Pin 9: 2A (Gate 2 Input A)
    Pin 10: 2B (Gate 2 Input B)
    Pin 11: NC (Not Connected)
    Pin 12: 2C (Gate 2 Input C)
    Pin 13: 2D (Gate 2 Input D)
    Pin 14: VCC
    """
    
    def __init__(self):
        super().__init__("7420", "DIP-14", "Dual 4-Input NAND Gates")
        
        # Create two NAND gate instances (modified to handle 4 inputs)
        self.gates = {
            'gate1': NANDGate(),
            'gate2': NANDGate()
        }
        
        # Pin mapping for 7420
        self.pin_mapping = {
            1: "1A (Gate 1 Input A)",
            2: "1B (Gate 1 Input B)",
            3: "NC (Not Connected)",
            4: "1C (Gate 1 Input C)",
            5: "1D (Gate 1 Input D)",
            6: "1Y (Gate 1 Output)",
            7: "GND",
            8: "2Y (Gate 2 Output)",
            9: "2A (Gate 2 Input A)",
            10: "2B (Gate 2 Input B)",
            11: "NC (Not Connected)",
            12: "2C (Gate 2 Input C)",
            13: "2D (Gate 2 Input D)",
            14: "VCC"
        }
        
        # Gate pin assignments (4 inputs each)
        self.gate_pins = {
            'gate1': {'inputs': [1, 2, 4, 5], 'output': 6},
            'gate2': {'inputs': [9, 10, 12, 13], 'output': 8}
        }
    
    def update_outputs(self):
        """Update all gate outputs based on current inputs"""
        if not self.powered:
            # Set all outputs to 0 when not powered
            for gate_info in self.gate_pins.values():
                self.pins[gate_info['output']] = 0
            return
        
        # Calculate outputs for each gate
        for gate_name, gate_info in self.gate_pins.items():
            gate = self.gates[gate_name]
            inputs = [self.pins[pin] for pin in gate_info['inputs']]
            
            # Only calculate if all inputs are connected
            if all(inp is not None for inp in inputs):
                # For 4-input NAND: output is 0 only when all inputs are 1
                output = 0 if all(inp == 1 for inp in inputs) else 1
                self.pins[gate_info['output']] = output
            else:
                self.pins[gate_info['output']] = None
    
    def set_pin(self, pin_number, value):
        """Override to update outputs when inputs change"""
        super().set_pin(pin_number, value)
        self.update_outputs()
    
    def get_gate_output(self, gate_number, input_a, input_b, input_c, input_d):
        """
        Get output of a specific gate for given inputs
        
        Args:
            gate_number (int): Gate number (1-2)
            input_a (int): First input (0 or 1)
            input_b (int): Second input (0 or 1)
            input_c (int): Third input (0 or 1)
            input_d (int): Fourth input (0 or 1)
            
        Returns:
            int: Gate output (0 or 1)
        """
        if not self.powered:
            return 0
        
        if gate_number < 1 or gate_number > 2:
            raise ValueError("Gate number must be 1-2")
        
        # 4-input NAND: output is 0 only when all inputs are 1
        return 0 if (input_a == 1 and input_b == 1 and input_c == 1 and input_d == 1) else 1
    
    def test_ic(self):
        """
        Test all gates with truth table verification (subset)
        
        Returns:
            bool: True if all tests pass
        """
        if not self.powered:
            print("IC must be powered for testing")
            return False
        
        # Key test cases for 4-input NAND
        test_cases = [
            (0, 0, 0, 0, 1), (0, 0, 0, 1, 1), (0, 0, 1, 1, 1), (0, 1, 1, 1, 1),
            (1, 0, 0, 0, 1), (1, 1, 0, 0, 1), (1, 1, 1, 0, 1), (1, 1, 1, 1, 0)
        ]
        
        print(f"\nTesting {self.ic_number} - {self.description}")
        print("=" * 60)
        
        all_passed = True
        
        for gate_num in range(1, 3):
            print(f"\nGate {gate_num} Test (Key Cases):")
            print("A B C D | Y | Expected | Pass")
            print("-" * 29)
            
            gate_passed = True
            for a, b, c, d, expected in test_cases:
                actual = self.get_gate_output(gate_num, a, b, c, d)
                passed = actual == expected
                gate_passed &= passed
                status = "✓" if passed else "✗"
                
                print(f"{a} {b} {c} {d} | {actual} |    {expected}     | {status}")
            
            if gate_passed:
                print(f"Gate {gate_num}: PASS ✓")
            else:
                print(f"Gate {gate_num}: FAIL ✗")
                all_passed = False
        
        print(f"\nOverall IC Test: {'PASS ✓' if all_passed else 'FAIL ✗'}")
        return all_passed
    
    def get_truth_table(self):
        """Generate partial truth table for the IC (key cases)"""
        if not self.powered:
            return "IC must be powered to generate truth table"
        
        table = f"\n{self.ic_number} Truth Table - 4-Input NAND Gates (Key Cases)\n"
        table += "=" * 55 + "\n"
        table += "Gate | A B C D | Y\n"
        table += "-" * 19 + "\n"
        
        # Show key test cases
        key_cases = [
            (0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 1), (0, 1, 1, 1),
            (1, 0, 0, 0), (1, 1, 0, 0), (1, 1, 1, 0), (1, 1, 1, 1)
        ]
        
        for gate_num in range(1, 3):
            for a, b, c, d in key_cases:
                output = self.get_gate_output(gate_num, a, b, c, d)
                table += f"  {gate_num}  | {a} {b} {c} {d} | {output}\n"
            if gate_num < 2:
                table += "-" * 19 + "\n"
        
        table += "\nNote: Only key cases shown. Full truth table has 16 combinations per gate.\n"
        return table

def main():
    """Demonstration of 7420 IC"""
    print("7420 IC Demonstration")
    print("=" * 30)
    
    # Create IC instance
    ic = IC7420()
    
    # Show pinout
    print(ic.get_pinout_diagram())
    
    # Connect power
    print("Connecting power...")
    ic.connect_power()
    
    # Test the IC
    ic.test_ic()
    
    # Show truth table
    print(ic.get_truth_table())
    
    # Test individual gates
    print("\nTesting individual gates:")
    print(f"Gate 1: 1 NAND 1 NAND 1 NAND 1 = {ic.get_gate_output(1, 1, 1, 1, 1)}")
    print(f"Gate 2: 0 NAND 1 NAND 1 NAND 1 = {ic.get_gate_output(2, 0, 1, 1, 1)}")

if __name__ == "__main__":
    main()
