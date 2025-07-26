"""
Base Flip-Flop Module
Digital Logic Design - Flip-Flops

This module provides the base class for all flip-flop implementations
with common functionality like clock, set, preset, and active high/low settings.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basic_gates'))

from AND import and_gate
from OR import or_gate
from NOT import not_gate
from NAND import nand_gate
from NOR import nor_gate

class BaseFlipFlop:
    """
    Base class for all flip-flop implementations
    
    Provides common functionality:
    - Clock edge detection
    - Set/Reset (Preset/Clear) functionality
    - Active high/low control
    - State management
    """
    
    def __init__(self, active_high_clock=True, active_high_set=True, active_high_reset=True):
        """
        Initialize base flip-flop
        
        Args:
            active_high_clock (bool): True for positive edge trigger, False for negative edge
            active_high_set (bool): True for active high set, False for active low
            active_high_reset (bool): True for active high reset, False for active low
        """
        self.active_high_clock = active_high_clock
        self.active_high_set = active_high_set
        self.active_high_reset = active_high_reset
        
        # Internal state
        self.q = 0  # Current output
        self.q_bar = 1  # Complement output
        self.previous_clock = 0  # Previous clock state for edge detection
        
        # Control signals
        self.set_signal = 0
        self.reset_signal = 0
        self.clock_signal = 0
        
    def _detect_clock_edge(self, clock):
        """
        Detect clock edge based on active high/low setting
        
        Args:
            clock (int): Current clock signal (0 or 1)
            
        Returns:
            bool: True if valid clock edge detected
        """
        if self.active_high_clock:
            # Positive edge trigger
            edge_detected = (self.previous_clock == 0 and clock == 1)
        else:
            # Negative edge trigger
            edge_detected = (self.previous_clock == 1 and clock == 0)
        
        self.previous_clock = clock
        return edge_detected
    
    def _process_set_reset(self, set_pin, reset_pin):
        """
        Process set and reset signals based on active high/low settings
        
        Args:
            set_pin (int): Set signal (0 or 1)
            reset_pin (int): Reset signal (0 or 1)
        """
        # Process set signal
        if self.active_high_set:
            effective_set = set_pin
        else:
            effective_set = not_gate(set_pin)
        
        # Process reset signal
        if self.active_high_reset:
            effective_reset = reset_pin
        else:
            effective_reset = not_gate(reset_pin)
        
        # Set has priority over reset in most implementations
        if effective_set:
            self.q = 1
            self.q_bar = 0
        elif effective_reset:
            self.q = 0
            self.q_bar = 1
        
        return effective_set, effective_reset
    
    def get_outputs(self):
        """
        Get current outputs
        
        Returns:
            tuple: (Q, Q_bar)
        """
        return (self.q, self.q_bar)
    
    def reset_state(self):
        """Reset flip-flop to initial state"""
        self.q = 0
        self.q_bar = 1
        self.previous_clock = 0
        self.set_signal = 0
        self.reset_signal = 0
        self.clock_signal = 0
    
    def print_state(self):
        """Print current state of the flip-flop"""
        print(f"Q: {self.q}, Q̄: {self.q_bar}")
        print(f"Clock: {self.clock_signal}, Set: {self.set_signal}, Reset: {self.reset_signal}")
        print(f"Active High - Clock: {self.active_high_clock}, Set: {self.active_high_set}, Reset: {self.active_high_reset}")
