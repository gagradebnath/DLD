"""
D Flip-Flop Implementation
Digital Logic Design - Flip-Flops

The D (Data) flip-flop has a single data input that is transferred to the output
on the clock edge. It's the simplest storage element.

Truth Table (Clock edge triggered):
D | Qn+1 | Comments
--|------|----------
0 | 0    | Store 0
1 | 1    | Store 1
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basic_gates'))
sys.path.append(os.path.dirname(__file__))

from base_flipflop import BaseFlipFlop
from AND import and_gate
from OR import or_gate
from NOT import not_gate
from sr_flipflop import SRFlipFlop

class DFlipFlop(BaseFlipFlop):
    """
    D Flip-Flop implementation using basic gates
    """
    
    def __init__(self, active_high_clock=True, active_high_set=True, active_high_reset=True):
        """
        Initialize D Flip-Flop
        
        Args:
            active_high_clock (bool): Clock edge trigger type
            active_high_set (bool): Set signal polarity
            active_high_reset (bool): Reset signal polarity
        """
        super().__init__(active_high_clock, active_high_set, active_high_reset)
        
    def update(self, d, clock, set_pin=0, reset_pin=0):
        """
        Update D flip-flop state
        
        Args:
            d (int): Data input (0 or 1)
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
            # D flip-flop simply transfers D to Q
            self.q = d
            self.q_bar = not_gate(d)
        
        return self.get_outputs()

class DFlipFlopFromSR(BaseFlipFlop):
    """
    D Flip-Flop implemented using SR flip-flop
    """
    
    def __init__(self, active_high_clock=True, active_high_set=True, active_high_reset=True):
        super().__init__(active_high_clock, active_high_set, active_high_reset)
        self.sr_ff = SRFlipFlop(active_high_clock, active_high_set, active_high_reset)
        
    def update(self, d, clock, set_pin=0, reset_pin=0):
        """
        Update D flip-flop using internal SR flip-flop
        
        Args:
            d (int): Data input (0 or 1)
            clock (int): Clock signal (0 or 1)
            set_pin (int): Asynchronous set (0 or 1)
            reset_pin (int): Asynchronous reset (0 or 1)
            
        Returns:
            tuple: (Q, Q_bar)
        """
        # Convert D input to S and R inputs
        # S = D, R = D̄
        s = d
        r = not_gate(d)
        
        # Update internal SR flip-flop
        q, q_bar = self.sr_ff.update(s, r, clock, set_pin, reset_pin)
        
        # Update our state to match
        self.q = q
        self.q_bar = q_bar
        self.clock_signal = clock
        self.set_signal = set_pin
        self.reset_signal = reset_pin
        
        return self.get_outputs()

class DLatch(BaseFlipFlop):
    """
    D Latch (transparent when enable is high)
    """
    
    def __init__(self, active_high_enable=True, active_high_set=True, active_high_reset=True):
        """
        Initialize D Latch
        
        Args:
            active_high_enable (bool): Enable signal polarity
            active_high_set (bool): Set signal polarity
            active_high_reset (bool): Reset signal polarity
        """
        super().__init__(True, active_high_set, active_high_reset)  # Clock not used in latch
        self.active_high_enable = active_high_enable
        
    def update(self, d, enable, set_pin=0, reset_pin=0):
        """
        Update D latch state
        
        Args:
            d (int): Data input (0 or 1)
            enable (int): Enable signal (0 or 1)
            set_pin (int): Asynchronous set (0 or 1)
            reset_pin (int): Asynchronous reset (0 or 1)
            
        Returns:
            tuple: (Q, Q_bar)
        """
        self.clock_signal = enable  # Use enable as clock for display
        self.set_signal = set_pin
        self.reset_signal = reset_pin
        
        # Process asynchronous set/reset first
        effective_set, effective_reset = self._process_set_reset(set_pin, reset_pin)
        
        if effective_set or effective_reset:
            return self.get_outputs()
        
        # Check enable signal
        effective_enable = enable if self.active_high_enable else not_gate(enable)
        
        if effective_enable:
            # Transparent - output follows input
            self.q = d
            self.q_bar = not_gate(d)
        # When enable is low, latch holds previous value
        
        return self.get_outputs()

def test_d_flipflop():
    """Test D Flip-Flop functionality"""
    print("=== D Flip-Flop Test ===")
    
    d_ff = DFlipFlop(active_high_clock=True, active_high_set=True, active_high_reset=True)
    
    print("Initial state:")
    d_ff.print_state()
    
    print("\nTest sequence:")
    test_cases = [
        # (D, Clock, Set, Reset, Description)
        (0, 0, 0, 0, "Initial - D=0, no clock"),
        (1, 1, 0, 0, "Store 1 on positive edge"),
        (1, 0, 0, 0, "Clock low, D=1"),
        (0, 1, 0, 0, "Store 0 on positive edge"),
        (1, 0, 0, 0, "Clock low, D=1"),
        (1, 1, 0, 0, "Store 1 on positive edge"),
        (0, 0, 1, 0, "Asynchronous set"),
        (1, 1, 0, 1, "Asynchronous reset"),
    ]
    
    for d, clk, set_pin, reset_pin, desc in test_cases:
        q, q_bar = d_ff.update(d, clk, set_pin, reset_pin)
        print(f"{desc}: D={d}, CLK={clk}, SET={set_pin}, RST={reset_pin} -> Q={q}, Q̄={q_bar}")

def test_d_flipflop_from_sr():
    """Test D Flip-Flop implemented using SR flip-flop"""
    print("\n=== D Flip-Flop from SR Test ===")
    
    d_ff_sr = DFlipFlopFromSR(active_high_clock=True)
    
    test_cases = [
        (0, 1), (1, 0), (1, 1), (0, 0), (0, 1), (1, 0)
    ]
    
    for d, clk in test_cases:
        q, q_bar = d_ff_sr.update(d, clk)
        print(f"D={d}, CLK={clk} -> Q={q}, Q̄={q_bar}")

def test_d_latch():
    """Test D Latch functionality"""
    print("\n=== D Latch Test ===")
    
    d_latch = DLatch(active_high_enable=True)
    
    print("D Latch test (transparent when enable=1):")
    test_cases = [
        # (D, Enable, Description)
        (0, 0, "D=0, Enable=0 (hold)"),
        (1, 0, "D=1, Enable=0 (hold)"),
        (1, 1, "D=1, Enable=1 (transparent)"),
        (0, 1, "D=0, Enable=1 (transparent)"),
        (1, 1, "D=1, Enable=1 (transparent)"),
        (0, 0, "D=0, Enable=0 (hold previous)"),
        (1, 0, "D=1, Enable=0 (hold previous)"),
    ]
    
    for d, enable, desc in test_cases:
        q, q_bar = d_latch.update(d, enable)
        print(f"{desc}: D={d}, EN={enable} -> Q={q}, Q̄={q_bar}")

if __name__ == "__main__":
    test_d_flipflop()
    test_d_flipflop_from_sr()
    test_d_latch()
