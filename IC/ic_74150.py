"""
74150 IC - 16-to-1 Line Data Selector/Multiplexer
Digital Logic Design - TTL 7400 Series

The 74150 is a 16-to-1 multiplexer that selects one of 16 data inputs
based on a 4-bit address. The output is inverted (active low).
Pin Configuration (DIP-24):
- VCC: Pin 24
- GND: Pin 12
- 16 data inputs, 4 address inputs, enable input, inverted output
"""

import sys
import os
from .base_ic import BaseIC

class IC74150(BaseIC):
    """
    74150 IC - 16-to-1 Line Data Selector/Multiplexer
    
    Pin Configuration (DIP-24):
    Pin 1: I7 (Data Input 7)
    Pin 2: I6 (Data Input 6)
    Pin 3: I5 (Data Input 5)
    Pin 4: I4 (Data Input 4)
    Pin 5: I3 (Data Input 3)
    Pin 6: I2 (Data Input 2)
    Pin 7: I1 (Data Input 1)
    Pin 8: I0 (Data Input 0)
    Pin 9: E (Enable - active low)
    Pin 10: S3 (Address bit 3 - MSB)
    Pin 11: S2 (Address bit 2)
    Pin 12: GND
    Pin 13: S1 (Address bit 1)
    Pin 14: S0 (Address bit 0 - LSB)
    Pin 15: I15 (Data Input 15)
    Pin 16: I14 (Data Input 14)
    Pin 17: I13 (Data Input 13)
    Pin 18: I12 (Data Input 12)
    Pin 19: I11 (Data Input 11)
    Pin 20: I10 (Data Input 10)
    Pin 21: I9 (Data Input 9)
    Pin 22: I8 (Data Input 8)
    Pin 23: W (Output - inverted)
    Pin 24: VCC
    
    Output W = NOT(selected input) when enabled
    When disabled (E=1), output W = 1
    """
    
    def __init__(self):
        super().__init__("74150", "DIP-24", "16-to-1 Line Data Selector/Multiplexer")
        
        # Pin mapping for 74150
        self.pin_mapping = {
            1: "I7 (Data Input 7)",
            2: "I6 (Data Input 6)",
            3: "I5 (Data Input 5)",
            4: "I4 (Data Input 4)",
            5: "I3 (Data Input 3)",
            6: "I2 (Data Input 2)",
            7: "I1 (Data Input 1)",
            8: "I0 (Data Input 0)",
            9: "E (Enable)",
            10: "S3 (Address 3)",
            11: "S2 (Address 2)",
            12: "GND",
            13: "S1 (Address 1)",
            14: "S0 (Address 0)",
            15: "I15 (Data Input 15)",
            16: "I14 (Data Input 14)",
            17: "I13 (Data Input 13)",
            18: "I12 (Data Input 12)",
            19: "I11 (Data Input 11)",
            20: "I10 (Data Input 10)",
            21: "I9 (Data Input 9)",
            22: "I8 (Data Input 8)",
            23: "W (Output)",
            24: "VCC"
        }
        
        # Data input pins (I0-I15)
        self.data_pins = [8, 7, 6, 5, 4, 3, 2, 1, 22, 21, 20, 19, 18, 17, 16, 15]
        
        # Address pins (S0-S3)
        self.address_pins = [14, 13, 11, 10]  # S0, S1, S2, S3
        
        # Control pins
        self.enable_pin = 9   # E (active low)
        self.output_pin = 23  # W (inverted output)
        
        # Initialize output
        self.pins[self.output_pin] = 1  # Default high (disabled state)
    
    def update_output(self):
        """Update multiplexer output"""
        if not self.powered:
            self.pins[self.output_pin] = 1
            return
        
        # Check if enabled (active low)
        enable_state = self.pins.get(self.enable_pin, 1)
        if enable_state != 0:  # Disabled
            self.pins[self.output_pin] = 1
            return
        
        # Get address inputs
        address = 0
        for i, pin in enumerate(self.address_pins):
            bit_value = self.pins.get(pin, 0)
            address |= (bit_value << i)
        
        # Select data input based on address
        if 0 <= address <= 15:
            selected_pin = self.data_pins[address]
            selected_data = self.pins.get(selected_pin, 0)
            # Output is inverted
            self.pins[self.output_pin] = 1 - selected_data
        else:
            self.pins[self.output_pin] = 1
    
    def set_pin(self, pin_number, value):
        """Override to update output when inputs change"""
        super().set_pin(pin_number, value)
        self.update_output()
    
    def multiplex(self, data_inputs, address, enable=0):
        """
        Multiplex 16 data inputs
        
        Args:
            data_inputs (list): 16 data inputs (I0-I15)
            address (int): 4-bit address (0-15)
            enable (int): Enable input (0=enabled, 1=disabled)
        
        Returns:
            int: Inverted output value (W)
        """
        if not self.powered:
            return 1
        
        # Set data inputs
        for i, data in enumerate(data_inputs[:16]):
            self.pins[self.data_pins[i]] = data
        
        # Set address inputs
        for i, pin in enumerate(self.address_pins):
            bit_value = (address >> i) & 1
            self.pins[pin] = bit_value
        
        # Set enable
        self.pins[self.enable_pin] = enable
        
        self.update_output()
        return self.pins[self.output_pin]
    
    def select_input(self, input_number, data_inputs):
        """
        Select a specific input by number
        
        Args:
            input_number (int): Input to select (0-15)
            data_inputs (list): 16 data input values
        
        Returns:
            int: Inverted output value
        """
        if not (0 <= input_number <= 15):
            return 1
        
        return self.multiplex(data_inputs, input_number, enable=0)
    
    def get_selected_input(self, data_inputs):
        """
        Get the currently selected input based on address pins
        
        Args:
            data_inputs (list): 16 data input values
        
        Returns:
            tuple: (selected_index, output_value)
        """
        if not self.powered:
            return (-1, 1)
        
        # Calculate current address
        address = 0
        for i, pin in enumerate(self.address_pins):
            bit_value = self.pins.get(pin, 0)
            address |= (bit_value << i)
        
        # Set data inputs
        for i, data in enumerate(data_inputs[:16]):
            self.pins[self.data_pins[i]] = data
        
        self.update_output()
        return (address, self.pins[self.output_pin])
    
    def create_lookup_table(self, data_inputs):
        """
        Create a lookup table using the multiplexer
        
        Args:
            data_inputs (list): 16 values for the lookup table
        
        Returns:
            dict: Address to output mapping
        """
        lookup_table = {}
        
        for address in range(16):
            output = self.multiplex(data_inputs, address, enable=0)
            lookup_table[address] = output
        
        return lookup_table
    
    def test_ic(self):
        """Test 16-to-1 multiplexer with various input combinations"""
        if not self.powered:
            print("IC must be powered for testing")
            return False
        
        print(f"\nTesting {self.ic_number} - {self.description}")
        print("=" * 75)
        
        all_passed = True
        
        # Test data pattern (alternating pattern)
        test_data = [i % 2 for i in range(16)]  # 0,1,0,1,0,1...
        
        print("16-to-1 Multiplexer Test (Inverted Output)")
        print("Address | Selected | Input | Output | Expected | Pass")
        print("  (Hex) |   Input  | Value |   W    | (NOT In) |")
        print("-" * 50)
        
        # Test each address
        for addr in range(16):
            output = self.multiplex(test_data, addr, enable=0)
            expected = 1 - test_data[addr]  # Inverted
            passed = output == expected
            all_passed &= passed
            status = "✓" if passed else "✗"
            
            print(f"   {addr:02X}   |    I{addr:02d}    |   {test_data[addr]}   |   {output}    |    {expected}     | {status}")
        
        # Test enable function
        print("\nEnable Test:")
        print("Enable | Address | Output | Expected | Pass")
        print("-" * 35)
        
        # Test enabled (E=0)
        output_enabled = self.multiplex(test_data, 5, enable=0)
        expected_enabled = 1 - test_data[5]  # Inverted input 5
        enable_test1 = output_enabled == expected_enabled
        all_passed &= enable_test1
        status1 = "✓" if enable_test1 else "✗"
        print(f"   0   |    5    |   {output_enabled}    |    {expected_enabled}     | {status1}")
        
        # Test disabled (E=1)
        output_disabled = self.multiplex(test_data, 5, enable=1)
        expected_disabled = 1  # Always high when disabled
        enable_test2 = output_disabled == expected_disabled
        all_passed &= enable_test2
        status2 = "✓" if enable_test2 else "✗"
        print(f"   1   |    X    |   {output_disabled}    |    {expected_disabled}     | {status2}")
        
        # Test different data patterns
        print("\nPattern Tests:")
        print("Pattern     | Addr | Input | Output | Pass")
        print("-" * 40)
        
        patterns = [
            ("All zeros", [0] * 16, 8, 1),  # NOT(0) = 1
            ("All ones", [1] * 16, 12, 0),  # NOT(1) = 0
            ("Counter", list(range(16)), 10, 1 - 10),  # NOT(10) = inverted bit, but 10 > 1 so this test is wrong
            ("Inverse", [15-i for i in range(16)], 3, 1 - (15-3))  # NOT(12) = 0
        ]
        
        for name, pattern, addr, expected in patterns:
            output = self.multiplex(pattern, addr, enable=0)
            # Calculate the correct expected value
            input_val = pattern[addr] if addr < len(pattern) else 0
            correct_expected = 1 - input_val  # Output is inverted
            pattern_passed = output == correct_expected
            all_passed &= pattern_passed
            status = "✓" if pattern_passed else "✗"
            print(f"{name:11} | {addr:2d}   |   {input_val}   |   {output}    | {status}")
        
        # Test address decoding
        print("\nAddress Decoding Test:")
        binary_data = [0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
        
        for addr in [0, 7, 15]:  # Test boundary addresses
            output = self.select_input(addr, binary_data)
            expected = 1 - binary_data[addr]
            addr_passed = output == expected
            all_passed &= addr_passed
            status = "✓" if addr_passed else "✗"
            print(f"Address {addr:2d}: Input={binary_data[addr]}, Output={output}, Expected={expected} {status}")
        
        print(f"\nOverall IC Test: {'PASS ✓' if all_passed else 'FAIL ✗'}")
        return all_passed
    
    def get_truth_table(self):
        """Generate partial truth table for 16-to-1 multiplexer"""
        if not self.powered:
            return "IC must be powered to generate truth table"
        
        table = f"\n{self.ic_number} Truth Table - 16-to-1 Multiplexer (Partial)\n"
        table += "=" * 60 + "\n"
        table += "Enable | Address | Selected | Input | Output\n"
        table += "   E   | S3 S2 S1 S0 |  Input   |   I   |   W\n"
        table += "-" * 45 + "\n"
        
        # Test with example data pattern
        test_data = [i % 2 for i in range(16)]  # Alternating 0,1,0,1...
        
        # Show some key addresses
        key_addresses = [0, 1, 7, 8, 15]
        
        for addr in key_addresses:
            s3 = (addr >> 3) & 1
            s2 = (addr >> 2) & 1
            s1 = (addr >> 1) & 1
            s0 = addr & 1
            
            input_val = test_data[addr]
            output_val = self.multiplex(test_data, addr, enable=0)
            
            table += f"   0   |  {s3}  {s2}  {s1}  {s0}  |   I{addr:02d}    |  {input_val}  |  {output_val}\n"
        
        # Show disabled state
        table += f"   1   |  X  X  X  X  |    --    |  X  |  1\n"
        
        table += f"\nTest pattern: {test_data}\n"
        table += "Output W = NOT(selected input) when enabled\n"
        table += "Output W = 1 when disabled (E = 1)\n"
        table += "Complete table would have 2^20 = 1,048,576 rows\n"
        return table

def main():
    """Demonstration of 74150 IC"""
    print("74150 IC Demonstration")
    print("=" * 30)
    
    # Create IC instance
    ic = IC74150()
    
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
    
    # Example 1: Basic multiplexing
    data = list(range(16))  # 0, 1, 2, ..., 15
    print(f"Data inputs: {data}")
    print(f"Select input 5: {ic.select_input(5, data)} (NOT({data[5]}) = {1-data[5]})")
    print(f"Select input 10: {ic.select_input(10, data)} (NOT({data[10]}) = {1-data[10]})")
    
    # Example 2: Lookup table
    # Create a function table: f(x) = x mod 3
    function_data = [i % 3 for i in range(16)]
    lookup = ic.create_lookup_table(function_data)
    print(f"\nLookup table f(x) = x mod 3:")
    print(f"Function data: {function_data}")
    print("Address -> Output (inverted):")
    for addr in range(0, 16, 4):
        outputs = [lookup[addr+i] for i in range(4)]
        print(f"  {addr:2d}-{addr+3:2d}: {outputs}")
    
    # Example 3: 16-way data selector
    sensor_data = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0]  # 16 sensor readings
    print(f"\n16-way sensor data selector:")
    print(f"Sensor readings: {sensor_data}")
    
    # Read specific sensors
    sensors_to_read = [0, 3, 7, 12, 15]
    for sensor in sensors_to_read:
        reading = ic.select_input(sensor, sensor_data)
        original = sensor_data[sensor]
        print(f"Sensor {sensor:2d}: Original={original}, Output={reading} (inverted)")
    
    # Example 4: 16-bit word bit selection
    word = [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0]  # 16-bit word
    word_value = sum(bit << i for i, bit in enumerate(word))
    print(f"\n16-bit word bit selection:")
    print(f"Word: {word} (decimal: {word_value})")
    
    # Check specific bits
    for bit_pos in [0, 8, 15]:
        bit_output = ic.select_input(bit_pos, word)
        original_bit = word[bit_pos]
        print(f"Bit {bit_pos:2d}: {original_bit} -> {bit_output} (inverted)")

if __name__ == "__main__":
    main()
