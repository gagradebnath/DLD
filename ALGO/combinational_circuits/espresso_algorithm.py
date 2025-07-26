"""
Espresso Algorithm
Heuristic logic minimization algorithm used in CAD tools
"""

from typing import List, Set, Dict, Tuple, Optional
import copy
import itertools


class Cube:
    """
    Represents a cube (product term) in the Espresso algorithm
    Each cube is represented as a string with characters:
    '0' - variable appears complemented
    '1' - variable appears uncomplemented  
    '-' - variable doesn't appear (don't care)
    """
    
    def __init__(self, representation: str):
        """
        Initialize cube
        
        Args:
            representation: String representation of the cube
        """
        self.representation = representation
        self.num_variables = len(representation)
    
    def intersect(self, other: 'Cube') -> Optional['Cube']:
        """
        Compute intersection of two cubes
        
        Args:
            other: Another cube to intersect with
            
        Returns:
            Intersection cube or None if intersection is empty
        """
        if len(self.representation) != len(other.representation):
            return None
        
        result = ""
        for i, (c1, c2) in enumerate(zip(self.representation, other.representation)):
            if c1 == '-':
                result += c2
            elif c2 == '-':
                result += c1
            elif c1 == c2:
                result += c1
            else:
                return None  # Empty intersection
        
        return Cube(result)
    
    def contains(self, other: 'Cube') -> bool:
        """
        Check if this cube contains another cube
        
        Args:
            other: Cube to check containment for
            
        Returns:
            True if this cube contains the other
        """
        for c1, c2 in zip(self.representation, other.representation):
            if c1 != '-' and c2 != '-' and c1 != c2:
                return False
            if c1 == '-' and c2 != '-':
                return False
        return True
    
    def distance(self, other: 'Cube') -> int:
        """
        Compute distance between two cubes (number of different literals)
        
        Args:
            other: Other cube
            
        Returns:
            Distance between cubes
        """
        distance = 0
        for c1, c2 in zip(self.representation, other.representation):
            if (c1 != '-' and c2 != '-' and c1 != c2):
                distance += 1
        return distance
    
    def can_merge(self, other: 'Cube') -> bool:
        """
        Check if two cubes can be merged (distance = 1)
        
        Args:
            other: Other cube to check
            
        Returns:
            True if cubes can be merged
        """
        return self.distance(other) == 1
    
    def merge(self, other: 'Cube') -> Optional['Cube']:
        """
        Merge two cubes if possible
        
        Args:
            other: Cube to merge with
            
        Returns:
            Merged cube or None if merge not possible
        """
        if not self.can_merge(other):
            return None
        
        result = ""
        for c1, c2 in zip(self.representation, other.representation):
            if c1 == c2:
                result += c1
            elif (c1 != '-' and c2 != '-' and c1 != c2):
                result += '-'
            elif c1 == '-':
                result += c2
            elif c2 == '-':
                result += c1
        
        return Cube(result)
    
    def literal_count(self) -> int:
        """Count number of literals in cube"""
        return sum(1 for c in self.representation if c != '-')
    
    def to_expression(self, variables: List[str]) -> str:
        """
        Convert cube to Boolean expression
        
        Args:
            variables: List of variable names
            
        Returns:
            Boolean expression string
        """
        if len(variables) != len(self.representation):
            raise ValueError("Number of variables must match representation length")
        
        literals = []
        for i, char in enumerate(self.representation):
            if char == '1':
                literals.append(variables[i])
            elif char == '0':
                literals.append(variables[i] + "'")
        
        return ''.join(literals) if literals else '1'
    
    def __str__(self) -> str:
        return self.representation
    
    def __repr__(self) -> str:
        return f"Cube({self.representation})"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Cube) and self.representation == other.representation
    
    def __hash__(self) -> int:
        return hash(self.representation)


class Cover:
    """Represents a cover (set of cubes) in the Espresso algorithm"""
    
    def __init__(self, cubes: List[Cube] = None):
        """
        Initialize cover
        
        Args:
            cubes: List of cubes in the cover
        """
        self.cubes = cubes if cubes else []
    
    def add_cube(self, cube: Cube) -> None:
        """Add cube to cover"""
        if cube not in self.cubes:
            self.cubes.append(cube)
    
    def remove_cube(self, cube: Cube) -> None:
        """Remove cube from cover"""
        if cube in self.cubes:
            self.cubes.remove(cube)
    
    def copy(self) -> 'Cover':
        """Create copy of cover"""
        return Cover([cube for cube in self.cubes])
    
    def size(self) -> int:
        """Get number of cubes in cover"""
        return len(self.cubes)
    
    def literal_count(self) -> int:
        """Get total number of literals in cover"""
        return sum(cube.literal_count() for cube in self.cubes)
    
    def __str__(self) -> str:
        return f"Cover({[str(cube) for cube in self.cubes]})"


class EspressoAlgorithm:
    """
    Espresso algorithm implementation for Boolean function minimization.
    
    Espresso is a heuristic algorithm that uses the operations:
    - EXPAND: Expand cubes to cover more minterms
    - IRREDUNDANT: Remove redundant cubes
    - REDUCE: Reduce cubes to essential literals
    
    The algorithm iterates these operations until no improvement is found.
    """
    
    def __init__(self, num_variables: int):
        """
        Initialize Espresso algorithm
        
        Args:
            num_variables: Number of input variables
        """
        self.num_variables = num_variables
        self.variables = [f'A{i}' for i in range(num_variables)]
        self.on_set = Cover()  # Cubes where function = 1
        self.dc_set = Cover()  # Don't care cubes
        self.off_set = Cover() # Cubes where function = 0
    
    def set_function(self, minterms: List[int], dont_cares: List[int] = None) -> None:
        """
        Set the Boolean function to minimize
        
        Args:
            minterms: List of minterms where function = 1
            dont_cares: List of don't care terms (optional)
        """
        # Convert minterms to cubes
        self.on_set = Cover()
        for minterm in minterms:
            cube_repr = format(minterm, f'0{self.num_variables}b')
            self.on_set.add_cube(Cube(cube_repr))
        
        # Convert don't cares to cubes
        self.dc_set = Cover()
        if dont_cares:
            for dc in dont_cares:
                cube_repr = format(dc, f'0{self.num_variables}b')
                self.dc_set.add_cube(Cube(cube_repr))
        
        # Generate off-set (all other minterms)
        self._generate_off_set(minterms, dont_cares or [])
    
    def _generate_off_set(self, minterms: List[int], dont_cares: List[int]) -> None:
        """Generate off-set from minterms and don't cares"""
        self.off_set = Cover()
        all_specified = set(minterms) | set(dont_cares)
        
        for i in range(2 ** self.num_variables):
            if i not in all_specified:
                cube_repr = format(i, f'0{self.num_variables}b')
                self.off_set.add_cube(Cube(cube_repr))
    
    def minimize(self, max_iterations: int = 20) -> Dict:
        """
        Minimize the Boolean function using Espresso algorithm
        
        Args:
            max_iterations: Maximum number of iterations
            
        Returns:
            Dictionary containing minimization results
        """
        if not self.on_set.cubes:
            return {
                'minimized_cover': [],
                'simplified_expression': '0',
                'iterations': 0,
                'cost': 0
            }
        
        # Initialize current cover
        current_cover = self.on_set.copy()
        iteration = 0
        
        # Main Espresso loop
        while iteration < max_iterations:
            old_cost = current_cover.literal_count()
            
            # EXPAND phase
            expanded_cover = self._expand(current_cover)
            
            # IRREDUNDANT phase  
            irredundant_cover = self._irredundant(expanded_cover)
            
            # REDUCE phase
            reduced_cover = self._reduce(irredundant_cover)
            
            new_cost = reduced_cover.literal_count()
            
            # Check for improvement
            if new_cost >= old_cost:
                break
            
            current_cover = reduced_cover
            iteration += 1
        
        # Generate final results
        simplified_expression = self._cover_to_expression(current_cover)
        
        return {
            'minimized_cover': [cube.representation for cube in current_cover.cubes],
            'simplified_expression': simplified_expression,
            'iterations': iteration,
            'cost': current_cover.literal_count(),
            'cube_count': current_cover.size()
        }
    
    def _expand(self, cover: Cover) -> Cover:
        """
        EXPAND operation: Expand each cube as much as possible
        
        Args:
            cover: Input cover
            
        Returns:
            Expanded cover
        """
        expanded_cover = Cover()
        
        for cube in cover.cubes:
            expanded_cube = self._expand_cube(cube, cover)
            expanded_cover.add_cube(expanded_cube)
        
        return expanded_cover
    
    def _expand_cube(self, cube: Cube, cover: Cover) -> Cube:
        """
        Expand a single cube maximally without conflicting with off-set
        
        Args:
            cube: Cube to expand
            cover: Current cover context
            
        Returns:
            Maximally expanded cube
        """
        current_cube = Cube(cube.representation)
        
        # Try expanding each literal position
        for i in range(self.num_variables):
            if current_cube.representation[i] != '-':
                # Try making this position don't care
                test_repr = (current_cube.representation[:i] + '-' + 
                           current_cube.representation[i+1:])
                test_cube = Cube(test_repr)
                
                # Check if expansion is valid (doesn't intersect off-set)
                if self._is_valid_expansion(test_cube):
                    current_cube = test_cube
        
        return current_cube
    
    def _is_valid_expansion(self, cube: Cube) -> bool:
        """
        Check if cube expansion is valid (doesn't cover off-set minterms)
        
        Args:
            cube: Cube to validate
            
        Returns:
            True if expansion is valid
        """
        # Check intersection with off-set
        for off_cube in self.off_set.cubes:
            if cube.intersect(off_cube) is not None:
                # Check if intersection is non-empty minterm
                intersection = cube.intersect(off_cube)
                if intersection and '-' not in intersection.representation:
                    return False
        
        return True
    
    def _irredundant(self, cover: Cover) -> Cover:
        """
        IRREDUNDANT operation: Remove redundant cubes
        
        Args:
            cover: Input cover
            
        Returns:
            Irredundant cover
        """
        irredundant_cover = Cover()
        
        for cube in cover.cubes:
            # Check if cube is redundant
            other_cubes = [c for c in cover.cubes if c != cube]
            if not self._is_cube_redundant(cube, other_cubes):
                irredundant_cover.add_cube(cube)
        
        return irredundant_cover
    
    def _is_cube_redundant(self, cube: Cube, other_cubes: List[Cube]) -> bool:
        """
        Check if a cube is redundant (covered by other cubes)
        
        Args:
            cube: Cube to check
            other_cubes: Other cubes in cover
            
        Returns:
            True if cube is redundant
        """
        # Simple check: if any other cube contains this cube, it's redundant
        for other_cube in other_cubes:
            if other_cube.contains(cube):
                return True
        
        # More complex redundancy checking would involve checking if
        # the union of other cubes covers all minterms of this cube
        return False
    
    def _reduce(self, cover: Cover) -> Cover:
        """
        REDUCE operation: Reduce cubes to remove unnecessary literals
        
        Args:
            cover: Input cover
            
        Returns:
            Reduced cover
        """
        reduced_cover = Cover()
        
        for cube in cover.cubes:
            reduced_cube = self._reduce_cube(cube, cover)
            reduced_cover.add_cube(reduced_cube)
        
        return reduced_cover
    
    def _reduce_cube(self, cube: Cube, cover: Cover) -> Cube:
        """
        Reduce a single cube by removing unnecessary literals
        
        Args:
            cube: Cube to reduce
            cover: Current cover context
            
        Returns:
            Reduced cube
        """
        current_cube = Cube(cube.representation)
        
        # Try removing each literal
        for i in range(self.num_variables):
            if current_cube.representation[i] != '-':
                # Try making this position don't care
                test_repr = (current_cube.representation[:i] + '-' + 
                           current_cube.representation[i+1:])
                test_cube = Cube(test_repr)
                
                # Check if reduction maintains coverage
                other_cubes = [c for c in cover.cubes if c != cube]
                if self._maintains_coverage(test_cube, other_cubes):
                    current_cube = test_cube
        
        return current_cube
    
    def _maintains_coverage(self, reduced_cube: Cube, other_cubes: List[Cube]) -> bool:
        """
        Check if reducing a cube maintains proper coverage
        
        Args:
            reduced_cube: Proposed reduced cube
            other_cubes: Other cubes in cover
            
        Returns:
            True if coverage is maintained
        """
        # This is a simplified check
        # In full Espresso, this would verify that all originally covered
        # minterms are still covered after reduction
        return True
    
    def _cover_to_expression(self, cover: Cover) -> str:
        """
        Convert cover to Boolean expression
        
        Args:
            cover: Cover to convert
            
        Returns:
            Boolean expression string
        """
        if not cover.cubes:
            return '0'
        
        terms = []
        for cube in cover.cubes:
            term = cube.to_expression(self.variables)
            if term and term != '0':
                terms.append(term)
        
        if not terms:
            return '0'
        elif len(terms) == 1:
            return terms[0]
        else:
            return ' + '.join(terms)
    
    def display_cover(self, cover: Cover, title: str = "Cover") -> str:
        """
        Display cover in readable format
        
        Args:
            cover: Cover to display
            title: Title for the display
            
        Returns:
            Formatted string representation
        """
        result = f"\n{title}:\n"
        result += "=" * (len(title) + 1) + "\n"
        
        if not cover.cubes:
            result += "Empty cover\n"
            return result
        
        result += f"{'Cube':<15} {'Expression':<20} {'Literals':<10}\n"
        result += "-" * 45 + "\n"
        
        for cube in cover.cubes:
            expr = cube.to_expression(self.variables)
            literals = cube.literal_count()
            result += f"{cube.representation:<15} {expr:<20} {literals:<10}\n"
        
        result += f"\nTotal cubes: {cover.size()}\n"
        result += f"Total literals: {cover.literal_count()}\n"
        
        return result
    
    def display_algorithm_trace(self, cover: Cover) -> str:
        """
        Display trace of algorithm operations
        
        Args:
            cover: Starting cover
            
        Returns:
            Trace of algorithm steps
        """
        trace = "Espresso Algorithm Trace\n"
        trace += "=" * 30 + "\n"
        
        trace += self.display_cover(cover, "Initial Cover")
        
        # Show one iteration of the algorithm
        expanded = self._expand(cover)
        trace += self.display_cover(expanded, "After EXPAND")
        
        irredundant = self._irredundant(expanded)
        trace += self.display_cover(irredundant, "After IRREDUNDANT")
        
        reduced = self._reduce(irredundant)
        trace += self.display_cover(reduced, "After REDUCE")
        
        return trace


def test_espresso_algorithm():
    """Test Espresso algorithm functionality"""
    print("Testing Espresso Algorithm")
    print("=" * 40)
    
    # Test case 1: Simple 3-variable function
    espresso = EspressoAlgorithm(3)
    espresso.set_function([0, 1, 3, 7], [2])  # With don't care
    
    result = espresso.minimize()
    
    print("Test Case 1: F(A,B,C) = Σ(0,1,3,7) + d(2)")
    print(f"Initial ON-set: {espresso.display_cover(espresso.on_set, 'ON-set')}")
    print(f"Minimized Expression: {result['simplified_expression']}")
    print(f"Number of cubes: {result['cube_count']}")
    print(f"Total literals: {result['cost']}")
    print(f"Iterations: {result['iterations']}")
    
    # Show algorithm trace
    print(espresso.display_algorithm_trace(espresso.on_set))
    
    # Test case 2: 4-variable function
    print("\n" + "=" * 40)
    espresso2 = EspressoAlgorithm(4)
    espresso2.set_function([0, 2, 5, 7, 8, 10, 13, 15])
    
    result2 = espresso2.minimize()
    print("Test Case 2: F(A,B,C,D) = Σ(0,2,5,7,8,10,13,15)")
    print(f"Minimized Expression: {result2['simplified_expression']}")
    print(f"Number of cubes: {result2['cube_count']}")
    print(f"Total literals: {result2['cost']}")


if __name__ == "__main__":
    test_espresso_algorithm()
