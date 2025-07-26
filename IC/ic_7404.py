"""
7404 IC - Hex Inverter (NOT Gates)
Digital Logic Design - TTL 7400 Series

The 7404 contains six independent NOT gates (inverters).
Pin Configuration (DIP-14):
- VCC: Pin 14
- GND: Pin 7
- 6 NOT gates with inputs and outputs
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basic_gates'))
from base_ic import BaseIC
from NOT import NOTGate

class IC7404(BaseIC):
    """
    7404 IC - Hex Inverter (NOT Gates)
    
    Pin Configuration:
    Pin 1: 1A (Gate 1 Input)
    Pin 2: 1Y (Gate 1 Output)
    Pin 3: 2A (Gate 2 Input)
    Pin 4: 2Y (Gate 2 Output)
    Pin 5: 3A (Gate 3 Input)
    Pin 6: 3Y (Gate 3 Output)
    Pin 7: GND
    Pin 8: 4Y (Gate 4 Output)
    Pin 9: 4A (Gate 4 Input)
    Pin 10: 5Y (Gate 5 Output)
    Pin 11: 5A (Gate 5 Input)
    Pin 12: 6Y (Gate 6 Output)
    Pin 13: 6A (Gate 6 Input)
    Pin 14: VCC
    """
    
    def __init__(self):
        super().__init__("7404", "DIP-14", "Hex Inverter (NOT Gates)")
        
        # Create six NOT gate instances
        self.gates = {
            'gate1': NOTGate(),
            'gate2': NOTGate(),
            'gate3': NOTGate(),
            'gate4': NOTGate(),
            'gate5': NOTGate(),
            'gate6': NOTGate()
        }
        
        # Pin mapping for 7404
        self.pin_mapping = {
            1: "1A (Gate 1 Input)",
            2: "1Y (Gate 1 Output)",
            3: "2A (Gate 2 Input)",
            4: "2Y (Gate 2 Output)",
            5: "3A (Gate 3 Input)",
            6: "3Y (Gate 3 Output)",
            7: "GND",
            8: "4Y (Gate 4 Output)",
            9: "4A (Gate 4 Input)",
            10: "5Y (Gate 5 Output)",
            11: "5A (Gate 5 Input)",
            12: "6Y (Gate 6 Output)",
            13: "6A (Gate 6 Input)",
            14: "VCC"
        }
        
        # Gate pin assignments
        self.gate_pins = {
            'gate1': {'inputs': [1], 'output': 2},
            'gate2': {'inputs': [3], 'output': 4},
            'gate3': {'inputs': [5], 'output': 6},
            'gate4': {'inputs': [9], 'output': 8},
            'gate5': {'inputs': [11], 'output': 10},
            'gate6': {'inputs': [13], 'output': 12}
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
    
    def get_gate_output(self, gate_number, input_a):
        """
        Get output of a specific gate for given input
        
        Args:
            gate_number (int): Gate number (1-6)
            input_a (int): Input (0 or 1)
            
        Returns:
            int: Gate output (0 or 1)
        """
        if not self.powered:
            return 0
        
        if gate_number < 1 or gate_number > 6:
            raise ValueError("Gate number must be 1-6")
        
        gate_name = f'gate{gate_number}'
        return self.gates[gate_name].evaluate(input_a)
    
    def test_ic(self):
        """
        Test all gates with truth table verification
        
        Returns:
            bool: True if all tests pass
        """
        if not self.powered:
            print("IC must be powered for testing")
            return False
        
        # NOT truth table: A | Y
        #                  0 | 1
        #                  1 | 0
        
        test_cases = [(0, 1), (1, 0)]
        
        print(f"\nTesting {self.ic_number} - {self.description}")
        print("=" * 50)
        
        all_passed = True
        
        for gate_num in range(1, 7):
            print(f"\nGate {gate_num} Test:")
            print("A | Y | Expected | Pass")
            print("-" * 20)
            
            gate_passed = True
            for a, expected in test_cases:
                actual = self.get_gate_output(gate_num, a)
                passed = actual == expected
                gate_passed &= passed
                status = "✓" if passed else "✗"
                
                print(f"{a} | {actual} |    {expected}     | {status}")
            
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
        
        table = f"\n{self.ic_number} Truth Table - NOT Gates\n"
        table += "=" * 35 + "\n"
        table += "Gate | A | Y\n"
        table += "-" * 12 + "\n"
        
        for gate_num in range(1, 7):
            for a in [0, 1]:
                output = self.get_gate_output(gate_num, a)
                table += f"  {gate_num}  | {a} | {output}\n"
            if gate_num < 6:
                table += "-" * 12 + "\n"
        
        return table
    
    def invert_all(self, inputs):
        """
        Invert all six inputs simultaneously
        
        Args:
            inputs (list): List of 6 inputs (0 or 1)
            
        Returns:
            list: List of 6 outputs
        """
        if not self.powered:
            return [0] * 6
        
        if len(inputs) != 6:
            raise ValueError("Must provide exactly 6 inputs")
        
        outputs = []
        for i, inp in enumerate(inputs):
            gate_num = i + 1
            output = self.get_gate_output(gate_num, inp)
            outputs.append(output)
        
        return outputs

def main():
    """Demonstration of 7404 IC"""
    print("7404 IC Demonstration")
    print("=" * 30)
    
    # Create IC instance
    ic = IC7404()
    
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
    print(f"Gate 1: NOT 0 = {ic.get_gate_output(1, 0)}")
    print(f"Gate 2: NOT 1 = {ic.get_gate_output(2, 1)}")
    print(f"Gate 3: NOT 0 = {ic.get_gate_output(3, 0)}")
    print(f"Gate 4: NOT 1 = {ic.get_gate_output(4, 1)}")
    print(f"Gate 5: NOT 0 = {ic.get_gate_output(5, 0)}")
    print(f"Gate 6: NOT 1 = {ic.get_gate_output(6, 1)}")
    
    # Test inverting multiple inputs
    print(f"\nInverting [0,1,0,1,0,1]: {ic.invert_all([0,1,0,1,0,1])}")
    print(f"Inverting [1,1,1,0,0,0]: {ic.invert_all([1,1,1,0,0,0])}")

if __name__ == "__main__":
    main()
