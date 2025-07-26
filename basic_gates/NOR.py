"""
NOR Gate Implementation
Digital Logic Design - Basic Gates

The NOR gate is the inverse of OR gate.
It outputs True only when all inputs are False.

Truth Table:
A | B | Output
--|---|-------
0 | 0 |   1
0 | 1 |   0
1 | 0 |   0
1 | 1 |   0
"""

class NORGate:
    """
    NOR Gate class implementation
    """
    
    def __init__(self, num_inputs=2):
        """
        Initialize NOR gate
        
        Args:
            num_inputs (int): Number of inputs for the gate
        """
        self.num_inputs = num_inputs
        self.gate_type = "NOR"
    
    def evaluate(self, *inputs):
        """
        Evaluate NOR gate output
        
        Args:
            *inputs: Variable number of inputs (0 or 1)
        
        Returns:
            int: Output of NOR gate (0 or 1)
        """
        if len(inputs) != self.num_inputs:
            raise ValueError(f"NOR gate expects {self.num_inputs} inputs, got {len(inputs)}")
        
        return int(not any(inputs))
    
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
def nor_gate(a, b):
    """
    NOR gate function for backward compatibility
    
    Args:
        a (int): First input (0 or 1)
        b (int): Second input (0 or 1)
    
    Returns:
        int: Output of NOR gate (0 or 1)
    """
    gate = NORGate(2)
    return gate.evaluate(a, b)

def nor_gate_multiple(*inputs):
    """
    NOR gate for multiple inputs
    
    Args:
        *inputs: Variable number of inputs (0 or 1)
    
    Returns:
        int: Output of NOR gate with multiple inputs
    """
    if len(inputs) < 2:
        raise ValueError("NOR gate requires at least 2 inputs")
    
    gate = NORGate(len(inputs))
    return gate.evaluate(*inputs)

def print_truth_table():
    """Print the truth table for NOR gate"""
    print("NOR Gate Truth Table:")
    print("A | B | Output")
    print("--|---|-------")
    for a in [0, 1]:
        for b in [0, 1]:
            output = nor_gate(a, b)
            print(f"{a} | {b} |   {output}")

def test_nor_gate():
    """Test function for NOR gate"""
    print("Testing NOR Gate:")
    test_cases = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    for a, b in test_cases:
        result = nor_gate(a, b)
        print(f"NOR({a}, {b}) = {result}")
    
    print("\nTesting multiple input NOR:")
    print(f"NOR(0, 0, 0) = {nor_gate_multiple(0, 0, 0)}")
    print(f"NOR(1, 0, 0) = {nor_gate_multiple(1, 0, 0)}")
    print(f"NOR(0, 1, 0) = {nor_gate_multiple(0, 1, 0)}")

if __name__ == "__main__":
    print_truth_table()
    print()
    test_nor_gate()
