"""
AND Gate Implementation
Digital Logic Design - Basic Gates

The AND gate outputs True only when all inputs are True.

Truth Table:
A | B | Output
--|---|-------
0 | 0 |   0
0 | 1 |   0
1 | 0 |   0
1 | 1 |   1
"""

class ANDGate:
    """
    AND Gate class implementation
    """
    
    def __init__(self, num_inputs=2):
        """
        Initialize AND gate
        
        Args:
            num_inputs (int): Number of inputs for the gate
        """
        self.num_inputs = num_inputs
        self.gate_type = "AND"
    
    def evaluate(self, *inputs):
        """
        Evaluate AND gate output
        
        Args:
            *inputs: Variable number of inputs (0 or 1)
        
        Returns:
            int: Output of AND gate (0 or 1)
        """
        if len(inputs) != self.num_inputs:
            raise ValueError(f"AND gate expects {self.num_inputs} inputs, got {len(inputs)}")
        
        return int(all(inputs))
    
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
def and_gate(a, b):
    """
    AND gate function for backward compatibility
    
    Args:
        a (int): First input (0 or 1)
        b (int): Second input (0 or 1)
    
    Returns:
        int: Output of AND gate (0 or 1)
    """
    gate = ANDGate(2)
    return gate.evaluate(a, b)

def and_gate_multiple(*inputs):
    """
    AND gate for multiple inputs
    
    Args:
        *inputs: Variable number of inputs (0 or 1)
    
    Returns:
        int: Output of AND gate with multiple inputs
    """
    if len(inputs) < 2:
        raise ValueError("AND gate requires at least 2 inputs")
    
    gate = ANDGate(len(inputs))
    return gate.evaluate(*inputs)

def print_truth_table():
    """Print the truth table for AND gate"""
    gate = ANDGate(2)
    print("AND Gate Truth Table:")
    print("A | B | Output")
    print("--|---|-------")
    for inputs, output in gate.get_truth_table():
        print(f"{inputs[0]} | {inputs[1]} |   {output}")

def test_and_gate():
    """Test function for AND gate"""
    print("Testing AND Gate:")
    
    # Test 2-input gate
    gate2 = ANDGate(2)
    test_cases = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    for a, b in test_cases:
        result = gate2(a, b)
        print(f"AND({a}, {b}) = {result}")
    
    # Test 3-input gate
    print("\nTesting 3-input AND:")
    gate3 = ANDGate(3)
    print(f"AND(0, 0, 0) = {gate3(0, 0, 0)}")
    print(f"AND(1, 1, 1) = {gate3(1, 1, 1)}")
    print(f"AND(1, 0, 1) = {gate3(1, 0, 1)}")

if __name__ == "__main__":
    print_truth_table()
    print()
    test_and_gate()
