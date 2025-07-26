"""
74153 IC - Dual 4-to-1 Line Data Selector/Multiplexer
Digital Logic Design - TTL 7400 Series

The 74153 contains two independent 4-to-1 multiplexers, each selecting
one of 4 inputs based on 2 shared select lines. Each has its own enable.
Pin Configuration (DIP-16):
- VCC: Pin 16
- GND: Pin 8
- Two independent 4-to-1 multiplexers with shared select lines
"""

import sys
import os
from .base_ic import BaseIC

class IC74153(BaseIC):
    """
    74153 IC - Dual 4-to-1 Line Data Selector/Multiplexer
    
    Pin Configuration (DIP-16):
    Pin 1: E2 (Enable 2 - active low)
    Pin 2: S1 (Select 1)
    Pin 3: I3_2 (Mux 2, Input 3)
    Pin 4: I2_2 (Mux 2, Input 2)
    Pin 5: I1_2 (Mux 2, Input 1)
    Pin 6: I0_2 (Mux 2, Input 0)
    Pin 7: Z2 (Mux 2, Output)
    Pin 8: GND
    Pin 9: Z1 (Mux 1, Output)
    Pin 10: I0_1 (Mux 1, Input 0)
    Pin 11: I1_1 (Mux 1, Input 1)
    Pin 12: I2_1 (Mux 1, Input 2)
    Pin 13: I3_1 (Mux 1, Input 3)
    Pin 14: S0 (Select 0)
    Pin 15: E1 (Enable 1 - active low)
    Pin 16: VCC
    
    Both multiplexers share the same select lines (S1, S0)
    When disabled, output is 0
    """
    
    def __init__(self):
        super().__init__("74153", "DIP-16", "Dual 4-to-1 Line Data Selector/Multiplexer")
        
        # Pin mapping for 74153
        self.pin_mapping = {
            1: "E2 (Enable 2)",
            2: "S1 (Select 1)",
            3: "I3_2 (Mux 2, Input 3)",
            4: "I2_2 (Mux 2, Input 2)",
            5: "I1_2 (Mux 2, Input 1)",
            6: "I0_2 (Mux 2, Input 0)",
            7: "Z2 (Mux 2, Output)",
            8: "GND",
            9: "Z1 (Mux 1, Output)",
            10: "I0_1 (Mux 1, Input 0)",
            11: "I1_1 (Mux 1, Input 1)",
            12: "I2_1 (Mux 1, Input 2)",
            13: "I3_1 (Mux 1, Input 3)",
            14: "S0 (Select 0)",
            15: "E1 (Enable 1)",
            16: "VCC"
        }
        
        # Multiplexer 1 pins
        self.mux1 = {
            'enable': 15,
            'inputs': [10, 11, 12, 13],  # I0_1, I1_1, I2_1, I3_1
            'output': 9  # Z1
        }
        
        # Multiplexer 2 pins
        self.mux2 = {
            'enable': 1,
            'inputs': [6, 5, 4, 3],  # I0_2, I1_2, I2_2, I3_2
            'output': 7  # Z2
        }
        
        # Shared select pins
        self.select_pins = [14, 2]  # S0, S1
        
        # Initialize outputs
        self.pins[self.mux1['output']] = 0
        self.pins[self.mux2['output']] = 0
    
    def update_mux(self, mux_info):
        """Update output for one multiplexer"""
        if not self.powered:
            self.pins[mux_info['output']] = 0
            return
        
        # Check if enabled (active low)
        enable_state = self.pins.get(mux_info['enable'], 1)
        if enable_state != 0:  # Disabled
            self.pins[mux_info['output']] = 0
            return
        
        # Get select inputs (shared)
        s0 = self.pins.get(self.select_pins[0], 0)  # S0
        s1 = self.pins.get(self.select_pins[1], 0)  # S1
        
        # Calculate selected input
        selected_index = s1 * 2 + s0
        
        # Get selected data input
        if 0 <= selected_index <= 3:
            selected_pin = mux_info['inputs'][selected_index]
            selected_data = self.pins.get(selected_pin, 0)
            self.pins[mux_info['output']] = selected_data
        else:
            self.pins[mux_info['output']] = 0
    
    def update_outputs(self):
        """Update both multiplexers"""
        self.update_mux(self.mux1)
        self.update_mux(self.mux2)
    
    def set_pin(self, pin_number, value):
        """Override to update outputs when inputs change"""
        super().set_pin(pin_number, value)
        self.update_outputs()
    
    def multiplex_1(self, inputs, s1, s0, enable=0):
        """
        Multiplex for MUX 1
        
        Args:
            inputs (list): 4 data inputs (I0_1 to I3_1)
            s1, s0 (int): Select inputs
            enable (int): Enable input (0 = enabled, 1 = disabled)
        
        Returns:
            int: Output value (Z1)
        """
        if not self.powered:
            return 0
        
        # Set inputs for MUX 1
        for i, data in enumerate(inputs[:4]):
            self.pins[self.mux1['inputs'][i]] = data
        
        # Set shared select lines
        self.pins[self.select_pins[0]] = s0  # S0
        self.pins[self.select_pins[1]] = s1  # S1
        
        # Set enable
        self.pins[self.mux1['enable']] = enable
        
        self.update_mux(self.mux1)
        return self.pins[self.mux1['output']]
    
    def multiplex_2(self, inputs, s1, s0, enable=0):
        """
        Multiplex for MUX 2
        
        Args:
            inputs (list): 4 data inputs (I0_2 to I3_2)
            s1, s0 (int): Select inputs
            enable (int): Enable input (0 = enabled, 1 = disabled)
        
        Returns:
            int: Output value (Z2)
        """
        if not self.powered:
            return 0
        
        # Set inputs for MUX 2
        for i, data in enumerate(inputs[:4]):
            self.pins[self.mux2['inputs'][i]] = data
        
        # Set shared select lines
        self.pins[self.select_pins[0]] = s0  # S0
        self.pins[self.select_pins[1]] = s1  # S1
        
        # Set enable
        self.pins[self.mux2['enable']] = enable
        
        self.update_mux(self.mux2)
        return self.pins[self.mux2['output']]
    
    def multiplex_both(self, inputs1, inputs2, s1, s0, enable1=0, enable2=0):
        """
        Operate both multiplexers simultaneously
        
        Args:
            inputs1 (list): 4 data inputs for MUX 1
            inputs2 (list): 4 data inputs for MUX 2
            s1, s0 (int): Shared select inputs
            enable1, enable2 (int): Individual enable inputs
        
        Returns:
            tuple: (Z1, Z2) output values
        """
        z1 = self.multiplex_1(inputs1, s1, s0, enable1)
        z2 = self.multiplex_2(inputs2, s1, s0, enable2)
        return (z1, z2)
    
    def select_input(self, input_number, inputs1, inputs2):
        """
        Select a specific input by number for both multiplexers
        
        Args:
            input_number (int): Input to select (0-3)
            inputs1, inputs2 (list): Data inputs for both muxes
        
        Returns:
            tuple: (Z1, Z2) output values
        """
        if not (0 <= input_number <= 3):
            return (0, 0)
        
        s1 = (input_number >> 1) & 1
        s0 = input_number & 1
        
        return self.multiplex_both(inputs1, inputs2, s1, s0, enable1=0, enable2=0)
    
    def test_ic(self):
        """Test both multiplexers with various input combinations"""
        if not self.powered:
            print("IC must be powered for testing")
            return False
        
        print(f"\nTesting {self.ic_number} - {self.description}")
        print("=" * 75)
        
        all_passed = True
        
        # Test data patterns
        test_data1 = [0, 1, 0, 1]  # I0_1 to I3_1
        test_data2 = [1, 0, 1, 0]  # I0_2 to I3_2
        
        print("Dual Multiplexer Test")
        print("Select | Data1 | Data2 | S1 S0 | E1 E2 | Z1 Z2 | Expected | Pass")
        print("-" * 65)
        
        # Test each input selection
        for input_num in range(4):
            s1 = (input_num >> 1) & 1
            s0 = input_num & 1
            
            outputs = self.multiplex_both(test_data1, test_data2, s1, s0, enable1=0, enable2=0)
            expected_z1 = test_data1[input_num]
            expected_z2 = test_data2[input_num]
            
            passed = (outputs[0] == expected_z1) and (outputs[1] == expected_z2)
            all_passed &= passed
            status = "✓" if passed else "✗"
            
            print(f"   {input_num}   |   {test_data1[input_num]}   |   {test_data2[input_num]}   | {s1}  {s0}  | 0  0  | {outputs[0]}  {outputs[1]}  |   {expected_z1}  {expected_z2}   | {status}")
        
        # Test individual enables
        print("\nIndividual Enable Test:")
        print("MUX | Enable | Output | Expected | Pass")
        print("-" * 35)
        
        # Test MUX 1 disabled, MUX 2 enabled
        outputs = self.multiplex_both(test_data1, test_data2, 0, 0, enable1=1, enable2=0)  # Select input 0
        enable_test1 = (outputs[0] == 0) and (outputs[1] == test_data2[0])
        all_passed &= enable_test1
        status1 = "✓" if enable_test1 else "✗"
        print(f" 1  |   1    |   {outputs[0]}    |    0     | {status1}")
        print(f" 2  |   0    |   {outputs[1]}    |    {test_data2[0]}     | {status1}")
        
        # Test MUX 1 enabled, MUX 2 disabled
        outputs = self.multiplex_both(test_data1, test_data2, 0, 1, enable1=0, enable2=1)  # Select input 1
        enable_test2 = (outputs[0] == test_data1[1]) and (outputs[1] == 0)
        all_passed &= enable_test2
        status2 = "✓" if enable_test2 else "✗"
        print(f" 1  |   0    |   {outputs[0]}    |    {test_data1[1]}     | {status2}")
        print(f" 2  |   1    |   {outputs[1]}    |    0     | {status2}")
        
        # Test different data patterns
        print("\nData Pattern Tests:")
        print("Pattern      | Sel | Z1 Z2 | Pass")
        print("-" * 30)
        
        patterns = [
            ([1, 1, 1, 1], [0, 0, 0, 0], "All 1s/0s"),
            ([0, 1, 1, 0], [1, 0, 0, 1], "Mixed"),
            ([1, 0, 1, 0], [0, 1, 0, 1], "Alternating")
        ]
        
        for pattern1, pattern2, name in patterns:
            # Test selecting input 2
            outputs = self.select_input(2, pattern1, pattern2)
            expected = (pattern1[2], pattern2[2])
            pattern_passed = outputs == expected
            all_passed &= pattern_passed
            status = "✓" if pattern_passed else "✗"
            print(f"{name:12} |  2  | {outputs[0]}  {outputs[1]}  | {status}")
        
        print(f"\nOverall IC Test: {'PASS ✓' if all_passed else 'FAIL ✗'}")
        return all_passed
    
    def get_truth_table(self):
        """Generate truth table for dual multiplexer"""
        if not self.powered:
            return "IC must be powered to generate truth table"
        
        table = f"\n{self.ic_number} Truth Table - Dual 4-to-1 Multiplexer\n"
        table += "=" * 65 + "\n"
        table += "Enable | Select | Selected | Z1 | Z2\n"
        table += "E1  E2 | S1  S0 |  Input   |    |\n"
        table += "-" * 35 + "\n"
        
        # Test with example data
        test_data1 = [0, 1, 0, 1]  # I0_1 to I3_1
        test_data2 = [1, 0, 1, 0]  # I0_2 to I3_2
        
        # Both enabled cases
        for input_num in range(4):
            s1 = (input_num >> 1) & 1
            s0 = input_num & 1
            
            outputs = self.multiplex_both(test_data1, test_data2, s1, s0, enable1=0, enable2=0)
            
            table += f" 0   0  |  {s1}   {s0} |    I{input_num}    | {outputs[0]}  | {outputs[1]}\n"
        
        # Enable variations
        table += f" 1   0  |  0   0 |    --    | 0  | {test_data2[0]}\n"  # MUX1 disabled
        table += f" 0   1  |  0   0 |    --    | {test_data1[0]}  | 0\n"  # MUX2 disabled
        table += f" 1   1  |  X   X |    --    | 0  | 0\n"  # Both disabled
        
        table += f"\nTest data: MUX1 = {test_data1}, MUX2 = {test_data2}\n"
        table += "Both multiplexers share select lines S1, S0\n"
        table += "Each has independent enable (active low)\n"
        return table

def main():
    """Demonstration of 74153 IC"""
    print("74153 IC Demonstration")
    print("=" * 30)
    
    # Create IC instance
    ic = IC74153()
    
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
    
    # Example 1: Independent operation
    data1 = [0, 1, 0, 1]
    data2 = [1, 0, 1, 0]
    print(f"MUX1 data: {data1}")
    print(f"MUX2 data: {data2}")
    print(f"Select input 2: {ic.select_input(2, data1, data2)}")
    print(f"Select input 3: {ic.select_input(3, data1, data2)}")
    
    # Example 2: Individual enables
    print(f"\nIndividual enable examples:")
    print(f"MUX1 only (select 1): {ic.multiplex_both(data1, data2, 0, 1, enable1=0, enable2=1)}")
    print(f"MUX2 only (select 1): {ic.multiplex_both(data1, data2, 0, 1, enable1=1, enable2=0)}")
    
    # Example 3: Parallel data processing
    # Process two 4-bit words simultaneously
    word1 = [1, 0, 1, 1]  # Binary 1101
    word2 = [0, 1, 0, 1]  # Binary 0101
    print(f"\nParallel 4-bit word processing:")
    print(f"Word1: {word1} (binary 1101)")
    print(f"Word2: {word2} (binary 0101)")
    for bit_pos in range(4):
        result = ic.select_input(bit_pos, word1, word2)
        print(f"Bit {bit_pos}: {result} (Word1[{bit_pos}]={word1[bit_pos]}, Word2[{bit_pos}]={word2[bit_pos]})")

if __name__ == "__main__":
    main()
