"""
7432 IC - Quad 2-Input OR Gates
Digital Logic Design - TTL 7400 Series

The 7432 contains four independent 2-input OR gates.
Pin Configuration (DIP-14):
- VCC: Pin 14
- GND: Pin 7
- 4 OR gates with inputs and outputs
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basic_gates'))
from base_ic import BaseIC
from OR import ORGate

class IC7432(BaseIC):
    """
    7432 IC - Quad 2-Input OR Gates
    
    Pin Configuration:
    Pin 1: 1A (Gate 1 Input A)
    Pin 2: 1B (Gate 1 Input B)
    Pin 3: 1Y (Gate 1 Output)
    Pin 4: 2A (Gate 2 Input A)
    Pin 5: 2B (Gate 2 Input B)
    Pin 6: 2Y (Gate 2 Output)
    Pin 7: GND
    Pin 8: 3Y (Gate 3 Output)
    Pin 9: 3A (Gate 3 Input A)
    Pin 10: 3B (Gate 3 Input B)
    Pin 11: 4Y (Gate 4 Output)
    Pin 12: 4A (Gate 4 Input A)
    Pin 13: 4B (Gate 4 Input B)
    Pin 14: VCC
    """
    
    def __init__(self):
        super().__init__("7432", "DIP-14", "Quad 2-Input OR Gates")
        
        # Create four OR gate instances
        self.gates = {
            'gate1': ORGate(),
            'gate2': ORGate(),
            'gate3': ORGate(),
            'gate4': ORGate()
        }
        
        # Pin mapping for 7432
        self.pin_mapping = {
            1: "1A (Gate 1 Input A)",
            2: "1B (Gate 1 Input B)",
            3: "1Y (Gate 1 Output)",
            4: "2A (Gate 2 Input A)",
            5: "2B (Gate 2 Input B)",
            6: "2Y (Gate 2 Output)",
            7: "GND",
            8: "3Y (Gate 3 Output)",
            9: "3A (Gate 3 Input A)",
            10: "3B (Gate 3 Input B)",
            11: "4Y (Gate 4 Output)",
            12: "4A (Gate 4 Input A)",
            13: "4B (Gate 4 Input B)",
            14: "VCC"
        }
        
        # Gate pin assignments
        self.gate_pins = {
            'gate1': {'inputs': [1, 2], 'output': 3},
            'gate2': {'inputs': [4, 5], 'output': 6},
            'gate3': {'inputs': [9, 10], 'output': 8},
            'gate4': {'inputs': [12, 13], 'output': 11}
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
                output = gate.evaluate(*inputs)
                self.pins[gate_info['output']] = output
            else:
                self.pins[gate_info['output']] = None
    
    def set_pin(self, pin_number, value):
        """Override to update outputs when inputs change"""
        super().set_pin(pin_number, value)
        self.update_outputs()
    
    def get_gate_output(self, gate_number, input_a, input_b):
        """
        Get output of a specific gate for given inputs
        
        Args:
            gate_number (int): Gate number (1-4)
            input_a (int): First input (0 or 1)
            input_b (int): Second input (0 or 1)
            
        Returns:
            int: Gate output (0 or 1)
        """
        if not self.powered:
            return 0
        
        if gate_number < 1 or gate_number > 4:
            raise ValueError("Gate number must be 1-4")
        
        gate_name = f'gate{gate_number}'
        return self.gates[gate_name].evaluate(input_a, input_b)
    
    def test_ic(self):
        """
        Test all gates with truth table verification
        
        Returns:
            bool: True if all tests pass
        """
        if not self.powered:
            print("IC must be powered for testing")
            return False
        
        # OR truth table: A B | Y
        #                 0 0 | 0
        #                 0 1 | 1
        #                 1 0 | 1
        #                 1 1 | 1
        
        test_cases = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 1)]
        
        print(f"\nTesting {self.ic_number} - {self.description}")
        print("=" * 50)
        
        all_passed = True
        
        for gate_num in range(1, 5):
            print(f"\nGate {gate_num} Test:")
            print("A B | Y | Expected | Pass")
            print("-" * 25)
            
            gate_passed = True
            for a, b, expected in test_cases:
                actual = self.get_gate_output(gate_num, a, b)
                passed = actual == expected
                gate_passed &= passed
                status = "✓" if passed else "✗"
                
                print(f"{a} {b} | {actual} |    {expected}     | {status}")
            
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
        
        table = f"\n{self.ic_number} Truth Table - OR Gates\n"
        table += "=" * 40 + "\n"
        table += "Gate | A B | Y\n"
        table += "-" * 15 + "\n"
        
        for gate_num in range(1, 5):
            for a in [0, 1]:
                for b in [0, 1]:
                    output = self.get_gate_output(gate_num, a, b)
                    table += f"  {gate_num}  | {a} {b} | {output}\n"
            if gate_num < 4:
                table += "-" * 15 + "\n"
        
        return table

def main():
    """Demonstration of 7432 IC"""
    print("7432 IC Demonstration")
    print("=" * 30)
    
    # Create IC instance
    ic = IC7432()
    
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
    print(f"Gate 1: 0 OR 0 = {ic.get_gate_output(1, 0, 0)}")
    print(f"Gate 2: 0 OR 1 = {ic.get_gate_output(2, 0, 1)}")
    print(f"Gate 3: 1 OR 0 = {ic.get_gate_output(3, 1, 0)}")
    print(f"Gate 4: 1 OR 1 = {ic.get_gate_output(4, 1, 1)}")

if __name__ == "__main__":
    main()
