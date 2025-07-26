"""
Quine-McCluskey Algorithm
Systematic minimization of Boolean functions using tabular method
"""

from typing import List, Set, Dict, Tuple, Optional
import itertools


class Term:
    """Represents a term in the Quine-McCluskey algorithm"""
    
    def __init__(self, minterms: Set[int], binary_rep: str):
        """
        Initialize term
        
        Args:
            minterms: Set of minterm indices this term covers
            binary_rep: Binary representation with '-' for don't cares
        """
        self.minterms = minterms
        self.binary_rep = binary_rep
        self.num_variables = len(binary_rep)
        self.used = False
    
    def can_combine_with(self, other: 'Term') -> bool:
        """
        Check if this term can combine with another term
        
        Args:
            other: Another term to check combination with
            
        Returns:
            True if terms can be combined (differ by exactly one literal)
        """
        if len(self.binary_rep) != len(other.binary_rep):
            return False
        
        differences = 0
        for i, (bit1, bit2) in enumerate(zip(self.binary_rep, other.binary_rep)):
            if bit1 != bit2:
                if bit1 == '-' or bit2 == '-':
                    return False
                differences += 1
                if differences > 1:
                    return False
        
        return differences == 1
    
    def combine_with(self, other: 'Term') -> 'Term':
        """
        Combine this term with another term
        
        Args:
            other: Term to combine with
            
        Returns:
            New combined term
        """
        if not self.can_combine_with(other):
            raise ValueError("Terms cannot be combined")
        
        new_binary = ""
        for bit1, bit2 in zip(self.binary_rep, other.binary_rep):
            if bit1 == bit2:
                new_binary += bit1
            else:
                new_binary += '-'
        
        new_minterms = self.minterms | other.minterms
        return Term(new_minterms, new_binary)
    
    def covers_minterm(self, minterm: int) -> bool:
        """
        Check if this term covers a specific minterm
        
        Args:
            minterm: Minterm index to check
            
        Returns:
            True if term covers the minterm
        """
        return minterm in self.minterms
    
    def to_expression(self, variables: List[str]) -> str:
        """
        Convert term to Boolean expression
        
        Args:
            variables: List of variable names
            
        Returns:
            Boolean expression string
        """
        if len(variables) != len(self.binary_rep):
            raise ValueError("Number of variables must match binary representation length")
        
        literals = []
        for i, bit in enumerate(self.binary_rep):
            if bit == '1':
                literals.append(variables[i])
            elif bit == '0':
                literals.append(variables[i] + "'")
            # Skip don't cares ('-')
        
        return ''.join(literals) if literals else '1'
    
    def __str__(self) -> str:
        return f"Term({sorted(self.minterms)}, {self.binary_rep})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Term) and self.binary_rep == other.binary_rep
    
    def __hash__(self) -> bool:
        return hash(self.binary_rep)


class QuineMcCluskey:
    """
    Quine-McCluskey algorithm implementation for Boolean function minimization.
    
    This is a systematic tabular method that finds all prime implicants
    and then determines the minimum set needed to cover all minterms.
    """
    
    def __init__(self, num_variables: int):
        """
        Initialize Quine-McCluskey algorithm
        
        Args:
            num_variables: Number of input variables
        """
        self.num_variables = num_variables
        self.variables = [f'A{i}' for i in range(num_variables)]
        self.minterms = set()
        self.dont_cares = set()
        self.prime_implicants = []
        
    def set_function(self, minterms: List[int], dont_cares: List[int] = None) -> None:
        """
        Set the Boolean function to minimize
        
        Args:
            minterms: List of minterms where function = 1
            dont_cares: List of don't care terms (optional)
        """
        self.minterms = set(minterms)
        self.dont_cares = set(dont_cares) if dont_cares else set()
        
        # Validate inputs
        max_value = 2 ** self.num_variables - 1
        for minterm in self.minterms | self.dont_cares:
            if minterm < 0 or minterm > max_value:
                raise ValueError(f"Minterm {minterm} out of range [0, {max_value}]")
    
    def _decimal_to_binary(self, decimal: int) -> str:
        """
        Convert decimal to binary string with fixed width
        
        Args:
            decimal: Decimal number to convert
            
        Returns:
            Binary string representation
        """
        return format(decimal, f'0{self.num_variables}b')
    
    def _count_ones(self, binary_str: str) -> int:
        """
        Count number of ones in binary string
        
        Args:
            binary_str: Binary string
            
        Returns:
            Number of ones
        """
        return binary_str.count('1')
    
    def _group_by_ones(self, terms: List[Term]) -> Dict[int, List[Term]]:
        """
        Group terms by number of ones in their binary representation
        
        Args:
            terms: List of terms to group
            
        Returns:
            Dictionary mapping number of ones to list of terms
        """
        groups = {}
        for term in terms:
            ones_count = self._count_ones(term.binary_rep)
            if ones_count not in groups:
                groups[ones_count] = []
            groups[ones_count].append(term)
        
        return groups
    
    def _find_prime_implicants(self) -> List[Term]:
        """
        Find all prime implicants using the Quine-McCluskey tabular method
        
        Returns:
            List of prime implicant terms
        """
        # Step 1: Create initial terms from minterms and don't cares
        all_terms = self.minterms | self.dont_cares
        current_terms = []
        
        for term in all_terms:
            binary_rep = self._decimal_to_binary(term)
            current_terms.append(Term({term}, binary_rep))
        
        prime_implicants = []
        
        # Step 2: Iteratively combine terms
        while current_terms:
            # Group terms by number of ones
            groups = self._group_by_ones(current_terms)
            next_terms = []
            
            # Try to combine terms between adjacent groups
            for ones_count in sorted(groups.keys()):
                if ones_count + 1 in groups:
                    group1 = groups[ones_count]
                    group2 = groups[ones_count + 1]
                    
                    # Try all combinations between the two groups
                    for term1 in group1:
                        for term2 in group2:
                            if term1.can_combine_with(term2):
                                combined_term = term1.combine_with(term2)
                                if combined_term not in next_terms:
                                    next_terms.append(combined_term)
                                term1.used = True
                                term2.used = True
            
            # Add unused terms to prime implicants
            for term in current_terms:
                if not term.used:
                    prime_implicants.append(term)
            
            current_terms = next_terms
        
        return prime_implicants
    
    def _create_coverage_table(self, prime_implicants: List[Term]) -> Dict[Term, Set[int]]:
        """
        Create coverage table showing which minterms each prime implicant covers
        
        Args:
            prime_implicants: List of prime implicants
            
        Returns:
            Dictionary mapping prime implicants to covered minterms
        """
        coverage = {}
        for pi in prime_implicants:
            covered_minterms = pi.minterms & self.minterms
            if covered_minterms:  # Only include PIs that cover actual minterms
                coverage[pi] = covered_minterms
        
        return coverage
    
    def _find_essential_prime_implicants(self, coverage: Dict[Term, Set[int]]) -> Tuple[List[Term], Set[int]]:
        """
        Find essential prime implicants
        
        Args:
            coverage: Coverage table
            
        Returns:
            Tuple of (essential prime implicants, covered minterms)
        """
        essential_pis = []
        covered_minterms = set()
        
        # Find minterms covered by only one prime implicant
        for minterm in self.minterms:
            covering_pis = [pi for pi, covered in coverage.items() if minterm in covered]
            
            if len(covering_pis) == 1:
                essential_pi = covering_pis[0]
                if essential_pi not in essential_pis:
                    essential_pis.append(essential_pi)
                    covered_minterms.update(coverage[essential_pi])
        
        return essential_pis, covered_minterms
    
    def _solve_covering_problem(self, coverage: Dict[Term, Set[int]], uncovered_minterms: Set[int]) -> List[Term]:
        """
        Solve the covering problem to find minimum set of prime implicants
        
        Args:
            coverage: Coverage table
            uncovered_minterms: Minterms not yet covered
            
        Returns:
            Minimum set of additional prime implicants
        """
        if not uncovered_minterms:
            return []
        
        # Filter coverage to only include PIs that cover uncovered minterms
        relevant_coverage = {}
        for pi, covered in coverage.items():
            relevant_covered = covered & uncovered_minterms
            if relevant_covered:
                relevant_coverage[pi] = relevant_covered
        
        # Use greedy approach for simplicity (can be improved with exact algorithms)
        selected_pis = []
        remaining_minterms = uncovered_minterms.copy()
        
        while remaining_minterms and relevant_coverage:
            # Choose PI that covers most remaining minterms
            best_pi = None
            best_coverage_size = 0
            
            for pi, covered in relevant_coverage.items():
                coverage_size = len(covered & remaining_minterms)
                if coverage_size > best_coverage_size:
                    best_coverage_size = coverage_size
                    best_pi = pi
            
            if best_pi:
                selected_pis.append(best_pi)
                newly_covered = relevant_coverage[best_pi] & remaining_minterms
                remaining_minterms -= newly_covered
                
                # Remove covered minterms from coverage table
                for pi in list(relevant_coverage.keys()):
                    relevant_coverage[pi] -= newly_covered
                    if not relevant_coverage[pi]:
                        del relevant_coverage[pi]
            else:
                break
        
        return selected_pis
    
    def minimize(self) -> Dict[str, any]:
        """
        Minimize the Boolean function using Quine-McCluskey algorithm
        
        Returns:
            Dictionary containing minimization results
        """
        if not self.minterms:
            return {
                'simplified_expression': '0',
                'prime_implicants': [],
                'essential_prime_implicants': [],
                'selected_prime_implicants': [],
                'cost': 0,
                'coverage_table': {}
            }
        
        # Step 1: Find all prime implicants
        prime_implicants = self._find_prime_implicants()
        
        # Step 2: Create coverage table
        coverage = self._create_coverage_table(prime_implicants)
        
        # Step 3: Find essential prime implicants
        essential_pis, covered_by_essential = self._find_essential_prime_implicants(coverage)
        
        # Step 4: Solve covering problem for remaining minterms
        uncovered_minterms = self.minterms - covered_by_essential
        additional_pis = self._solve_covering_problem(coverage, uncovered_minterms)
        
        # Step 5: Combine results
        selected_pis = essential_pis + additional_pis
        
        # Generate simplified expression
        expression_terms = []
        for pi in selected_pis:
            term_expr = pi.to_expression(self.variables)
            if term_expr != '1':
                expression_terms.append(term_expr)
            else:
                return {
                    'simplified_expression': '1',
                    'prime_implicants': [pi.to_expression(self.variables) for pi in prime_implicants],
                    'essential_prime_implicants': [pi.to_expression(self.variables) for pi in essential_pis],
                    'selected_prime_implicants': [pi.to_expression(self.variables) for pi in selected_pis],
                    'cost': 1,
                    'coverage_table': {pi.to_expression(self.variables): list(covered) for pi, covered in coverage.items()}
                }
        
        simplified_expression = ' + '.join(expression_terms) if expression_terms else '0'
        
        return {
            'simplified_expression': simplified_expression,
            'prime_implicants': [pi.to_expression(self.variables) for pi in prime_implicants],
            'essential_prime_implicants': [pi.to_expression(self.variables) for pi in essential_pis],
            'selected_prime_implicants': [pi.to_expression(self.variables) for pi in selected_pis],
            'cost': len(selected_pis),
            'coverage_table': {pi.to_expression(self.variables): list(covered) for pi, covered in coverage.items()}
        }
    
    def display_prime_implicant_table(self) -> str:
        """
        Display the prime implicant table
        
        Returns:
            Formatted string representation of the table
        """
        prime_implicants = self._find_prime_implicants()
        
        result = "\nPrime Implicant Table:\n"
        result += "=" * 50 + "\n"
        result += f"{'Prime Implicant':<20} {'Binary':<15} {'Covers Minterms':<20}\n"
        result += "-" * 50 + "\n"
        
        for pi in prime_implicants:
            expr = pi.to_expression(self.variables)
            covered = list(pi.minterms & self.minterms)
            result += f"{expr:<20} {pi.binary_rep:<15} {str(covered):<20}\n"
        
        return result
    
    def display_coverage_table(self) -> str:
        """
        Display the coverage table
        
        Returns:
            Formatted string representation of the coverage table
        """
        prime_implicants = self._find_prime_implicants()
        coverage = self._create_coverage_table(prime_implicants)
        
        result = "\nCoverage Table:\n"
        result += "=" * 60 + "\n"
        
        # Header
        result += f"{'Prime Implicant':<20}"
        for minterm in sorted(self.minterms):
            result += f"{minterm:<4}"
        result += "\n"
        result += "-" * 60 + "\n"
        
        # Rows
        for pi, covered in coverage.items():
            expr = pi.to_expression(self.variables)
            result += f"{expr:<20}"
            for minterm in sorted(self.minterms):
                mark = "X" if minterm in covered else " "
                result += f"{mark:<4}"
            result += "\n"
        
        return result


def test_quine_mccluskey():
    """Test Quine-McCluskey algorithm functionality"""
    print("Testing Quine-McCluskey Algorithm")
    print("=" * 50)
    
    # Test case 1: Simple 3-variable function
    qm = QuineMcCluskey(3)
    qm.set_function([0, 1, 2, 5, 6, 7])
    
    result = qm.minimize()
    print("Test Case 1: F(A,B,C) = Σ(0,1,2,5,6,7)")
    print(f"Simplified Expression: {result['simplified_expression']}")
    print(f"Prime Implicants: {result['prime_implicants']}")
    print(f"Essential Prime Implicants: {result['essential_prime_implicants']}")
    print(f"Cost: {result['cost']}")
    
    print(qm.display_prime_implicant_table())
    print(qm.display_coverage_table())
    
    # Test case 2: Function with don't cares
    print("\n" + "=" * 50)
    qm2 = QuineMcCluskey(4)
    qm2.set_function([0, 1, 2, 8, 10, 11, 14, 15], [5, 7])
    
    result2 = qm2.minimize()
    print("Test Case 2: F(A,B,C,D) = Σ(0,1,2,8,10,11,14,15) + d(5,7)")
    print(f"Simplified Expression: {result2['simplified_expression']}")
    print(f"Prime Implicants: {result2['prime_implicants']}")
    print(f"Selected Prime Implicants: {result2['selected_prime_implicants']}")
    print(f"Cost: {result2['cost']}")


if __name__ == "__main__":
    test_quine_mccluskey()
