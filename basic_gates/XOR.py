"""
XOR Gate Implementation
Digital Logic Design - Basic Gates

The XOR (Exclusive OR) gate outputs True when inputs are different.
It outputs False when both inputs are the same.

Truth Table:
A | B | Output
--|---|-------
0 | 0 |   0
0 | 1 |   1
1 | 0 |   1
1 | 1 |   0
"""

class XORGate:
    """
    XOR Gate class implementation
    """
    
    def __init__(self, num_inputs=2):
        """
        Initialize XOR gate
        
        Args:
            num_inputs (int): Number of inputs for the gate
        """
        self.num_inputs = num_inputs
        self.gate_type = "XOR"
    
    def evaluate(self, *inputs):
        """
        Evaluate XOR gate output
        
        Args:
            *inputs: Variable number of inputs (0 or 1)
        
        Returns:
            int: Output of XOR gate (0 or 1)
        """
        if len(inputs) != self.num_inputs:
            raise ValueError(f"XOR gate expects {self.num_inputs} inputs, got {len(inputs)}")
        
        # XOR with multiple inputs: output is 1 if odd number of 1s
        return int(sum(inputs) % 2 == 1)
    
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
def xor_gate(a, b):
    """
    XOR gate function for backward compatibility
    
    Args:
        a (int): First input (0 or 1)
        b (int): Second input (0 or 1)
    
    Returns:
        int: Output of XOR gate (0 or 1)
    """
    gate = XORGate(2)
    return gate.evaluate(a, b)

def xor_gate_multiple(*inputs):
    """
    XOR gate for multiple inputs
    
    Args:
        *inputs: Variable number of inputs (0 or 1)
    
    Returns:
        int: Output of cascaded XOR gates
    """
    if len(inputs) < 2:
        raise ValueError("XOR gate requires at least 2 inputs")
    
    gate = XORGate(len(inputs))
    return gate.evaluate(*inputs)

def print_truth_table():
    """Print the truth table for XOR gate"""
    print("XOR Gate Truth Table:")
    print("A | B | Output")
    print("--|---|-------")
    for a in [0, 1]:
        for b in [0, 1]:
            output = xor_gate(a, b)
            print(f"{a} | {b} |   {output}")

def test_xor_gate():
    """Test function for XOR gate"""
    print("Testing XOR Gate:")
    test_cases = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    for a, b in test_cases:
        result = xor_gate(a, b)
        print(f"XOR({a}, {b}) = {result}")
    
    print("\nTesting multiple input XOR:")
    print(f"XOR(0, 0, 0) = {xor_gate_multiple(0, 0, 0)}")
    print(f"XOR(1, 1, 1) = {xor_gate_multiple(1, 1, 1)}")
    print(f"XOR(0, 1, 1) = {xor_gate_multiple(0, 1, 1)}")

if __name__ == "__main__":
    print_truth_table()
    print()
    test_xor_gate()
