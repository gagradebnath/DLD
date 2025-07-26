"""
Base IC Class
Digital Logic Design - Integrated Circuits

This module provides the base class for all IC implementations
with common functionality for pin management, power, and testing.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basic_gates'))

class BaseIC:
    """
    Base class for all IC implementations
    
    Provides common functionality:
    - Pin management and mapping
    - Power supply handling (VCC/GND)
    - IC identification and testing
    - Truth table generation
    """
    
    def __init__(self, ic_number, package_type="DIP-14", description="Generic IC"):
        """
        Initialize base IC
        
        Args:
            ic_number (str): IC part number (e.g., "7400")
            package_type (str): Package type (e.g., "DIP-14", "DIP-16")
            description (str): IC description
        """
        self.ic_number = ic_number
        self.package_type = package_type
        self.description = description
        
        # Extract number of pins from package type
        if "DIP-" in package_type:
            self.num_pins = int(package_type.split("-")[1])
        else:
            self.num_pins = 14  # Default
        
        # Standard power pins for DIP packages
        if self.num_pins == 14:
            self.vcc_pin = 14
            self.gnd_pin = 7
        elif self.num_pins == 16:
            self.vcc_pin = 16
            self.gnd_pin = 8
        else:
            self.vcc_pin = self.num_pins
            self.gnd_pin = self.num_pins // 2
        
        # Pin states (1-indexed to match IC pin numbering)
        self.pins = {i: None for i in range(1, self.num_pins + 1)}
        
        # Power state
        self.powered = False
        
        # Gate instances (to be defined by subclasses)
        self.gates = {}
        
        # Pin mapping (to be defined by subclasses)
        self.pin_mapping = {}
    
    def set_pin(self, pin_number, value):
        """
        Set a pin to a specific logic level
        
        Args:
            pin_number (int): Pin number (1-indexed)
            value (int): Logic level (0 or 1)
        """
        if 1 <= pin_number <= self.num_pins:
            if pin_number == self.vcc_pin:
                self.powered = (value == 1)
            elif pin_number == self.gnd_pin:
                pass  # Ground pin, should always be 0
            else:
                self.pins[pin_number] = value
        else:
            raise ValueError(f"Invalid pin number {pin_number}. IC has pins 1-{self.num_pins}")
    
    def get_pin(self, pin_number):
        """
        Get the current logic level of a pin
        
        Args:
            pin_number (int): Pin number (1-indexed)
            
        Returns:
            int: Logic level (0, 1, or None if not connected)
        """
        if not self.powered:
            return 0  # All outputs are 0 when not powered
        
        if 1 <= pin_number <= self.num_pins:
            if pin_number == self.vcc_pin:
                return 1 if self.powered else 0
            elif pin_number == self.gnd_pin:
                return 0
            else:
                return self.pins[pin_number]
        else:
            raise ValueError(f"Invalid pin number {pin_number}. IC has pins 1-{self.num_pins}")
    
    def connect_power(self, vcc=1, gnd=0):
        """
        Connect power to the IC
        
        Args:
            vcc (int): VCC level (should be 1)
            gnd (int): GND level (should be 0)
        """
        self.set_pin(self.vcc_pin, vcc)
        self.set_pin(self.gnd_pin, gnd)
    
    def is_powered(self):
        """Check if IC is properly powered"""
        return self.powered
    
    def reset_pins(self):
        """Reset all pins to None (disconnected state)"""
        for pin in range(1, self.num_pins + 1):
            if pin not in [self.vcc_pin, self.gnd_pin]:
                self.pins[pin] = None
        self.powered = False
    
    def get_pin_description(self, pin_number):
        """
        Get description of a pin's function
        
        Args:
            pin_number (int): Pin number
            
        Returns:
            str: Pin description
        """
        if pin_number == self.vcc_pin:
            return "VCC (Power)"
        elif pin_number == self.gnd_pin:
            return "GND (Ground)"
        elif pin_number in self.pin_mapping:
            return self.pin_mapping[pin_number]
        else:
            return "Not connected"
    
    def get_pinout_diagram(self):
        """
        Generate a text-based pinout diagram
        
        Returns:
            str: ASCII pinout diagram
        """
        diagram = f"\n{self.ic_number} ({self.package_type}) - {self.description}\n"
        diagram += "=" * (len(self.ic_number) + len(self.package_type) + len(self.description) + 7) + "\n"
        
        # For DIP packages, show pins in dual-inline format
        if "DIP" in self.package_type:
            left_pins = list(range(1, self.num_pins // 2 + 1))
            right_pins = list(range(self.num_pins, self.num_pins // 2, -1))
            
            diagram += "\n"
            for i, (left, right) in enumerate(zip(left_pins, right_pins)):
                left_desc = self.get_pin_description(left)
                right_desc = self.get_pin_description(right)
                diagram += f"{left:2d} ┤{left_desc:^12}├─────────┤{right_desc:^12}├ {right:2d}\n"
            diagram += "\n"
        
        return diagram
    
    def test_ic(self):
        """
        Test IC functionality (to be implemented by subclasses)
        
        Returns:
            bool: True if all tests pass
        """
        return True
    
    def __str__(self):
        """String representation of the IC"""
        power_status = "Powered" if self.powered else "Not powered"
        return f"{self.ic_number} - {self.description} ({power_status})"
    
    def __repr__(self):
        """Detailed string representation"""
        return f"IC('{self.ic_number}', '{self.package_type}', powered={self.powered})"
