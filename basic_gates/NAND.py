"""
NAND Gate Implementation
Digital Logic Design - Basic Gates

The NAND gate is the inverse of AND gate.
It outputs False only when all inputs are True.

Truth Table:
A | B | Output
--|---|-------
0 | 0 |   1
0 | 1 |   1
1 | 0 |   1
1 | 1 |   0
"""

class NANDGate:
    """
    NAND Gate class implementation
    """
    
    def __init__(self, num_inputs=2):
        """
        Initialize NAND gate
        
        Args:
            num_inputs (int): Number of inputs for the gate
        """
        self.num_inputs = num_inputs
        self.gate_type = "NAND"
    
    def evaluate(self, *inputs):
        """
        Evaluate NAND gate output
        
        Args:
            *inputs: Variable number of inputs (0 or 1)
        
        Returns:
            int: Output of NAND gate (0 or 1)
        """
        if len(inputs) != self.num_inputs:
            raise ValueError(f"NAND gate expects {self.num_inputs} inputs, got {len(inputs)}")
        
        return int(not all(inputs))
    
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
def nand_gate(a, b):
    """
    NAND gate function for backward compatibility
    
    Args:
        a (int): First input (0 or 1)
        b (int): Second input (0 or 1)
    
    Returns:
        int: Output of NAND gate (0 or 1)
    """
    gate = NANDGate(2)
    return gate.evaluate(a, b)

def nand_gate_multiple(*inputs):
    """
    NAND gate for multiple inputs
    
    Args:
        *inputs: Variable number of inputs (0 or 1)
    
    Returns:
        int: Output of NAND gate with multiple inputs
    """
    if len(inputs) < 2:
        raise ValueError("NAND gate requires at least 2 inputs")
    
    gate = NANDGate(len(inputs))
    return gate.evaluate(*inputs)

def print_truth_table():
    """Print the truth table for NAND gate"""
    print("NAND Gate Truth Table:")
    print("A | B | Output")
    print("--|---|-------")
    for a in [0, 1]:
        for b in [0, 1]:
            output = nand_gate(a, b)
            print(f"{a} | {b} |   {output}")

def test_nand_gate():
    """Test function for NAND gate"""
    print("Testing NAND Gate:")
    test_cases = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    for a, b in test_cases:
        result = nand_gate(a, b)
        print(f"NAND({a}, {b}) = {result}")
    
    print("\nTesting multiple input NAND:")
    print(f"NAND(0, 0, 0) = {nand_gate_multiple(0, 0, 0)}")
    print(f"NAND(1, 1, 1) = {nand_gate_multiple(1, 1, 1)}")
    print(f"NAND(1, 0, 1) = {nand_gate_multiple(1, 0, 1)}")

if __name__ == "__main__":
    print_truth_table()
    print()
    test_nand_gate()
