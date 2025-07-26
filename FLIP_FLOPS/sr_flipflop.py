"""
SR Flip-Flop Implementation
Digital Logic Design - Flip-Flops

The SR (Set-Reset) flip-flop is the most basic flip-flop.
It has two inputs: Set (S) and Reset (R).

Truth Table (Clock edge triggered):
S | R | Qn+1 | Comments
--|---|------|----------
0 | 0 | Qn   | No change
0 | 1 | 0    | Reset
1 | 0 | 1    | Set  
1 | 1 | X    | Invalid/Forbidden
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basic_gates'))
sys.path.append(os.path.dirname(__file__))

from base_flipflop import BaseFlipFlop
from NAND import nand_gate
from NOR import nor_gate
from NOT import not_gate

class SRFlipFlop(BaseFlipFlop):
    """
    SR Flip-Flop implementation using NAND gates
    """
    
    def __init__(self, active_high_clock=True, active_high_set=True, active_high_reset=True, 
                 implementation='nand'):
        """
        Initialize SR Flip-Flop
        
        Args:
            active_high_clock (bool): Clock edge trigger type
            active_high_set (bool): Set signal polarity
            active_high_reset (bool): Reset signal polarity
            implementation (str): 'nand' or 'nor' gate implementation
        """
        super().__init__(active_high_clock, active_high_set, active_high_reset)
        self.implementation = implementation
        
    def update(self, s, r, clock, set_pin=0, reset_pin=0):
        """
        Update SR flip-flop state
        
        Args:
            s (int): Set input (0 or 1)
            r (int): Reset input (0 or 1)
            clock (int): Clock signal (0 or 1)
            set_pin (int): Asynchronous set (0 or 1)
            reset_pin (int): Asynchronous reset (0 or 1)
            
        Returns:
            tuple: (Q, Q_bar)
        """
        self.clock_signal = clock
        self.set_signal = set_pin
        self.reset_signal = reset_pin
        
        # Process asynchronous set/reset first
        effective_set, effective_reset = self._process_set_reset(set_pin, reset_pin)
        
        # If asynchronous set or reset is active, skip synchronous operation
        if effective_set or effective_reset:
            return self.get_outputs()
        
        # Check for clock edge
        if self._detect_clock_edge(clock):
            if s == 1 and r == 1:
                # Invalid state - maintain current state or implement race condition
                print("Warning: Invalid SR inputs (S=1, R=1)")
                return self.get_outputs()
            elif s == 1 and r == 0:
                # Set
                self.q = 1
                self.q_bar = 0
            elif s == 0 and r == 1:
                # Reset
                self.q = 0
                self.q_bar = 1
            # s == 0 and r == 0: No change
        
        return self.get_outputs()
    
    def _sr_latch_nand(self, s, r):
        """
        Internal SR latch using NAND gates
        
        Args:
            s (int): Set input
            r (int): Reset input
            
        Returns:
            tuple: (Q, Q_bar)
        """
        # NAND-based SR latch
        # For NAND implementation, inputs are inverted
        s_bar = not_gate(s)
        r_bar = not_gate(r)
        
        # Cross-coupled NAND gates
        q_new = nand_gate(s_bar, self.q_bar)
        q_bar_new = nand_gate(r_bar, self.q)
        
        return q_new, q_bar_new
    
    def _sr_latch_nor(self, s, r):
        """
        Internal SR latch using NOR gates
        
        Args:
            s (int): Set input
            r (int): Reset input
            
        Returns:
            tuple: (Q, Q_bar)
        """
        # Cross-coupled NOR gates
        q_new = nor_gate(r, self.q_bar)
        q_bar_new = nor_gate(s, self.q)
        
        return q_new, q_bar_new

def test_sr_flipflop():
    """Test SR Flip-Flop functionality"""
    print("=== SR Flip-Flop Test ===")
    
    # Test with active high signals
    sr_ff = SRFlipFlop(active_high_clock=True, active_high_set=True, active_high_reset=True)
    
    print("Initial state:")
    sr_ff.print_state()
    
    print("\nTest sequence:")
    test_cases = [
        # (S, R, Clock, Set, Reset, Description)
        (0, 0, 0, 0, 0, "Initial - no inputs"),
        (1, 0, 1, 0, 0, "Set on positive edge"),
        (1, 0, 0, 0, 0, "Clock low"),
        (0, 0, 1, 0, 0, "No change on positive edge"),
        (0, 1, 0, 0, 0, "Reset input, clock low"),
        (0, 1, 1, 0, 0, "Reset on positive edge"),
        (0, 0, 0, 1, 0, "Asynchronous set"),
        (0, 0, 0, 0, 1, "Asynchronous reset"),
    ]
    
    for s, r, clk, set_pin, reset_pin, desc in test_cases:
        q, q_bar = sr_ff.update(s, r, clk, set_pin, reset_pin)
        print(f"{desc}: S={s}, R={r}, CLK={clk}, SET={set_pin}, RST={reset_pin} -> Q={q}, Q̄={q_bar}")

if __name__ == "__main__":
    test_sr_flipflop()
