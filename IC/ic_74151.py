"""
74151 IC - 8-to-1 Line Data Selector/Multiplexer
Digital Logic Design - TTL 7400 Series

The 74151 selects one of 8 inputs based on 3 select lines and routes it
to complementary outputs (Y and Y̅). Includes enable input for 3-state operation.
Pin Configuration (DIP-16):
- VCC: Pin 16
- GND: Pin 8
- 8 data inputs, 3 select inputs, enable, and complementary outputs
"""

import sys
import os
from .base_ic import BaseIC

class IC74151(BaseIC):
    """
    74151 IC - 8-to-1 Line Data Selector/Multiplexer
    
    Pin Configuration (DIP-16):
    Pin 1: D3 (Data Input 3)
    Pin 2: D2 (Data Input 2)
    Pin 3: D1 (Data Input 1)
    Pin 4: D0 (Data Input 0)
    Pin 5: Y (Output)
    Pin 6: W (Inverted Output)
    Pin 7: E (Enable - active low)
    Pin 8: GND
    Pin 9: S2 (Select 2 - MSB)
    Pin 10: S1 (Select 1)
    Pin 11: S0 (Select 0 - LSB)
    Pin 12: D7 (Data Input 7)
    Pin 13: D6 (Data Input 6)
    Pin 14: D5 (Data Input 5)
    Pin 15: D4 (Data Input 4)
    Pin 16: VCC
    
    When enabled (E=0), Y = selected data input, W = ~Y
    When disabled (E=1), Y = 0, W = 1
    """
    
    def __init__(self):
        super().__init__("74151", "DIP-16", "8-to-1 Line Data Selector/Multiplexer")
        
        # Pin mapping for 74151
        self.pin_mapping = {
            1: "D3 (Data Input 3)",
            2: "D2 (Data Input 2)",
            3: "D1 (Data Input 1)",
            4: "D0 (Data Input 0)",
            5: "Y (Output)",
            6: "W (Inverted Output)",
            7: "E (Enable - active low)",
            8: "GND",
            9: "S2 (Select 2 - MSB)",
            10: "S1 (Select 1)",
            11: "S0 (Select 0 - LSB)",
            12: "D7 (Data Input 7)",
            13: "D6 (Data Input 6)",
            14: "D5 (Data Input 5)",
            15: "D4 (Data Input 4)",
            16: "VCC"
        }
        
        # Pin assignments
        self.data_pins = [4, 3, 2, 1, 15, 14, 13, 12]  # D0-D7
        self.select_pins = [11, 10, 9]  # S0, S1, S2
        self.enable_pin = 7   # E
        self.output_pin = 5   # Y
        self.inv_output_pin = 6  # W
        
        # Initialize outputs
        self.pins[self.output_pin] = 0
        self.pins[self.inv_output_pin] = 1
    
    def update_outputs(self):
        """Update outputs based on select inputs and enable"""
        if not self.powered:
            # Set outputs to 0 when not powered
            self.pins[self.output_pin] = 0
            self.pins[self.inv_output_pin] = 1
            return
        
        # Check if enabled (active low)
        enable_state = self.pins.get(self.enable_pin, 1)
        if enable_state != 0:  # Disabled
            self.pins[self.output_pin] = 0
            self.pins[self.inv_output_pin] = 1
            return
        
        # Get select inputs
        s0 = self.pins.get(self.select_pins[0], 0)
        s1 = self.pins.get(self.select_pins[1], 0)
        s2 = self.pins.get(self.select_pins[2], 0)
        
        # Calculate selected input
        selected_index = s2 * 4 + s1 * 2 + s0
        
        # Get selected data input
        if 0 <= selected_index <= 7:
            selected_pin = self.data_pins[selected_index]
            selected_data = self.pins.get(selected_pin, 0)
            
            # Set outputs
            self.pins[self.output_pin] = selected_data
            self.pins[self.inv_output_pin] = 1 - selected_data
        else:
            # Invalid selection
            self.pins[self.output_pin] = 0
            self.pins[self.inv_output_pin] = 1
    
    def set_pin(self, pin_number, value):
        """Override to update outputs when inputs change"""
        super().set_pin(pin_number, value)
        self.update_outputs()
    
    def multiplex(self, data_inputs, s2, s1, s0, enable=0):
        """
        Multiplex 8 data inputs to single output
        
        Args:
            data_inputs (list): 8 data inputs (D0-D7)
            s2, s1, s0 (int): Select inputs (binary address)
            enable (int): Enable input (0 = enabled, 1 = disabled)
        
        Returns:
            tuple: (Y, W) output values
        """
        if not self.powered:
            return (0, 1)
        
        # Set data inputs
        for i, data in enumerate(data_inputs[:8]):
            self.pins[self.data_pins[i]] = data
        
        # Set select inputs
        self.pins[self.select_pins[0]] = s0  # S0
        self.pins[self.select_pins[1]] = s1  # S1
        self.pins[self.select_pins[2]] = s2  # S2
        
        # Set enable
        self.pins[self.enable_pin] = enable
        
        self.update_outputs()
        
        # Return outputs
        return (self.pins[self.output_pin], self.pins[self.inv_output_pin])
    
    def select_input(self, input_number, data_inputs):
        """
        Select a specific input by number
        
        Args:
            input_number (int): Input to select (0-7)
            data_inputs (list): 8 data input values
        
        Returns:
            tuple: (Y, W) output values
        """
        if not (0 <= input_number <= 7):
            return (0, 1)
        
        s2 = (input_number >> 2) & 1
        s1 = (input_number >> 1) & 1
        s0 = input_number & 1
        
        return self.multiplex(data_inputs, s2, s1, s0, enable=0)
    
    def get_selected_input(self):
        """Get the currently selected input number (0-7) or None if disabled"""
        if not self.powered:
            return None
        
        # Check if enabled
        if self.pins.get(self.enable_pin, 1) != 0:
            return None
        
        # Calculate selected input from select lines
        s0 = self.pins.get(self.select_pins[0], 0)
        s1 = self.pins.get(self.select_pins[1], 0)
        s2 = self.pins.get(self.select_pins[2], 0)
        
        return s2 * 4 + s1 * 2 + s0
    
    def test_ic(self):
        """Test the multiplexer with various input combinations"""
        if not self.powered:
            print("IC must be powered for testing")
            return False
        
        print(f"\nTesting {self.ic_number} - {self.description}")
        print("=" * 70)
        print("Multiplexer Test")
        print("Selected Input | Data | S2 S1 S0 | E | Y W | Pass")
        print("-" * 45)
        
        all_passed = True
        
        # Test data: alternating pattern
        test_data = [0, 1, 0, 1, 1, 0, 1, 0]  # D0-D7
        
        # Test each input selection
        for input_num in range(8):
            s2 = (input_num >> 2) & 1
            s1 = (input_num >> 1) & 1
            s0 = input_num & 1
            
            outputs = self.multiplex(test_data, s2, s1, s0, enable=0)
            expected_y = test_data[input_num]
            expected_w = 1 - expected_y
            
            passed = (outputs[0] == expected_y) and (outputs[1] == expected_w)
            all_passed &= passed
            status = "✓" if passed else "✗"
            
            print(f"      D{input_num}       |  {test_data[input_num]}   | {s2}  {s1}  {s0}  | 0 | {outputs[0]} {outputs[1]} | {status}")
        
        # Test enable function
        print("\nEnable Function Test:")
        print("E | Y W | Expected | Pass")
        print("-" * 25)
        
        # Test disabled state
        outputs = self.multiplex(test_data, 0, 0, 0, enable=1)  # Try to select D0 but disabled
        disabled_passed = (outputs[0] == 0) and (outputs[1] == 1)
        all_passed &= disabled_passed
        status = "✓" if disabled_passed else "✗"
        print(f"1 | {outputs[0]} {outputs[1]} |   0 1    | {status}")
        
        # Test enabled state
        outputs = self.multiplex(test_data, 0, 0, 0, enable=0)  # Select D0, enabled
        enabled_passed = (outputs[0] == test_data[0]) and (outputs[1] == (1 - test_data[0]))
        all_passed &= enabled_passed
        status = "✓" if enabled_passed else "✗"
        print(f"0 | {outputs[0]} {outputs[1]} |   {test_data[0]} {1-test_data[0]}    | {status}")
        
        # Test different data patterns
        print("\nData Pattern Tests:")
        print("Pattern    | Sel | Y W | Pass")
        print("-" * 25)
        
        patterns = [
            ([1, 1, 1, 1, 0, 0, 0, 0], "High/Low"),
            ([0, 0, 0, 0, 1, 1, 1, 1], "Low/High"),
            ([1, 0, 1, 0, 1, 0, 1, 0], "Alternating")
        ]
        
        for pattern, name in patterns:
            # Test selecting input 2 (should give pattern[2])
            outputs = self.select_input(2, pattern)
            expected = (pattern[2], 1 - pattern[2])
            pattern_passed = outputs == expected
            all_passed &= pattern_passed
            status = "✓" if pattern_passed else "✗"
            print(f"{name:10} |  2  | {outputs[0]} {outputs[1]} | {status}")
        
        print(f"\nOverall IC Test: {'PASS ✓' if all_passed else 'FAIL ✗'}")
        return all_passed
    
    def get_truth_table(self):
        """Generate truth table for multiplexer"""
        if not self.powered:
            return "IC must be powered to generate truth table"
        
        table = f"\n{self.ic_number} Truth Table - 8-to-1 Multiplexer\n"
        table += "=" * 60 + "\n"
        table += "Enable | Select  | Selected | Y | W\n"
        table += "   E   | S2 S1 S0|  Input   |   |\n"
        table += "-" * 35 + "\n"
        
        # Test with simple data pattern
        test_data = [0, 1, 0, 1, 1, 0, 1, 0]
        
        # Enabled cases
        for input_num in range(8):
            s2 = (input_num >> 2) & 1
            s1 = (input_num >> 1) & 1
            s0 = input_num & 1
            
            outputs = self.multiplex(test_data, s2, s1, s0, enable=0)
            
            table += f"   0   |  {s2}  {s1}  {s0} |    D{input_num}    | {outputs[0]} | {outputs[1]}\n"
        
        # Disabled case
        outputs = self.multiplex(test_data, 0, 0, 0, enable=1)
        table += f"   1   |  X  X  X |   None   | {outputs[0]} | {outputs[1]}\n"
        
        table += f"\nTest data used: D0-D7 = {test_data}\n"
        table += "When enabled: Y = selected data input, W = ~Y\n"
        table += "When disabled: Y = 0, W = 1\n"
        return table

def main():
    """Demonstration of 74151 IC"""
    print("74151 IC Demonstration")
    print("=" * 30)
    
    # Create IC instance
    ic = IC74151()
    
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
    
    # Example 1: Simple data selection
    data = [0, 1, 0, 1, 1, 0, 1, 0]
    print(f"Data inputs: {data}")
    print(f"Select D3: {ic.select_input(3, data)}")
    print(f"Select D7: {ic.select_input(7, data)}")
    
    # Example 2: Logic function implementation
    # Implement AND gate using multiplexer: Y = A·B
    # Truth table: 00->0, 01->0, 10->0, 11->1
    and_data = [0, 0, 0, 1, 0, 0, 0, 0]  # Only D3 (11 binary) is 1
    print(f"\nAND gate implementation:")
    print(f"A=0, B=0 (select D0): {ic.select_input(0, and_data)}")  # Should be (0,1)
    print(f"A=0, B=1 (select D1): {ic.select_input(1, and_data)}")  # Should be (0,1)
    print(f"A=1, B=0 (select D2): {ic.select_input(2, and_data)}")  # Should be (0,1)
    print(f"A=1, B=1 (select D3): {ic.select_input(3, and_data)}")  # Should be (1,0)

if __name__ == "__main__":
    main()
