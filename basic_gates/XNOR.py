"""
XNOR Gate Implementation
Digital Logic Design - Basic Gates

The XNOR (Exclusive NOR) gate is the inverse of XOR gate.
It outputs True when both inputs are the same (both 0 or both 1).

Truth Table:
A | B | Output
--|---|-------
0 | 0 |   1
0 | 1 |   0
1 | 0 |   0
1 | 1 |   1
"""

class XNORGate:
    """
    XNOR Gate class implementation
    """
    
    def __init__(self, num_inputs=2):
        """
        Initialize XNOR gate
        
        Args:
            num_inputs (int): Number of inputs for the gate
        """
        self.num_inputs = num_inputs
        self.gate_type = "XNOR"
    
    def evaluate(self, *inputs):
        """
        Evaluate XNOR gate output
        
        Args:
            *inputs: Variable number of inputs (0 or 1)
        
        Returns:
            int: Output of XNOR gate (0 or 1)
        """
        if len(inputs) != self.num_inputs:
            raise ValueError(f"XNOR gate expects {self.num_inputs} inputs, got {len(inputs)}")
        
        # XNOR with multiple inputs: output is 1 if even number of 1s
        return int(sum(inputs) % 2 == 0)
    
    def __call__(self, *inputs):
        """Allow gate to be called like a function"""
        return self.evaluate(*inputs)
    
    def get_truth_table(self):
        """
        Generate truth table for the gate
        
        Returns:
            list: List of tuples (inputs, output)
        """
        truth_table = []
        for i in range(2 ** self.num_inputs):
            inputs = []
            for j in range(self.num_inputs):
                inputs.append((i >> j) & 1)
            inputs.reverse()  # MSB first
            output = self.evaluate(*inputs)
            truth_table.append((tuple(inputs), output))
        return truth_table

# Backward compatibility functions
def xnor_gate(a, b):
    """
    XNOR gate function for backward compatibility
    
    Args:
        a (int): First input (0 or 1)
        b (int): Second input (0 or 1)
    
    Returns:
        int: Output of XNOR gate (0 or 1)
    """
    gate = XNORGate(2)
    return gate.evaluate(a, b)

def xnor_gate_multiple(*inputs):
    """
    XNOR gate for multiple inputs
    
    Args:
        *inputs: Variable number of inputs (0 or 1)
    
    Returns:
        int: Output of cascaded XNOR gates
    """
    if len(inputs) < 2:
        raise ValueError("XNOR gate requires at least 2 inputs")
    
    gate = XNORGate(len(inputs))
    return gate.evaluate(*inputs)

def print_truth_table():
    """Print the truth table for XNOR gate"""
    print("XNOR Gate Truth Table:")
    print("A | B | Output")
    print("--|---|-------")
    for a in [0, 1]:
        for b in [0, 1]:
            output = xnor_gate(a, b)
            print(f"{a} | {b} |   {output}")

def test_xnor_gate():
    """Test function for XNOR gate"""
    print("Testing XNOR Gate:")
    test_cases = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    for a, b in test_cases:
        result = xnor_gate(a, b)
        print(f"XNOR({a}, {b}) = {result}")
    
    print("\nTesting multiple input XNOR:")
    print(f"XNOR(0, 0, 0) = {xnor_gate_multiple(0, 0, 0)}")
    print(f"XNOR(1, 1, 1) = {xnor_gate_multiple(1, 1, 1)}")
    print(f"XNOR(0, 1, 1) = {xnor_gate_multiple(0, 1, 1)}")

if __name__ == "__main__":
    print_truth_table()
    print()
    test_xnor_gate()
