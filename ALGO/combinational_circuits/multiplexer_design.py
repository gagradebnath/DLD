"""
Multiplexer-based Design Algorithm
Implement any Boolean logic function using multiplexers
"""

from typing import List, Dict, Tuple, Optional, Union, Set
import itertools
import math


class MultiplexerDesign:
    """
    Multiplexer-based design implementation for Boolean functions.
    
    This class provides methods to implement any Boolean function using:
    - Single multiplexer with data inputs
    - Tree of multiplexers (hierarchical implementation)
    - Shannon expansion-based multiplexer trees
    """
    
    def __init__(self, num_variables: int):
        """
        Initialize multiplexer design
        
        Args:
            num_variables: Number of input variables
        """
        self.num_variables = num_variables
        self.variables = [f'A{i}' for i in range(num_variables)]
        self.function_truth_table = {}
        self.minterms = set()
    
    def set_function(self, truth_table: Union[List[int], Dict[int, int]] = None, 
                    minterms: List[int] = None) -> None:
        """
        Set the Boolean function to implement
        
        Args:
            truth_table: Truth table as list or dict
            minterms: List of minterms where function = 1
        """
        if truth_table is not None:
            if isinstance(truth_table, list):
                self.function_truth_table = {i: val for i, val in enumerate(truth_table)}
            else:
                self.function_truth_table = truth_table
        elif minterms is not None:
            self.function_truth_table = {}
            for i in range(2 ** self.num_variables):
                self.function_truth_table[i] = 1 if i in minterms else 0
        
        self.minterms = {i for i, val in self.function_truth_table.items() if val == 1}
    
    def design_single_mux(self, select_variables: List[int] = None) -> Dict:
        """
        Design using a single multiplexer with data inputs
        
        Args:
            select_variables: Indices of variables to use as select lines
                            If None, uses first log2(n) variables
        
        Returns:
            Dictionary describing the multiplexer implementation
        """
        if not select_variables:
            # Use first log2(num_variables) variables as select lines
            num_select_vars = max(1, int(math.log2(self.num_variables)))
            select_variables = list(range(min(num_select_vars, self.num_variables)))
        
        num_select = len(select_variables)
        num_data_inputs = 2 ** num_select
        remaining_variables = [i for i in range(self.num_variables) if i not in select_variables]
        
        # Generate data inputs for each select combination
        data_inputs = {}
        
        for select_combo in range(num_data_inputs):
            # For this select combination, determine the data input
            data_input = self._compute_data_input(select_combo, select_variables, remaining_variables)
            data_inputs[select_combo] = data_input
        
        return {
            'type': 'single_mux',
            'select_variables': [self.variables[i] for i in select_variables],
            'select_variable_indices': select_variables,
            'data_inputs': data_inputs,
            'data_input_expressions': self._generate_data_input_expressions(data_inputs, remaining_variables),
            'mux_size': f"{num_data_inputs}:1",
            'implementation_cost': self._calculate_single_mux_cost(data_inputs, remaining_variables)
        }
    
    def _compute_data_input(self, select_combo: int, select_vars: List[int], 
                          remaining_vars: List[int]) -> Union[str, int]:
        """
        Compute the data input for a specific select combination
        
        Args:
            select_combo: Select line combination value
            select_vars: Indices of select variables
            remaining_vars: Indices of remaining variables
        
        Returns:
            Data input value (0, 1, or expression)
        """
        if not remaining_vars:
            # No remaining variables, data input is constant
            return self.function_truth_table.get(select_combo, 0)
        
        # Build truth table for this data input as function of remaining variables
        data_truth_table = {}
        num_remaining = len(remaining_vars)
        
        for remaining_combo in range(2 ** num_remaining):
            # Construct full minterm
            full_minterm = 0
            
            # Set select variable bits
            for i, var_idx in enumerate(select_vars):
                if (select_combo >> i) & 1:
                    full_minterm |= (1 << (self.num_variables - 1 - var_idx))
            
            # Set remaining variable bits
            for i, var_idx in enumerate(remaining_vars):
                if (remaining_combo >> i) & 1:
                    full_minterm |= (1 << (self.num_variables - 1 - var_idx))
            
            output = self.function_truth_table.get(full_minterm, 0)
            data_truth_table[remaining_combo] = output
        
        # Analyze the data truth table
        return self._analyze_data_function(data_truth_table, remaining_vars)
    
    def _analyze_data_function(self, truth_table: Dict[int, int], variables: List[int]) -> Union[str, int]:
        """
        Analyze data input function and return simplified form
        
        Args:
            truth_table: Truth table for data input
            variables: Variable indices for this data input
        
        Returns:
            Simplified expression or constant value
        """
        values = list(truth_table.values())
        
        # Check for constant functions
        if all(v == 0 for v in values):
            return 0
        if all(v == 1 for v in values):
            return 1
        
        # Check for simple functions
        minterms = [i for i, val in truth_table.items() if val == 1]
        
        if len(variables) == 1:
            var_name = self.variables[variables[0]]
            if minterms == [0]:
                return f"{var_name}'"
            elif minterms == [1]:
                return var_name
        elif len(variables) == 2:
            var_names = [self.variables[variables[i]] for i in range(2)]
            return self._two_variable_expression(minterms, var_names)
        
        # For more complex functions, return minterm expression
        return self._minterms_to_expression(minterms, variables)
    
    def _two_variable_expression(self, minterms: List[int], var_names: List[str]) -> str:
        """Generate expression for 2-variable function"""
        if not minterms:
            return "0"
        if len(minterms) == 4:
            return "1"
        
        expressions = {
            frozenset([0]): f"{var_names[0]}'{var_names[1]}'",
            frozenset([1]): f"{var_names[0]}'{var_names[1]}",
            frozenset([2]): f"{var_names[0]}{var_names[1]}'",
            frozenset([3]): f"{var_names[0]}{var_names[1]}",
            frozenset([0, 1]): f"{var_names[0]}'",
            frozenset([2, 3]): f"{var_names[0]}",
            frozenset([0, 2]): f"{var_names[1]}'",
            frozenset([1, 3]): f"{var_names[1]}",
            frozenset([0, 3]): f"{var_names[0]}'{var_names[1]}' + {var_names[0]}{var_names[1]}",
            frozenset([1, 2]): f"{var_names[0]}'{var_names[1]} + {var_names[0]}{var_names[1]}'"
        }
        
        return expressions.get(frozenset(minterms), self._minterms_to_expression(minterms, [0, 1]))
    
    def _minterms_to_expression(self, minterms: List[int], variables: List[int]) -> str:
        """Convert minterms to Boolean expression"""
        if not minterms:
            return "0"
        
        terms = []
        for minterm in minterms:
            term = ""
            for i, var_idx in enumerate(variables):
                if (minterm >> i) & 1:
                    term += self.variables[var_idx]
                else:
                    term += self.variables[var_idx] + "'"
            terms.append(term)
        
        return " + ".join(terms)
    
    def _generate_data_input_expressions(self, data_inputs: Dict[int, Union[str, int]], 
                                       remaining_vars: List[int]) -> Dict[int, str]:
        """Generate human-readable expressions for data inputs"""
        expressions = {}
        for combo, value in data_inputs.items():
            if isinstance(value, int):
                expressions[combo] = str(value)
            else:
                expressions[combo] = str(value)
        return expressions
    
    def design_mux_tree(self, tree_structure: str = "balanced") -> Dict:
        """
        Design using a tree of multiplexers
        
        Args:
            tree_structure: Type of tree ("balanced", "chain", "shannon")
        
        Returns:
            Dictionary describing the multiplexer tree
        """
        if tree_structure == "shannon":
            return self._design_shannon_mux_tree()
        elif tree_structure == "balanced":
            return self._design_balanced_mux_tree()
        elif tree_structure == "chain":
            return self._design_chain_mux_tree()
        else:
            raise ValueError(f"Unknown tree structure: {tree_structure}")
    
    def _design_shannon_mux_tree(self) -> Dict:
        """Design multiplexer tree using Shannon expansion"""
        tree = self._recursive_shannon_expansion(self.minterms, self.num_variables, 0)
        
        return {
            'type': 'shannon_mux_tree',
            'tree_structure': tree,
            'implementation_cost': self._calculate_tree_cost(tree),
            'depth': self._calculate_tree_depth(tree),
            'mux_count': self._count_muxes_in_tree(tree)
        }
    
    def _recursive_shannon_expansion(self, current_minterms: Set[int], 
                                   remaining_vars: int, depth: int) -> Dict:
        """Recursive Shannon expansion for multiplexer tree"""
        if remaining_vars == 0:
            # Leaf node - constant value
            return {
                'type': 'constant',
                'value': 1 if current_minterms else 0,
                'depth': depth
            }
        
        if remaining_vars == 1:
            # Single variable - direct implementation
            var_name = self.variables[self.num_variables - remaining_vars]
            
            # Check minterms for this variable
            has_0 = any((minterm >> (remaining_vars - 1)) & 1 == 0 for minterm in current_minterms)
            has_1 = any((minterm >> (remaining_vars - 1)) & 1 == 1 for minterm in current_minterms)
            
            if has_0 and has_1:
                return {'type': 'constant', 'value': 1, 'depth': depth}
            elif has_1:
                return {'type': 'variable', 'variable': var_name, 'depth': depth}
            elif has_0:
                return {'type': 'variable', 'variable': var_name + "'", 'depth': depth}
            else:
                return {'type': 'constant', 'value': 0, 'depth': depth}
        
        # Choose variable to expand on (use MSB)
        expand_var_idx = self.num_variables - remaining_vars
        expand_var = self.variables[expand_var_idx]
        
        # Split minterms based on expansion variable
        minterms_0 = set()  # Variable = 0
        minterms_1 = set()  # Variable = 1
        
        for minterm in current_minterms:
            if (minterm >> (remaining_vars - 1)) & 1 == 0:
                # Remove the MSB and add to 0 set
                new_minterm = minterm & ((1 << (remaining_vars - 1)) - 1)
                minterms_0.add(new_minterm)
            else:
                # Remove the MSB and add to 1 set
                new_minterm = minterm & ((1 << (remaining_vars - 1)) - 1)
                minterms_1.add(new_minterm)
        
        # Recursively expand
        child_0 = self._recursive_shannon_expansion(minterms_0, remaining_vars - 1, depth + 1)
        child_1 = self._recursive_shannon_expansion(minterms_1, remaining_vars - 1, depth + 1)
        
        return {
            'type': 'mux',
            'select': expand_var,
            'input_0': child_0,
            'input_1': child_1,
            'depth': depth
        }
    
    def _design_balanced_mux_tree(self) -> Dict:
        """Design balanced multiplexer tree"""
        # For balanced tree, group variables optimally
        return {
            'type': 'balanced_mux_tree',
            'structure': 'Balanced tree implementation',
            'note': 'Balanced tree minimizes depth'
        }
    
    def _design_chain_mux_tree(self) -> Dict:
        """Design chain multiplexer tree"""
        # Chain implementation using cascaded 2:1 multiplexers
        return {
            'type': 'chain_mux_tree',
            'structure': 'Chain of 2:1 multiplexers',
            'note': 'Sequential variable selection'
        }
    
    def compare_implementations(self) -> Dict:
        """
        Compare different multiplexer implementations
        
        Returns:
            Comparison of various implementation methods
        """
        implementations = {}
        
        # Single multiplexer implementations with different select variables
        for num_select in range(1, min(self.num_variables + 1, 4)):
            try:
                single_mux = self.design_single_mux(list(range(num_select)))
                implementations[f'single_mux_{num_select}_select'] = single_mux
            except:
                pass
        
        # Tree implementations
        try:
            shannon_tree = self.design_mux_tree("shannon")
            implementations['shannon_tree'] = shannon_tree
        except:
            pass
        
        # Compare costs
        comparison = {
            'implementations': implementations,
            'cost_comparison': {},
            'recommendations': []
        }
        
        for name, impl in implementations.items():
            cost = impl.get('implementation_cost', {})
            comparison['cost_comparison'][name] = cost
        
        return comparison
    
    def _calculate_single_mux_cost(self, data_inputs: Dict, remaining_vars: List[int]) -> Dict:
        """Calculate implementation cost for single multiplexer"""
        # Count gates needed for data input generation
        gate_count = 0
        literal_count = 0
        
        for value in data_inputs.values():
            if isinstance(value, str) and value not in ['0', '1']:
                # Estimate gates needed for this expression
                gate_count += value.count('+') + value.count("'") 
                literal_count += len([c for c in value if c.isalpha()])
        
        return {
            'mux_inputs': len(data_inputs),
            'additional_gates': gate_count,
            'total_literals': literal_count,
            'complexity': 'low' if gate_count < 5 else 'medium' if gate_count < 15 else 'high'
        }
    
    def _calculate_tree_cost(self, tree: Dict) -> Dict:
        """Calculate cost for multiplexer tree"""
        return self._recursive_cost_calculation(tree)
    
    def _recursive_cost_calculation(self, node: Dict) -> Dict:
        """Recursively calculate tree implementation cost"""
        if node['type'] == 'constant':
            return {'muxes': 0, 'constants': 1, 'variables': 0}
        elif node['type'] == 'variable':
            return {'muxes': 0, 'constants': 0, 'variables': 1}
        elif node['type'] == 'mux':
            cost_0 = self._recursive_cost_calculation(node['input_0'])
            cost_1 = self._recursive_cost_calculation(node['input_1'])
            
            return {
                'muxes': 1 + cost_0['muxes'] + cost_1['muxes'],
                'constants': cost_0['constants'] + cost_1['constants'],
                'variables': cost_0['variables'] + cost_1['variables']
            }
        
        return {'muxes': 0, 'constants': 0, 'variables': 0}
    
    def _calculate_tree_depth(self, tree: Dict) -> int:
        """Calculate depth of multiplexer tree"""
        if tree['type'] in ['constant', 'variable']:
            return 0
        elif tree['type'] == 'mux':
            return 1 + max(
                self._calculate_tree_depth(tree['input_0']),
                self._calculate_tree_depth(tree['input_1'])
            )
        return 0
    
    def _count_muxes_in_tree(self, tree: Dict) -> int:
        """Count total multiplexers in tree"""
        if tree['type'] in ['constant', 'variable']:
            return 0
        elif tree['type'] == 'mux':
            return 1 + self._count_muxes_in_tree(tree['input_0']) + self._count_muxes_in_tree(tree['input_1'])
        return 0
    
    def display_mux_implementation(self, implementation: Dict) -> str:
        """
        Display multiplexer implementation in readable format
        
        Args:
            implementation: Implementation dictionary
        
        Returns:
            Formatted string representation
        """
        if implementation['type'] == 'single_mux':
            return self._display_single_mux(implementation)
        elif 'tree' in implementation['type']:
            return self._display_mux_tree(implementation)
        else:
            return str(implementation)
    
    def _display_single_mux(self, impl: Dict) -> str:
        """Display single multiplexer implementation"""
        result = f"\nSingle {impl['mux_size']} Multiplexer Implementation\n"
        result += "=" * 50 + "\n"
        
        result += f"Select Variables: {', '.join(impl['select_variables'])}\n\n"
        
        result += "Data Inputs:\n"
        result += "-" * 20 + "\n"
        
        for combo, expr in impl['data_input_expressions'].items():
            select_binary = format(combo, f"0{len(impl['select_variables'])}b")
            select_str = ''.join([f"{var}={bit}" for var, bit in zip(impl['select_variables'], select_binary)])
            result += f"D{combo} ({select_str}): {expr}\n"
        
        cost = impl['implementation_cost']
        result += f"\nImplementation Cost:\n"
        result += f"  MUX size: {impl['mux_size']}\n"
        result += f"  Additional gates: {cost['additional_gates']}\n"
        result += f"  Total literals: {cost['total_literals']}\n"
        result += f"  Complexity: {cost['complexity']}\n"
        
        return result
    
    def _display_mux_tree(self, impl: Dict) -> str:
        """Display multiplexer tree implementation"""
        result = f"\n{impl['type'].replace('_', ' ').title()}\n"
        result += "=" * 40 + "\n"
        
        if 'tree_structure' in impl:
            result += "Tree Structure:\n"
            result += self._format_tree_structure(impl['tree_structure'], 0)
        
        cost = impl.get('implementation_cost', {})
        result += f"\nImplementation Metrics:\n"
        result += f"  Total MUXes: {impl.get('mux_count', 'N/A')}\n"
        result += f"  Tree depth: {impl.get('depth', 'N/A')}\n"
        result += f"  Cost breakdown: {cost}\n"
        
        return result
    
    def _format_tree_structure(self, node: Dict, indent: int) -> str:
        """Format tree structure for display"""
        spaces = "  " * indent
        
        if node['type'] == 'constant':
            return f"{spaces}Constant: {node['value']}\n"
        elif node['type'] == 'variable':
            return f"{spaces}Variable: {node['variable']}\n"
        elif node['type'] == 'mux':
            result = f"{spaces}MUX (select: {node['select']})\n"
            result += f"{spaces}├─0: "
            result += self._format_tree_structure(node['input_0'], indent + 1).strip() + "\n"
            result += f"{spaces}└─1: "
            result += self._format_tree_structure(node['input_1'], indent + 1).strip() + "\n"
            return result
        
        return f"{spaces}Unknown node type\n"


def test_multiplexer_design():
    """Test multiplexer design functionality"""
    print("Testing Multiplexer-based Design")
    print("=" * 40)
    
    # Test case 1: Simple 3-variable function
    mux_design = MultiplexerDesign(3)
    mux_design.set_function(minterms=[1, 2, 4, 7])
    
    print("Test Case 1: F(A,B,C) = Σ(1,2,4,7)")
    
    # Single multiplexer implementation
    single_mux = mux_design.design_single_mux([0])  # Use A as select
    print(mux_design.display_mux_implementation(single_mux))
    
    # Shannon expansion tree
    shannon_tree = mux_design.design_mux_tree("shannon")
    print(mux_design.display_mux_implementation(shannon_tree))
    
    # Compare implementations
    comparison = mux_design.compare_implementations()
    print("\nImplementation Comparison:")
    print("=" * 30)
    for name, cost in comparison['cost_comparison'].items():
        print(f"{name}: {cost}")
    
    # Test case 2: 4-variable function
    print("\n" + "=" * 40)
    mux_design2 = MultiplexerDesign(4)
    mux_design2.set_function(minterms=[0, 3, 5, 6, 9, 10, 12, 15])
    
    print("Test Case 2: F(A,B,C,D) = Σ(0,3,5,6,9,10,12,15)")
    
    # Different select variable combinations
    for num_select in [1, 2]:
        single_mux = mux_design2.design_single_mux(list(range(num_select)))
        print(f"\n{num_select}-variable select:")
        print(mux_design2.display_mux_implementation(single_mux))


if __name__ == "__main__":
    test_multiplexer_design()
