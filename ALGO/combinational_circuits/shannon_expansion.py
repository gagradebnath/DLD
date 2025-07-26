"""
Shannon Expansion Algorithm
Recursive Boolean function decomposition using Shannon's expansion theorem
"""

from typing import Dict, List, Set, Tuple, Union, Optional, Callable
import itertools
from functools import lru_cache


class BooleanFunction:
    """Represents a Boolean function for Shannon expansion"""
    
    def __init__(self, truth_table: Union[List[int], Dict[int, int]] = None, 
                 expression: str = None, num_variables: int = None):
        """
        Initialize Boolean function
        
        Args:
            truth_table: Truth table as list or dict mapping minterm->value
            expression: Boolean expression string (optional)
            num_variables: Number of input variables
        """
        self.num_variables = num_variables
        self.variables = [f'A{i}' for i in range(num_variables)] if num_variables else []
        self.expression = expression
        
        if isinstance(truth_table, list):
            self.truth_table = {i: val for i, val in enumerate(truth_table)}
            if not num_variables:
                self.num_variables = len(truth_table).bit_length() - 1
                self.variables = [f'A{i}' for i in range(self.num_variables)]
        elif isinstance(truth_table, dict):
            self.truth_table = truth_table
            if not num_variables:
                max_minterm = max(truth_table.keys()) if truth_table else 0
                self.num_variables = (max_minterm + 1).bit_length() - 1
                self.variables = [f'A{i}' for i in range(self.num_variables)]
        else:
            self.truth_table = {}
    
    def evaluate(self, inputs: Union[List[int], Dict[str, int], int]) -> int:
        """
        Evaluate function for given inputs
        
        Args:
            inputs: Input values as list, dict, or minterm index
            
        Returns:
            Function output (0 or 1)
        """
        if isinstance(inputs, int):
            return self.truth_table.get(inputs, 0)
        elif isinstance(inputs, list):
            minterm = sum(bit * (2 ** i) for i, bit in enumerate(reversed(inputs)))
            return self.truth_table.get(minterm, 0)
        elif isinstance(inputs, dict):
            minterm = 0
            for i, var in enumerate(self.variables):
                if var in inputs and inputs[var]:
                    minterm += 2 ** (self.num_variables - 1 - i)
            return self.truth_table.get(minterm, 0)
        else:
            return 0
    
    def get_minterms(self) -> Set[int]:
        """Get set of minterms where function = 1"""
        return {minterm for minterm, value in self.truth_table.items() if value == 1}
    
    def get_maxterms(self) -> Set[int]:
        """Get set of maxterms where function = 0"""
        return {minterm for minterm, value in self.truth_table.items() if value == 0}
    
    def copy(self) -> 'BooleanFunction':
        """Create a copy of this function"""
        return BooleanFunction(
            truth_table=self.truth_table.copy(),
            expression=self.expression,
            num_variables=self.num_variables
        )


class ShannonExpansion:
    """
    Shannon Expansion implementation for recursive Boolean function decomposition.
    
    Shannon's expansion theorem states that any Boolean function f can be expressed as:
    f(x1, x2, ..., xn) = xi·f(x1, ..., xi-1, 1, xi+1, ..., xn) + xi'·f(x1, ..., xi-1, 0, xi+1, ..., xn)
    
    This is useful for:
    - Function decomposition
    - Building decision trees/diagrams
    - Multiplexer-based implementations
    - Hierarchical circuit design
    """
    
    def __init__(self, function: BooleanFunction):
        """
        Initialize Shannon expansion
        
        Args:
            function: Boolean function to decompose
        """
        self.function = function
        self.expansion_tree = None
        self.decomposition_cache = {}
    
    def expand_on_variable(self, variable_index: int) -> Tuple[BooleanFunction, BooleanFunction]:
        """
        Perform Shannon expansion on a specific variable
        
        Args:
            variable_index: Index of variable to expand on
            
        Returns:
            Tuple of (positive cofactor, negative cofactor)
        """
        if variable_index >= self.function.num_variables:
            raise ValueError(f"Variable index {variable_index} out of range")
        
        # Create positive cofactor (variable = 1)
        positive_cofactor = self._create_cofactor(variable_index, 1)
        
        # Create negative cofactor (variable = 0)
        negative_cofactor = self._create_cofactor(variable_index, 0)
        
        return positive_cofactor, negative_cofactor
    
    def _create_cofactor(self, variable_index: int, value: int) -> BooleanFunction:
        """
        Create cofactor by setting a variable to a specific value
        
        Args:
            variable_index: Index of variable to fix
            value: Value to set variable to (0 or 1)
            
        Returns:
            Cofactor function
        """
        cofactor_truth_table = {}
        
        # Iterate through all minterms
        for minterm, output in self.function.truth_table.items():
            # Check if this minterm has the variable set to the desired value
            variable_bit = (minterm >> (self.function.num_variables - 1 - variable_index)) & 1
            
            if variable_bit == value:
                # Remove the fixed variable bit from minterm
                new_minterm = self._remove_bit(minterm, variable_index, self.function.num_variables)
                cofactor_truth_table[new_minterm] = output
        
        # Create new function with one less variable
        cofactor = BooleanFunction(
            truth_table=cofactor_truth_table,
            num_variables=self.function.num_variables - 1
        )
        
        # Update variable names
        cofactor.variables = [var for i, var in enumerate(self.function.variables) if i != variable_index]
        
        return cofactor
    
    def _remove_bit(self, number: int, bit_position: int, total_bits: int) -> int:
        """
        Remove a bit from a number at a specific position
        
        Args:
            number: Original number
            bit_position: Position of bit to remove (0-indexed from left)
            total_bits: Total number of bits
            
        Returns:
            Number with bit removed
        """
        # Convert to binary, remove bit, convert back
        binary = format(number, f'0{total_bits}b')
        new_binary = binary[:bit_position] + binary[bit_position + 1:]
        return int(new_binary, 2) if new_binary else 0
    
    def recursive_expansion(self, max_depth: int = None) -> Dict:
        """
        Perform recursive Shannon expansion to build expansion tree
        
        Args:
            max_depth: Maximum depth of expansion (None for complete expansion)
            
        Returns:
            Dictionary representing the expansion tree
        """
        if max_depth is None:
            max_depth = self.function.num_variables
        
        self.expansion_tree = self._recursive_expand(self.function, 0, max_depth, [])
        return self.expansion_tree
    
    def _recursive_expand(self, func: BooleanFunction, depth: int, max_depth: int, 
                         expansion_path: List[Tuple[int, int]]) -> Dict:
        """
        Recursive helper for Shannon expansion
        
        Args:
            func: Current function to expand
            depth: Current depth in expansion tree
            max_depth: Maximum expansion depth
            expansion_path: Path of variable assignments leading to this node
            
        Returns:
            Node dictionary for expansion tree
        """
        node = {
            'function': func,
            'depth': depth,
            'path': expansion_path.copy(),
            'variables': func.variables.copy(),
            'minterms': func.get_minterms(),
            'is_leaf': False,
            'children': {}
        }
        
        # Check termination conditions
        if (depth >= max_depth or 
            func.num_variables == 0 or 
            self._is_constant_function(func)):
            node['is_leaf'] = True
            node['constant_value'] = self._get_constant_value(func)
            return node
        
        # Choose variable to expand on (use first variable for simplicity)
        if func.num_variables > 0:
            expand_var_index = 0
            expand_var_name = func.variables[expand_var_index]
            
            # Perform Shannon expansion
            positive_cofactor, negative_cofactor = self._expand_function_on_variable(func, expand_var_index)
            
            # Recursively expand cofactors
            pos_path = expansion_path + [(expand_var_name, 1)]
            neg_path = expansion_path + [(expand_var_name, 0)]
            
            node['expansion_variable'] = expand_var_name
            node['children']['1'] = self._recursive_expand(positive_cofactor, depth + 1, max_depth, pos_path)
            node['children']['0'] = self._recursive_expand(negative_cofactor, depth + 1, max_depth, neg_path)
        
        return node
    
    def _expand_function_on_variable(self, func: BooleanFunction, var_index: int) -> Tuple[BooleanFunction, BooleanFunction]:
        """
        Expand function on specific variable (helper for recursive expansion)
        
        Args:
            func: Function to expand
            var_index: Variable index to expand on
            
        Returns:
            Tuple of (positive cofactor, negative cofactor)
        """
        return self.expand_on_variable(var_index) if func == self.function else self._create_cofactor_pair(func, var_index)
    
    def _create_cofactor_pair(self, func: BooleanFunction, var_index: int) -> Tuple[BooleanFunction, BooleanFunction]:
        """Create cofactor pair for a given function and variable"""
        # Create temporary Shannon expander for this function
        temp_expander = ShannonExpansion(func)
        return temp_expander.expand_on_variable(var_index)
    
    def _is_constant_function(self, func: BooleanFunction) -> bool:
        """Check if function is constant (all 0s or all 1s)"""
        if not func.truth_table:
            return True
        
        values = set(func.truth_table.values())
        return len(values) <= 1
    
    def _get_constant_value(self, func: BooleanFunction) -> Optional[int]:
        """Get constant value if function is constant"""
        if not func.truth_table:
            return 0
        
        values = set(func.truth_table.values())
        return list(values)[0] if len(values) == 1 else None
    
    def generate_multiplexer_implementation(self) -> Dict:
        """
        Generate multiplexer-based implementation using Shannon expansion
        
        Returns:
            Dictionary describing multiplexer tree structure
        """
        if not self.expansion_tree:
            self.recursive_expansion()
        
        return self._create_mux_tree(self.expansion_tree)
    
    def _create_mux_tree(self, node: Dict) -> Dict:
        """
        Create multiplexer tree from expansion tree
        
        Args:
            node: Expansion tree node
            
        Returns:
            Multiplexer tree node
        """
        mux_node = {
            'type': 'mux' if not node['is_leaf'] else 'constant',
            'depth': node['depth'],
            'path': node['path']
        }
        
        if node['is_leaf']:
            mux_node['value'] = node.get('constant_value', 0)
        else:
            mux_node['select_variable'] = node['expansion_variable']
            mux_node['input_0'] = self._create_mux_tree(node['children']['0'])
            mux_node['input_1'] = self._create_mux_tree(node['children']['1'])
        
        return mux_node
    
    def generate_expression_from_expansion(self, simplified: bool = True) -> str:
        """
        Generate Boolean expression from Shannon expansion
        
        Args:
            simplified: Whether to attempt simplification
            
        Returns:
            Boolean expression string
        """
        if not self.expansion_tree:
            self.recursive_expansion()
        
        expression = self._node_to_expression(self.expansion_tree)
        
        if simplified:
            # Basic simplification rules
            expression = self._simplify_expression(expression)
        
        return expression
    
    def _node_to_expression(self, node: Dict) -> str:
        """
        Convert expansion tree node to Boolean expression
        
        Args:
            node: Expansion tree node
            
        Returns:
            Boolean expression for this node
        """
        if node['is_leaf']:
            constant = node.get('constant_value', 0)
            return '1' if constant == 1 else '0'
        
        var = node['expansion_variable']
        expr_1 = self._node_to_expression(node['children']['1'])
        expr_0 = self._node_to_expression(node['children']['0'])
        
        # Shannon expansion: f = var·f1 + var'·f0
        terms = []
        if expr_1 != '0':
            if expr_1 == '1':
                terms.append(var)
            else:
                terms.append(f"{var}·({expr_1})")
        
        if expr_0 != '0':
            if expr_0 == '1':
                terms.append(f"{var}'")
            else:
                terms.append(f"{var}'·({expr_0})")
        
        if not terms:
            return '0'
        elif len(terms) == 1:
            return terms[0]
        else:
            return ' + '.join(terms)
    
    def _simplify_expression(self, expression: str) -> str:
        """
        Basic expression simplification
        
        Args:
            expression: Boolean expression to simplify
            
        Returns:
            Simplified expression
        """
        # Basic simplification rules
        simplified = expression
        
        # Remove redundant parentheses and clean up
        simplified = simplified.replace('·(1)', '')
        simplified = simplified.replace('(1)·', '')
        simplified = simplified.replace(' + 0', '')
        simplified = simplified.replace('0 + ', '')
        simplified = simplified.replace('·0', '0')
        simplified = simplified.replace('0·', '0')
        
        # Clean up multiple spaces and operators
        while '  ' in simplified:
            simplified = simplified.replace('  ', ' ')
        
        return simplified.strip() if simplified.strip() else '0'
    
    def display_expansion_tree(self) -> str:
        """
        Display the Shannon expansion tree in a readable format
        
        Returns:
            String representation of expansion tree
        """
        if not self.expansion_tree:
            self.recursive_expansion()
        
        return self._format_tree_node(self.expansion_tree, 0)
    
    def _format_tree_node(self, node: Dict, indent_level: int) -> str:
        """
        Format a single node of the expansion tree
        
        Args:
            node: Tree node to format
            indent_level: Current indentation level
            
        Returns:
            Formatted string for this node and its children
        """
        indent = "  " * indent_level
        result = ""
        
        if node['is_leaf']:
            path_str = " → ".join([f"{var}={val}" for var, val in node['path']])
            constant = node.get('constant_value', 0)
            result += f"{indent}Leaf: {path_str} → {constant}\n"
        else:
            var = node['expansion_variable']
            path_str = " → ".join([f"{var}={val}" for var, val in node['path']])
            result += f"{indent}Node: {path_str} | Expand on {var}\n"
            
            result += f"{indent}├─ {var}=1:\n"
            result += self._format_tree_node(node['children']['1'], indent_level + 1)
            
            result += f"{indent}└─ {var}=0:\n"
            result += self._format_tree_node(node['children']['0'], indent_level + 1)
        
        return result
    
    def analyze_decomposition_complexity(self) -> Dict:
        """
        Analyze the complexity of the Shannon decomposition
        
        Returns:
            Dictionary with complexity metrics
        """
        if not self.expansion_tree:
            self.recursive_expansion()
        
        metrics = self._calculate_tree_metrics(self.expansion_tree)
        
        return {
            'total_nodes': metrics['node_count'],
            'leaf_nodes': metrics['leaf_count'],
            'internal_nodes': metrics['internal_count'],
            'tree_depth': metrics['max_depth'],
            'avg_path_length': metrics['avg_path_length'],
            'multiplexer_count': metrics['internal_count'],
            'constant_inputs': metrics['leaf_count']
        }
    
    def _calculate_tree_metrics(self, node: Dict) -> Dict:
        """Calculate metrics for expansion tree"""
        if node['is_leaf']:
            return {
                'node_count': 1,
                'leaf_count': 1,
                'internal_count': 0,
                'max_depth': node['depth'],
                'path_lengths': [node['depth']],
                'avg_path_length': node['depth']
            }
        
        # Recursively calculate for children
        child_0_metrics = self._calculate_tree_metrics(node['children']['0'])
        child_1_metrics = self._calculate_tree_metrics(node['children']['1'])
        
        # Combine metrics
        total_nodes = 1 + child_0_metrics['node_count'] + child_1_metrics['node_count']
        total_leaves = child_0_metrics['leaf_count'] + child_1_metrics['leaf_count']
        total_internal = 1 + child_0_metrics['internal_count'] + child_1_metrics['internal_count']
        max_depth = max(child_0_metrics['max_depth'], child_1_metrics['max_depth'])
        
        path_lengths = child_0_metrics['path_lengths'] + child_1_metrics['path_lengths']
        avg_path_length = sum(path_lengths) / len(path_lengths) if path_lengths else 0
        
        return {
            'node_count': total_nodes,
            'leaf_count': total_leaves,
            'internal_count': total_internal,
            'max_depth': max_depth,
            'path_lengths': path_lengths,
            'avg_path_length': avg_path_length
        }


def test_shannon_expansion():
    """Test Shannon expansion functionality"""
    print("Testing Shannon Expansion Algorithm")
    print("=" * 50)
    
    # Test case 1: Simple 3-variable function F(A,B,C) = A'B + BC'
    truth_table = [0, 1, 1, 0, 0, 1, 1, 1]  # Truth table for A'B + BC'
    func = BooleanFunction(truth_table, num_variables=3)
    func.variables = ['A', 'B', 'C']
    
    shannon = ShannonExpansion(func)
    
    print("Test Case 1: F(A,B,C) = A'B + BC'")
    print(f"Original minterms: {sorted(func.get_minterms())}")
    
    # Perform expansion on variable A (index 0)
    pos_cofactor, neg_cofactor = shannon.expand_on_variable(0)
    print(f"Positive cofactor F(A=1): minterms = {sorted(pos_cofactor.get_minterms())}")
    print(f"Negative cofactor F(A=0): minterms = {sorted(neg_cofactor.get_minterms())}")
    
    # Complete recursive expansion
    expansion_tree = shannon.recursive_expansion()
    print("\nExpansion Tree:")
    print(shannon.display_expansion_tree())
    
    # Generate expression
    expression = shannon.generate_expression_from_expansion()
    print(f"Generated Expression: {expression}")
    
    # Generate multiplexer implementation
    mux_tree = shannon.generate_multiplexer_implementation()
    print(f"\nMultiplexer Implementation:")
    print(f"Tree structure generated with {shannon.analyze_decomposition_complexity()}")
    
    # Complexity analysis
    complexity = shannon.analyze_decomposition_complexity()
    print(f"\nComplexity Analysis:")
    for metric, value in complexity.items():
        print(f"  {metric}: {value}")


if __name__ == "__main__":
    test_shannon_expansion()
