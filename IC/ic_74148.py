"""
74148 IC - 8-to-3 Line Priority Encoder
Digital Logic Design - TTL 7400 Series

The 74148 encodes 8 input lines into a 3-bit binary code with priority encoding.
Includes enable and cascading features for building larger encoders.
Pin Configuration (DIP-16):
- VCC: Pin 16
- GND: Pin 8
- 8 inputs (active low), 3 outputs (active low), plus control signals
"""

import sys
import os
from .base_ic import BaseIC

class IC74148(BaseIC):
    """
    74148 IC - 8-to-3 Line Priority Encoder
    
    Pin Configuration (DIP-16):
    Pin 1: D4 (Input 4)
    Pin 2: D5 (Input 5)
    Pin 3: D6 (Input 6)
    Pin 4: D7 (Input 7)
    Pin 5: EI (Enable Input - active low)
    Pin 6: A2 (Output A2)
    Pin 7: A1 (Output A1)
    Pin 8: GND
    Pin 9: A0 (Output A0)
    Pin 10: D3 (Input 3)
    Pin 11: D2 (Input 2)
    Pin 12: D1 (Input 1)
    Pin 13: D0 (Input 0)
    Pin 14: GS (Group Select - active low)
    Pin 15: EO (Enable Output - active low)
    Pin 16: VCC
    
    Priority: D7 > D6 > D5 > D4 > D3 > D2 > D1 > D0
    All inputs and outputs are active LOW
    """
    
    def __init__(self):
        super().__init__("74148", "DIP-16", "8-to-3 Line Priority Encoder")
        
        # Pin mapping for 74148
        self.pin_mapping = {
            1: "D4 (Input 4)",
            2: "D5 (Input 5)",
            3: "D6 (Input 6)",
            4: "D7 (Input 7)",
            5: "EI (Enable Input)",
            6: "A2 (Output A2)",
            7: "A1 (Output A1)",
            8: "GND",
            9: "A0 (Output A0)",
            10: "D3 (Input 3)",
            11: "D2 (Input 2)",
            12: "D1 (Input 1)",
            13: "D0 (Input 0)",
            14: "GS (Group Select)",
            15: "EO (Enable Output)",
            16: "VCC"
        }
        
        # Input and output pin assignments
        self.input_pins = {
            0: 13, 1: 12, 2: 11, 3: 10,
            4: 1, 5: 2, 6: 3, 7: 4
        }
        self.data_output_pins = [9, 7, 6]  # A0, A1, A2
        self.ei_pin = 5   # Enable Input
        self.gs_pin = 14  # Group Select
        self.eo_pin = 15  # Enable Output
        
        # Initialize outputs to inactive (high)
        for pin in self.data_output_pins + [self.gs_pin, self.eo_pin]:
            self.pins[pin] = 1
    
    def update_outputs(self):
        """Update outputs based on current inputs and enable"""
        if not self.powered:
            # Set all outputs to inactive when not powered
            for pin in self.data_output_pins + [self.gs_pin, self.eo_pin]:
                self.pins[pin] = 1
            return
        
        # Check if enabled (EI must be low to enable)
        ei_state = self.pins.get(self.ei_pin, 1)
        if ei_state != 0:  # Not enabled
            # All outputs inactive
            for pin in self.data_output_pins:
                self.pins[pin] = 1
            self.pins[self.gs_pin] = 1  # GS inactive
            self.pins[self.eo_pin] = 1  # EO inactive
            return
        
        # Find highest priority active input (lowest logic level)
        # Priority: D7 > D6 > D5 > D4 > D3 > D2 > D1 > D0
        active_input = None
        
        for input_num in range(7, -1, -1):  # Check from 7 down to 0
            pin = self.input_pins[input_num]
            if self.pins[pin] is not None and self.pins[pin] == 0:  # Active low
                active_input = input_num
                break
        
        if active_input is not None:
            # Valid input found - encode it (inverted output)
            binary = active_input
            self.pins[9] = (binary & 1) ^ 1        # A0 (inverted)
            self.pins[7] = ((binary >> 1) & 1) ^ 1 # A1 (inverted)
            self.pins[6] = ((binary >> 2) & 1) ^ 1 # A2 (inverted)
            
            self.pins[self.gs_pin] = 0  # GS active (indicates valid input)
            self.pins[self.eo_pin] = 1  # EO inactive (input present)
        else:
            # No active input
            for pin in self.data_output_pins:
                self.pins[pin] = 1  # All data outputs inactive
            
            self.pins[self.gs_pin] = 1  # GS inactive (no valid input)
            self.pins[self.eo_pin] = 0  # EO active (no input, enable chain)
    
    def set_pin(self, pin_number, value):
        """Override to update outputs when inputs change"""
        super().set_pin(pin_number, value)
        self.update_outputs()
    
    def encode_inputs(self, data_inputs, enable_input=0):
        """
        Encode data inputs to binary output
        
        Args:
            data_inputs (dict): Dict with input number as key, state as value
                              e.g., {7: 0, 6: 1, 5: 1, ...} (0 = active, 1 = inactive)
            enable_input (int): Enable input state (0 = enabled, 1 = disabled)
        
        Returns:
            tuple: (A2, A1, A0, GS, EO) - all inverted outputs
        """
        if not self.powered:
            return (1, 1, 1, 1, 1)
        
        # Set enable input
        self.pins[self.ei_pin] = enable_input
        
        # Set data inputs
        for input_num, state in data_inputs.items():
            if 0 <= input_num <= 7:
                pin = self.input_pins[input_num]
                self.pins[pin] = state
        
        self.update_outputs()
        
        # Return outputs
        return (self.pins[6], self.pins[7], self.pins[9], 
                self.pins[self.gs_pin], self.pins[self.eo_pin])  # A2, A1, A0, GS, EO
    
    def get_binary_output(self):
        """Get current binary output as integer (corrected for inversion)"""
        if not self.powered or self.pins.get(self.ei_pin, 1) != 0:
            return None
        
        # Check if there's a valid input (GS active)
        if self.pins[self.gs_pin] != 0:
            return None
        
        # Convert inverted outputs back to positive logic
        a0 = self.pins[9] ^ 1
        a1 = self.pins[7] ^ 1
        a2 = self.pins[6] ^ 1
        
        return a2 * 4 + a1 * 2 + a0
    
    def test_ic(self):
        """Test the priority encoder with various input combinations"""
        if not self.powered:
            print("IC must be powered for testing")
            return False
        
        print(f"\nTesting {self.ic_number} - {self.description}")
        print("=" * 75)
        print("Priority Encoder Test (All signals Active LOW)")
        print("Active Input | A2 A1 A0 | GS EO | Binary | Expected | Pass")
        print("-" * 55)
        
        all_passed = True
        
        # Test single input cases
        for input_num in range(7, -1, -1):
            # Set all inputs inactive except test input
            inputs = {i: 1 for i in range(8)}
            inputs[input_num] = 0  # Make test input active
            
            outputs = self.encode_inputs(inputs, enable_input=0)
            actual_binary = self.get_binary_output()
            
            passed = actual_binary == input_num
            all_passed &= passed
            status = "✓" if passed else "✗"
            
            print(f"     {input_num}       |  {outputs[0]} {outputs[1]} {outputs[2]}  | {outputs[3]} {outputs[4]} |   {actual_binary}    |    {input_num}     | {status}")
        
        # Test priority encoding
        print("\nPriority Encoding Test:")
        print("Active Inputs | Highest | A2 A1 A0 | Binary | Pass")
        print("-" * 45)
        
        priority_tests = [
            ([7, 3, 1], 7),
            ([6, 4, 2, 0], 6),
            ([5, 2], 5),
            ([4, 1], 4),
            ([3, 0], 3)
        ]
        
        for active_list, expected_highest in priority_tests:
            inputs = {i: 1 for i in range(8)}
            for input_num in active_list:
                inputs[input_num] = 0
            
            outputs = self.encode_inputs(inputs, enable_input=0)
            actual_binary = self.get_binary_output()
            
            passed = actual_binary == expected_highest
            all_passed &= passed
            status = "✓" if passed else "✗"
            
            active_str = ','.join(map(str, sorted(active_list, reverse=True)))
            print(f"   {active_str:8} |    {expected_highest}    |  {outputs[0]} {outputs[1]} {outputs[2]}  |   {actual_binary}    | {status}")
        
        # Test enable function
        print("\nEnable Function Test:")
        print("EI | Any Input | A2 A1 A0 | GS EO | Pass")
        print("-" * 35)
        
        # Test disabled state
        inputs = {7: 0}  # Input 7 active
        outputs = self.encode_inputs(inputs, enable_input=1)  # Disabled
        disabled_passed = all(out == 1 for out in outputs[:3]) and outputs[3] == 1
        all_passed &= disabled_passed
        print(f" 1 |     7     |  {outputs[0]} {outputs[1]} {outputs[2]}  | {outputs[3]} {outputs[4]} | {'✓' if disabled_passed else '✗'}")
        
        print(f"\nOverall IC Test: {'PASS ✓' if all_passed else 'FAIL ✗'}")
        return all_passed
    
    def get_truth_table(self):
        """Generate truth table for priority encoder"""
        if not self.powered:
            return "IC must be powered to generate truth table"
        
        table = f"\n{self.ic_number} Truth Table - Priority Encoder\n"
        table += "=" * 55 + "\n"
        table += "EI | Input Active | A2 A1 A0 | GS EO | Binary\n"
        table += "-" * 40 + "\n"
        
        # Enabled cases
        for input_num in range(7, -1, -1):
            inputs = {i: 1 for i in range(8)}
            inputs[input_num] = 0
            
            outputs = self.encode_inputs(inputs, enable_input=0)
            binary = self.get_binary_output()
            
            table += f" 0 |      {input_num}       |  {outputs[0]} {outputs[1]} {outputs[2]}  | {outputs[3]} {outputs[4]} |   {binary}\n"
        
        # Disabled case
        inputs = {7: 0}
        outputs = self.encode_inputs(inputs, enable_input=1)
        table += f" 1 |    Any      |  {outputs[0]} {outputs[1]} {outputs[2]}  | {outputs[3]} {outputs[4]} |  None\n"
        
        table += "\nNote: All signals are active LOW\n"
        table += "Priority: D7 > D6 > D5 > D4 > D3 > D2 > D1 > D0\n"
        table += "GS = Group Select (0 when valid input present)\n"
        table += "EO = Enable Output (0 when no input and enabled)\n"
        return table

def main():
    """Demonstration of 74148 IC"""
    print("74148 IC Demonstration")
    print("=" * 30)
    
    # Create IC instance
    ic = IC74148()
    
    # Show pinout
    print(ic.get_pinout_diagram())
    
    # Connect power
    print("Connecting power...")
    ic.connect_power()
    
    # Test the IC
    ic.test_ic()
    
    # Show truth table
    print(ic.get_truth_table())
    
    # Interactive examples
    print("\nInteractive Examples:")
    print("Encoding input 5:", ic.encode_inputs({5: 0}))
    print("Priority test (7,3,1):", ic.encode_inputs({7: 0, 3: 0, 1: 0}))
    print("Disabled state:", ic.encode_inputs({7: 0}, enable_input=1))

if __name__ == "__main__":
    main()
