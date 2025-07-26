"""
74138 IC - 3-to-8 Line Decoder/Demultiplexer
Digital Logic Design - TTL 7400 Series

The 74138 decodes a 3-bit binary input to activate one of 8 outputs.
Can function as a demultiplexer with data input on enable pins.
Pin Configuration (DIP-16):
- VCC: Pin 16
- GND: Pin 8
- 3 select inputs, 3 enable inputs, 8 outputs (active low)
"""

import sys
import os
from .base_ic import BaseIC

class IC74138(BaseIC):
    """
    74138 IC - 3-to-8 Line Decoder/Demultiplexer
    
    Pin Configuration (DIP-16):
    Pin 1: A0 (Select Input A0 - LSB)
    Pin 2: A1 (Select Input A1)
    Pin 3: A2 (Select Input A2 - MSB)
    Pin 4: E1 (Enable 1 - active low)
    Pin 5: E2 (Enable 2 - active low)
    Pin 6: E3 (Enable 3 - active high)
    Pin 7: Y7 (Output 7)
    Pin 8: GND
    Pin 9: Y6 (Output 6)
    Pin 10: Y5 (Output 5)
    Pin 11: Y4 (Output 4)
    Pin 12: Y3 (Output 3)
    Pin 13: Y2 (Output 2)
    Pin 14: Y1 (Output 1)
    Pin 15: Y0 (Output 0)
    Pin 16: VCC
    
    Enable condition: E1=0 AND E2=0 AND E3=1
    All outputs are active LOW
    """
    
    def __init__(self):
        super().__init__("74138", "DIP-16", "3-to-8 Line Decoder/Demultiplexer")
        
        # Pin mapping for 74138
        self.pin_mapping = {
            1: "A0 (Select A0 - LSB)",
            2: "A1 (Select A1)",
            3: "A2 (Select A2 - MSB)",
            4: "E1 (Enable 1 - active low)",
            5: "E2 (Enable 2 - active low)",
            6: "E3 (Enable 3 - active high)",
            7: "Y7 (Output 7)",
            8: "GND",
            9: "Y6 (Output 6)",
            10: "Y5 (Output 5)",
            11: "Y4 (Output 4)",
            12: "Y3 (Output 3)",
            13: "Y2 (Output 2)",
            14: "Y1 (Output 1)",
            15: "Y0 (Output 0)",
            16: "VCC"
        }
        
        # Pin assignments
        self.select_pins = [1, 2, 3]  # A0, A1, A2
        self.enable_pins = [4, 5, 6]  # E1, E2, E3
        self.output_pins = [15, 14, 13, 12, 11, 10, 9, 7]  # Y0-Y7
        
        # Initialize all outputs to inactive (high)
        for pin in self.output_pins:
            self.pins[pin] = 1
    
    def update_outputs(self):
        """Update outputs based on select inputs and enable conditions"""
        if not self.powered:
            # Set all outputs to inactive when not powered
            for pin in self.output_pins:
                self.pins[pin] = 1
            return
        
        # Check enable condition: E1=0 AND E2=0 AND E3=1
        e1 = self.pins.get(4, 1)  # Default to disabled
        e2 = self.pins.get(5, 1)  # Default to disabled
        e3 = self.pins.get(6, 0)  # Default to disabled
        
        enabled = (e1 == 0) and (e2 == 0) and (e3 == 1)
        
        if not enabled:
            # All outputs inactive when disabled
            for pin in self.output_pins:
                self.pins[pin] = 1
            return
        
        # Get select inputs
        a0 = self.pins.get(1, 0)
        a1 = self.pins.get(2, 0)
        a2 = self.pins.get(3, 0)
        
        # Calculate selected output (binary to decimal)
        selected = a2 * 4 + a1 * 2 + a0
        
        # Set all outputs inactive first
        for pin in self.output_pins:
            self.pins[pin] = 1
        
        # Activate selected output (active low)
        if 0 <= selected <= 7:
            selected_pin = self.output_pins[selected]
            self.pins[selected_pin] = 0
    
    def set_pin(self, pin_number, value):
        """Override to update outputs when inputs change"""
        super().set_pin(pin_number, value)
        self.update_outputs()
    
    def decode(self, a2, a1, a0, e1=0, e2=0, e3=1):
        """
        Decode 3-bit input to 8 outputs
        
        Args:
            a2, a1, a0 (int): Select inputs (binary address)
            e1, e2 (int): Enable inputs 1&2 (active low)
            e3 (int): Enable input 3 (active high)
        
        Returns:
            list: 8-element list of output states (Y0-Y7, active low)
        """
        if not self.powered:
            return [1] * 8
        
        # Set inputs
        self.pins[1] = a0
        self.pins[2] = a1
        self.pins[3] = a2
        self.pins[4] = e1
        self.pins[5] = e2
        self.pins[6] = e3
        
        self.update_outputs()
        
        # Return output states
        return [self.pins[pin] for pin in self.output_pins]
    
    def demultiplex(self, data_input, a2, a1, a0):
        """
        Use as demultiplexer - route data input to selected output
        
        Args:
            data_input (int): Data to route (0 or 1)
            a2, a1, a0 (int): Select inputs (destination address)
        
        Returns:
            list: 8-element list of output states
        """
        # For demultiplexer operation, use E3 as data input
        # E1 and E2 are tied low for enable
        return self.decode(a2, a1, a0, e1=0, e2=0, e3=data_input)
    
    def get_selected_output(self):
        """Get the currently selected output number (0-7) or None if disabled"""
        if not self.powered:
            return None
        
        # Check if enabled
        e1 = self.pins.get(4, 1)
        e2 = self.pins.get(5, 1)
        e3 = self.pins.get(6, 0)
        
        if not ((e1 == 0) and (e2 == 0) and (e3 == 1)):
            return None
        
        # Find active output (the one that's low)
        for i, pin in enumerate(self.output_pins):
            if self.pins[pin] == 0:
                return i
        
        return None
    
    def test_ic(self):
        """Test the decoder with various input combinations"""
        if not self.powered:
            print("IC must be powered for testing")
            return False
        
        print(f"\nTesting {self.ic_number} - {self.description}")
        print("=" * 70)
        print("Decoder Test (Outputs Active LOW)")
        print("A2 A1 A0 | E1 E2 E3 | Y7 Y6 Y5 Y4 Y3 Y2 Y1 Y0 | Selected | Pass")
        print("-" * 65)
        
        all_passed = True
        
        # Test all valid decode combinations
        for addr in range(8):
            a2 = (addr >> 2) & 1
            a1 = (addr >> 1) & 1
            a0 = addr & 1
            
            outputs = self.decode(a2, a1, a0, e1=0, e2=0, e3=1)
            selected = self.get_selected_output()
            
            # Check that only the addressed output is active (low)
            expected_outputs = [1] * 8
            expected_outputs[addr] = 0
            
            passed = (outputs == expected_outputs) and (selected == addr)
            all_passed &= passed
            status = "✓" if passed else "✗"
            
            out_str = ' '.join(map(str, outputs))
            print(f" {a2}  {a1}  {a0}  |  0  0  1 |  {out_str}  |    {selected}     | {status}")
        
        # Test enable function
        print("\nEnable Function Test:")
        print("A2 A1 A0 | E1 E2 E3 | All Outputs | Pass")
        print("-" * 35)
        
        enable_tests = [
            (0, 1, 1, "E1=1"),  # E1 disabled
            (1, 0, 1, "E2=1"),  # E2 disabled  
            (0, 0, 0, "E3=0"),  # E3 disabled
        ]
        
        for e1, e2, e3, desc in enable_tests:
            outputs = self.decode(0, 0, 0, e1, e2, e3)  # Try to select Y0
            disabled_passed = all(out == 1 for out in outputs)  # All should be inactive
            all_passed &= disabled_passed
            status = "✓" if disabled_passed else "✗"
            
            print(f" 0  0  0  | {e1}  {e2}  {e3} | All HIGH   | {status} ({desc})")
        
        print(f"\nOverall IC Test: {'PASS ✓' if all_passed else 'FAIL ✗'}")
        return all_passed
    
    def get_truth_table(self):
        """Generate truth table for decoder"""
        if not self.powered:
            return "IC must be powered to generate truth table"
        
        table = f"\n{self.ic_number} Truth Table - 3-to-8 Decoder\n"
        table += "=" * 60 + "\n"
        table += "Enable |  Select  | Y7 Y6 Y5 Y4 Y3 Y2 Y1 Y0 | Active Output\n"
        table += "E1 E2 E3| A2 A1 A0 |                        |\n"
        table += "-" * 55 + "\n"
        
        # Enabled cases
        for addr in range(8):
            a2 = (addr >> 2) & 1
            a1 = (addr >> 1) & 1
            a0 = addr & 1
            
            outputs = self.decode(a2, a1, a0, e1=0, e2=0, e3=1)
            out_str = ' '.join(map(str, outputs))
            
            table += f" 0  0  1 |  {a2}  {a1}  {a0}  |  {out_str}  |     Y{addr}\n"
        
        # Disabled case
        outputs = self.decode(0, 0, 0, e1=1, e2=0, e3=1)
        out_str = ' '.join(map(str, outputs))
        table += f"Any other|   X  X  X |  {out_str}  |    None\n"
        
        table += "\nNote: Outputs are active LOW\n"
        table += "Enable condition: E1=0 AND E2=0 AND E3=1\n"
        return table

def main():
    """Demonstration of 74138 IC"""
    print("74138 IC Demonstration")
    print("=" * 30)
    
    # Create IC instance
    ic = IC74138()
    
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
    print("Decoder Examples:")
    print("Select Y3:", ic.decode(0, 1, 1))  # Binary 011 = 3
    print("Select Y7:", ic.decode(1, 1, 1))  # Binary 111 = 7
    
    print("\nDemultiplexer Examples:")
    print("Route 1 to Y2:", ic.demultiplex(1, 0, 1, 0))  # Route data=1 to address 010=2
    print("Route 0 to Y5:", ic.demultiplex(0, 1, 0, 1))  # Route data=0 to address 101=5

if __name__ == "__main__":
    main()
