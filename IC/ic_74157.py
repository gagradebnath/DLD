"""
74157 IC - Quad 2-to-1 Line Data Selector/Multiplexer (Non-inverting)
Digital Logic Design - TTL 7400 Series

The 74157 contains four independent 2-to-1 multiplexers with a common select line.
When select is low, A inputs are routed to outputs; when high, B inputs are routed.
Pin Configuration (DIP-16):
- VCC: Pin 16
- GND: Pin 8
- Four 2-to-1 multiplexers with shared select and enable
"""

import sys
import os
from .base_ic import BaseIC

class IC74157(BaseIC):
    """
    74157 IC - Quad 2-to-1 Line Data Selector/Multiplexer (Non-inverting)
    
    Pin Configuration (DIP-16):
    Pin 1: S (Select)
    Pin 2: A1 (MUX 1, Input A)
    Pin 3: B1 (MUX 1, Input B)
    Pin 4: Y1 (MUX 1, Output)
    Pin 5: A2 (MUX 2, Input A)
    Pin 6: B2 (MUX 2, Input B)
    Pin 7: Y2 (MUX 2, Output)
    Pin 8: GND
    Pin 9: Y3 (MUX 3, Output)
    Pin 10: B3 (MUX 3, Input B)
    Pin 11: A3 (MUX 3, Input A)
    Pin 12: Y4 (MUX 4, Output)
    Pin 13: B4 (MUX 4, Input B)
    Pin 14: A4 (MUX 4, Input A)
    Pin 15: E (Enable - active low)
    Pin 16: VCC
    
    When S = 0: Y = A (A inputs to outputs)
    When S = 1: Y = B (B inputs to outputs)
    When E = 1: All outputs are 0 (disabled)
    """
    
    def __init__(self):
        super().__init__("74157", "DIP-16", "Quad 2-to-1 Line Data Selector/Multiplexer")
        
        # Pin mapping for 74157
        self.pin_mapping = {
            1: "S (Select)",
            2: "A1 (MUX 1, Input A)",
            3: "B1 (MUX 1, Input B)",
            4: "Y1 (MUX 1, Output)",
            5: "A2 (MUX 2, Input A)",
            6: "B2 (MUX 2, Input B)",
            7: "Y2 (MUX 2, Output)",
            8: "GND",
            9: "Y3 (MUX 3, Output)",
            10: "B3 (MUX 3, Input B)",
            11: "A3 (MUX 3, Input A)",
            12: "Y4 (MUX 4, Output)",
            13: "B4 (MUX 4, Input B)",
            14: "A4 (MUX 4, Input A)",
            15: "E (Enable)",
            16: "VCC"
        }
        
        # Control pins
        self.select_pin = 1    # S
        self.enable_pin = 15   # E (active low)
        
        # Multiplexer definitions
        self.multiplexers = [
            {'a': 2, 'b': 3, 'y': 4},   # MUX 1
            {'a': 5, 'b': 6, 'y': 7},   # MUX 2
            {'a': 11, 'b': 10, 'y': 9}, # MUX 3
            {'a': 14, 'b': 13, 'y': 12} # MUX 4
        ]
        
        # Initialize outputs
        for mux in self.multiplexers:
            self.pins[mux['y']] = 0
    
    def update_outputs(self):
        """Update all multiplexer outputs"""
        if not self.powered:
            for mux in self.multiplexers:
                self.pins[mux['y']] = 0
            return
        
        # Check if enabled (active low)
        enable_state = self.pins.get(self.enable_pin, 1)
        if enable_state != 0:  # Disabled
            for mux in self.multiplexers:
                self.pins[mux['y']] = 0
            return
        
        # Get select input
        select = self.pins.get(self.select_pin, 0)
        
        # Update each multiplexer
        for mux in self.multiplexers:
            if select == 0:
                # Select A input
                input_value = self.pins.get(mux['a'], 0)
            else:
                # Select B input
                input_value = self.pins.get(mux['b'], 0)
            
            self.pins[mux['y']] = input_value
    
    def set_pin(self, pin_number, value):
        """Override to update outputs when inputs change"""
        super().set_pin(pin_number, value)
        self.update_outputs()
    
    def multiplex(self, a_inputs, b_inputs, select, enable=0):
        """
        Multiplex four 2-to-1 channels
        
        Args:
            a_inputs (list): 4 A inputs (A1-A4)
            b_inputs (list): 4 B inputs (B1-B4)
            select (int): Select input (0=A, 1=B)
            enable (int): Enable input (0=enabled, 1=disabled)
        
        Returns:
            list: 4 output values (Y1-Y4)
        """
        if not self.powered:
            return [0, 0, 0, 0]
        
        # Set A inputs
        for i, a_val in enumerate(a_inputs[:4]):
            self.pins[self.multiplexers[i]['a']] = a_val
        
        # Set B inputs
        for i, b_val in enumerate(b_inputs[:4]):
            self.pins[self.multiplexers[i]['b']] = b_val
        
        # Set control pins
        self.pins[self.select_pin] = select
        self.pins[self.enable_pin] = enable
        
        self.update_outputs()
        
        # Return outputs
        return [self.pins[mux['y']] for mux in self.multiplexers]
    
    def select_a_inputs(self, a_inputs):
        """
        Select A inputs for all multiplexers
        
        Args:
            a_inputs (list): 4 A input values
        
        Returns:
            list: 4 output values
        """
        b_inputs = [0, 0, 0, 0]  # Don't care when selecting A
        return self.multiplex(a_inputs, b_inputs, select=0, enable=0)
    
    def select_b_inputs(self, b_inputs):
        """
        Select B inputs for all multiplexers
        
        Args:
            b_inputs (list): 4 B input values
        
        Returns:
            list: 4 output values
        """
        a_inputs = [0, 0, 0, 0]  # Don't care when selecting B
        return self.multiplex(a_inputs, b_inputs, select=1, enable=0)
    
    def route_inputs(self, inputs_a, inputs_b, route_to_a=True):
        """
        Route one set of inputs to outputs
        
        Args:
            inputs_a (list): A input values
            inputs_b (list): B input values
            route_to_a (bool): True to route A to Y, False to route B to Y
        
        Returns:
            list: Output values
        """
        select = 0 if route_to_a else 1
        return self.multiplex(inputs_a, inputs_b, select, enable=0)
    
    def parallel_switch(self, data1, data2, switch_position):
        """
        Act as a 4-bit parallel switch between two data sources
        
        Args:
            data1 (list): First 4-bit data source (A inputs)
            data2 (list): Second 4-bit data source (B inputs)
            switch_position (int): 0 for data1, 1 for data2
        
        Returns:
            list: Selected 4-bit data
        """
        return self.multiplex(data1, data2, switch_position, enable=0)
    
    def test_ic(self):
        """Test quad 2-to-1 multiplexer with various input combinations"""
        if not self.powered:
            print("IC must be powered for testing")
            return False
        
        print(f"\nTesting {self.ic_number} - {self.description}")
        print("=" * 75)
        
        all_passed = True
        
        # Test data patterns
        a_data = [0, 1, 0, 1]  # A1-A4
        b_data = [1, 0, 1, 0]  # B1-B4
        
        print("Quad 2-to-1 Multiplexer Test")
        print("A Inputs | B Inputs | S | E | Y Outputs | Expected | Pass")
        print("-" * 60)
        
        # Test selecting A inputs
        outputs = self.multiplex(a_data, b_data, select=0, enable=0)
        a_passed = outputs == a_data
        all_passed &= a_passed
        status_a = "✓" if a_passed else "✗"
        print(f"  {a_data}  |  {b_data}  | 0 | 0 |   {outputs}   |   {a_data}   | {status_a}")
        
        # Test selecting B inputs
        outputs = self.multiplex(a_data, b_data, select=1, enable=0)
        b_passed = outputs == b_data
        all_passed &= b_passed
        status_b = "✓" if b_passed else "✗"
        print(f"  {a_data}  |  {b_data}  | 1 | 0 |   {outputs}   |   {b_data}   | {status_b}")
        
        # Test disabled state
        outputs = self.multiplex(a_data, b_data, select=0, enable=1)
        disabled_expected = [0, 0, 0, 0]
        disabled_passed = outputs == disabled_expected
        all_passed &= disabled_passed
        status_disabled = "✓" if disabled_passed else "✗"
        print(f"  {a_data}  |  {b_data}  | X | 1 |   {outputs}   |   {disabled_expected}   | {status_disabled}")
        
        # Test different data patterns
        print("\nPattern Tests:")
        print("Pattern Name | A Data | B Data | Sel | Output | Pass")
        print("-" * 50)
        
        patterns = [
            ("All zeros", [0, 0, 0, 0], [1, 1, 1, 1], 0),
            ("All ones", [1, 1, 1, 1], [0, 0, 0, 0], 0),
            ("Alternating", [1, 0, 1, 0], [0, 1, 0, 1], 1),
            ("Counter", [0, 0, 1, 1], [1, 1, 0, 0], 0)
        ]
        
        for name, a_pat, b_pat, sel in patterns:
            outputs = self.multiplex(a_pat, b_pat, sel, enable=0)
            expected = a_pat if sel == 0 else b_pat
            pattern_passed = outputs == expected
            all_passed &= pattern_passed
            status = "✓" if pattern_passed else "✗"
            print(f"{name:12} | {a_pat} | {b_pat} |  {sel}  | {outputs} | {status}")
        
        # Test individual multiplexer control
        print("\nIndividual MUX Test (using mixed inputs):")
        mixed_a = [1, 0, 1, 0]
        mixed_b = [0, 1, 0, 1]
        
        # Test both selections
        for sel in [0, 1]:
            outputs = self.multiplex(mixed_a, mixed_b, sel, enable=0)
            expected = mixed_a if sel == 0 else mixed_b
            source = "A" if sel == 0 else "B"
            individual_passed = outputs == expected
            all_passed &= individual_passed
            status = "✓" if individual_passed else "✗"
            print(f"Select {source} inputs: {outputs} (expected {expected}) {status}")
        
        print(f"\nOverall IC Test: {'PASS ✓' if all_passed else 'FAIL ✗'}")
        return all_passed
    
    def get_truth_table(self):
        """Generate truth table for quad 2-to-1 multiplexer"""
        if not self.powered:
            return "IC must be powered to generate truth table"
        
        table = f"\n{self.ic_number} Truth Table - Quad 2-to-1 Multiplexer\n"
        table += "=" * 55 + "\n"
        table += "Enable | Select | A Input | B Input | Output\n"
        table += "   E   |   S    |    A    |    B    |   Y\n"
        table += "-" * 40 + "\n"
        
        # Truth table for one multiplexer (all work the same)
        truth_cases = [
            (0, 0, 0, 0, 0),  # E=0, S=0, A=0, B=X -> Y=A=0
            (0, 0, 1, 0, 1),  # E=0, S=0, A=1, B=X -> Y=A=1
            (0, 0, 0, 1, 0),  # E=0, S=0, A=0, B=X -> Y=A=0
            (0, 0, 1, 1, 1),  # E=0, S=0, A=1, B=X -> Y=A=1
            (0, 1, 0, 0, 0),  # E=0, S=1, A=X, B=0 -> Y=B=0
            (0, 1, 1, 0, 0),  # E=0, S=1, A=X, B=0 -> Y=B=0
            (0, 1, 0, 1, 1),  # E=0, S=1, A=X, B=1 -> Y=B=1
            (0, 1, 1, 1, 1),  # E=0, S=1, A=X, B=1 -> Y=B=1
            (1, 0, 0, 0, 0),  # E=1, disabled -> Y=0
            (1, 0, 1, 1, 0),  # E=1, disabled -> Y=0
            (1, 1, 0, 0, 0),  # E=1, disabled -> Y=0
            (1, 1, 1, 1, 0),  # E=1, disabled -> Y=0
        ]
        
        for e, s, a, b, y in truth_cases:
            x_a = "X" if s == 1 else str(a)
            x_b = "X" if s == 0 else str(b)
            table += f"   {e}   |   {s}    |    {x_a}    |    {x_b}    |   {y}\n"
        
        table += "\nFunction: Y = (E') · ((S')·A + S·B)\n"
        table += "All four multiplexers operate identically\n"
        table += "X = Don't care (input not selected)\n"
        return table

def main():
    """Demonstration of 74157 IC"""
    print("74157 IC Demonstration")
    print("=" * 30)
    
    # Create IC instance
    ic = IC74157()
    
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
    
    # Example 1: Data selection
    data_a = [1, 0, 1, 1]  # 4-bit word A
    data_b = [0, 1, 0, 0]  # 4-bit word B
    print(f"Data A: {data_a} (binary 1011)")
    print(f"Data B: {data_b} (binary 0100)")
    print(f"Select A: {ic.select_a_inputs(data_a)}")
    print(f"Select B: {ic.select_b_inputs(data_b)}")
    
    # Example 2: Parallel data switching
    cpu_data = [1, 1, 0, 1]
    memory_data = [0, 1, 1, 0]
    print(f"\nParallel Data Switching:")
    print(f"CPU data:    {cpu_data}")
    print(f"Memory data: {memory_data}")
    print(f"Route CPU:    {ic.parallel_switch(cpu_data, memory_data, 0)}")
    print(f"Route Memory: {ic.parallel_switch(cpu_data, memory_data, 1)}")
    
    # Example 3: 4-bit bus multiplexer
    bus1 = [0, 0, 1, 1]  # Bus 1 data
    bus2 = [1, 1, 0, 0]  # Bus 2 data
    print(f"\n4-bit Bus Multiplexer:")
    print(f"Bus 1: {bus1}")
    print(f"Bus 2: {bus2}")
    
    for switch_pos in [0, 1]:
        bus_name = "Bus 1" if switch_pos == 0 else "Bus 2"
        result = ic.parallel_switch(bus1, bus2, switch_pos)
        print(f"Switch to {bus_name}: {result}")
    
    # Example 4: Nibble selection
    low_nibble = [1, 0, 1, 0]
    high_nibble = [0, 1, 0, 1]
    print(f"\nNibble Selection:")
    print(f"Low nibble:  {low_nibble}")
    print(f"High nibble: {high_nibble}")
    print(f"Select low:  {ic.route_inputs(low_nibble, high_nibble, route_to_a=True)}")
    print(f"Select high: {ic.route_inputs(low_nibble, high_nibble, route_to_a=False)}")

if __name__ == "__main__":
    main()
