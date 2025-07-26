"""
Advanced IC Demonstration - 7400 Series Data Processing ICs
Digital Logic Design Library

This demonstration showcases the advanced data processing capabilities
of the 7400 series TTL ICs including encoders, decoders, and multiplexers.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from IC.ic_74138 import IC74138
from IC.ic_74139 import IC74139
from IC.ic_74147 import IC74147
from IC.ic_74148 import IC74148
from IC.ic_74150 import IC74150
from IC.ic_74151 import IC74151
from IC.ic_74153 import IC74153
from IC.ic_74157 import IC74157

def test_decoders():
    """Test decoder ICs"""
    print("=" * 60)
    print("DECODER ICs DEMONSTRATION")
    print("=" * 60)
    
    # Test 74138 (3-to-8 Decoder)
    print("\n74138 - 3-to-8 Line Decoder/Demultiplexer")
    print("-" * 45)
    ic138 = IC74138()
    ic138.connect_power()
    
    # Demonstrate address decoding
    print("Address Decoding Example:")
    for addr in range(8):
        a2 = (addr >> 2) & 1
        a1 = (addr >> 1) & 1
        a0 = addr & 1
        outputs = ic138.decode(a2, a1, a0, e1=0, e2=0, e3=1)
        active_output = outputs.index(0) if 0 in outputs else -1
        print(f"Address {addr} (binary {addr:03b}): Output Y{active_output} active")
    
    # Test 74139 (Dual 2-to-4 Decoder)
    print("\n74139 - Dual 2-to-4 Line Decoder/Demultiplexer")
    print("-" * 48)
    ic139 = IC74139()
    ic139.connect_power()
    
    # Demonstrate dual operation
    print("Dual Decoder Example:")
    for addr in range(4):
        a1 = (addr >> 1) & 1
        a0 = addr & 1
        outputs1 = ic139.decode_1(a1, a0, enable=0)
        outputs2 = ic139.decode_2(a1, a0, enable=0)
        active1 = outputs1.index(0) if 0 in outputs1 else -1
        active2 = outputs2.index(0) if 0 in outputs2 else -1
        print(f"Address {addr}: Decoder1 Y{active1}, Decoder2 Y{active2}")

def test_encoders():
    """Test encoder ICs"""
    print("\n" + "=" * 60)
    print("ENCODER ICs DEMONSTRATION")
    print("=" * 60)
    
    # Test 74147 (10-to-4 Priority Encoder)
    print("\n74147 - 10-to-4 Line Priority Encoder (Decimal to BCD)")
    print("-" * 57)
    ic147 = IC74147()
    ic147.connect_power()
    
    # Demonstrate priority encoding
    print("Priority Encoding Example (highest priority wins):")
    print("Note: 74147 uses active-low inputs and outputs")
    test_cases = [
        ({i: 1 for i in range(10)}, "No inputs active"),  # All high = no inputs
        ({0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, "Input 1 active"),  # Only 0 is low
        ({0: 1, 1: 1, 2: 1, 3: 1, 4: 0, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, "Input 4 active"),  # Only 4 is low
        ({0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, "Inputs 1-4 active"),  # 0-3 are low
        ({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 1}, "Inputs 1-9 active"),  # 0-8 low
        ({0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 0}, "Input 9 active (highest)")  # Only 9 low
    ]
    
    for inputs, description in test_cases:
        bcd_output = ic147.encode_decimal(inputs)
        decimal_value = ic147.get_bcd_output()
        print(f"{description:25}: BCD {bcd_output} -> decimal {decimal_value}")
    
    # Test 74148 (8-to-3 Priority Encoder)
    print("\n74148 - 8-to-3 Line Priority Encoder with Cascade")
    print("-" * 50)
    ic148 = IC74148()
    ic148.connect_power()
    
    # Demonstrate cascade features
    print("Priority Encoding with Cascade Control:")
    test_inputs = [
        ({i: 1 for i in range(8)}, "No inputs active"),  # All high
        ({0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, "Input 0 active"),  # Only 0 low
        ({0: 1, 1: 1, 2: 1, 3: 0, 4: 1, 5: 1, 6: 1, 7: 1}, "Input 3 active"),  # Only 3 low
        ({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 1}, "Inputs 0-6 active"),  # 0-6 low
        ({0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0}, "Input 7 active (highest)")  # Only 7 low
    ]
    
    for inputs, description in test_inputs:
        result = ic148.encode_inputs(inputs, enable_input=0)
        a2, a1, a0, gs, eo = result
        output_code = [a2, a1, a0]
        print(f"{description:25}: Code {output_code}, GS={gs}, EO={eo}")

def test_multiplexers():
    """Test multiplexer ICs"""
    print("\n" + "=" * 60)
    print("MULTIPLEXER ICs DEMONSTRATION")
    print("=" * 60)
    
    # Test 74150 (16-to-1 Multiplexer)
    print("\n74150 - 16-to-1 Line Data Selector/Multiplexer")
    print("-" * 48)
    ic150 = IC74150()
    ic150.connect_power()
    
    # Create a lookup table
    fibonacci = [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1]  # Fibonacci mod 2
    print("16-bit Fibonacci sequence (mod 2) lookup:")
    print(f"Data: {fibonacci}")
    
    # Test some selections
    test_addresses = [0, 3, 7, 12, 15]
    for addr in test_addresses:
        output = ic150.select_input(addr, fibonacci)
        original = fibonacci[addr]
        print(f"Address {addr:2d}: Input={original}, Output={output} (inverted)")
    
    # Test 74151 (8-to-1 Multiplexer)
    print("\n74151 - 8-to-1 Line Data Selector/Multiplexer")
    print("-" * 46)
    ic151 = IC74151()
    ic151.connect_power()
    
    # Demonstrate complementary outputs
    test_data = [1, 0, 1, 1, 0, 1, 0, 0]
    print(f"Test data: {test_data}")
    print("Address | Input | Y | W (inverted)")
    print("-" * 32)
    
    for addr in range(8):
        y_output, w_output = ic151.select_input(addr, test_data)
        print(f"   {addr}    |   {test_data[addr]}   | {y_output} | {w_output}")
    
    # Test 74153 (Dual 4-to-1 Multiplexer)
    print("\n74153 - Dual 4-to-1 Line Data Selector/Multiplexer")
    print("-" * 50)
    ic153 = IC74153()
    ic153.connect_power()
    
    # Demonstrate parallel processing
    word1 = [1, 0, 1, 1]  # 4-bit word 1
    word2 = [0, 1, 0, 1]  # 4-bit word 2
    print(f"Word 1: {word1}")
    print(f"Word 2: {word2}")
    print("Select | Output 1 | Output 2")
    print("-" * 25)
    
    for select in range(4):
        outputs = ic153.select_input(select, word1, word2)
        print(f"   {select}   |    {outputs[0]}     |    {outputs[1]}")
    
    # Test 74157 (Quad 2-to-1 Multiplexer)
    print("\n74157 - Quad 2-to-1 Line Data Selector/Multiplexer")
    print("-" * 50)
    ic157 = IC74157()
    ic157.connect_power()
    
    # Demonstrate 4-bit bus switching
    bus_a = [1, 0, 1, 0]  # Bus A data
    bus_b = [0, 1, 1, 1]  # Bus B data
    print(f"Bus A: {bus_a}")
    print(f"Bus B: {bus_b}")
    print(f"Select A: {ic157.select_a_inputs(bus_a)}")
    print(f"Select B: {ic157.select_b_inputs(bus_b)}")

def practical_applications():
    """Demonstrate practical applications"""
    print("\n" + "=" * 60)
    print("PRACTICAL APPLICATIONS")
    print("=" * 60)
    
    # Address Decoder for Memory System
    print("\n1. Memory Address Decoder (74138)")
    print("-" * 35)
    ic138 = IC74138()
    ic138.connect_power()
    
    print("8-bank memory system:")
    memory_banks = ["RAM", "ROM", "I/O", "Graphics", "Sound", "Network", "Storage", "Reserved"]
    
    for bank in range(8):
        a2 = (bank >> 2) & 1
        a1 = (bank >> 1) & 1
        a0 = bank & 1
        outputs = ic138.decode(a2, a1, a0, e1=0, e2=0, e3=1)
        selected = outputs.index(0)
        print(f"Address A2A1A0 = {bank:03b}: Select {memory_banks[selected]} bank")
    
    # Data Router using Multiplexers
    print("\n2. 4-bit Data Router (74153)")
    print("-" * 30)
    ic153 = IC74153()
    ic153.connect_power()
    
    # Route data from 4 different sources
    cpu_data = [1, 1, 0, 1]
    dma_data = [0, 1, 1, 0]
    timer_data = [1, 0, 1, 1]
    uart_data = [0, 0, 1, 0]
    
    data_sources = [cpu_data, dma_data, timer_data, uart_data]
    source_names = ["CPU", "DMA", "Timer", "UART"]
    
    print("Data routing example:")
    for i, (data, name) in enumerate(zip(data_sources[:4], source_names)):
        # Use two 74153 ICs to handle 4 data sources
        if i < 2:  # First two sources
            outputs = ic153.select_input(i, data_sources[0], data_sources[1])
            if i == 0:
                print(f"Route {name:5} data {data}: Output {list(outputs)}")
        else:  # Would need second IC for sources 2-3
            print(f"Route {name:5} data {data}: (would use second 74153)")
    
    # Priority Interrupt Controller
    print("\n3. Priority Interrupt Controller (74148)")
    print("-" * 40)
    ic148 = IC74148()
    ic148.connect_power()
    
    # Simulate interrupt requests (active-low: 0 = IRQ active, 1 = IRQ inactive)
    interrupts = [
        ([1, 1, 1, 1, 1, 1, 1, 1], "No interrupts"),              # All inactive (high)
        ([0, 1, 1, 1, 1, 1, 1, 1], "Keyboard (IRQ0)"),            # Only IRQ0 active (low)
        ([1, 0, 1, 1, 1, 1, 1, 1], "Timer (IRQ1)"),               # Only IRQ1 active (low)
        ([0, 0, 1, 1, 1, 1, 1, 1], "Keyboard + Timer"),           # IRQ0 and IRQ1 both active
        ([1, 1, 1, 1, 1, 1, 0, 1], "Hard Disk (IRQ6)"),           # Only IRQ6 active (low)
        ([0, 0, 0, 0, 0, 0, 0, 0], "Multiple interrupts"),        # All active - highest wins
    ]
    
    irq_names = ["Keyboard", "Timer", "Serial", "Network", "Mouse", "Sound", "HDD", "NMI"]
    
    print("Interrupt priority handling:")
    for irq_pattern, description in interrupts:
        result = ic148.encode_inputs({i: irq_pattern[i] for i in range(len(irq_pattern))}, enable_input=0)
        a2, a1, a0, gs, eo = result
        output_code = [a2, a1, a0]
        
        if gs == 0:  # Group select active (interrupt present)
            # The output code is inverted (active-low), so invert to get true binary value
            irq_number = (1-a2)*4 + (1-a1)*2 + (1-a0)*1
            irq_name = irq_names[irq_number] if irq_number < 8 else "Unknown"
            print(f"{description:20}: Highest priority IRQ{irq_number} ({irq_name})")
        else:
            print(f"{description:20}: No active interrupts")

def test_all_advanced_ics():
    """Run comprehensive test of all advanced ICs"""
    print("=" * 70)
    print("COMPREHENSIVE TEST OF ADVANCED 7400 SERIES ICs")
    print("=" * 70)
    
    ics = [
        (IC74138, "74138 - 3-to-8 Decoder"),
        (IC74139, "74139 - Dual 2-to-4 Decoder"),
        (IC74147, "74147 - 10-to-4 Priority Encoder"),
        (IC74148, "74148 - 8-to-3 Priority Encoder"),
        (IC74150, "74150 - 16-to-1 Multiplexer"),
        (IC74151, "74151 - 8-to-1 Multiplexer"),
        (IC74153, "74153 - Dual 4-to-1 Multiplexer"),
        (IC74157, "74157 - Quad 2-to-1 Multiplexer")
    ]
    
    results = []
    
    for ic_class, name in ics:
        try:
            ic = ic_class()
            ic.connect_power()
            result = ic.test_ic()
            status = "✅ PASS" if result else "❌ FAIL"
            results.append((name, status, result))
            print(f"{name:35}: {status}")
        except Exception as e:
            status = f"❌ ERROR - {str(e)}"
            results.append((name, status, False))
            print(f"{name:35}: {status}")
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, _, result in results if result)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 ALL ADVANCED ICs PASS TESTING!")
    else:
        print("⚠️  Some ICs need attention")
        failed = [name for name, _, result in results if not result]
        print(f"Failed ICs: {', '.join(failed)}")

def main():
    """Main demonstration program"""
    print("🔌 ADVANCED 7400 SERIES IC DEMONSTRATION")
    print("Digital Logic Design - Data Processing ICs")
    print("=" * 70)
    
    try:
        # Run comprehensive tests first
        test_all_advanced_ics()
        
        # Detailed demonstrations
        test_decoders()
        test_encoders()
        test_multiplexers()
        practical_applications()
        
        print("\n" + "=" * 70)
        print("✅ DEMONSTRATION COMPLETE")
        print("=" * 70)
        print("All advanced ICs are ready for use in digital logic designs!")
        print("These ICs provide the building blocks for:")
        print("• Memory address decoding")
        print("• Data routing and selection")
        print("• Priority encoding systems")
        print("• Interrupt controllers")
        print("• Bus multiplexing")
        print("• Digital signal processing")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
