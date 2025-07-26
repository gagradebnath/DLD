"""
OR Gate Implementation
Digital Logic Design - Basic Gates

The OR gate outputs True when at least one input is True.

Truth Table:
A | B | Output
--|---|-------
0 | 0 |   0
0 | 1 |   1
1 | 0 |   1
1 | 1 |   1
"""

class ORGate:
    """
    OR Gate class implementation
    """
    
    def __init__(self, num_inputs=2):
        """
        Initialize OR gate
        
        Args:
            num_inputs (int): Number of inputs for the gate
        """
        self.num_inputs = num_inputs
        self.gate_type = "OR"
    
    def evaluate(self, *inputs):
        """
        Evaluate OR gate output
        
        Args:
            *inputs: Variable number of inputs (0 or 1)
        
        Returns:
            int: Output of OR gate (0 or 1)
        """
        if len(inputs) != self.num_inputs:
            raise ValueError(f"OR gate expects {self.num_inputs} inputs, got {len(inputs)}")
        
        return int(any(inputs))
    
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
def or_gate(a, b):
    """
    OR gate function for backward compatibility
    
    Args:
        a (int): First input (0 or 1)
        b (int): Second input (0 or 1)
    
    Returns:
        int: Output of OR gate (0 or 1)
    """
    gate = ORGate(2)
    return gate.evaluate(a, b)

def or_gate_multiple(*inputs):
    """
    OR gate for multiple inputs
    
    Args:
        *inputs: Variable number of inputs (0 or 1)
    
    Returns:
        int: Output of OR gate with multiple inputs
    """
    if len(inputs) < 2:
        raise ValueError("OR gate requires at least 2 inputs")
    
    gate = ORGate(len(inputs))
    return gate.evaluate(*inputs)

def print_truth_table():
    """Print the truth table for OR gate"""
    print("OR Gate Truth Table:")
    print("A | B | Output")
    print("--|---|-------")
    for a in [0, 1]:
        for b in [0, 1]:
            output = or_gate(a, b)
            print(f"{a} | {b} |   {output}")

def test_or_gate():
    """Test function for OR gate"""
    print("Testing OR Gate:")
    test_cases = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    for a, b in test_cases:
        result = or_gate(a, b)
        print(f"OR({a}, {b}) = {result}")
    
    print("\nTesting multiple input OR:")
    print(f"OR(0, 0, 0) = {or_gate_multiple(0, 0, 0)}")
    print(f"OR(1, 0, 0) = {or_gate_multiple(1, 0, 0)}")
    print(f"OR(0, 1, 0) = {or_gate_multiple(0, 1, 0)}")

if __name__ == "__main__":
    print_truth_table()
    print()
    test_or_gate()
