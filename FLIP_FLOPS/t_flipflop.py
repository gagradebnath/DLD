"""
T Flip-Flop Implementation
Digital Logic Design - Flip-Flops

The T (Toggle) flip-flop has a single toggle input. When T=1 and clock edge occurs,
the output toggles. When T=0, the output remains unchanged.

Truth Table (Clock edge triggered):
T | Qn+1 | Comments
--|------|----------
0 | Qn   | No change
1 | Q̄n   | Toggle
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basic_gates'))
sys.path.append(os.path.dirname(__file__))

from base_flipflop import BaseFlipFlop
from AND import and_gate
from OR import or_gate
from NOT import not_gate
from XOR import xor_gate
from jk_flipflop import JKFlipFlop
from d_flipflop import DFlipFlop

class TFlipFlop(BaseFlipFlop):
    """
    T Flip-Flop implementation using basic gates
    """
    
    def __init__(self, active_high_clock=True, active_high_set=True, active_high_reset=True):
        """
        Initialize T Flip-Flop
        
        Args:
            active_high_clock (bool): Clock edge trigger type
            active_high_set (bool): Set signal polarity
            active_high_reset (bool): Reset signal polarity
        """
        super().__init__(active_high_clock, active_high_set, active_high_reset)
        
    def update(self, t, clock, set_pin=0, reset_pin=0):
        """
        Update T flip-flop state
        
        Args:
            t (int): Toggle input (0 or 1)
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
            if t == 1:
                # Toggle
                self.q = not_gate(self.q)
                self.q_bar = not_gate(self.q_bar)
            # If t == 0, no change occurs
        
        return self.get_outputs()

class TFlipFlopFromJK(BaseFlipFlop):
    """
    T Flip-Flop implemented using JK flip-flop
    """
    
    def __init__(self, active_high_clock=True, active_high_set=True, active_high_reset=True):
        super().__init__(active_high_clock, active_high_set, active_high_reset)
        self.jk_ff = JKFlipFlop(active_high_clock, active_high_set, active_high_reset)
        
    def update(self, t, clock, set_pin=0, reset_pin=0):
        """
        Update T flip-flop using internal JK flip-flop
        
        For T flip-flop: J = K = T
        When T=0: J=K=0 (no change)
        When T=1: J=K=1 (toggle)
        
        Args:
            t (int): Toggle input (0 or 1)
            clock (int): Clock signal (0 or 1)
            set_pin (int): Asynchronous set (0 or 1)
            reset_pin (int): Asynchronous reset (0 or 1)
            
        Returns:
            tuple: (Q, Q_bar)
        """
        # Set J = K = T
        j = t
        k = t
        
        # Update internal JK flip-flop
        q, q_bar = self.jk_ff.update(j, k, clock, set_pin, reset_pin)
        
        # Update our state to match
        self.q = q
        self.q_bar = q_bar
        self.clock_signal = clock
        self.set_signal = set_pin
        self.reset_signal = reset_pin
        
        return self.get_outputs()

class TFlipFlopFromD(BaseFlipFlop):
    """
    T Flip-Flop implemented using D flip-flop with feedback
    """
    
    def __init__(self, active_high_clock=True, active_high_set=True, active_high_reset=True):
        super().__init__(active_high_clock, active_high_set, active_high_reset)
        self.d_ff = DFlipFlop(active_high_clock, active_high_set, active_high_reset)
        
    def update(self, t, clock, set_pin=0, reset_pin=0):
        """
        Update T flip-flop using internal D flip-flop
        
        For T flip-flop from D: D = T ⊕ Q (XOR gate)
        When T=0: D = Q (no change)
        When T=1: D = Q̄ (toggle)
        
        Args:
            t (int): Toggle input (0 or 1)
            clock (int): Clock signal (0 or 1)
            set_pin (int): Asynchronous set (0 or 1)
            reset_pin (int): Asynchronous reset (0 or 1)
            
        Returns:
            tuple: (Q, Q_bar)
        """
        # Calculate D input: D = T ⊕ Q
        d = xor_gate(t, self.q)
        
        # Update internal D flip-flop
        q, q_bar = self.d_ff.update(d, clock, set_pin, reset_pin)
        
        # Update our state to match
        self.q = q
        self.q_bar = q_bar
        self.clock_signal = clock
        self.set_signal = set_pin
        self.reset_signal = reset_pin
        
        return self.get_outputs()

class FrequencyDivider:
    """
    Frequency divider using T flip-flops
    Divides input clock frequency by 2^n where n is the number of T flip-flops
    """
    
    def __init__(self, num_stages, active_high_clock=True):
        """
        Initialize frequency divider
        
        Args:
            num_stages (int): Number of T flip-flop stages
            active_high_clock (bool): Clock polarity
        """
        self.num_stages = num_stages
        self.t_flipflops = []
        
        for i in range(num_stages):
            t_ff = TFlipFlop(active_high_clock)
            self.t_flipflops.append(t_ff)
    
    def update(self, clock):
        """
        Update frequency divider
        
        Args:
            clock (int): Input clock signal
            
        Returns:
            list: Outputs of all stages
        """
        outputs = []
        current_clock = clock
        
        for i, t_ff in enumerate(self.t_flipflops):
            # Each T flip-flop has T=1 (always toggle on clock edge)
            q, q_bar = t_ff.update(1, current_clock)
            outputs.append(q)
            
            # Next stage uses output of current stage as clock
            current_clock = q
        
        return outputs
    
    def get_division_ratio(self):
        """Get the division ratio"""
        return 2 ** self.num_stages

def test_t_flipflop():
    """Test T Flip-Flop functionality"""
    print("=== T Flip-Flop Test ===")
    
    t_ff = TFlipFlop(active_high_clock=True, active_high_set=True, active_high_reset=True)
    
    print("Initial state:")
    t_ff.print_state()
    
    print("\nTest sequence:")
    test_cases = [
        # (T, Clock, Set, Reset, Description)
        (0, 0, 0, 0, "Initial - T=0, no clock"),
        (1, 1, 0, 0, "Toggle on positive edge"),
        (1, 0, 0, 0, "Clock low, T=1"),
        (1, 1, 0, 0, "Toggle again on positive edge"),
        (0, 0, 0, 0, "T=0, clock low"),
        (0, 1, 0, 0, "No change on positive edge (T=0)"),
        (1, 0, 0, 0, "T=1, clock low"),
        (1, 1, 0, 0, "Toggle on positive edge"),
        (0, 0, 1, 0, "Asynchronous set"),
        (0, 0, 0, 1, "Asynchronous reset"),
    ]
    
    for t, clk, set_pin, reset_pin, desc in test_cases:
        q, q_bar = t_ff.update(t, clk, set_pin, reset_pin)
        print(f"{desc}: T={t}, CLK={clk}, SET={set_pin}, RST={reset_pin} -> Q={q}, Q̄={q_bar}")

def test_t_flipflop_from_jk():
    """Test T Flip-Flop implemented using JK flip-flop"""
    print("\n=== T Flip-Flop from JK Test ===")
    
    t_ff_jk = TFlipFlopFromJK(active_high_clock=True)
    
    print("T flip-flop using JK (T controls both J and K):")
    test_cases = [
        (0, 1), (1, 0), (1, 1), (1, 0), (1, 1), (0, 0), (0, 1)
    ]
    
    for t, clk in test_cases:
        q, q_bar = t_ff_jk.update(t, clk)
        print(f"T={t}, CLK={clk} -> Q={q}, Q̄={q_bar}")

def test_t_flipflop_from_d():
    """Test T Flip-Flop implemented using D flip-flop"""
    print("\n=== T Flip-Flop from D Test ===")
    
    t_ff_d = TFlipFlopFromD(active_high_clock=True)
    
    print("T flip-flop using D with feedback (D = T ⊕ Q):")
    test_cases = [
        (0, 1), (1, 0), (1, 1), (1, 0), (1, 1), (0, 0), (0, 1)
    ]
    
    for t, clk in test_cases:
        q, q_bar = t_ff_d.update(t, clk)
        print(f"T={t}, CLK={clk} -> Q={q}, Q̄={q_bar}")

def test_frequency_divider():
    """Test frequency divider using T flip-flops"""
    print("\n=== Frequency Divider Test ===")
    
    # Create a 3-stage frequency divider (divide by 8)
    freq_div = FrequencyDivider(3, active_high_clock=True)
    
    print(f"3-stage frequency divider (÷{freq_div.get_division_ratio()}):")
    print("CLK | Q2 Q1 Q0")
    print("----|--------")
    
    # Simulate several clock cycles
    for cycle in range(16):
        clock = cycle % 2  # Alternate clock signal
        outputs = freq_div.update(clock)
        print(f" {clock}  | {outputs[2]} {outputs[1]} {outputs[0]}")

if __name__ == "__main__":
    test_t_flipflop()
    test_t_flipflop_from_jk()
    test_t_flipflop_from_d()
    test_frequency_divider()
