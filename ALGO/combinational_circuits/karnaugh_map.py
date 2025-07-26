"""
Karnaugh Map Algorithm
Boolean expression simplification using K-Maps
"""

import itertools
from typing import List, Dict, Tuple, Set, Optional


class KarnaughMap:
    """
    Karnaugh Map implementation for Boolean function simplification.
    
    The K-Map is a graphical method for simplifying Boolean expressions
    by grouping adjacent cells containing 1s (minterms).
    """
    
    def __init__(self, num_variables: int):
        """
        Initialize Karnaugh Map
        
        Args:
            num_variables: Number of input variables (2-6 supported)
        """
        if num_variables < 2 or num_variables > 6:
            raise ValueError("K-Map supports 2-6 variables only")
            
        self.num_variables = num_variables
        self.variables = [f'A{i}' for i in range(num_variables)]
        self.size = 2 ** num_variables
        self.kmap = {}
        self.minterms = set()
        self.maxterms = set()
        
        # Gray code sequences for different map sizes
        self.gray_codes = {
            2: ['0', '1'],
            4: ['00', '01', '11', '10'],
            8: ['000', '001', '011', '010', '110', '111', '101', '100']
        }
    
    def set_function_from_minterms(self, minterms: List[int]) -> None:
        """
        Set the Boolean function using minterms
        
        Args:
            minterms: List of minterm indices where function = 1
        """
        self.minterms = set(minterms)
        self.maxterms = set(range(self.size)) - self.minterms
        
        # Fill K-map
        for i in range(self.size):
            self.kmap[i] = 1 if i in self.minterms else 0
    
    def set_function_from_truth_table(self, truth_table: List[int]) -> None:
        """
        Set the Boolean function from truth table
        
        Args:
            truth_table: List of output values (0 or 1)
        """
        if len(truth_table) != self.size:
            raise ValueError(f"Truth table must have {self.size} entries")
        
        self.minterms = {i for i, val in enumerate(truth_table) if val == 1}
        self.maxterms = {i for i, val in enumerate(truth_table) if val == 0}
        
        for i, val in enumerate(truth_table):
            self.kmap[i] = val
    
    def get_adjacent_cells(self, cell: int) -> List[int]:
        """
        Get adjacent cells in K-map (differ by 1 bit)
        
        Args:
            cell: Cell index
            
        Returns:
            List of adjacent cell indices
        """
        adjacent = []
        cell_binary = format(cell, f'0{self.num_variables}b')
        
        for i in range(self.num_variables):
            # Flip bit i
            new_binary = list(cell_binary)
            new_binary[i] = '0' if new_binary[i] == '1' else '1'
            adjacent_cell = int(''.join(new_binary), 2)
            adjacent.append(adjacent_cell)
        
        return adjacent
    
    def find_prime_implicants(self) -> List[Set[int]]:
        """
        Find all prime implicants using a simplified grouping method
        
        Returns:
            List of prime implicant sets
        """
        if not self.minterms:
            return []
        
        # For 3-variable K-map, use a simpler approach
        if self.num_variables == 3:
            return self._find_prime_implicants_3var()
        
        # Start with individual minterms as initial groups
        current_groups = [{minterm} for minterm in self.minterms]
        prime_implicants = []
        max_iterations = 10  # Prevent infinite loops
        iteration = 0
        
        while current_groups and iteration < max_iterations:
            next_groups = []
            used_groups = set()
            
            # Try to combine groups
            for i, group1 in enumerate(current_groups):
                if i in used_groups:
                    continue
                    
                combined = False
                for j in range(i + 1, len(current_groups)):
                    if j in used_groups:
                        continue
                        
                    group2 = current_groups[j]
                    
                    # Simple combination check - groups must be adjacent
                    if self._can_combine_simple(group1, group2):
                        combined_group = group1 | group2
                        if combined_group not in next_groups:
                            next_groups.append(combined_group)
                        used_groups.add(i)
                        used_groups.add(j)
                        combined = True
                        break
                
                # If group couldn't be combined, it's a prime implicant
                if not combined and i not in used_groups:
                    prime_implicants.append(group1)
            
            current_groups = next_groups
            iteration += 1
        
        # Add any remaining groups as prime implicants
        for group in current_groups:
            if group not in prime_implicants:
                prime_implicants.append(group)
        
        return prime_implicants
    
    def _find_prime_implicants_3var(self) -> List[Set[int]]:
        """Simplified prime implicant finding for 3 variables"""
        prime_implicants = []
        
        # Check for pairs first
        covered = set()
        minterms_list = list(self.minterms)
        
        for i, m1 in enumerate(minterms_list):
            if m1 in covered:
                continue
            for j, m2 in enumerate(minterms_list[i+1:], i+1):
                if m2 in covered:
                    continue
                # Check if they differ by exactly one bit
                if bin(m1 ^ m2).count('1') == 1:
                    prime_implicants.append({m1, m2})
                    covered.add(m1)
                    covered.add(m2)
                    break
        
        # Add uncovered minterms as individual prime implicants
        for m in self.minterms:
            if m not in covered:
                prime_implicants.append({m})
        
        return prime_implicants
    
    def _can_combine_simple(self, group1: Set[int], group2: Set[int]) -> bool:
        """
        Simple check if two groups can be combined
        
        Args:
            group1, group2: Sets of minterm indices
            
        Returns:
            True if groups can be combined
        """
        # Groups must be same size and power of 2
        if len(group1) != len(group2):
            return False
        
        if len(group1) not in [1, 2, 4]:
            return False
        
        # For single minterms, check if they differ by one bit
        if len(group1) == 1 and len(group2) == 1:
            m1 = list(group1)[0]
            m2 = list(group2)[0]
            return bin(m1 ^ m2).count('1') == 1
        
        return False
    
    def find_essential_prime_implicants(self, prime_implicants: List[Set[int]]) -> Tuple[List[Set[int]], Set[int]]:
        """
        Find essential prime implicants using coverage analysis
        
        Args:
            prime_implicants: List of all prime implicants
            
        Returns:
            Tuple of (essential prime implicants, covered minterms)
        """
        essential = []
        covered_minterms = set()
        
        # Find minterms covered by only one prime implicant
        for minterm in self.minterms:
            covering_implicants = [pi for pi in prime_implicants if minterm in pi]
            
            if len(covering_implicants) == 1:
                essential_pi = covering_implicants[0]
                if essential_pi not in essential:
                    essential.append(essential_pi)
                    covered_minterms.update(essential_pi)
        
        return essential, covered_minterms
    
    def minimize_expression(self) -> Dict[str, any]:
        """
        Minimize the Boolean expression using K-map method
        
        Returns:
            Dictionary containing minimization results
        """
        if not self.minterms:
            return {
                'simplified_expression': '0',
                'prime_implicants': [],
                'essential_prime_implicants': [],
                'cost': 0
            }
        
        # Find all prime implicants
        prime_implicants = self.find_prime_implicants()
        
        # Find essential prime implicants
        essential_pis, covered_minterms = self.find_essential_prime_implicants(prime_implicants)
        
        # Find minimum cover for remaining minterms
        remaining_minterms = self.minterms - covered_minterms
        additional_pis = self._find_minimum_cover(prime_implicants, remaining_minterms)
        
        # Combine essential and additional prime implicants
        final_pis = essential_pis + additional_pis
        
        # Generate simplified expression
        expression = self._generate_expression(final_pis)
        
        return {
            'simplified_expression': expression,
            'prime_implicants': [self._pi_to_string(pi) for pi in prime_implicants],
            'essential_prime_implicants': [self._pi_to_string(pi) for pi in essential_pis],
            'final_prime_implicants': [self._pi_to_string(pi) for pi in final_pis],
            'cost': len(final_pis)
        }
    
    def _find_minimum_cover(self, prime_implicants: List[Set[int]], uncovered_minterms: Set[int]) -> List[Set[int]]:
        """
        Find minimum set of prime implicants to cover remaining minterms
        
        Args:
            prime_implicants: All prime implicants
            uncovered_minterms: Minterms not yet covered
            
        Returns:
            Minimum set of additional prime implicants
        """
        if not uncovered_minterms:
            return []
        
        # Simple greedy approach - choose PI that covers most uncovered minterms
        selected = []
        remaining = uncovered_minterms.copy()
        
        while remaining:
            best_pi = None
            best_coverage = 0
            
            for pi in prime_implicants:
                if pi not in selected:
                    coverage = len(pi & remaining)
                    if coverage > best_coverage:
                        best_coverage = coverage
                        best_pi = pi
            
            if best_pi:
                selected.append(best_pi)
                remaining -= best_pi
            else:
                break
        
        return selected
    
    def _pi_to_string(self, prime_implicant: Set[int]) -> str:
        """
        Convert prime implicant to string representation
        
        Args:
            prime_implicant: Set of minterm indices
            
        Returns:
            String representation of the prime implicant
        """
        if not prime_implicant:
            return ""
        
        # Find the pattern (which bits are constant)
        pi_list = list(prime_implicant)
        if len(pi_list) == 1:
            # Single minterm
            minterm = pi_list[0]
            binary = format(minterm, f'0{self.num_variables}b')
            term = ""
            for i, bit in enumerate(binary):
                if bit == '1':
                    term += self.variables[i]
                else:
                    term += self.variables[i] + "'"
            return term
        
        # Multiple minterms - find don't care positions
        first_binary = format(pi_list[0], f'0{self.num_variables}b')
        pattern = list(first_binary)
        
        for minterm in pi_list[1:]:
            binary = format(minterm, f'0{self.num_variables}b')
            for i, bit in enumerate(binary):
                if pattern[i] != bit:
                    pattern[i] = '-'  # Don't care
        
        # Generate term from pattern
        term = ""
        for i, bit in enumerate(pattern):
            if bit == '1':
                term += self.variables[i]
            elif bit == '0':
                term += self.variables[i] + "'"
            # Skip don't cares
        
        return term if term else "1"
    
    def _generate_expression(self, prime_implicants: List[Set[int]]) -> str:
        """
        Generate final Boolean expression from prime implicants
        
        Args:
            prime_implicants: Selected prime implicants
            
        Returns:
            Simplified Boolean expression string
        """
        if not prime_implicants:
            return "0"
        
        terms = []
        for pi in prime_implicants:
            term = self._pi_to_string(pi)
            if term and term != "1":
                terms.append(term)
            elif term == "1":
                return "1"  # Function is always true
        
        return " + ".join(terms) if terms else "1"
    
    def display_kmap(self) -> str:
        """
        Display K-map in tabular format
        
        Returns:
            String representation of K-map
        """
        if self.num_variables == 2:
            return self._display_2var_kmap()
        elif self.num_variables == 3:
            return self._display_3var_kmap()
        elif self.num_variables == 4:
            return self._display_4var_kmap()
        else:
            return self._display_generic_kmap()
    
    def _display_2var_kmap(self) -> str:
        """Display 2-variable K-map"""
        result = f"\nK-Map for {self.variables[0]}, {self.variables[1]}:\n"
        result += f"    {self.variables[1]}'\t{self.variables[1]}\n"
        result += f"{self.variables[0]}'\t{self.kmap[0]}\t{self.kmap[1]}\n"
        result += f"{self.variables[0]}\t{self.kmap[2]}\t{self.kmap[3]}\n"
        return result
    
    def _display_3var_kmap(self) -> str:
        """Display 3-variable K-map"""
        result = f"\nK-Map for {self.variables[0]}, {self.variables[1]}, {self.variables[2]}:\n"
        result += f"\\{self.variables[1]}{self.variables[2]}\t00\t01\t11\t10\n"
        result += f"{self.variables[0]}'  \t{self.kmap[0]}\t{self.kmap[1]}\t{self.kmap[3]}\t{self.kmap[2]}\n"
        result += f"{self.variables[0]}   \t{self.kmap[4]}\t{self.kmap[5]}\t{self.kmap[7]}\t{self.kmap[6]}\n"
        return result
    
    def _display_4var_kmap(self) -> str:
        """Display 4-variable K-map"""
        result = f"\nK-Map for {self.variables[0]}, {self.variables[1]}, {self.variables[2]}, {self.variables[3]}:\n"
        result += f"\\{self.variables[2]}{self.variables[3]}\t00\t01\t11\t10\n"
        result += f"{self.variables[0]}'{self.variables[1]}'\t{self.kmap[0]}\t{self.kmap[1]}\t{self.kmap[3]}\t{self.kmap[2]}\n"
        result += f"{self.variables[0]}'{self.variables[1]} \t{self.kmap[4]}\t{self.kmap[5]}\t{self.kmap[7]}\t{self.kmap[6]}\n"
        result += f"{self.variables[0]} {self.variables[1]} \t{self.kmap[12]}\t{self.kmap[13]}\t{self.kmap[15]}\t{self.kmap[14]}\n"
        result += f"{self.variables[0]} {self.variables[1]}'\t{self.kmap[8]}\t{self.kmap[9]}\t{self.kmap[11]}\t{self.kmap[10]}\n"
        return result
    
    def _display_generic_kmap(self) -> str:
        """Display generic K-map for >4 variables"""
        result = f"\nK-Map for {', '.join(self.variables)}:\n"
        result += "Minterm\tValue\n"
        for i in range(self.size):
            binary = format(i, f'0{self.num_variables}b')
            result += f"{i}({binary})\t{self.kmap[i]}\n"
        return result


# Example usage and test functions
def test_kmap():
    """Test K-map functionality"""
    print("Testing Karnaugh Map Implementation")
    print("=" * 40)
    
    # Test 3-variable function: F(A,B,C) = Σ(1,3,5,7)
    kmap = KarnaughMap(3)
    kmap.set_function_from_minterms([1, 3, 5, 7])
    
    print(kmap.display_kmap())
    
    result = kmap.minimize_expression()
    print(f"Simplified Expression: {result['simplified_expression']}")
    print(f"Prime Implicants: {result['prime_implicants']}")
    print(f"Essential Prime Implicants: {result['essential_prime_implicants']}")
    
    # Test 4-variable function
    print("\n" + "=" * 40)
    kmap4 = KarnaughMap(4)
    kmap4.set_function_from_minterms([0, 1, 2, 5, 6, 7, 8, 9, 10, 14])
    
    print(kmap4.display_kmap())
    
    result4 = kmap4.minimize_expression()
    print(f"Simplified Expression: {result4['simplified_expression']}")
    print(f"Cost (number of terms): {result4['cost']}")


if __name__ == "__main__":
    test_kmap()
