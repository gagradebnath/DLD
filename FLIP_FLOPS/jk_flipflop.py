"""
JK Flip-Flop Implementation
Digital Logic Design - Flip-Flops

The JK flip-flop is an enhanced version of SR flip-flop that eliminates the forbidden state.
When J=K=1, the output toggles.

Truth Table (Clock edge triggered):
J | K | Qn+1 | Comments
--|---|------|----------
0 | 0 | Qn   | No change
0 | 1 | 0    | Reset
1 | 0 | 1    | Set
1 | 1 | Q̄n   | Toggle
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'basic_gates'))
sys.path.append(os.path.dirname(__file__))

from base_flipflop import BaseFlipFlop
from AND import and_gate
from OR import or_gate
from NOT import not_gate
from NAND import nand_gate

class JKFlipFlop(BaseFlipFlop):
    """
    JK Flip-Flop implementation using basic gates
    """
    
    def __init__(self, active_high_clock=True, active_high_set=True, active_high_reset=True):
        """
        Initialize JK Flip-Flop
        
        Args:
            active_high_clock (bool): Clock edge trigger type
            active_high_set (bool): Set signal polarity  
            active_high_reset (bool): Reset signal polarity
        """
        super().__init__(active_high_clock, active_high_set, active_high_reset)
        
    def update(self, j, k, clock, set_pin=0, reset_pin=0):
        """
        Update JK flip-flop state
        
        Args:
            j (int): J input (0 or 1)
            k (int): K input (0 or 1)
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
            # JK logic implementation
            if j == 0 and k == 0:
                # No change
                pass
            elif j == 0 and k == 1:
                # Reset
                self.q = 0
                self.q_bar = 1
            elif j == 1 and k == 0:
                # Set
                self.q = 1
                self.q_bar = 0
            elif j == 1 and k == 1:
                # Toggle
                self.q = not_gate(self.q)
                self.q_bar = not_gate(self.q_bar)
        
        return self.get_outputs()
    
    def _jk_logic_gates(self, j, k, clock):
        """
        Internal JK logic using basic gates
        
        Args:
            j (int): J input
            k (int): K input
            clock (int): Clock input
            
        Returns:
            tuple: (Q, Q_bar)
        """
        # JK flip-flop logic:
        # S = J AND Q̄ AND Clock
        # R = K AND Q AND Clock
        
        # Generate S and R for internal SR latch
        s = and_gate(and_gate(j, self.q_bar), clock)
        r = and_gate(and_gate(k, self.q), clock)
        
        # SR latch logic
        if s == 1 and r == 0:
            return 1, 0
        elif s == 0 and r == 1:
            return 0, 1
        else:
            return self.q, self.q_bar

class MasterSlaveJKFlipFlop(JKFlipFlop):
    """
    Master-Slave JK Flip-Flop to eliminate race conditions
    """
    
    def __init__(self, active_high_clock=True, active_high_set=True, active_high_reset=True):
        super().__init__(active_high_clock, active_high_set, active_high_reset)
        # Master latch state
        self.master_q = 0
        self.master_q_bar = 1
        
    def update(self, j, k, clock, set_pin=0, reset_pin=0):
        """
        Update Master-Slave JK flip-flop state
        """
        self.clock_signal = clock
        self.set_signal = set_pin
        self.reset_signal = reset_pin
        
        # Process asynchronous set/reset first
        effective_set, effective_reset = self._process_set_reset(set_pin, reset_pin)
        
        if effective_set or effective_reset:
            self.master_q = self.q
            self.master_q_bar = self.q_bar
            return self.get_outputs()
        
        # Master-Slave operation
        if clock == 1:
            # Master latch active (transparent)
            self._update_master(j, k)
        elif self._detect_clock_edge(clock):
            # Slave latch updates on clock edge (negative edge in this case)
            self.q = self.master_q
            self.q_bar = self.master_q_bar
        
        return self.get_outputs()
    
    def _update_master(self, j, k):
        """Update master latch"""
        if j == 0 and k == 0:
            pass  # No change
        elif j == 0 and k == 1:
            self.master_q = 0
            self.master_q_bar = 1
        elif j == 1 and k == 0:
            self.master_q = 1
            self.master_q_bar = 0
        elif j == 1 and k == 1:
            # Toggle based on current slave output
            self.master_q = not_gate(self.q)
            self.master_q_bar = not_gate(self.q_bar)

def test_jk_flipflop():
    """Test JK Flip-Flop functionality"""
    print("=== JK Flip-Flop Test ===")
    
    jk_ff = JKFlipFlop(active_high_clock=True, active_high_set=True, active_high_reset=True)
    
    print("Initial state:")
    jk_ff.print_state()
    
    print("\nTest sequence:")
    test_cases = [
        # (J, K, Clock, Set, Reset, Description)
        (0, 0, 0, 0, 0, "Initial - no inputs"),
        (1, 0, 1, 0, 0, "Set on positive edge"),
        (1, 0, 0, 0, 0, "Clock low"),
        (0, 0, 1, 0, 0, "No change on positive edge"),
        (0, 1, 0, 0, 0, "Reset input, clock low"),
        (0, 1, 1, 0, 0, "Reset on positive edge"),
        (1, 1, 0, 0, 0, "Toggle input, clock low"),
        (1, 1, 1, 0, 0, "Toggle on positive edge"),
        (1, 1, 0, 0, 0, "Clock low"),
        (1, 1, 1, 0, 0, "Toggle again on positive edge"),
        (0, 0, 0, 1, 0, "Asynchronous set"),
        (0, 0, 0, 0, 1, "Asynchronous reset"),
    ]
    
    for j, k, clk, set_pin, reset_pin, desc in test_cases:
        q, q_bar = jk_ff.update(j, k, clk, set_pin, reset_pin)
        print(f"{desc}: J={j}, K={k}, CLK={clk}, SET={set_pin}, RST={reset_pin} -> Q={q}, Q̄={q_bar}")

def test_master_slave_jk():
    """Test Master-Slave JK Flip-Flop"""
    print("\n=== Master-Slave JK Flip-Flop Test ===")
    
    ms_jk_ff = MasterSlaveJKFlipFlop(active_high_clock=True)
    
    print("Master-Slave JK test with clock pulse:")
    test_sequence = [
        (1, 1, 0), (1, 1, 1), (1, 1, 0),  # Toggle sequence
        (1, 0, 0), (1, 0, 1), (1, 0, 0),  # Set sequence
        (0, 1, 0), (0, 1, 1), (0, 1, 0),  # Reset sequence
    ]
    
    for j, k, clk in test_sequence:
        q, q_bar = ms_jk_ff.update(j, k, clk)
        print(f"J={j}, K={k}, CLK={clk} -> Q={q}, Q̄={q_bar}")

if __name__ == "__main__":
    test_jk_flipflop()
    test_master_slave_jk()
