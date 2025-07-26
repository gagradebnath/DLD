"""
7410 IC - Triple 3-Input NAND Gates
Digital Logic Design - TTL 7400 Series

The 7410 contains three independent 3-input NAND gates.
Pin Configuration (DIP-14):
- VCC: Pin 14
- GND: Pin 7
- 3 NAND gates with 3 inputs each
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basic_gates'))
from base_ic import BaseIC
from NAND import NANDGate

class IC7410(BaseIC):
    """
    7410 IC - Triple 3-Input NAND Gates
    
    Pin Configuration:
    Pin 1: 1A (Gate 1 Input A)
    Pin 2: 1B (Gate 1 Input B)
    Pin 3: 2A (Gate 2 Input A)
    Pin 4: 2B (Gate 2 Input B)
    Pin 5: 2C (Gate 2 Input C)
    Pin 6: 2Y (Gate 2 Output)
    Pin 7: GND
    Pin 8: 3Y (Gate 3 Output)
    Pin 9: 3A (Gate 3 Input A)
    Pin 10: 3B (Gate 3 Input B)
    Pin 11: 3C (Gate 3 Input C)
    Pin 12: 1Y (Gate 1 Output)
    Pin 13: 1C (Gate 1 Input C)
    Pin 14: VCC
    """
    
    def __init__(self):
        super().__init__("7410", "DIP-14", "Triple 3-Input NAND Gates")
        
        # Create three NAND gate instances (modified to handle 3 inputs)
        self.gates = {
            'gate1': NANDGate(),
            'gate2': NANDGate(),
            'gate3': NANDGate()
        }
        
        # Pin mapping for 7410
        self.pin_mapping = {
            1: "1A (Gate 1 Input A)",
            2: "1B (Gate 1 Input B)",
            3: "2A (Gate 2 Input A)",
            4: "2B (Gate 2 Input B)",
            5: "2C (Gate 2 Input C)",
            6: "2Y (Gate 2 Output)",
            7: "GND",
            8: "3Y (Gate 3 Output)",
            9: "3A (Gate 3 Input A)",
            10: "3B (Gate 3 Input B)",
            11: "3C (Gate 3 Input C)",
            12: "1Y (Gate 1 Output)",
            13: "1C (Gate 1 Input C)",
            14: "VCC"
        }
        
        # Gate pin assignments (3 inputs each)
        self.gate_pins = {
            'gate1': {'inputs': [1, 2, 13], 'output': 12},
            'gate2': {'inputs': [3, 4, 5], 'output': 6},
            'gate3': {'inputs': [9, 10, 11], 'output': 8}
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
                # For 3-input NAND: output is 0 only when all inputs are 1
                output = 0 if all(inp == 1 for inp in inputs) else 1
                self.pins[gate_info['output']] = output
            else:
                self.pins[gate_info['output']] = None
    
    def set_pin(self, pin_number, value):
        """Override to update outputs when inputs change"""
        super().set_pin(pin_number, value)
        self.update_outputs()
    
    def get_gate_output(self, gate_number, input_a, input_b, input_c):
        """
        Get output of a specific gate for given inputs
        
        Args:
            gate_number (int): Gate number (1-3)
            input_a (int): First input (0 or 1)
            input_b (int): Second input (0 or 1)
            input_c (int): Third input (0 or 1)
            
        Returns:
            int: Gate output (0 or 1)
        """
        if not self.powered:
            return 0
        
        if gate_number < 1 or gate_number > 3:
            raise ValueError("Gate number must be 1-3")
        
        # 3-input NAND: output is 0 only when all inputs are 1
        return 0 if (input_a == 1 and input_b == 1 and input_c == 1) else 1
    
    def test_ic(self):
        """
        Test all gates with truth table verification
        
        Returns:
            bool: True if all tests pass
        """
        if not self.powered:
            print("IC must be powered for testing")
            return False
        
        # 3-input NAND truth table: A B C | Y
        #                           0 0 0 | 1
        #                           0 0 1 | 1
        #                           0 1 0 | 1
        #                           0 1 1 | 1
        #                           1 0 0 | 1
        #                           1 0 1 | 1
        #                           1 1 0 | 1
        #                           1 1 1 | 0
        
        test_cases = [
            (0, 0, 0, 1), (0, 0, 1, 1), (0, 1, 0, 1), (0, 1, 1, 1),
            (1, 0, 0, 1), (1, 0, 1, 1), (1, 1, 0, 1), (1, 1, 1, 0)
        ]
        
        print(f"\nTesting {self.ic_number} - {self.description}")
        print("=" * 55)
        
        all_passed = True
        
        for gate_num in range(1, 4):
            print(f"\nGate {gate_num} Test:")
            print("A B C | Y | Expected | Pass")
            print("-" * 27)
            
            gate_passed = True
            for a, b, c, expected in test_cases:
                actual = self.get_gate_output(gate_num, a, b, c)
                passed = actual == expected
                gate_passed &= passed
                status = "✓" if passed else "✗"
                
                print(f"{a} {b} {c} | {actual} |    {expected}     | {status}")
            
            if gate_passed:
                print(f"Gate {gate_num}: PASS ✓")
            else:
                print(f"Gate {gate_num}: FAIL ✗")
                all_passed = False
        
        print(f"\nOverall IC Test: {'PASS ✓' if all_passed else 'FAIL ✗'}")
        return all_passed
    
    def get_truth_table(self):
        """Generate complete truth table for the IC"""
        if not self.powered:
            return "IC must be powered to generate truth table"
        
        table = f"\n{self.ic_number} Truth Table - 3-Input NAND Gates\n"
        table += "=" * 45 + "\n"
        table += "Gate | A B C | Y\n"
        table += "-" * 17 + "\n"
        
        for gate_num in range(1, 4):
            for a in [0, 1]:
                for b in [0, 1]:
                    for c in [0, 1]:
                        output = self.get_gate_output(gate_num, a, b, c)
                        table += f"  {gate_num}  | {a} {b} {c} | {output}\n"
            if gate_num < 3:
                table += "-" * 17 + "\n"
        
        return table

def main():
    """Demonstration of 7410 IC"""
    print("7410 IC Demonstration")
    print("=" * 30)
    
    # Create IC instance
    ic = IC7410()
    
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
    print(f"Gate 1: 1 NAND 1 NAND 1 = {ic.get_gate_output(1, 1, 1, 1)}")
    print(f"Gate 2: 0 NAND 1 NAND 1 = {ic.get_gate_output(2, 0, 1, 1)}")
    print(f"Gate 3: 1 NAND 0 NAND 1 = {ic.get_gate_output(3, 1, 0, 1)}")

if __name__ == "__main__":
    main()
