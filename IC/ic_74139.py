"""
74139 IC - Dual 2-to-4 Line Decoder/Demultiplexer
Digital Logic Design - TTL 7400 Series

The 74139 contains two independent 2-to-4 decoders, each decoding 
2-bit input to 4 outputs. Can act as demultiplexers with enable input.
Pin Configuration (DIP-16):
- VCC: Pin 16
- GND: Pin 8
- Two independent 2-to-4 decoders with enable
"""

import sys
import os
from .base_ic import BaseIC

class IC74139(BaseIC):
    """
    74139 IC - Dual 2-to-4 Line Decoder/Demultiplexer
    
    Pin Configuration (DIP-16):
    Pin 1: E1 (Enable 1 - active low)
    Pin 2: A0_1 (Decoder 1, Select A0)
    Pin 3: A1_1 (Decoder 1, Select A1)
    Pin 4: Y0_1 (Decoder 1, Output 0)
    Pin 5: Y1_1 (Decoder 1, Output 1)
    Pin 6: Y2_1 (Decoder 1, Output 2)
    Pin 7: Y3_1 (Decoder 1, Output 3)
    Pin 8: GND
    Pin 9: Y3_2 (Decoder 2, Output 3)
    Pin 10: Y2_2 (Decoder 2, Output 2)
    Pin 11: Y1_2 (Decoder 2, Output 1)
    Pin 12: Y0_2 (Decoder 2, Output 0)
    Pin 13: A1_2 (Decoder 2, Select A1)
    Pin 14: A0_2 (Decoder 2, Select A0)
    Pin 15: E2 (Enable 2 - active low)
    Pin 16: VCC
    
    All outputs are active LOW
    """
    
    def __init__(self):
        super().__init__("74139", "DIP-16", "Dual 2-to-4 Line Decoder/Demultiplexer")
        
        # Pin mapping for 74139
        self.pin_mapping = {
            1: "E1 (Enable 1)",
            2: "A0_1 (Decoder 1, A0)",
            3: "A1_1 (Decoder 1, A1)",
            4: "Y0_1 (Decoder 1, Y0)",
            5: "Y1_1 (Decoder 1, Y1)",
            6: "Y2_1 (Decoder 1, Y2)",
            7: "Y3_1 (Decoder 1, Y3)",
            8: "GND",
            9: "Y3_2 (Decoder 2, Y3)",
            10: "Y2_2 (Decoder 2, Y2)",
            11: "Y1_2 (Decoder 2, Y1)",
            12: "Y0_2 (Decoder 2, Y0)",
            13: "A1_2 (Decoder 2, A1)",
            14: "A0_2 (Decoder 2, A0)",
            15: "E2 (Enable 2)",
            16: "VCC"
        }
        
        # Decoder 1 pins
        self.decoder1 = {
            'enable': 1,
            'select': [2, 3],    # A0_1, A1_1
            'outputs': [4, 5, 6, 7]  # Y0_1, Y1_1, Y2_1, Y3_1
        }
        
        # Decoder 2 pins
        self.decoder2 = {
            'enable': 15,
            'select': [14, 13],  # A0_2, A1_2
            'outputs': [12, 11, 10, 9]  # Y0_2, Y1_2, Y2_2, Y3_2
        }
        
        # Initialize all outputs to inactive (high)
        for decoder in [self.decoder1, self.decoder2]:
            for pin in decoder['outputs']:
                self.pins[pin] = 1
    
    def update_decoder(self, decoder_info):
        """Update outputs for one decoder"""
        if not self.powered:
            # Set all outputs to inactive when not powered
            for pin in decoder_info['outputs']:
                self.pins[pin] = 1
            return
        
        # Check if enabled (active low)
        enable_state = self.pins.get(decoder_info['enable'], 1)
        if enable_state != 0:  # Not enabled
            # All outputs inactive
            for pin in decoder_info['outputs']:
                self.pins[pin] = 1
            return
        
        # Get select inputs
        a0 = self.pins.get(decoder_info['select'][0], 0)
        a1 = self.pins.get(decoder_info['select'][1], 0)
        
        # Calculate selected output
        selected = a1 * 2 + a0
        
        # Set all outputs inactive first
        for pin in decoder_info['outputs']:
            self.pins[pin] = 1
        
        # Activate selected output (active low)
        if 0 <= selected <= 3:
            selected_pin = decoder_info['outputs'][selected]
            self.pins[selected_pin] = 0
    
    def update_outputs(self):
        """Update both decoders"""
        self.update_decoder(self.decoder1)
        self.update_decoder(self.decoder2)
    
    def set_pin(self, pin_number, value):
        """Override to update outputs when inputs change"""
        super().set_pin(pin_number, value)
        self.update_outputs()
    
    def decode_1(self, a1, a0, enable=0):
        """
        Decode inputs for decoder 1
        
        Args:
            a1, a0 (int): Select inputs
            enable (int): Enable input (0 = enabled, 1 = disabled)
        
        Returns:
            list: 4-element list of output states (Y0-Y3, active low)
        """
        if not self.powered:
            return [1] * 4
        
        # Set inputs for decoder 1
        self.pins[1] = enable  # E1
        self.pins[2] = a0      # A0_1
        self.pins[3] = a1      # A1_1
        
        self.update_decoder(self.decoder1)
        
        # Return output states
        return [self.pins[pin] for pin in self.decoder1['outputs']]
    
    def decode_2(self, a1, a0, enable=0):
        """
        Decode inputs for decoder 2
        
        Args:
            a1, a0 (int): Select inputs
            enable (int): Enable input (0 = enabled, 1 = disabled)
        
        Returns:
            list: 4-element list of output states (Y0-Y3, active low)
        """
        if not self.powered:
            return [1] * 4
        
        # Set inputs for decoder 2
        self.pins[15] = enable  # E2
        self.pins[14] = a0      # A0_2
        self.pins[13] = a1      # A1_2
        
        self.update_decoder(self.decoder2)
        
        # Return output states
        return [self.pins[pin] for pin in self.decoder2['outputs']]
    
    def decode_both(self, a1_1, a0_1, enable_1, a1_2, a0_2, enable_2):
        """
        Decode inputs for both decoders simultaneously
        
        Returns:
            tuple: (decoder1_outputs, decoder2_outputs)
        """
        out1 = self.decode_1(a1_1, a0_1, enable_1)
        out2 = self.decode_2(a1_2, a0_2, enable_2)
        return (out1, out2)
    
    def demultiplex_1(self, data_input, a1, a0):
        """Use decoder 1 as demultiplexer"""
        # For demux operation, use enable as data input
        return self.decode_1(a1, a0, enable=(1 - data_input))
    
    def demultiplex_2(self, data_input, a1, a0):
        """Use decoder 2 as demultiplexer"""
        # For demux operation, use enable as data input
        return self.decode_2(a1, a0, enable=(1 - data_input))
    
    def test_ic(self):
        """Test both decoders with various input combinations"""
        if not self.powered:
            print("IC must be powered for testing")
            return False
        
        print(f"\nTesting {self.ic_number} - {self.description}")
        print("=" * 75)
        
        all_passed = True
        
        # Test Decoder 1
        print("Decoder 1 Test (Outputs Active LOW)")
        print("A1 A0 | E1 | Y3 Y2 Y1 Y0 | Selected | Pass")
        print("-" * 35)
        
        for addr in range(4):
            a1 = (addr >> 1) & 1
            a0 = addr & 1
            
            outputs = self.decode_1(a1, a0, enable=0)
            
            # Check that only the addressed output is active (low)
            expected_outputs = [1] * 4
            expected_outputs[addr] = 0
            
            passed = outputs == expected_outputs
            all_passed &= passed
            status = "✓" if passed else "✗"
            
            out_str = ' '.join(map(str, outputs))
            print(f" {a1}  {a0}  | 0  |  {out_str}  |    {addr}     | {status}")
        
        # Test Decoder 1 disabled
        outputs = self.decode_1(0, 0, enable=1)
        disabled_passed = all(out == 1 for out in outputs)
        all_passed &= disabled_passed
        print(f" 0  0  | 1  |  {' '.join(map(str, outputs))}  |   None   | {'✓' if disabled_passed else '✗'}")
        
        # Test Decoder 2
        print("\nDecoder 2 Test (Outputs Active LOW)")
        print("A1 A0 | E2 | Y3 Y2 Y1 Y0 | Selected | Pass")
        print("-" * 35)
        
        for addr in range(4):
            a1 = (addr >> 1) & 1
            a0 = addr & 1
            
            outputs = self.decode_2(a1, a0, enable=0)
            
            # Check that only the addressed output is active (low)
            expected_outputs = [1] * 4
            expected_outputs[addr] = 0
            
            passed = outputs == expected_outputs
            all_passed &= passed
            status = "✓" if passed else "✗"
            
            out_str = ' '.join(map(str, outputs))
            print(f" {a1}  {a0}  | 0  |  {out_str}  |    {addr}     | {status}")
        
        # Test Decoder 2 disabled
        outputs = self.decode_2(0, 0, enable=1)
        disabled_passed = all(out == 1 for out in outputs)
        all_passed &= disabled_passed
        print(f" 0  0  | 1  |  {' '.join(map(str, outputs))}  |   None   | {'✓' if disabled_passed else '✗'}")
        
        # Test both decoders simultaneously
        print("\nDual Operation Test:")
        print("Dec1: A1=1,A0=0,E=0  Dec2: A1=0,A0=1,E=0")
        out1, out2 = self.decode_both(1, 0, 0, 0, 1, 0)  # Dec1 selects Y2, Dec2 selects Y1
        
        dual_passed = (out1 == [1, 1, 0, 1]) and (out2 == [1, 0, 1, 1])
        all_passed &= dual_passed
        print(f"Decoder 1 outputs: {out1} (Y2 active)")
        print(f"Decoder 2 outputs: {out2} (Y1 active)")
        print(f"Dual operation: {'✓' if dual_passed else '✗'}")
        
        print(f"\nOverall IC Test: {'PASS ✓' if all_passed else 'FAIL ✗'}")
        return all_passed
    
    def get_truth_table(self):
        """Generate truth table for both decoders"""
        if not self.powered:
            return "IC must be powered to generate truth table"
        
        table = f"\n{self.ic_number} Truth Table - Dual 2-to-4 Decoder\n"
        table += "=" * 65 + "\n"
        table += "Decoder 1          | Decoder 2\n"
        table += "A1 A0 E1| Y3 Y2 Y1 Y0| A1 A0 E2| Y3 Y2 Y1 Y0\n"
        table += "-" * 60 + "\n"
        
        for addr in range(4):
            a1 = (addr >> 1) & 1
            a0 = addr & 1
            
            out1 = self.decode_1(a1, a0, enable=0)
            out2 = self.decode_2(a1, a0, enable=0)
            
            out1_str = ' '.join(map(str, out1))
            out2_str = ' '.join(map(str, out2))
            
            table += f" {a1}  {a0}  0 |  {out1_str} | {a1}  {a0}  0 |  {out2_str}\n"
        
        # Disabled cases
        out1_dis = self.decode_1(0, 0, enable=1)
        out2_dis = self.decode_2(0, 0, enable=1)
        out1_str = ' '.join(map(str, out1_dis))
        out2_str = ' '.join(map(str, out2_dis))
        table += f" X  X  1 |  {out1_str} | X  X  1 |  {out2_str}\n"
        
        table += "\nNote: Outputs are active LOW\n"
        table += "Each decoder is independent\n"
        return table

def main():
    """Demonstration of 74139 IC"""
    print("74139 IC Demonstration")
    print("=" * 30)
    
    # Create IC instance
    ic = IC74139()
    
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
    print("Decoder 1 - Select Y2:", ic.decode_1(1, 0))  # Binary 10 = 2
    print("Decoder 2 - Select Y3:", ic.decode_2(1, 1))  # Binary 11 = 3
    
    print("\nDemultiplexer Examples:")
    print("Demux 1 - Route 1 to Y1:", ic.demultiplex_1(1, 0, 1))  # Route data=1 to addr=01
    print("Demux 2 - Route 0 to Y0:", ic.demultiplex_2(0, 0, 0))  # Route data=0 to addr=00

if __name__ == "__main__":
    main()
