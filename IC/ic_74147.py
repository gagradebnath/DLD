"""
74147 IC - 10-to-4 Line Priority Encoder (Decimal to BCD)
Digital Logic Design - TTL 7400 Series

The 74147 encodes 10 input lines (representing decimal digits 0-9) 
into a 4-bit BCD (Binary-Coded Decimal) output with priority encoding.
Pin Configuration (DIP-16):
- VCC: Pin 16
- GND: Pin 8
- 10 inputs (active low), 4 outputs (active low)
"""

import sys
import os
from .base_ic import BaseIC

class IC74147(BaseIC):
    """
    74147 IC - 10-to-4 Line Priority Encoder (Decimal to BCD)
    
    Pin Configuration (DIP-16):
    Pin 1: D4 (Input 4)
    Pin 2: D5 (Input 5)
    Pin 3: D6 (Input 6)
    Pin 4: D7 (Input 7)
    Pin 5: A3 (Output A3 - MSB)
    Pin 6: A2 (Output A2)
    Pin 7: A1 (Output A1)
    Pin 8: GND
    Pin 9: A0 (Output A0 - LSB)
    Pin 10: D3 (Input 3)
    Pin 11: D2 (Input 2)
    Pin 12: D1 (Input 1)
    Pin 13: D9 (Input 9)
    Pin 14: D8 (Input 8)
    Pin 15: D0 (Input 0)
    Pin 16: VCC
    
    Note: Inputs are active LOW, Outputs are active LOW
    Input D0 is typically connected to VCC (not used for encoding)
    """
    
    def __init__(self):
        super().__init__("74147", "DIP-16", "10-to-4 Line Priority Encoder (Decimal to BCD)")
        
        # Pin mapping for 74147
        self.pin_mapping = {
            1: "D4 (Input 4)",
            2: "D5 (Input 5)",
            3: "D6 (Input 6)",
            4: "D7 (Input 7)",
            5: "A3 (Output A3 - MSB)",
            6: "A2 (Output A2)",
            7: "A1 (Output A1)",
            8: "GND",
            9: "A0 (Output A0 - LSB)",
            10: "D3 (Input 3)",
            11: "D2 (Input 2)",
            12: "D1 (Input 1)",
            13: "D9 (Input 9)",
            14: "D8 (Input 8)",
            15: "D0 (Input 0)",
            16: "VCC"
        }
        
        # Input and output pin assignments
        self.input_pins = {
            0: 15, 1: 12, 2: 11, 3: 10, 4: 1,
            5: 2, 6: 3, 7: 4, 8: 14, 9: 13
        }
        self.output_pins = [9, 7, 6, 5]  # A0, A1, A2, A3
        
        # Initialize all outputs to high (inactive)
        for pin in self.output_pins:
            self.pins[pin] = 1
    
    def update_outputs(self):
        """Update outputs based on current inputs (priority encoding)"""
        if not self.powered:
            # Set all outputs to high when not powered
            for pin in self.output_pins:
                self.pins[pin] = 1
            return
        
        # Find highest priority active input (lowest logic level)
        # Priority: 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2 > 1 > 0
        active_input = None
        
        for digit in range(9, -1, -1):  # Check from 9 down to 0
            pin = self.input_pins[digit]
            if self.pins[pin] is not None and self.pins[pin] == 0:  # Active low
                active_input = digit
                break
        
        if active_input is not None:
            # Convert to BCD (inverted output - active low)
            bcd = active_input
            self.pins[9] = (bcd & 1) ^ 1      # A0 (inverted)
            self.pins[7] = ((bcd >> 1) & 1) ^ 1  # A1 (inverted)
            self.pins[6] = ((bcd >> 2) & 1) ^ 1  # A2 (inverted)
            self.pins[5] = ((bcd >> 3) & 1) ^ 1  # A3 (inverted)
        else:
            # No active input - all outputs high
            for pin in self.output_pins:
                self.pins[pin] = 1
    
    def set_pin(self, pin_number, value):
        """Override to update outputs when inputs change"""
        super().set_pin(pin_number, value)
        self.update_outputs()
    
    def encode_decimal(self, decimal_inputs):
        """
        Encode decimal inputs to BCD output
        
        Args:
            decimal_inputs (dict): Dict with decimal digit as key, active state as value
                                 e.g., {9: 0, 8: 1, 7: 1, ...} (0 = active, 1 = inactive)
        
        Returns:
            tuple: (A3, A2, A1, A0) BCD output (inverted)
        """
        if not self.powered:
            return (1, 1, 1, 1)
        
        # Set input pins
        for digit, state in decimal_inputs.items():
            if 0 <= digit <= 9:
                pin = self.input_pins[digit]
                self.pins[pin] = state
        
        self.update_outputs()
        
        # Return outputs
        return (self.pins[5], self.pins[6], self.pins[7], self.pins[9])  # A3, A2, A1, A0
    
    def get_bcd_output(self):
        """Get current BCD output as integer (corrected for inversion)"""
        if not self.powered:
            return 0
        
        # Convert inverted outputs back to positive logic
        a0 = self.pins[9] ^ 1
        a1 = self.pins[7] ^ 1  
        a2 = self.pins[6] ^ 1
        a3 = self.pins[5] ^ 1
        
        return a3 * 8 + a2 * 4 + a1 * 2 + a0
    
    def test_ic(self):
        """Test the priority encoder with various input combinations"""
        if not self.powered:
            print("IC must be powered for testing")
            return False
        
        print(f"\nTesting {self.ic_number} - {self.description}")
        print("=" * 70)
        print("Priority Encoder Test (Inputs Active LOW, Outputs Active LOW)")
        print("Active Input | A3 A2 A1 A0 | BCD Value | Expected | Pass")
        print("-" * 55)
        
        all_passed = True
        
        # Test cases: (active_input, expected_bcd)
        test_cases = [
            (9, 9), (8, 8), (7, 7), (6, 6), (5, 5),
            (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)
        ]
        
        for active_input, expected in test_cases:
            # Set all inputs inactive (high) except the test input
            inputs = {i: 1 for i in range(10)}
            inputs[active_input] = 0  # Make test input active (low)
            
            outputs = self.encode_decimal(inputs)
            actual_bcd = self.get_bcd_output()
            
            passed = actual_bcd == expected
            all_passed &= passed
            status = "✓" if passed else "✗"
            
            print(f"    {active_input}     |  {outputs[0]} {outputs[1]} {outputs[2]} {outputs[3]}  |     {actual_bcd}     |    {expected}     | {status}")
        
        # Test priority encoding (multiple inputs active)
        print("\nPriority Encoding Test (Multiple Active Inputs):")
        print("Active Inputs | Highest | A3 A2 A1 A0 | BCD | Pass")
        print("-" * 45)
        
        priority_tests = [
            ([9, 5, 2], 9),
            ([8, 6, 3, 1], 8),
            ([7, 4], 7),
            ([5, 2, 1], 5),
            ([3, 1], 3)
        ]
        
        for active_list, expected_highest in priority_tests:
            # Set all inputs inactive except those in active_list
            inputs = {i: 1 for i in range(10)}
            for digit in active_list:
                inputs[digit] = 0
            
            outputs = self.encode_decimal(inputs)
            actual_bcd = self.get_bcd_output()
            
            passed = actual_bcd == expected_highest
            all_passed &= passed
            status = "✓" if passed else "✗"
            
            active_str = ','.join(map(str, sorted(active_list, reverse=True)))
            print(f"   {active_str:8} |    {expected_highest}    |  {outputs[0]} {outputs[1]} {outputs[2]} {outputs[3]}  | {actual_bcd:2d}  | {status}")
        
        print(f"\nOverall IC Test: {'PASS ✓' if all_passed else 'FAIL ✗'}")
        return all_passed
    
    def get_truth_table(self):
        """Generate truth table for priority encoder"""
        if not self.powered:
            return "IC must be powered to generate truth table"
        
        table = f"\n{self.ic_number} Truth Table - Priority Encoder\n"
        table += "=" * 50 + "\n"
        table += "Input Active | A3 A2 A1 A0 | BCD Output\n"
        table += "-" * 35 + "\n"
        
        for digit in range(9, -1, -1):
            inputs = {i: 1 for i in range(10)}
            inputs[digit] = 0
            
            outputs = self.encode_decimal(inputs)
            bcd = self.get_bcd_output()
            
            table += f"     {digit}       |  {outputs[0]} {outputs[1]} {outputs[2]} {outputs[3]}  |     {bcd}\n"
        
        table += "\nNote: Inputs and outputs are active LOW\n"
        table += "Priority: 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2 > 1 > 0\n"
        return table

def main():
    """Demonstration of 74147 IC"""
    print("74147 IC Demonstration")
    print("=" * 30)
    
    # Create IC instance
    ic = IC74147()
    
    # Show pinout
    print(ic.get_pinout_diagram())
    
    # Connect power
    print("Connecting power...")
    ic.connect_power()
    
    # Test the IC
    ic.test_ic()
    
    # Show truth table
    print(ic.get_truth_table())
    
    # Interactive example
    print("\nInteractive Examples:")
    print("Encoding decimal 7:", ic.encode_decimal({7: 0}))
    print("Encoding decimal 3:", ic.encode_decimal({3: 0}))
    print("Multiple inputs (9,5,2):", ic.encode_decimal({9: 0, 5: 0, 2: 0}))

if __name__ == "__main__":
    main()
