# Digital Logic Design - Combinational Circuit Algorithms

This package provides comprehensive implementations of fundamental algorithms for Boolean function optimization and combinational circuit design.

## 📋 Overview

The package includes 5 key algorithms used in digital logic design:

1. **Karnaugh Map (K-Map)** - Graphical Boolean expression simplification
2. **Quine-McCluskey Algorithm** - Systematic tabular minimization  
3. **Shannon Expansion** - Recursive Boolean function decomposition
4. **Espresso Algorithm** - Heuristic logic minimization (CAD tools)
5. **Multiplexer Design** - Hardware implementation using multiplexers

## 🚀 Quick Start

```python
from ALGO.combinational_circuits import *

# Example: Minimize a Boolean function using K-Map
kmap = KarnaughMap(3)  # 3 variables
kmap.set_function_from_minterms([1, 3, 5, 7])
result = kmap.minimize_expression()
print(f"Simplified: {result['simplified_expression']}")
```

## 📊 Algorithm Details

### 1. Karnaugh Map (K-Map)
**Purpose**: Visual method for Boolean expression simplification  
**Best for**: Manual design, learning, functions with ≤4 variables  
**Algorithm**: Groups adjacent 1s in a grid to identify prime implicants

```python
kmap = KarnaughMap(num_variables=4)
kmap.set_function_from_minterms([0, 1, 4, 5, 6, 7])
result = kmap.minimize_expression()
print(kmap.display_kmap())  # Visual representation
```

### 2. Quine-McCluskey Algorithm  
**Purpose**: Systematic minimization of Boolean functions  
**Best for**: Automated tools, guaranteed optimal results  
**Algorithm**: Tabular method finding all prime implicants then minimum cover

```python
qm = QuineMcCluskey(num_variables=4)
qm.set_function(minterms=[0, 1, 4, 5], dont_cares=[2, 3])
result = qm.minimize()
print(qm.display_coverage_table())
```

### 3. Shannon Expansion
**Purpose**: Recursive Boolean function decomposition  
**Best for**: Multiplexer implementations, hierarchical design  
**Algorithm**: f(x1,...,xn) = xi·f(...,1,...) + xi'·f(...,0,...)

```python
truth_table = [0, 1, 1, 0, 0, 1, 1, 1]  # 3-variable function
func = BooleanFunction(truth_table, num_variables=3)
shannon = ShannonExpansion(func)
tree = shannon.recursive_expansion()
print(shannon.display_expansion_tree())
```

### 4. Espresso Algorithm
**Purpose**: Heuristic logic minimization used in CAD tools  
**Best for**: Large functions, near-optimal results  
**Algorithm**: Iterative EXPAND-IRREDUNDANT-REDUCE operations

```python
espresso = EspressoAlgorithm(num_variables=4)
espresso.set_function([0, 2, 5, 7, 8, 10, 13, 15], [1, 6])
result = espresso.minimize(max_iterations=10)
print(f"Iterations: {result['iterations']}")
```

### 5. Multiplexer Design
**Purpose**: Implement Boolean functions using multiplexers  
**Best for**: Hardware implementation, structured design  
**Algorithm**: Shannon expansion or direct data input computation

```python
mux_design = MultiplexerDesign(num_variables=3)
mux_design.set_function(minterms=[1, 2, 4, 7])

# Single MUX implementation
single_mux = mux_design.design_single_mux(select_variables=[0])
print(mux_design.display_mux_implementation(single_mux))

# Tree implementation  
mux_tree = mux_design.design_mux_tree("shannon")
```

## 🎯 Use Cases & Applications

### Digital Circuit Design
- **Full Adders**: Optimize carry and sum logic
- **Decoders**: BCD to 7-segment display drivers
- **Encoders**: Priority encoders for interrupt systems
- **ALUs**: Arithmetic and logic unit optimization

### CAD Tool Development
- **Logic Synthesis**: Automated circuit optimization
- **Technology Mapping**: Map to specific gate libraries
- **Timing Optimization**: Critical path reduction

### Educational Applications
- **Learning**: Understand Boolean algebra concepts
- **Comparison**: See different optimization approaches
- **Verification**: Cross-check manual calculations

## 📈 Performance Comparison

| Algorithm | Optimality | Complexity | Best Use Case |
|-----------|------------|------------|---------------|
| K-Map | Optimal (small functions) | Low | Manual design, learning |
| Quine-McCluskey | Optimal | Medium | Systematic optimization |  
| Shannon Expansion | Structured | Medium | MUX implementations |
| Espresso | Near-optimal | High | CAD tools, large functions |
| MUX Design | Implementation-focused | Variable | Hardware realization |

## 🧪 Testing & Examples

Run the comprehensive test suite:
```bash
python ALGO/combinational_circuits/test_suite.py
```

Try the interactive demo:
```bash
python ALGO/demo.py
```

## 🔧 Implementation Features

### Karnaugh Map
- Support for 2-6 variables
- Visual K-map display
- Prime implicant identification
- Essential prime implicant detection

### Quine-McCluskey  
- Systematic prime implicant generation
- Coverage table analysis
- Don't care handling
- Minimum cover selection

### Shannon Expansion
- Recursive decomposition trees
- Multiplexer tree generation
- Complexity analysis
- Expression generation

### Espresso Algorithm
- Cube representation
- EXPAND/IRREDUNDANT/REDUCE operations
- Iterative improvement
- Cost optimization

### Multiplexer Design
- Single MUX implementations
- Shannon expansion trees
- Cost analysis
- Multiple implementation comparisons

## 📚 Educational Value

This package serves as:
- **Reference Implementation**: Clean, well-documented algorithms
- **Learning Tool**: Understand optimization techniques
- **Comparison Platform**: See trade-offs between methods
- **Research Base**: Foundation for advanced algorithms

## 🔬 Algorithm Complexity

| Algorithm | Time Complexity | Space Complexity | Scalability |
|-----------|----------------|------------------|-------------|
| K-Map | O(2^n) | O(2^n) | n ≤ 6 practical |
| Quine-McCluskey | O(3^n) | O(2^n) | n ≤ 8 practical |
| Shannon Expansion | O(2^n) | O(2^n) | n ≤ 10 practical |
| Espresso | O(iterations × cubes²) | O(cubes) | Large functions |
| MUX Design | O(2^n) | O(2^n) | Hardware dependent |

## 🎓 Learning Path

1. **Start with K-Maps**: Understand visual minimization
2. **Learn Quine-McCluskey**: Systematic approach
3. **Explore Shannon Expansion**: Decomposition concepts  
4. **Study Espresso**: Industrial-strength methods
5. **Apply MUX Design**: Hardware implementation

## 🔍 Example: Full Adder Sum Function

```python
# S = A ⊕ B ⊕ Cin (minterms: 1,2,4,7)
minterms = [1, 2, 4, 7]

# Compare all algorithms
kmap = KarnaughMap(3)
kmap.set_function_from_minterms(minterms)
print("K-Map:", kmap.minimize_expression()['simplified_expression'])

qm = QuineMcCluskey(3)  
qm.set_function(minterms)
print("QM:", qm.minimize()['simplified_expression'])

# Results show XOR pattern: A'B'Cin + A'BCin' + AB'Cin' + ABCin
```

## 🚀 Advanced Features

- **Don't Care Optimization**: Handle undefined inputs
- **Multiple Output Functions**: Optimize related functions together
- **Technology Mapping**: Map to specific gate libraries
- **Timing Constraints**: Consider propagation delays
- **Power Optimization**: Minimize switching activity

## 📖 References

1. Karnaugh, M. (1953). "The map method for synthesis of combinational logic circuits"
2. Quine, W.V. (1952). "The problem of simplifying truth functions"  
3. McCluskey, E.J. (1956). "Minimization of Boolean functions"
4. Shannon, C.E. (1948). "A mathematical theory of communication"
5. Brayton, R.K. et al. (1984). "Logic Minimization Algorithms for VLSI Synthesis"

This implementation provides a solid foundation for understanding and applying Boolean function optimization in digital logic design.
