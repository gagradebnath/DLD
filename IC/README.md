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


## API Reference

### BaseIC Class

All ICs inherit from `BaseIC` which provides:

- `connect_power(vcc=1, gnd=0)` - Connect power to the IC
- `set_pin(pin_number, value)` - Set a pin to logic level
- `get_pin(pin_number)` - Get current pin logic level
- `is_powered()` - Check if IC is powered
- `get_pinout_diagram()` - Generate ASCII pinout diagram
- `test_ic()` - Run comprehensive tests
- `reset_pins()` - Reset all pins to disconnected state

### Gate-Specific Methods

Each IC also provides:

- `get_gate_output(gate_number, *inputs)` - Calculate gate output
- `get_truth_table()` - Generate truth table
- `update_outputs()` - Refresh all output pins

## Testing

Run the comprehensive test suite:

```python
from IC.ic_test_suite import ICTestSuite

suite = ICTestSuite()
all_passed = suite.test_all_ics()

if all_passed:
    print("All ICs passed testing!")
else:
    print("Some ICs failed - check the detailed results")
```

## Educational Applications

This package is ideal for:

- Digital logic education
- Circuit simulation
- Understanding TTL IC behavior
- Learning object-oriented design
- Exploring digital electronics concepts

## Dependencies

- Python 3.6+
- Standard library only (no external dependencies)

## Contributing

The modular design makes it easy to add new ICs:

1. Inherit from `BaseIC`
2. Define pin mappings
3. Implement gate logic
4. Add to the IC catalog
5. Write tests

## License

Educational use - part of Digital Logic Design library.

## See Also

- `../basic_gates/` - Individual logic gate implementations
- `../FLIP_FLOPS/` - Sequential circuit implementations  
- `../INPUTS/` - Signal source implementations
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

# Use Gate A (pins 1,2 → 3)
result = nand_ic.get_gate_output(1,1, 0)  # Returns 1 (NAND of 1,0)

# Use Gate B (pins 4,5 → 6)
result = nand_ic.get_gate_output(2,1, 1)  # Returns 0 (NAND of 1,1)

# Use Gate C (pins 9,10 → 8)
result = nand_ic.get_gate_output(3,0, 0)  # Returns 1 (NAND of 0,0)

# Use Gate D (pins 12,13 → 11)
result = nand_ic.get_gate_output(4,0, 1)  # Returns 1 (NAND of 0,1)

# Test the IC
if nand_ic.test_ic():
    print("IC7400 is working correctly")
```

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
result = nor_ic.get_gate_output(1,0, 0)  # Returns 1 (NOR of 0,0)

# Gate B (pins 5,6 → 4)
result = nor_ic.get_gate_output(2,1, 0)  # Returns 0 (NOR of 1,0)

# Gate C (pins 8,9 → 10)
result = nor_ic.get_gate_output(3,0, 1)  # Returns 0 (NOR of 0,1)

# Gate D (pins 11,12 → 13)
result = nor_ic.get_gate_output(4,1, 1)  # Returns 0 (NOR of 1,1)
```

### IC7404 - Hex Inverter

**Package**: 14-pin DIP  
**Function**: Six independent NOT gates

```python
from IC.ic_7404 import IC7404

not_ic = IC7404()
not_ic.connect_power()

# Use each inverter
result = not_ic.get_gate_output(1,1)  # Pin 1 → 2, Returns 0
result = not_ic.get_gate_output(2,0)  # Pin 3 → 4, Returns 1
result = not_ic.get_gate_output(3,1)  # Pin 5 → 6, Returns 0
result = not_ic.get_gate_output(4,0)  # Pin 9 → 8, Returns 1
result = not_ic.get_gate_output(5,1)  # Pin 11 → 10, Returns 0
result = not_ic.get_gate_output(6,0)  # Pin 13 → 12, Returns 1
```

### IC7408 - Quad 2-Input AND Gate

**Package**: 14-pin DIP  
**Function**: Four independent 2-input AND gates

```python
from IC.ic_7408 import IC7408

and_ic = IC7408()
and_ic.connect_power()

# Gate A (pins 1,2 → 3)
result = and_ic.get_gate_output(1,1, 1)  # Returns 1 (AND of 1,1)

# Gate B (pins 4,5 → 6)
result = and_ic.get_gate_output(2,1, 0)  # Returns 0 (AND of 1,0)

# Gate C (pins 9,10 → 8)
result = and_ic.get_gate_output(3,0, 1)  # Returns 0 (AND of 0,1)

# Gate D (pins 12,13 → 11)
result = and_ic.get_gate_output(4,0, 0)  # Returns 0 (AND of 0,0)
```

### IC7410 - Triple 3-Input NAND Gate

**Package**: 14-pin DIP  
**Function**: Three independent 3-input NAND gates

```python
from IC.ic_7410 import IC7410

nand3_ic = IC7410()
nand3_ic.connect_power()

# Gate A (pins 1,2,13 → 12)
result = nand3_ic.get_gate_output(1,1, 1, 1)  # Returns 0 (NAND of 1,1,1)

# Gate B (pins 3,4,5 → 6)
result = nand3_ic.get_gate_output(2,1, 0, 1)  # Returns 1 (NAND of 1,0,1)

# Gate C (pins 9,10,11 → 8)
result = nand3_ic.get_gate_output(3,0, 0, 0)  # Returns 1 (NAND of 0,0,0)
```

### IC7420 - Dual 4-Input NAND Gate

**Package**: 14-pin DIP  
**Function**: Two independent 4-input NAND gates

```python
from IC.ic_7420 import IC7420

nand4_ic = IC7420()
nand4_ic.connect_power()

# Gate A (pins 1,2,4,5 → 6)
result = nand4_ic.get_gate_output(1,1, 1, 1, 1)  # Returns 0 (NAND of 1,1,1,1)

# Gate B (pins 9,10,12,13 → 8)
result = nand4_ic.get_gate_output(2,1, 0, 1, 1)  # Returns 1 (NAND of 1,0,1,1)
```

### IC7430 - Single 8-Input NAND Gate

**Package**: 14-pin DIP  
**Function**: One 8-input NAND gate

```python
from IC.ic_7430 import IC7430

nand8_ic = IC7430()
nand8_ic.connect_power()

# Single gate (pins 1,2,3,4,5,6,11,12 → 8)
result = nand8_ic.get_gate_output(1, 1, 1, 1, 1, 1, 1, 1)  # Returns 0
result = nand8_ic.get_gate_output(1, 1, 1, 1, 1, 1, 1, 0)  # Returns 1
```

### IC7432 - Quad 2-Input OR Gate

**Package**: 14-pin DIP  
**Function**: Four independent 2-input OR gates

```python
from IC.ic_7432 import IC7432

or_ic = IC7432()
or_ic.connect_power()

# Gate A (pins 1,2 → 3)
result = or_ic.get_gate_output(1,0, 0)  # Returns 0 (OR of 0,0)

# Gate B (pins 4,5 → 6)
result = or_ic.get_gate_output(2,1, 0)  # Returns 1 (OR of 1,0)

# Gate C (pins 9,10 → 8)
result = or_ic.get_gate_output(3,0, 1)  # Returns 1 (OR of 0,1)

# Gate D (pins 12,13 → 11)
result = or_ic.get_gate_output(4,1, 1)  # Returns 1 (OR of 1,1)
```

### IC7486 - Quad 2-Input XOR Gate

**Package**: 14-pin DIP  
**Function**: Four independent 2-input XOR gates

```python
from IC.ic_7486 import IC7486

xor_ic = IC7486()
xor_ic.connect_power()

# Gate A (pins 1,2 → 3)
result = xor_ic.get_gate_output(1,0, 0)  # Returns 0 (XOR of 0,0)

# Gate B (pins 4,5 → 6)
result = xor_ic.get_gate_output(2,1, 0)  # Returns 1 (XOR of 1,0)

# Gate C (pins 9,10 → 8)
result = xor_ic.get_gate_output(3,0, 1)  # Returns 1 (XOR of 0,1)

# Gate D (pins 12,13 → 11)
result = xor_ic.get_gate_output(4,1, 1)  # Returns 0 (XOR of 1,1)
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
```

### Encoders

#### IC74147 - 10-to-4 Line Priority Encoder (Decimal to BCD)

**Package**: 16-pin DIP  
**Function**: Encodes highest priority active input (0-9) to 4-bit BCD (active-low)

```python
from IC.ic_74147 import IC74147

encoder = IC74147()
encoder.connect_power()

# Single input active (input 7)
inputs = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0, 8: 1, 9: 1}
bcd_output = encoder.encode_decimal(inputs)
# Returns: [1, 0, 0, 0] (inverted BCD for 7)

decimal_value = encoder.get_bcd_output()
# Returns: 7

# Multiple inputs active (priority encoding)
inputs = {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 0}
bcd_output = encoder.encode_decimal(inputs)
decimal_value = encoder.get_bcd_output()
# Returns: 9 (highest priority active input)

# Keyboard encoder example
keypad_inputs = {0: 1, 1: 1, 2: 1, 3: 0, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}
if encoder.encode_decimal(keypad_inputs):
    pressed_key = encoder.get_bcd_output()
    print(f"Key {pressed_key} pressed")
```

**Input Priority** (highest to lowest): 9, 8, 7, 6, 5, 4, 3, 2, 1, 0

#### IC74148 - 8-to-3 Line Priority Encoder with Cascade

**Package**: 16-pin DIP  
**Function**: Encodes highest priority active input (0-7) to 3-bit binary with cascade capability

```python
from IC.ic_74148 import IC74148

priority_encoder = IC74148()
priority_encoder.connect_power()

# Single interrupt active (IRQ 5)
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
if gs == 0:  # Group select active
    print(f"Interrupt: {irq_names[highest_irq]}")
```

**Cascade Signals**:
- **GS** (Group Select): 0 = valid input present, 1 = no inputs
- **EO** (Enable Output): 0 = enable next stage, 1 = disable next stage

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
    print(f"Address 0x{address:X}: Data 0x{program_memory[address]:02X} -> Output {data_out}")

# Function generator
sine_table = [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0]  # Approximate sine
for phase in range(16):
    sine_out = mux16.select_input(phase, sine_table)
    print(f"Phase {phase}: Sine = {1-sine_out}")  # Invert output
```

#### IC74151 - 8-to-1 Line Data Selector/Multiplexer

**Package**: 16-pin DIP  
**Function**: Selects one of 8 inputs with complementary outputs (Y and W)

```python
from IC.ic_74151 import IC74151

mux8 = IC74151()
mux8.connect_power()

# 8-bit data
data = [1, 0, 1, 1, 0, 1, 0, 0]

# Select input 3
y_output, w_output = mux8.select_input(3, data)
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

# Data routing with enable
data_bus = [1, 0, 1, 0, 1, 1, 0, 1]
select_lines = 5  # Binary 101
y, w = mux8.select_input(select_lines, data_bus)
print(f"Selected data: {y}, Inverted: {w}")
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

# Independent enable control
outputs = dual_mux.multiplex_both(word1, word2, select=3, enable1=0, enable2=1)
# MUX1 enabled, MUX2 disabled
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

# Select Bus A (select = 0)
output = quad_mux.route_inputs(bus_a, bus_b, select=0, enable=0)
# Returns: [1, 0, 1, 0] (Bus A selected)

# Select Bus B (select = 1)
output = quad_mux.route_inputs(bus_a, bus_b, select=1, enable=0)
# Returns: [0, 1, 1, 1] (Bus B selected)

# CPU/DMA bus switching
cpu_bus = [1, 1, 0, 1]
dma_bus = [0, 0, 1, 0]

# CPU mode (DMA_REQUEST = 0)
system_bus = quad_mux.route_inputs(cpu_bus, dma_bus, select=0, enable=0)
print(f"CPU mode: System bus = {system_bus}")

# DMA mode (DMA_REQUEST = 1)
system_bus = quad_mux.route_inputs(cpu_bus, dma_bus, select=1, enable=0)
print(f"DMA mode: System bus = {system_bus}")

# Individual bus selection methods
selected_a = quad_mux.select_a_inputs(bus_a)  # Always select A inputs
selected_b = quad_mux.select_b_inputs(bus_b)  # Always select B inputs

# Parallel switching with enable
output = quad_mux.parallel_switch(bus_a, bus_b, select=1, enable=0)
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

# Or import from package
from IC import create_ic

# Create IC instances
nand_gates = IC7400()
decoder = IC74138()
multiplexer = IC74151()

# Always connect power before use
nand_gates.connect_power()
decoder.connect_power()
multiplexer.connect_power()

# Use the ICs
result = nand_gates.get_gate_output(1,1, 0)
outputs = decoder.decode(1, 0, 1, 0, 0, 1)
mux_out = multiplexer.select_input(3, [1,0,1,1,0,1,0,0])
```

### Factory Functions

```python
from IC import create_ic, list_ics

# List all available ICs
list_ics()

# Create ICs using factory function
ic1 = create_ic('7400')  # Creates IC7400
ic2 = create_ic('74138')  # Creates IC74138
ic3 = create_ic('74151')  # Creates IC74151

# All factory-created ICs are automatically powered
result = ic1.get_gate_output(1,1, 0)  # Ready to use
```

### Testing ICs

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
```

---

## Quick Reference

### Logic Gate ICs

| IC    | Function | Gates | Inputs | Package |
|-------|----------|-------|---------|---------|
| 7400  | NAND     | 4     | 2      | 14-pin  |
| 7402  | NOR      | 4     | 2      | 14-pin  |
| 7404  | NOT      | 6     | 1      | 14-pin  |
| 7408  | AND      | 4     | 2      | 14-pin  |
| 7410  | NAND     | 3     | 3      | 14-pin  |
| 7420  | NAND     | 2     | 4      | 14-pin  |
| 7430  | NAND     | 1     | 8      | 14-pin  |
| 7432  | OR       | 4     | 2      | 14-pin  |
| 7486  | XOR      | 4     | 2      | 14-pin  |

### Advanced Data Processing ICs

| IC     | Function | Inputs | Outputs | Package | Features |
|--------|----------|--------|---------|---------|----------|
| 74138  | 3-8 Decoder | 3 + 3E | 8 | 16-pin | Active-low outputs |
| 74139  | Dual 2-4 Decoder | 2×(2+1E) | 2×4 | 16-pin | Independent decoders |
| 74147  | 10-4 Encoder | 10 | 4 | 16-pin | Priority, BCD output |
| 74148  | 8-3 Encoder | 8 + 1E | 3 + 2 | 16-pin | Cascade capability |
| 74150  | 16-1 Mux | 16 + 4A + 1E | 1 | 24-pin | Inverted output |
| 74151  | 8-1 Mux | 8 + 3A + 1E | 2 | 16-pin | Complementary outputs |
| 74153  | Dual 4-1 Mux | 2×4 + 2A + 2E | 2 | 16-pin | Shared select lines |
| 74157  | Quad 2-1 Mux | 2×4 + 1S + 1E | 4 | 16-pin | 4-bit bus switching |

**Legend**: A=Address, E=Enable, S=Select

### Pin Numbering Convention

All ICs follow standard DIP (Dual In-line Package) pinout:
- **14-pin**: Pins 1-7 (left side), 8-14 (right side)
- **16-pin**: Pins 1-8 (left side), 9-16 (right side)  
- **24-pin**: Pins 1-12 (left side), 13-24 (right side)
- **Power**: VCC (top-right), GND (bottom-left)

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
        # operation: 0=AND, 1=OR, 2=XOR, 3=NAND
        
        # Compute all operations
        and_result = []
        or_result = []
        xor_result = []
        nand_result = []
        
        for i in range(4):
            # AND: double NAND
            nand1 = self.nand_gates.get_gate_output(1,a[i], b[i])
            and_bit = self.nand_gates.get_gate_output(2,nand1, nand1)
            and_result.append(and_bit)
            
            # OR
            or_bit = self.or_gates.get_gate_output(1,a[i], b[i])
            or_result.append(or_bit)
            
            # XOR
            xor_bit = self.xor_gates.get_gate_output(1,a[i], b[i])
            xor_result.append(xor_bit)
            
            # NAND
            nand_bit = self.nand_gates.get_gate_output(3,a[i], b[i])
            nand_result.append(nand_bit)
        
        # Select operation using multiplexers
        if operation == 0:
            return and_result
        elif operation == 1:
            return or_result
        elif operation == 2:
            return xor_result
        else:
            return nand_result

# Usage
alu = Simple4BitALU()
a = [1, 0, 1, 1]  # 4-bit input A
b = [0, 1, 1, 0]  # 4-bit input B

result = alu.compute(a, b, operation=2)  # XOR operation
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
        # address is 6-bit: AAAAAA (A5 A4 A3 A2 A1 A0)
        
        # Main decoder uses A5, A4, A3
        main_addr = (address >> 3) & 0x7
        a2 = (main_addr >> 2) & 1
        a1 = (main_addr >> 1) & 1
        a0 = main_addr & 1
        
        main_outputs = self.main_decoder.decode(a2, a1, a0, e1=0, e2=0, e3=1)
        main_select = main_outputs.index(0)
        
        # Sub decoder uses A2, A1
        sub_addr = (address >> 1) & 0x3
        s1 = (sub_addr >> 1) & 1
        s0 = sub_addr & 1
        
        sub_outputs = self.sub_decoder.decode_1(s1, s0, enable=0)
        sub_select = sub_outputs.index(0)
        
        return {
            'main_block': main_select,
            'main_name': self.memory_map[main_select],
            'sub_block': sub_select,
            'byte_select': address & 1
        }

# Usage
decoder = MemoryDecoder()

for addr in [0x00, 0x0F, 0x1A, 0x2C, 0x3F]:
    result = decoder.decode_address(addr)
    print(f"Address 0x{addr:02X}: {result['main_name']}, "
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
        
        self.irq_handlers = {
            0: self.timer_handler,
            1: self.keyboard_handler,
            2: self.serial_handler,
            3: self.network_handler,
            4: self.mouse_handler,
            5: self.sound_handler,
            6: self.disk_handler,
            7: self.nmi_handler
        }
    
    def check_interrupts(self, irq_lines):
        """
        Check for active interrupts and return highest priority
        irq_lines: dict with IRQ number as key, state as value
        (0 = active interrupt, 1 = no interrupt)
        """
        a2, a1, a0, gs, eo = self.encoder.encode_inputs(irq_lines, enable_input=0)
        
        if gs == 0:  # Valid interrupt present
            # Convert inverted output to IRQ number
            irq_number = (1-a2)*4 + (1-a1)*2 + (1-a0)*1
            return irq_number
        else:
            return None  # No interrupts
    
    def handle_interrupt(self, irq_lines):
        irq = self.check_interrupts(irq_lines)
        if irq is not None:
            print(f"Handling {self.irq_names[irq]} (IRQ{irq})")
            self.irq_handlers[irq]()
            return irq
        return None
    
    def timer_handler(self):
        print("Timer interrupt: System tick")
    
    def keyboard_handler(self):
        print("Keyboard interrupt: Key pressed")
    
    def serial_handler(self):
        print("Serial interrupt: Data received")
    
    def network_handler(self):
        print("Network interrupt: Packet arrived")
    
    def mouse_handler(self):
        print("Mouse interrupt: Movement detected")
    
    def sound_handler(self):
        print("Sound interrupt: Buffer empty")
    
    def disk_handler(self):
        print("Disk interrupt: Operation complete")
    
    def nmi_handler(self):
        print("NMI: Critical system error!")

# Usage
controller = InterruptController()

# Simulate various interrupt scenarios
scenarios = [
    {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1},  # No interrupts
    {0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1},  # Timer only
    {0: 0, 1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1},  # Timer + Keyboard
    {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0},  # All interrupts
    {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0},  # NMI only
]

for i, scenario in enumerate(scenarios):
    print(f"\nScenario {i+1}:")
    irq = controller.handle_interrupt(scenario)
    if irq is None:
        print("No interrupts to handle")
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

### Timing Considerations

```python
# Propagation delay simulation
class TimedIC74151(IC74151):
    def __init__(self):
        super().__init__()
        self.propagation_delay = 13e-9  # 13ns typical
    
    def select_input(self, address, data, simulate_delay=True):
        if simulate_delay:
            import time
            time.sleep(self.propagation_delay)
        
        return super().select_input(address, data)
```

### Error Handling

```python
# Robust IC usage with error handling
def safe_ic_operation():
    try:
        ic = IC74138()
        ic.connect_power()
        
        if not ic.test_ic():
            raise RuntimeError("IC failed self-test")
        
        # Use IC safely
        result = ic.decode(1, 0, 1, 0, 0, 1)
        return result
        
    except Exception as e:
        print(f"IC operation failed: {e}")
        return None
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

---

## License

This library is provided for educational purposes. All 7400-series IC specifications are industry standards and are used for reference only.

---

*For more examples and advanced usage, see the `advanced_ic_demo.py` file in the project root.*
print(ic.get_truth_table())
```

## Package Structure

```
IC/
├── __init__.py              # Package initialization and factory functions
├── base_ic.py              # Base IC class with common functionality
├── ic_7400.py              # 7400 - Quad 2-Input NAND
├── ic_7402.py              # 7402 - Quad 2-Input NOR
├── ic_7404.py              # 7404 - Hex Inverter
├── ic_7408.py              # 7408 - Quad 2-Input AND
├── ic_7432.py              # 7432 - Quad 2-Input OR
├── ic_7486.py              # 7486 - Quad 2-Input XOR
├── ic_7410.py              # 7410 - Triple 3-Input NAND
├── ic_7420.py              # 7420 - Dual 4-Input NAND
├── ic_7430.py              # 7430 - Single 8-Input NAND
├── ic_test_suite.py        # Comprehensive testing and demo suite
└── README.md               # This file
```

## Features

### Realistic IC Behavior
- Proper pin numbering (1-14 for DIP-14 packages)
- Power pins (VCC and GND)
- Pin state management
- Power-off behavior (outputs go to 0)

### Testing and Validation
- Automated truth table verification
- Interactive testing modes
- Comprehensive test suites
- Error detection and reporting

### Educational Tools
- ASCII pinout diagrams
- Truth table generation
- Logic family comparisons
- Digital circuit examples

## Usage Examples

### Basic IC Operations

```python
from IC import get_ic

# Factory function to create any IC
nand_ic = get_ic('7400')
and_ic = get_ic('7408')
not_ic = get_ic('7404')

# Power the ICs
for ic in [nand_ic, and_ic, not_ic]:
    ic.connect_power()

# Use the gates
nand_output = nand_ic.get_gate_output(1, 1, 1)  # 1 NAND 1 = 0
and_output = and_ic.get_gate_output(1, 1, 1)    # 1 AND 1 = 1
not_output = not_ic.get_gate_output(1, 1)       # NOT 1 = 0
```

### Building Digital Circuits

```python
from IC.ic_7486 import IC7486  # XOR gates
from IC.ic_7408 import IC7408  # AND gates

# Half Adder Implementation
xor_ic = IC7486()  # For sum output
and_ic = IC7408()  # For carry output

xor_ic.connect_power()
and_ic.connect_power()

def half_adder(a, b):
    sum_bit = xor_ic.get_gate_output(1, a, b)    # A XOR B
    carry_bit = and_ic.get_gate_output(1, a, b)  # A AND B
    return sum_bit, carry_bit

# Test the half adder
for a in [0, 1]:
    for b in [0, 1]:
        s, c = half_adder(a, b)
        print(f"{a} + {b} = {s} (carry: {c})")
```

### Interactive Testing

```python
from IC.ic_test_suite import ICTestSuite

# Create test suite
suite = ICTestSuite()

# Test all ICs
suite.test_all_ics()

# Interactive mode
suite.interactive_mode()

# Demonstrate specific IC
suite.demonstrate_ic('7400')
```

## Pin Configurations

Each IC follows standard DIP-14 pinout conventions:

### 7400 (Quad NAND) Example
```
    7400 (DIP-14) - Quad 2-Input NAND Gates
====================================================

 1 ┤1A (Gate 1 In A)├─────────┤VCC (Power)     ├ 14
 2 ┤1B (Gate 1 In B)├─────────┤4B (Gate 4 In B)├ 13
 3 ┤1Y (Gate 1 Out) ├─────────┤4A (Gate 4 In A)├ 12
 4 ┤2A (Gate 2 In A)├─────────┤4Y (Gate 4 Out) ├ 11
 5 ┤2B (Gate 2 In B)├─────────┤3B (Gate 3 In B)├ 10
 6 ┤2Y (Gate 2 Out) ├─────────┤3A (Gate 3 In A)├  9
 7 ┤GND (Ground)    ├─────────┤3Y (Gate 3 Out) ├  8
```
