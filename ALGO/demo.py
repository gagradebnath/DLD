"""
Digital Logic Design - Combinational Circuit Algorithms Demo
Interactive demonstration of Boolean function minimization algorithms
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from combinational_circuits.karnaugh_map import KarnaughMap
from combinational_circuits.quine_mccluskey import QuineMcCluskey  
from combinational_circuits.shannon_expansion import ShannonExpansion, BooleanFunction
from combinational_circuits.espresso_algorithm import EspressoAlgorithm
from combinational_circuits.multiplexer_design import MultiplexerDesign


def display_banner():
    """Display welcome banner"""
    print("="*80)
    print("     DIGITAL LOGIC DESIGN - COMBINATIONAL CIRCUIT ALGORITHMS")
    print("="*80)
    print("This demo showcases 5 fundamental algorithms for Boolean function optimization:")
    print("1. Karnaugh Map (K-Map) - Graphical simplification method")
    print("2. Quine-McCluskey - Systematic tabular minimization")
    print("3. Shannon Expansion - Recursive function decomposition")
    print("4. Espresso Algorithm - Heuristic logic minimization (CAD tools)")
    print("5. Multiplexer Design - Hardware implementation using MUXes")
    print("="*80)


def demo_function_analysis():
    """Demonstrate comprehensive analysis of a Boolean function"""
    print("\n🔍 COMPREHENSIVE FUNCTION ANALYSIS")
    print("-" * 50)
    
    # Example function: Full Adder Sum output
    print("Example: Full Adder Sum Function")
    print("S = A ⊕ B ⊕ Cin")
    print("Truth Table Analysis for S(A,B,Cin)")
    
    # Minterms where Sum = 1: (1,2,4,7) 
    minterms = [1, 2, 4, 7]
    num_vars = 3
    variables = ['A', 'B', 'Cin']
    
    print(f"Minterms: Σ{minterms}")
    print(f"Variables: {variables}")
    
    # 1. Karnaugh Map Analysis
    print("\n📊 1. KARNAUGH MAP ANALYSIS")
    try:
        kmap = KarnaughMap(num_vars)
        kmap.variables = variables
        kmap.set_function_from_minterms(minterms)
        
        print(kmap.display_kmap())
        
        print("Finding prime implicants...")
        result = kmap.minimize_expression()
        print(f"✅ Simplified Expression: {result['simplified_expression']}")
        print(f"   Prime Implicants: {result['prime_implicants']}")
        print(f"   Cost: {result['cost']} terms")
        
    except Exception as e:
        print(f"❌ K-Map Error: {e}")
        import traceback
        traceback.print_exc()
    
    # 2. Quine-McCluskey Analysis
    print("\n📋 2. QUINE-MCCLUSKEY ANALYSIS")
    try:
        qm = QuineMcCluskey(num_vars)
        qm.variables = variables
        qm.set_function(minterms)
        
        result = qm.minimize()
        print(f"✅ Minimized Expression: {result['simplified_expression']}")
        print(f"   Selected Prime Implicants: {result['selected_prime_implicants']}")
        print(f"   Total Cost: {result['cost']} literals")
        
        print(qm.display_prime_implicant_table())
        
    except Exception as e:
        print(f"❌ Quine-McCluskey Error: {e}")
    
    # 3. Shannon Expansion Analysis
    print("\n🌳 3. SHANNON EXPANSION ANALYSIS")
    try:
        # Create truth table
        truth_table = [0] * 8
        for m in minterms:
            truth_table[m] = 1
        
        func = BooleanFunction(truth_table, num_variables=num_vars)
        func.variables = variables
        
        shannon = ShannonExpansion(func)
        shannon.recursive_expansion()
        
        print("Shannon Expansion Tree:")
        print(shannon.display_expansion_tree())
        
        expression = shannon.generate_expression_from_expansion()
        print(f"✅ Shannon Expression: {expression}")
        
        complexity = shannon.analyze_decomposition_complexity()
        print(f"   Tree Complexity: {complexity['multiplexer_count']} MUXes, depth {complexity['tree_depth']}")
        
    except Exception as e:
        print(f"❌ Shannon Expansion Error: {e}")
    
    # 4. Multiplexer Implementation
    print("\n🔌 4. MULTIPLEXER IMPLEMENTATION")
    try:
        mux_design = MultiplexerDesign(num_vars)
        mux_design.variables = variables
        mux_design.set_function(minterms=minterms)
        
        # Single MUX implementation
        single_mux = mux_design.design_single_mux([0])  # Use A as select
        print("Single Multiplexer Implementation:")
        print(mux_design.display_mux_implementation(single_mux))
        
        # Shannon tree implementation
        shannon_tree = mux_design.design_mux_tree("shannon")
        print("Shannon MUX Tree Implementation:")
        print(mux_design.display_mux_implementation(shannon_tree))
        
    except Exception as e:
        print(f"❌ Multiplexer Design Error: {e}")


def demo_algorithm_comparison():
    """Compare algorithms on various function types"""
    print("\n⚖️  ALGORITHM COMPARISON")
    print("-" * 50)
    
    test_functions = [
        {
            'name': 'XOR Function',
            'minterms': [1, 2],
            'num_vars': 2,
            'description': 'Simple 2-input XOR'
        },
        {
            'name': 'Majority Function',
            'minterms': [3, 5, 6, 7],
            'num_vars': 3,
            'description': '3-input majority gate'
        },
        {
            'name': 'Parity Function',
            'minterms': [1, 2, 4, 7],
            'num_vars': 3,
            'description': '3-input even parity'
        }
    ]
    
    for func_info in test_functions:
        print(f"\n🧪 Testing: {func_info['name']}")
        print(f"   Description: {func_info['description']}")
        print(f"   Minterms: Σ{func_info['minterms']}")
        
        # Test K-Map
        try:
            kmap = KarnaughMap(func_info['num_vars'])
            kmap.set_function_from_minterms(func_info['minterms'])
            result = kmap.minimize_expression()
            print(f"   K-Map: {result['simplified_expression']} ({result['cost']} terms)")
        except:
            print(f"   K-Map: Error")
        
        # Test Quine-McCluskey
        try:
            qm = QuineMcCluskey(func_info['num_vars'])
            qm.set_function(func_info['minterms'])
            result = qm.minimize()
            print(f"   QM: {result['simplified_expression']} ({result['cost']} literals)")
        except:
            print(f"   QM: Error")
        
        # Test Multiplexer Design
        try:
            mux = MultiplexerDesign(func_info['num_vars'])
            mux.set_function(minterms=func_info['minterms'])
            single = mux.design_single_mux([0])
            print(f"   MUX: {single['mux_size']} + {single['implementation_cost']['additional_gates']} gates")
        except:
            print(f"   MUX: Error")


def interactive_demo():
    """Interactive demonstration allowing user input"""
    print("\n🎮 INTERACTIVE DEMO")
    print("-" * 50)
    print("Enter your own Boolean function to analyze!")
    
    try:
        # Get user input
        num_vars = int(input("Number of variables (2-4): "))
        if num_vars < 2 or num_vars > 4:
            print("❌ Please enter 2-4 variables")
            return
        
        print(f"Enter minterms for {num_vars} variables (0 to {2**num_vars-1}):")
        minterms_input = input("Minterms (comma-separated): ")
        minterms = [int(x.strip()) for x in minterms_input.split(',') if x.strip().isdigit()]
        
        if not minterms:
            print("❌ No valid minterms entered")
            return
        
        print(f"\n🔬 Analyzing function with {num_vars} variables and minterms {minterms}")
        
        # Analyze with available algorithms
        print("\n📊 Results:")
        
        # K-Map
        try:
            kmap = KarnaughMap(num_vars)
            kmap.set_function_from_minterms(minterms)
            result = kmap.minimize_expression()
            print(f"K-Map: {result['simplified_expression']}")
        except Exception as e:
            print(f"K-Map: Error - {e}")
        
        # Quine-McCluskey
        try:
            qm = QuineMcCluskey(num_vars)
            qm.set_function(minterms)
            result = qm.minimize()
            print(f"Quine-McCluskey: {result['simplified_expression']}")
        except Exception as e:
            print(f"Quine-McCluskey: Error - {e}")
        
        # Multiplexer
        try:
            mux = MultiplexerDesign(num_vars)
            mux.set_function(minterms=minterms)
            single = mux.design_single_mux([0])
            print(f"MUX Implementation: {single['mux_size']} multiplexer")
        except Exception as e:
            print(f"MUX Design: Error - {e}")
            
    except ValueError:
        print("❌ Invalid input format")
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled by user")


def demo_applications():
    """Demonstrate practical applications"""
    print("\n🏭 PRACTICAL APPLICATIONS")
    print("-" * 50)
    
    applications = [
        {
            'name': 'Adder Circuit Design',
            'description': 'Full adder carry output optimization',
            'minterms': [3, 5, 6, 7],  # Cout = AB + ACin + BCin
            'num_vars': 3,
            'use_case': 'Arithmetic Logic Units (ALUs)'
        },
        {
            'name': 'BCD to 7-Segment Decoder',
            'description': 'Display driver optimization (segment a)',
            'minterms': [0, 2, 3, 5, 6, 7, 8, 9],
            'num_vars': 4,
            'use_case': 'Digital displays and calculators'
        },
        {
            'name': 'Priority Encoder',
            'description': '4-to-2 priority encoder high bit',
            'minterms': [4, 5, 6, 7],
            'num_vars': 4,
            'use_case': 'Interrupt controllers and data selectors'
        }
    ]
    
    for app in applications:
        print(f"\n🎯 {app['name']}")
        print(f"   Use Case: {app['use_case']}")
        print(f"   Function: {app['description']}")
        print(f"   Minterms: Σ{app['minterms']}")
        
        # Quick optimization comparison
        try:
            # K-Map
            kmap = KarnaughMap(app['num_vars'])
            kmap.set_function_from_minterms(app['minterms'])
            kmap_result = kmap.minimize_expression()
            
            # Quine-McCluskey
            qm = QuineMcCluskey(app['num_vars'])
            qm.set_function(app['minterms'])
            qm_result = qm.minimize()
            
            print(f"   Optimized: {kmap_result['simplified_expression']}")
            print(f"   Cost: {kmap_result['cost']} terms, {qm_result['cost']} literals")
            
        except Exception as e:
            print(f"   Analysis Error: {e}")


def main():
    """Main demo program"""
    display_banner()
    
    print("\n🚀 Starting Combinational Circuit Algorithms Demo...")
    
    # Core demonstrations
    demo_function_analysis()
    demo_algorithm_comparison()
    demo_applications()
    
    # Interactive session
    print("\n" + "="*80)
    response = input("Would you like to try the interactive demo? (y/n): ")
    if response.lower().startswith('y'):
        interactive_demo()
    
    # Conclusion
    print("\n" + "="*80)
    print("🎉 DEMO COMPLETED!")
    print("="*80)
    print("Key Takeaways:")
    print("• K-Maps: Best for manual design and learning (≤4 variables)")
    print("• Quine-McCluskey: Systematic and optimal for medium functions")
    print("• Shannon Expansion: Excellent for multiplexer implementations")
    print("• Espresso: Industry standard for CAD tools")
    print("• MUX Design: Practical hardware implementation method")
    print("\nThese algorithms form the foundation of modern digital logic design!")
    print("="*80)


if __name__ == "__main__":
    main()
