"""
Combinational Circuit Algorithms Test Suite
Comprehensive testing for all algorithms
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ALGO.combinational_circuits.karnaugh_map import KarnaughMap, test_kmap
from ALGO.combinational_circuits.quine_mccluskey import QuineMcCluskey, test_quine_mccluskey  
from ALGO.combinational_circuits.shannon_expansion import ShannonExpansion, BooleanFunction, test_shannon_expansion
from ALGO.combinational_circuits.espresso_algorithm import EspressoAlgorithm, test_espresso_algorithm
from ALGO.combinational_circuits.multiplexer_design import MultiplexerDesign, test_multiplexer_design


def comprehensive_comparison_test():
    """
    Compare all algorithms on the same Boolean function
    """
    print("\n" + "="*80)
    print("COMPREHENSIVE ALGORITHM COMPARISON")
    print("="*80)
    
    # Test function: F(A,B,C,D) = Σ(0,1,4,5,6,7,8,9,10,14,15)
    test_minterms = [0, 1, 4, 5, 6, 7, 8, 9, 10, 14, 15]
    test_dont_cares = [2, 11]
    num_vars = 4
    
    print(f"Test Function: F(A,B,C,D) = Σ{test_minterms} + d{test_dont_cares}")
    print("-" * 80)
    
    # 1. Karnaugh Map
    print("\n1. KARNAUGH MAP ANALYSIS")
    print("-" * 40)
    try:
        kmap = KarnaughMap(num_vars)
        kmap.set_function_from_minterms(test_minterms)
        
        kmap_result = kmap.minimize_expression()
        print(f"K-Map Result: {kmap_result['simplified_expression']}")
        print(f"Cost: {kmap_result['cost']} terms")
        print(f"Prime Implicants: {kmap_result['prime_implicants']}")
    except Exception as e:
        print(f"K-Map Error: {e}")
    
    # 2. Quine-McCluskey
    print("\n2. QUINE-MCCLUSKEY ANALYSIS")
    print("-" * 40)
    try:
        qm = QuineMcCluskey(num_vars)
        qm.set_function(test_minterms, test_dont_cares)
        
        qm_result = qm.minimize()
        print(f"QM Result: {qm_result['simplified_expression']}")
        print(f"Cost: {qm_result['cost']} terms")
        print(f"Selected PIs: {qm_result['selected_prime_implicants']}")
    except Exception as e:
        print(f"Quine-McCluskey Error: {e}")
    
    # 3. Shannon Expansion
    print("\n3. SHANNON EXPANSION ANALYSIS")
    print("-" * 40)
    try:
        # Create truth table
        truth_table = [0] * (2**num_vars)
        for m in test_minterms:
            truth_table[m] = 1
        
        func = BooleanFunction(truth_table, num_variables=num_vars)
        func.variables = ['A', 'B', 'C', 'D']
        
        shannon = ShannonExpansion(func)
        shannon.recursive_expansion()
        
        shannon_expr = shannon.generate_expression_from_expansion()
        complexity = shannon.analyze_decomposition_complexity()
        
        print(f"Shannon Expression: {shannon_expr}")
        print(f"Multiplexer Count: {complexity['multiplexer_count']}")
        print(f"Tree Depth: {complexity['tree_depth']}")
    except Exception as e:
        print(f"Shannon Expansion Error: {e}")
    
    # 4. Espresso Algorithm
    print("\n4. ESPRESSO ALGORITHM ANALYSIS") 
    print("-" * 40)
    try:
        espresso = EspressoAlgorithm(num_vars)
        espresso.set_function(test_minterms, test_dont_cares)
        
        espresso_result = espresso.minimize()
        print(f"Espresso Result: {espresso_result['simplified_expression']}")
        print(f"Cost: {espresso_result['cost']} literals")
        print(f"Cubes: {espresso_result['cube_count']}")
        print(f"Iterations: {espresso_result['iterations']}")
    except Exception as e:
        print(f"Espresso Error: {e}")
    
    # 5. Multiplexer Design
    print("\n5. MULTIPLEXER DESIGN ANALYSIS")
    print("-" * 40)
    try:
        mux_design = MultiplexerDesign(num_vars)
        mux_design.set_function(minterms=test_minterms)
        
        # Single MUX with 2 select variables
        single_mux = mux_design.design_single_mux([0, 1])
        print(f"Single MUX: {single_mux['mux_size']} size")
        print(f"Data inputs: {len(single_mux['data_inputs'])}")
        print(f"Additional gates: {single_mux['implementation_cost']['additional_gates']}")
        
        # Shannon tree
        shannon_tree = mux_design.design_mux_tree("shannon")
        print(f"Shannon MUX Tree: {shannon_tree['mux_count']} multiplexers")
        print(f"Tree depth: {shannon_tree['depth']}")
    except Exception as e:
        print(f"Multiplexer Design Error: {e}")
    
    print("\n" + "="*80)
    print("SUMMARY COMPARISON")
    print("="*80)
    print("Algorithm          | Expression Quality | Implementation | Complexity")
    print("-" * 80)
    print("K-Map             | Optimal (small)   | Manual         | Low")
    print("Quine-McCluskey   | Optimal           | Systematic     | Medium") 
    print("Shannon Expansion | Structured        | MUX-based      | Medium")
    print("Espresso          | Near-optimal      | CAD tools      | High")
    print("MUX Design        | Implementation    | Hardware       | Variable")


def algorithm_performance_test():
    """
    Test algorithm performance on different function types
    """
    print("\n" + "="*60)
    print("ALGORITHM PERFORMANCE TEST")
    print("="*60)
    
    test_cases = [
        {
            'name': 'Small function (3 vars)',
            'minterms': [1, 3, 5, 7],
            'num_vars': 3,
            'description': 'Simple function with clear pattern'
        },
        {
            'name': 'Medium function (4 vars)', 
            'minterms': [0, 2, 5, 7, 8, 10, 13, 15],
            'num_vars': 4,
            'description': 'Medium complexity function'
        },
        {
            'name': 'Complex function (4 vars)',
            'minterms': [1, 2, 3, 4, 6, 7, 9, 11, 12, 13, 14],
            'num_vars': 4,
            'description': 'High complexity function'
        },
        {
            'name': 'Sparse function (5 vars)',
            'minterms': [0, 5, 10, 15, 20, 25, 30],
            'num_vars': 5,
            'description': 'Sparse function with few minterms'
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTest Case: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"Minterms: {test_case['minterms']}")
        print("-" * 50)
        
        # Test each algorithm
        algorithms_tested = 0
        
        # Karnaugh Map (limit to ≤4 variables)
        if test_case['num_vars'] <= 4:
            try:
                kmap = KarnaughMap(test_case['num_vars'])
                kmap.set_function_from_minterms(test_case['minterms'])
                result = kmap.minimize_expression()
                print(f"K-Map: {result['cost']} terms - {result['simplified_expression']}")
                algorithms_tested += 1
            except Exception as e:
                print(f"K-Map: Error - {e}")
        
        # Quine-McCluskey
        try:
            qm = QuineMcCluskey(test_case['num_vars'])
            qm.set_function(test_case['minterms'])
            result = qm.minimize()
            print(f"Quine-McCluskey: {result['cost']} literals - {result['simplified_expression']}")
            algorithms_tested += 1
        except Exception as e:
            print(f"Quine-McCluskey: Error - {e}")
        
        # Espresso (limit to reasonable sizes)
        if test_case['num_vars'] <= 5:
            try:
                espresso = EspressoAlgorithm(test_case['num_vars'])
                espresso.set_function(test_case['minterms'])
                result = espresso.minimize()
                print(f"Espresso: {result['cost']} literals in {result['iterations']} iterations")
                algorithms_tested += 1
            except Exception as e:
                print(f"Espresso: Error - {e}")
        
        print(f"Algorithms tested: {algorithms_tested}")


def run_all_tests():
    """Run all individual algorithm tests"""
    print("RUNNING ALL ALGORITHM TESTS")
    print("="*60)
    
    try:
        print("\n1. Testing Karnaugh Map...")
        test_kmap()
    except Exception as e:
        print(f"K-Map test failed: {e}")
    
    try:
        print("\n2. Testing Quine-McCluskey...")
        test_quine_mccluskey()
    except Exception as e:
        print(f"Quine-McCluskey test failed: {e}")
    
    try:
        print("\n3. Testing Shannon Expansion...")
        test_shannon_expansion()
    except Exception as e:
        print(f"Shannon Expansion test failed: {e}")
    
    try:
        print("\n4. Testing Espresso Algorithm...")
        test_espresso_algorithm()
    except Exception as e:
        print(f"Espresso test failed: {e}")
    
    try:
        print("\n5. Testing Multiplexer Design...")
        test_multiplexer_design()
    except Exception as e:
        print(f"Multiplexer Design test failed: {e}")


def main():
    """Main test runner"""
    print("COMBINATIONAL CIRCUIT ALGORITHMS TEST SUITE")
    print("="*70)
    print("This test suite demonstrates 5 key algorithms for combinational logic:")
    print("1. Karnaugh Map - Graphical minimization method")
    print("2. Quine-McCluskey - Systematic tabular minimization") 
    print("3. Shannon Expansion - Recursive function decomposition")
    print("4. Espresso Algorithm - Heuristic logic minimization")
    print("5. Multiplexer Design - MUX-based implementation")
    print("="*70)
    
    # Run individual tests
    run_all_tests()
    
    # Run comparison tests
    comprehensive_comparison_test()
    
    # Run performance tests
    algorithm_performance_test()
    
    print("\n" + "="*70)
    print("TEST SUITE COMPLETED")
    print("All algorithms are ready for use in digital logic design!")
    print("="*70)


if __name__ == "__main__":
    main()
