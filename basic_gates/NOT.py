"""
NOT Gate Implementation
Digital Logic Design - Basic Gates

The NOT gate (inverter) outputs the opposite of its input.

Truth Table:
A | Output
--|-------
0 |   1
1 |   0
"""

class NOTGate:
    """
    NOT Gate class implementation
    """
    
    def __init__(self):
        """
        Initialize NOT gate (always single input)
        """
        self.num_inputs = 1
        self.gate_type = "NOT"
    
    def evaluate(self, a):
        """
        Evaluate NOT gate output
        
        Args:
            a (int): Input (0 or 1)
        
        Returns:
            int: Output of NOT gate (0 or 1)
        """
        return int(not a)
    
    def __call__(self, a):
        """Allow gate to be called like a function"""
        return self.evaluate(a)
    
    def get_truth_table(self):
        """
        Generate truth table for the gate
        
        Returns:
            list: List of tuples (inputs, output)
        """
        return [((0,), 1), ((1,), 0)]

# Backward compatibility functions
def not_gate(a):
    """
    NOT gate function for backward compatibility
    
    Args:
        a (int): Input (0 or 1)
    
    Returns:
        int: Output of NOT gate (0 or 1)
    """
    gate = NOTGate()
    return gate.evaluate(a)

def not_gate_multiple(*inputs):
    """
    NOT gate for multiple inputs (inverts each input independently)
    
    Args:
        *inputs: Variable number of inputs (0 or 1)
    
    Returns:
        list: List of inverted outputs
    """
    gate = NOTGate()
    return [gate.evaluate(inp) for inp in inputs]

def print_truth_table():
    """Print the truth table for NOT gate"""
    print("NOT Gate Truth Table:")
    print("A | Output")
    print("--|-------")
    for a in [0, 1]:
        output = not_gate(a)
        print(f"{a} |   {output}")

def test_not_gate():
    """Test function for NOT gate"""
    print("Testing NOT Gate:")
    test_cases = [0, 1]
    
    for a in test_cases:
        result = not_gate(a)
        print(f"NOT({a}) = {result}")
    
    print("\nTesting multiple input NOT:")
    inputs = [0, 1, 0, 1]
    results = not_gate_multiple(*inputs)
    print(f"NOT({inputs}) = {results}")

if __name__ == "__main__":
    print_truth_table()
    print()
    test_not_gate()
