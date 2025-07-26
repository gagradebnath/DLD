# Digital Logic Design IC Library

## 7400-Series TTL Integrated Circuits

This library provides a comprehensive collection of 7400-series TTL (Transistor-Transistor Logic) integrated circuits implemented in Python. Each IC simulates the authentic behavior of its physical counterpart, including active-low signaling, proper timing characteristics, and DIP package pinouts.

## Table of Contents

- [Overview](#overview)
- [Basic Logic Gates](#basic-logic-gates)
- [Advanced Data Processing ICs](#advanced-data-processing-ics)
- [Installation and Usage](#installation-and-usage)
- [Quick Reference](#quick-reference)
- [Examples](#examples)

---

## Overview

### IC Categories

The library contains **17 integrated circuits** organized into four categories:

1. **Logic Gates (9 ICs)**: Basic boolean operations
2. **Decoders (2 ICs)**: Address-to-output selection
3. **Encoders (2 ICs)**: Priority input encoding
4. **Multiplexers (4 ICs)**: Data selection and routing

### Common Features

- **Authentic TTL Behavior**: Active-low signaling where appropriate
- **Power Management**: All ICs require `connect_power()` before use
- **DIP Package Simulation**: Accurate pin numbering and layouts
- **Built-in Testing**: Each IC includes comprehensive self-test methods
- **Error Handling**: Robust validation and error reporting

---

## Basic Logic Gates

### IC7400 - Quad 2-Input NAND Gate

**Package**: 14-pin DIP  
**Function**: Four independent 2-input NAND gates

```python
from IC.ic_7400 import IC7400

# Create and power the IC
nand_ic = IC7400()
nand_ic.connect_power()

# Use specific gate method (preferred)
result = nand_ic.gate_a(1, 0)  # Gate A: NAND(1,0) = 1
result = nand_ic.gate_b(1, 1)  # Gate B: NAND(1,1) = 0
result = nand_ic.gate_c(0, 0)  # Gate C: NAND(0,0) = 1
result = nand_ic.gate_d(0, 1)  # Gate D: NAND(0,1) = 1

# Alternative: Use get_gate_output method
result = nand_ic.get_gate_output(1, 1, 0)  # Gate 1: NAND(1,0) = 1

# Test the IC
if nand_ic.test_ic():
    print("IC7400 is working correctly")
```

**Gate Methods**:
- `gate_a(a, b)` - Gate A (pins 1,2 → 3)
- `gate_b(a, b)` - Gate B (pins 4,5 → 6)  
- `gate_c(a, b)` - Gate C (pins 9,10 → 8)
- `gate_d(a, b)` - Gate D (pins 12,13 → 11)

**Truth Table (per gate)**:
| A | B | Output |
|---|---|--------|
| 0 | 0 |   1    |
| 0 | 1 |   1    |
| 1 | 0 |   1    |
| 1 | 1 |   0    |

### IC7402 - Quad 2-Input NOR Gate

**Package**: 14-pin DIP  
**Function**: Four independent 2-input NOR gates

```python
from IC.ic_7402 import IC7402

nor_ic = IC7402()
nor_ic.connect_power()

# Gate A (pins 2,3 → 1)
result = nor_ic.gate_a(0, 0)  # NOR(0,0) = 1

# Gate B (pins 5,6 → 4)
result = nor_ic.gate_b(1, 0)  # NOR(1,0) = 0

# Gate C (pins 8,9 → 10)
result = nor_ic.gate_c(0, 1)  # NOR(0,1) = 0

# Gate D (pins 11,12 → 13)
result = nor_ic.gate_d(1, 1)  # NOR(1,1) = 0
```
### IC7404 - Hex Inverter

**Package**: 14-pin DIP  
**Function**: Six independent NOT gates

```python
from IC.ic_7404 import IC7404

not_ic = IC7404()
not_ic.connect_power()

# Use each inverter
result = not_ic.gate_a(1)  # Pin 1 → 2, Returns 0
result = not_ic.gate_b(0)  # Pin 3 → 4, Returns 1
result = not_ic.gate_c(1)  # Pin 5 → 6, Returns 0
result = not_ic.gate_d(0)  # Pin 9 → 8, Returns 1
result = not_ic.gate_e(1)  # Pin 11 → 10, Returns 0
result = not_ic.gate_f(0)  # Pin 13 → 12, Returns 1
```

### IC7408 - Quad 2-Input AND Gate

**Package**: 14-pin DIP  
**Function**: Four independent 2-input AND gates

```python
from IC.ic_7408 import IC7408

and_ic = IC7408()
and_ic.connect_power()

# Gate A (pins 1,2 → 3)
result = and_ic.gate_a(1, 1)  # AND(1,1) = 1

# Gate B (pins 4,5 → 6)
result = and_ic.gate_b(1, 0)  # AND(1,0) = 0

# Gate C (pins 9,10 → 8)
result = and_ic.gate_c(0, 1)  # AND(0,1) = 0

# Gate D (pins 12,13 → 11)
result = and_ic.gate_d(0, 0)  # AND(0,0) = 0
```

### IC7410 - Triple 3-Input NAND Gate

**Package**: 14-pin DIP  
**Function**: Three independent 3-input NAND gates

```python
from IC.ic_7410 import IC7410

nand3_ic = IC7410()
nand3_ic.connect_power()

# Gate A (pins 1,2,13 → 12)
result = nand3_ic.gate_a(1, 1, 1)  # NAND(1,1,1) = 0

# Gate B (pins 3,4,5 → 6)
result = nand3_ic.gate_b(1, 0, 1)  # NAND(1,0,1) = 1

# Gate C (pins 9,10,11 → 8)
result = nand3_ic.gate_c(0, 0, 0)  # NAND(0,0,0) = 1
```

### IC7420 - Dual 4-Input NAND Gate

**Package**: 14-pin DIP  
**Function**: Two independent 4-input NAND gates

```python
from IC.ic_7420 import IC7420

nand4_ic = IC7420()
nand4_ic.connect_power()

# Gate A (pins 1,2,4,5 → 6)
result = nand4_ic.gate_a(1, 1, 1, 1)  # NAND(1,1,1,1) = 0

# Gate B (pins 9,10,12,13 → 8)
result = nand4_ic.gate_b(1, 0, 1, 1)  # NAND(1,0,1,1) = 1
```

### IC7430 - Single 8-Input NAND Gate

**Package**: 14-pin DIP  
**Function**: One 8-input NAND gate

```python
from IC.ic_7430 import IC7430

nand8_ic = IC7430()
nand8_ic.connect_power()

# Single gate (pins 1,2,3,4,5,6,11,12 → 8)
result = nand8_ic.gate(1, 1, 1, 1, 1, 1, 1, 1)  # NAND all 1s = 0
result = nand8_ic.gate(1, 1, 1, 1, 1, 1, 1, 0)  # NAND with one 0 = 1
```

### IC7432 - Quad 2-Input OR Gate

**Package**: 14-pin DIP  
**Function**: Four independent 2-input OR gates

```python
from IC.ic_7432 import IC7432

or_ic = IC7432()
or_ic.connect_power()

# Gate A (pins 1,2 → 3)
result = or_ic.gate_a(0, 0)  # OR(0,0) = 0

# Gate B (pins 4,5 → 6)
result = or_ic.gate_b(1, 0)  # OR(1,0) = 1

# Gate C (pins 9,10 → 8)
result = or_ic.gate_c(0, 1)  # OR(0,1) = 1

# Gate D (pins 12,13 → 11)
result = or_ic.gate_d(1, 1)  # OR(1,1) = 1
```

### IC7486 - Quad 2-Input XOR Gate

**Package**: 14-pin DIP  
**Function**: Four independent 2-input XOR gates

```python
from IC.ic_7486 import IC7486

xor_ic = IC7486()
xor_ic.connect_power()

# Gate A (pins 1,2 → 3)
result = xor_ic.gate_a(0, 0)  # XOR(0,0) = 0

# Gate B (pins 4,5 → 6)
result = xor_ic.gate_b(1, 0)  # XOR(1,0) = 1

# Gate C (pins 9,10 → 8)
result = xor_ic.gate_c(0, 1)  # XOR(0,1) = 1

# Gate D (pins 12,13 → 11)
result = xor_ic.gate_d(1, 1)  # XOR(1,1) = 0
```

---

## Advanced Data Processing ICs

### Decoders

#### IC74138 - 3-to-8 Line Decoder/Demultiplexer

**Package**: 16-pin DIP  
**Function**: Decodes 3-bit address to select one of 8 outputs (active-low)

```python
from IC.ic_74138 import IC74138

decoder = IC74138()
decoder.connect_power()

# Decode address 5 (binary 101)
# E1=0, E2=0, E3=1 (enable), A2=1, A1=0, A0=1
outputs = decoder.decode(a2=1, a1=0, a0=1, e1=0, e2=0, e3=1)
# Returns: [1, 1, 1, 1, 1, 0, 1, 1] (Y5 is active/low)

# Memory address decoding example
memory_banks = ["RAM", "ROM", "I/O", "Graphics", "Sound", "Network", "Storage", "Reserved"]
for addr in range(8):
    a2 = (addr >> 2) & 1
    a1 = (addr >> 1) & 1
    a0 = addr & 1
    outputs = decoder.decode(a2, a1, a0, e1=0, e2=0, e3=1)
    selected_bank = outputs.index(0)  # Find active output
    print(f"Address {addr:03b}: Select {memory_banks[selected_bank]}")

# Check which output is selected
selected = decoder.get_selected_output()  # Returns output number (0-7) or None

# Use as demultiplexer
outputs = decoder.demultiplex(data_input=1, a2=1, a1=0, a0=1)  # Route data to Y5
```

**Enable Truth Table**:
| E1 | E2 | E3 | Operation |
|----|----|----|-----------|
| 0  | 0  | 1  | Decode    |
| 1  | X  | X  | Disabled  |
| X  | 1  | X  | Disabled  |
| X  | X  | 0  | Disabled  |

#### IC74139 - Dual 2-to-4 Line Decoder/Demultiplexer

**Package**: 16-pin DIP  
**Function**: Two independent 2-to-4 decoders (active-low outputs)

```python
from IC.ic_74139 import IC74139

dual_decoder = IC74139()
dual_decoder.connect_power()

# Decoder 1: Select address 2 (binary 10)
outputs1 = dual_decoder.decode_1(a1=1, a0=0, enable=0)
# Returns: [1, 1, 0, 1] (Y2 is active/low)

# Decoder 2: Select address 1 (binary 01)
outputs2 = dual_decoder.decode_2(a1=0, a0=1, enable=0)
# Returns: [1, 0, 1, 1] (Y1 is active/low)

# Chip select logic example
chip_enables = dual_decoder.decode_1(a1=1, a0=1, enable=0)  # Enable chip 3
peripheral_enables = dual_decoder.decode_2(a1=0, a0=0, enable=0)  # Enable peripheral 0

# Get selected outputs
selected1 = dual_decoder.get_selected_output_1()  # Returns 0-3 or None
selected2 = dual_decoder.get_selected_output_2()  # Returns 0-3 or None
```

### Encoders

#### IC74147 - 10-to-4 Line Priority Encoder (Decimal to BCD)

**Package**: 16-pin DIP  
**Function**: Encodes highest priority active input (0-9) to 4-bit BCD (active-low)

```python
from IC.ic_74147 import IC74147

encoder = IC74147()
encoder.connect_power()

# Single input active (input 7) - note: inputs are active-low
inputs = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0, 8: 1, 9: 1}
bcd_output = encoder.encode_decimal(inputs)
# Returns: [1, 0, 0, 0] (inverted BCD for 7)

decimal_value = encoder.get_bcd_output()
# Returns: 7

# Multiple inputs active (priority encoding - highest wins)
inputs = {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 0}
bcd_output = encoder.encode_decimal(inputs)
decimal_value = encoder.get_bcd_output()
# Returns: 9 (highest priority active input)

# Keypad encoder example
keypad_inputs = {0: 1, 1: 1, 2: 1, 3: 0, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}
if encoder.encode_decimal(keypad_inputs):
    pressed_key = encoder.get_bcd_output()
    print(f"Key {pressed_key} pressed")

# Check if any input is active
is_active = encoder.is_any_input_active()  # Returns True/False
```

**Input Priority** (highest to lowest): 9, 8, 7, 6, 5, 4, 3, 2, 1, 0  
**Note**: All inputs and outputs are active-low

#### IC74148 - 8-to-3 Line Priority Encoder with Cascade

**Package**: 16-pin DIP  
**Function**: Encodes highest priority active input (0-7) to 3-bit binary with cascade capability

```python
from IC.ic_74148 import IC74148

priority_encoder = IC74148()
priority_encoder.connect_power()

# Single interrupt active (IRQ 5) - inputs are active-low
irq_inputs = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 0, 6: 1, 7: 1}
a2, a1, a0, gs, eo = priority_encoder.encode_inputs(irq_inputs, enable_input=0)
# Returns: (0, 1, 0, 0, 1) - Binary 5 inverted, GS active, EO inactive

# Convert inverted output to binary
irq_number = (1-a2)*4 + (1-a1)*2 + (1-a0)*1  # = 5

# Multiple interrupts (priority system)
irq_inputs = {0: 0, 1: 0, 2: 1, 3: 0, 4: 1, 5: 1, 6: 1, 7: 0}
a2, a1, a0, gs, eo = priority_encoder.encode_inputs(irq_inputs, enable_input=0)
highest_irq = (1-a2)*4 + (1-a1)*2 + (1-a0)*1  # = 7 (highest priority)

# Interrupt controller example
irq_names = ["Timer", "Keyboard", "Serial", "Network", "Mouse", "Sound", "Disk", "NMI"]
if gs == 0:  # Group select active (interrupt present)
    print(f"Interrupt: {irq_names[highest_irq]}")

# Get highest priority input directly
highest = priority_encoder.get_highest_priority_input()  # Returns 0-7 or None
```

**Cascade Signals**:
- **GS** (Group Select): 0 = valid input present, 1 = no inputs
- **EO** (Enable Output): 0 = enable next stage, 1 = disable next stage  
**Input Priority** (highest to lowest): 7, 6, 5, 4, 3, 2, 1, 0

### Multiplexers

#### IC74150 - 16-to-1 Line Data Selector/Multiplexer

**Package**: 24-pin DIP  
**Function**: Selects one of 16 inputs based on 4-bit address (inverted output)

```python
from IC.ic_74150 import IC74150

mux16 = IC74150()
mux16.connect_power()

# Create 16-bit lookup table
data = [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1]

# Select input 10 (address 1010)
output = mux16.select_input(address=10, data_inputs=data)
# Returns: 0 (inverted from input value 1)

# ROM/EPROM emulation
program_memory = [0x00, 0xFF, 0xA5, 0x5A, 0x33, 0xCC, 0xF0, 0x0F,
                  0x11, 0x22, 0x44, 0x88, 0x01, 0x02, 0x04, 0x08]

for address in range(16):
    data_out = mux16.select_input(address, program_memory)
    original = program_memory[address]
    print(f"Address 0x{address:X}: Data 0x{original:02X} -> Output {data_out} (inverted)")

# Function generator with enable control
sine_table = [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0]  # Approximate sine
for phase in range(16):
    sine_out = mux16.select_input(phase, sine_table, enable=0)  # Enable active-low
    print(f"Phase {phase}: Sine = {1-sine_out}")  # Invert for true output

# Check if enabled
enabled = mux16.is_enabled()  # Returns True/False
```

**Note**: Output is inverted (active-low), enable is active-low

#### IC74151 - 8-to-1 Line Data Selector/Multiplexer

**Package**: 16-pin DIP  
**Function**: Selects one of 8 inputs with complementary outputs (Y and W)

```python
from IC.ic_74151 import IC74151

mux8 = IC74151()
mux8.connect_power()

# 8-bit data
data = [1, 0, 1, 1, 0, 1, 0, 0]

# Select input 3 with enable (active-low)
y_output, w_output = mux8.select_input(3, data, enable=0)
# Returns: (1, 0) - Y = data[3], W = NOT(data[3])

# Function implementation using multiplexer
# Implement f(A,B,C) = ABC + A'BC + AB'C + ABC'
truth_table = [0, 0, 1, 1, 1, 1, 1, 1]  # Truth table for function

for a in [0, 1]:
    for b in [0, 1]:
        for c in [0, 1]:
            address = a*4 + b*2 + c  # 3-bit address
            y, w = mux8.select_input(address, truth_table)
            print(f"f({a},{b},{c}) = {y}")

# Data routing with strobe
data_bus = [1, 0, 1, 0, 1, 1, 0, 1]
select_lines = 5  # Binary 101
y, w = mux8.route_data(select_lines, data_bus, strobe=0)  # Strobe enable
print(f"Selected data: {y}, Inverted: {w}")

# Get currently selected input number
selected = mux8.get_selected_input()  # Returns 0-7 or None if disabled
```

#### IC74153 - Dual 4-to-1 Line Data Selector/Multiplexer

**Package**: 16-pin DIP  
**Function**: Two independent 4-to-1 multiplexers with shared select lines

```python
from IC.ic_74153 import IC74153

dual_mux = IC74153()
dual_mux.connect_power()

# 4-bit data words
word1 = [1, 0, 1, 1]  # First 4-to-1 mux
word2 = [0, 1, 0, 1]  # Second 4-to-1 mux

# Select input 2 for both multiplexers
outputs = dual_mux.select_input(select=2, data1=word1, data2=word2)
# Returns: [1, 0] - word1[2] and word2[2]

# Parallel data processing
for select in range(4):
    out1, out2 = dual_mux.select_input(select, word1, word2)
    print(f"Select {select}: MUX1={out1}, MUX2={out2}")

# ALU data path selection
alu_result = [1, 1, 0, 0]    # ALU operation results
memory_data = [0, 1, 1, 0]   # Memory read data

operation_select = 1  # Select ALU result
cpu_data, mem_data = dual_mux.select_input(operation_select, alu_result, memory_data)
print(f"CPU gets: {cpu_data}, Memory interface: {mem_data}")

# Individual enable control
outputs = dual_mux.multiplex_both(word1, word2, select=3, enable1=0, enable2=1)
# MUX1 enabled, MUX2 disabled (returns [selected_value, 0])

# Get current selections
sel1, sel2 = dual_mux.get_selected_inputs()  # Returns selected input numbers
```

#### IC74157 - Quad 2-to-1 Line Data Selector/Multiplexer

**Package**: 16-pin DIP  
**Function**: Four independent 2-to-1 multiplexers (4-bit bus switching)

```python
from IC.ic_74157 import IC74157

quad_mux = IC74157()
quad_mux.connect_power()

# Two 4-bit data buses
bus_a = [1, 0, 1, 0]  # Bus A
bus_b = [0, 1, 1, 1]  # Bus B

# Select Bus A (select = 0) with enable
output = quad_mux.route_inputs(bus_a, bus_b, select=0, enable=0)
# Returns: [1, 0, 1, 0] (Bus A selected)

# Select Bus B (select = 1)
output = quad_mux.route_inputs(bus_a, bus_b, select=1, enable=0)
# Returns: [0, 1, 1, 1] (Bus B selected)

# CPU/DMA bus switching
cpu_bus = [1, 1, 0, 1]
dma_bus = [0, 0, 1, 0]

# CPU mode (DMA_REQUEST = 0)
system_bus = quad_mux.multiplex(cpu_bus, dma_bus, select=0, enable=0)
print(f"CPU mode: System bus = {system_bus}")

# DMA mode (DMA_REQUEST = 1)
system_bus = quad_mux.multiplex(cpu_bus, dma_bus, select=1, enable=0)
print(f"DMA mode: System bus = {system_bus}")

# Individual bus selection methods
selected_a = quad_mux.select_a_inputs(bus_a)  # Always select A inputs
selected_b = quad_mux.select_b_inputs(bus_b)  # Always select B inputs

# Parallel switching with enable
output = quad_mux.parallel_switch(bus_a, bus_b, select=1, enable=0)

# Get current state
is_a_selected = quad_mux.is_a_selected()  # Returns True if A inputs selected
is_enabled = quad_mux.is_enabled()        # Returns True if IC is enabled
```

---

## Installation and Usage

### Basic Setup

```python
# Import required modules
import sys
import os
sys.path.append(os.path.dirname(__file__))

# Import specific ICs
from IC.ic_7400 import IC7400
from IC.ic_74138 import IC74138
from IC.ic_74151 import IC74151

# Create IC instances
nand_gates = IC7400()
decoder = IC74138()
multiplexer = IC74151()

# Always connect power before use
nand_gates.connect_power()
decoder.connect_power()
multiplexer.connect_power()

# Use the ICs with correct method names
result = nand_gates.gate_a(1, 0)                        # Individual gate method
outputs = decoder.decode(1, 0, 1, 0, 0, 1)             # Main functionality method
y_out, w_out = multiplexer.select_input(3, [1,0,1,1,0,1,0,0])  # Returns tuple
```

### Running Demonstrations

```python
# Run the comprehensive advanced IC demo
python advanced_ic_demo.py

# Run the IC test suite
from IC.ic_test_suite import ICTestSuite

# Create test suite instance
suite = ICTestSuite()

# Test all ICs
all_passed = suite.test_all_ics()

# Interactive mode
suite.interactive_mode()

# Demonstrate specific IC
suite.demonstrate_ic('7400')
```

### Testing Individual ICs

```python
# Test individual IC
ic = IC7400()
ic.connect_power()

if ic.test_ic():
    print("IC is functioning correctly")
else:
    print("IC has failed self-test")

# Test all ICs in a design
ics = [IC7400(), IC74138(), IC74151()]
for ic in ics:
    ic.connect_power()
    status = "PASS" if ic.test_ic() else "FAIL"
    print(f"{ic.__class__.__name__}: {status}")

# Get truth table and pinout information
print(ic.get_truth_table())
print(ic.get_pinout_diagram())
```

---

## Quick Reference

### Logic Gate ICs

| IC    | Function | Gates | Inputs | Package | Method Names |
|-------|----------|-------|---------|---------|--------------|
| 7400  | NAND     | 4     | 2      | 14-pin  | gate_a/b/c/d(a,b) |
| 7402  | NOR      | 4     | 2      | 14-pin  | gate_a/b/c/d(a,b) |
| 7404  | NOT      | 6     | 1      | 14-pin  | gate_a/b/c/d/e/f(a) |
| 7408  | AND      | 4     | 2      | 14-pin  | gate_a/b/c/d(a,b) |
| 7410  | NAND     | 3     | 3      | 14-pin  | gate_a/b/c(a,b,c) |
| 7420  | NAND     | 2     | 4      | 14-pin  | gate_a/b(a,b,c,d) |
| 7430  | NAND     | 1     | 8      | 14-pin  | gate(a,b,c,d,e,f,g,h) |
| 7432  | OR       | 4     | 2      | 14-pin  | gate_a/b/c/d(a,b) |
| 7486  | XOR      | 4     | 2      | 14-pin  | gate_a/b/c/d(a,b) |

### Advanced Data Processing ICs

| IC     | Function | Method Names | Key Features |
|--------|----------|--------------|--------------|
| 74138  | 3-8 Decoder | decode(a2,a1,a0,e1,e2,e3) | Active-low outputs |
| 74139  | Dual 2-4 Decoder | decode_1/2(a1,a0,enable) | Independent decoders |
| 74147  | 10-4 Encoder | encode_decimal(inputs) | Priority, BCD output |
| 74148  | 8-3 Encoder | encode_inputs(inputs,enable) | Cascade capability |
| 74150  | 16-1 Mux | select_input(addr,data) | Inverted output |
| 74151  | 8-1 Mux | select_input(addr,data,enable) | Complementary outputs |
| 74153  | Dual 4-1 Mux | select_input(sel,data1,data2) | Shared select lines |
| 74157  | Quad 2-1 Mux | route_inputs(a,b,sel,en) | 4-bit bus switching |

### Common Method Patterns

**Logic Gates:**
- `gate_a(input1, input2)` - Individual gate methods
- `get_gate_output(gate_num, input1, input2)` - Generic gate access
- `test_ic()` - Comprehensive testing
- `get_truth_table()` - Generate truth table

**Advanced ICs:**
- Main function methods: `decode()`, `encode_decimal()`, `select_input()`
- Helper methods: `get_selected_output()`, `is_enabled()`
- Status methods: `is_any_input_active()`, `get_highest_priority_input()`

### Pin Numbering Convention

All ICs follow standard DIP (Dual In-line Package) pinout:
- **14-pin**: Pins 1-7 (left side), 8-14 (right side)
- **16-pin**: Pins 1-8 (left side), 9-16 (right side)  
- **24-pin**: Pins 1-12 (left side), 13-24 (right side)
- **Power**: VCC (top-right), GND (bottom-left)

### Active-Low Signals

Many 7400 series ICs use active-low signaling:
- **74138**: All outputs are active-low (0 = selected)
- **74139**: All outputs are active-low (0 = selected)
- **74147**: Inputs and outputs are active-low (0 = active)
- **74148**: Inputs and outputs are active-low (0 = active)
- **74150**: Enable is active-low, output is inverted
- **74151**: Enable is active-low
- **74157**: Enable is active-low

---

## Examples

### Building a 4-bit ALU

```python
from IC.ic_7400 import IC7400
from IC.ic_7432 import IC7432
from IC.ic_7486 import IC7486
from IC.ic_74157 import IC74157

class Simple4BitALU:
    def __init__(self):
        self.nand_gates = IC7400()
        self.or_gates = IC7432()
        self.xor_gates = IC7486()
        self.mux = IC74157()
        
        # Power up all ICs
        for ic in [self.nand_gates, self.or_gates, self.xor_gates, self.mux]:
            ic.connect_power()
    
    def compute(self, a, b, operation):
        """
        operation: 0=AND, 1=OR, 2=XOR, 3=NAND
        """
        results = []
        
        for i in range(4):
            # AND: double NAND (NAND the result of NAND)
            nand1 = self.nand_gates.gate_a(a[i], b[i])
            and_bit = self.nand_gates.gate_b(nand1, nand1)
            
            # OR: direct operation
            or_bit = self.or_gates.gate_a(a[i], b[i])
            
            # XOR: direct operation
            xor_bit = self.xor_gates.gate_a(a[i], b[i])
            
            # NAND: direct operation
            nand_bit = self.nand_gates.gate_c(a[i], b[i])
            
            # Store all operation results
            ops = [and_bit, or_bit, xor_bit, nand_bit]
            results.append(ops[operation])
        
        return results

# Usage
alu = Simple4BitALU()
a = [1, 0, 1, 1]  # 4-bit input A
b = [0, 1, 1, 0]  # 4-bit input B

result = alu.compute(a, b, operation=2)  # XOR operation
print(f"A = {a}")
print(f"B = {b}")
print(f"A XOR B = {result}")
```

### Memory Address Decoder

```python
from IC.ic_74138 import IC74138
from IC.ic_74139 import IC74139

class MemoryDecoder:
    def __init__(self):
        self.main_decoder = IC74138()      # 8 main blocks
        self.sub_decoder = IC74139()       # 4 sub-blocks each
        
        self.main_decoder.connect_power()
        self.sub_decoder.connect_power()
        
        self.memory_map = {
            0: "System ROM",
            1: "User RAM", 
            2: "Video RAM",
            3: "I/O Ports",
            4: "Expansion 1",
            5: "Expansion 2",
            6: "Network",
            7: "Reserved"
        }
    
    def decode_address(self, address):
        """
        Decode 6-bit address: AAAAAA (A5 A4 A3 A2 A1 A0)
        """
        # Main decoder uses A5, A4, A3
        main_addr = (address >> 3) & 0x7
        a2 = (main_addr >> 2) & 1
        a1 = (main_addr >> 1) & 1
        a0 = main_addr & 1
        
        main_outputs = self.main_decoder.decode(a2, a1, a0, e1=0, e2=0, e3=1)
        main_select = main_outputs.index(0)  # Find active output
        
        # Sub decoder uses A2, A1
        sub_addr = (address >> 1) & 0x3
        s1 = (sub_addr >> 1) & 1
        s0 = sub_addr & 1
        
        sub_outputs = self.sub_decoder.decode_1(s1, s0, enable=0)
        sub_select = sub_outputs.index(0)  # Find active output
        
        return {
            'main_block': main_select,
            'main_name': self.memory_map[main_select],
            'sub_block': sub_select,
            'byte_select': address & 1,
            'full_address': f"0x{address:02X}"
        }

# Usage
decoder = MemoryDecoder()

test_addresses = [0x00, 0x0F, 0x1A, 0x2C, 0x3F]
for addr in test_addresses:
    result = decoder.decode_address(addr)
    print(f"Address {result['full_address']}: {result['main_name']}, "
          f"Sub-block {result['sub_block']}, "
          f"Byte {result['byte_select']}")
```

### Interrupt Priority Controller

```python
from IC.ic_74148 import IC74148

class InterruptController:
    def __init__(self):
        self.encoder = IC74148()
        self.encoder.connect_power()
        
        self.irq_names = [
            "Timer",       # IRQ0
            "Keyboard",    # IRQ1
            "Serial Port", # IRQ2
            "Network",     # IRQ3
            "Mouse",       # IRQ4
            "Sound",       # IRQ5
            "Disk Drive",  # IRQ6
            "NMI"          # IRQ7 (highest priority)
        ]
    
    def check_interrupts(self, irq_lines):
        """
        Check for active interrupts and return highest priority
        irq_lines: dict with IRQ number as key, state as value
        (0 = active interrupt, 1 = no interrupt) - active low
        """
        a2, a1, a0, gs, eo = self.encoder.encode_inputs(irq_lines, enable_input=0)
        
        if gs == 0:  # Group select active (valid interrupt present)
            # Convert inverted output to IRQ number
            irq_number = (1-a2)*4 + (1-a1)*2 + (1-a0)*1
            return irq_number, self.irq_names[irq_number]
        else:
            return None, "No interrupts"
    
    def handle_interrupt_scenario(self, scenario_name, irq_lines):
        irq_num, irq_name = self.check_interrupts(irq_lines)
        if irq_num is not None:
            print(f"{scenario_name}: Handling {irq_name} (IRQ{irq_num})")
        else:
            print(f"{scenario_name}: {irq_name}")
        return irq_num

# Usage
controller = InterruptController()

# Simulate various interrupt scenarios (0 = interrupt active, 1 = inactive)
scenarios = [
    ("No interrupts", {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}),
    ("Timer only", {0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}),
    ("Timer + Keyboard", {0: 0, 1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}),
    ("Multiple IRQs", {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}),
    ("NMI only", {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0}),
]

print("Interrupt Priority Controller Demo:")
print("=" * 40)
for scenario_name, irq_pattern in scenarios:
    controller.handle_interrupt_scenario(scenario_name, irq_pattern)
```

### Data Routing System

```python
from IC.ic_74151 import IC74151
from IC.ic_74153 import IC74153
from IC.ic_74157 import IC74157

class DataRouter:
    def __init__(self):
        self.mux8 = IC74151()    # 8-to-1 multiplexer
        self.dual_mux = IC74153() # Dual 4-to-1 multiplexer
        self.quad_mux = IC74157() # Quad 2-to-1 multiplexer
        
        # Power up all ICs
        for ic in [self.mux8, self.dual_mux, self.quad_mux]:
            ic.connect_power()
    
    def route_8_channels(self, data_sources, channel_select):
        """Route one of 8 data sources to output"""
        y, w = self.mux8.select_input(channel_select, data_sources, enable=0)
        return y, w  # y = selected data, w = inverted
    
    def route_dual_4_channels(self, data1, data2, select):
        """Route parallel 4-bit data streams"""
        return self.dual_mux.select_input(select, data1, data2)
    
    def switch_buses(self, bus_a, bus_b, select_b):
        """Switch between two 4-bit buses"""
        return self.quad_mux.route_inputs(bus_a, bus_b, select=select_b, enable=0)

# Usage
router = DataRouter()

# Example 1: CPU data source selection
print("Example 1: CPU Data Source Selection")
print("=" * 35)
data_sources = [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0]
source_names = ["Register A", "Register B", "Memory", "ALU", "Immediate", "Stack", "I/O", "Cache"]

for i in range(8):
    selected, inverted = router.route_8_channels(data_sources, i)
    print(f"Select {i} ({source_names[i]}): Data=0x{data_sources[i]:02X}, Output={selected}")

# Example 2: Parallel data processing
print("\nExample 2: Parallel Data Processing")
print("=" * 35)
stream1 = [1, 0, 1, 1]  # First data stream
stream2 = [0, 1, 0, 1]  # Second data stream

for sel in range(4):
    out1, out2 = router.route_dual_4_channels(stream1, stream2, sel)
    print(f"Select {sel}: Stream1[{sel}]={out1}, Stream2[{sel}]={out2}")

# Example 3: Bus switching (CPU vs DMA)
print("\nExample 3: Bus Switching (CPU vs DMA)")
print("=" * 35)
cpu_bus = [1, 1, 0, 1]   # CPU data bus
dma_bus = [0, 0, 1, 0]   # DMA data bus

print("CPU mode (select=0):", router.switch_buses(cpu_bus, dma_bus, select_b=0))
print("DMA mode (select=1):", router.switch_buses(cpu_bus, dma_bus, select_b=1))
```

### Function Generator Using Multiplexers

```python
from IC.ic_74150 import IC74150

class FunctionGenerator:
    def __init__(self):
        self.mux = IC74150()
        self.mux.connect_power()
    
    def generate_waveform(self, lookup_table, phase):
        """Generate waveform using 16-point lookup table"""
        return self.mux.select_input(phase, lookup_table)
    
    def create_sine_wave(self, steps=16):
        """Create approximated sine wave lookup table"""
        import math
        sine_table = []
        for i in range(steps):
            angle = 2 * math.pi * i / steps
            value = 1 if math.sin(angle) >= 0 else 0
            sine_table.append(value)
        return sine_table
    
    def create_triangle_wave(self, steps=16):
        """Create triangle wave lookup table"""
        triangle = []
        half = steps // 2
        for i in range(steps):
            if i < half:
                value = 1 if i % 2 == 0 else 0
            else:
                value = 1 if (steps - i) % 2 == 0 else 0
            triangle.append(value)
        return triangle

# Usage
generator = FunctionGenerator()

# Generate different waveforms
print("Function Generator Demo")
print("=" * 25)

# Sine wave approximation
sine_table = [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0]
print("Sine Wave (16 steps):")
for phase in range(16):
    output = generator.generate_waveform(sine_table, phase)
    # Note: 74150 output is inverted
    actual_value = 1 - output
    print(f"Phase {phase:2d}: {actual_value}")

# Square wave
square_table = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
print("\nSquare Wave (50% duty cycle):")
for phase in range(0, 16, 2):  # Sample every other phase
    output = generator.generate_waveform(square_table, phase)
    actual_value = 1 - output  # Invert for true output
    print(f"Phase {phase:2d}: {actual_value}")
```

### Running the Complete Demo

```python
# To run the comprehensive demonstration
if __name__ == "__main__":
    print("🔌 7400 SERIES IC LIBRARY DEMONSTRATION")
    print("=" * 50)
    
    # Import the main demo
    import advanced_ic_demo
    
    # Run the complete demonstration
    advanced_ic_demo.main()
    
    # Or run individual components
    print("\n" + "="*50)
    print("INDIVIDUAL COMPONENT TESTS")
    print("="*50)
    
    # Test basic gates
    from IC.ic_test_suite import ICTestSuite
    suite = ICTestSuite()
    suite.test_all_ics()
    
    # Interactive mode
    print("\nEntering interactive mode...")
    suite.interactive_mode()
```

---

## Advanced Topics

### Cascading ICs

Multiple ICs can be cascaded for larger systems:

```python
# 16-bit address decoder using two 74138s
def create_16bit_decoder():
    high_decoder = IC74138()  # A15-A13
    low_decoder = IC74138()   # A12-A10
    
    high_decoder.connect_power()
    low_decoder.connect_power()
    
    return high_decoder, low_decoder

# Expandable priority encoder using 74148s  
def create_16input_encoder():
    high_encoder = IC74148()  # IRQ15-IRQ8
    low_encoder = IC74148()   # IRQ7-IRQ0
    
    high_encoder.connect_power()
    low_encoder.connect_power()
    
    # Cascade connection: high_eo → low_ei
    return high_encoder, low_encoder
```

### Real-World Applications

The ICs in this library are used in:

- **74138/74139**: Memory address decoding, chip select logic
- **74147/74148**: Keyboard encoders, interrupt controllers
- **74150/74151**: ROM/EPROM emulation, function generators
- **74153/74157**: Bus multiplexing, data path switching
- **Basic Gates**: Building blocks for custom logic circuits

### Testing and Validation

```python
# Run comprehensive testing
from IC.ic_test_suite import ICTestSuite

suite = ICTestSuite()

# Test all ICs
if suite.test_all_ics():
    print("All ICs passed testing!")
    
# Test specific IC families
suite.compare_logic_families()

# Interactive testing
suite.interactive_mode()

# Individual IC demonstration
suite.demonstrate_ic('74138')
```

---

## Contributing

To add new ICs to the library:

1. Inherit from `BaseIC` class
2. Implement required methods (`update_outputs`, `test_ic`)
3. Follow pin numbering conventions
4. Add comprehensive documentation
5. Include usage examples
6. Update this README

## Dependencies

- Python 3.6+
- Standard library only (no external dependencies)

## Package Structure

```
IC/
├── __init__.py              # Package initialization
├── base_ic.py              # Base IC class with common functionality
├── ic_7400.py              # 7400 - Quad 2-Input NAND
├── ic_7402.py              # 7402 - Quad 2-Input NOR
├── ic_7404.py              # 7404 - Hex Inverter
├── ic_7408.py              # 7408 - Quad 2-Input AND
├── ic_7410.py              # 7410 - Triple 3-Input NAND
├── ic_7420.py              # 7420 - Dual 4-Input NAND
├── ic_7430.py              # 7430 - Single 8-Input NAND
├── ic_7432.py              # 7432 - Quad 2-Input OR
├── ic_7486.py              # 7486 - Quad 2-Input XOR
├── ic_74138.py             # 74138 - 3-to-8 Decoder
├── ic_74139.py             # 74139 - Dual 2-to-4 Decoder
├── ic_74147.py             # 74147 - 10-to-4 Priority Encoder
├── ic_74148.py             # 74148 - 8-to-3 Priority Encoder
├── ic_74150.py             # 74150 - 16-to-1 Multiplexer
├── ic_74151.py             # 74151 - 8-to-1 Multiplexer
├── ic_74153.py             # 74153 - Dual 4-to-1 Multiplexer
├── ic_74157.py             # 74157 - Quad 2-to-1 Multiplexer
├── ic_test_suite.py        # Comprehensive testing and demo suite
└── README.md               # This file
```

## License

This library is provided for educational purposes. All 7400-series IC specifications are industry standards and are used for reference only.

---

## See Also

- **`advanced_ic_demo.py`** - Comprehensive demonstration of all advanced ICs
- **`../basic_gates/`** - Individual logic gate implementations
- **`../FLIP_FLOPS/`** - Sequential circuit implementations  
- **`../INPUTS/`** - Signal source implementations

---

*For the most up-to-date examples and advanced usage, run `python advanced_ic_demo.py` in the project root or use the interactive test suite.*
