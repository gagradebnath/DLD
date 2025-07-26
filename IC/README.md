# 7400 Series IC Implementation

A comprehensive object-oriented implementation of TTL 7400 series integrated circuits in Python.

## Overview

This package provides faithful implementations of common 7400 series logic ICs, complete with:
- Realistic pin configurations
- Power management (VCC/GND)
- Comprehensive testing suites
- Interactive demonstrations
- Truth table generation
- Pinout diagrams

## Available ICs

| IC Number | Description | Gates | Logic Function |
|-----------|-------------|--------|----------------|
| 7400 | Quad 2-Input NAND Gates | 4 | NAND |
| 7402 | Quad 2-Input NOR Gates | 4 | NOR |
| 7404 | Hex Inverter (NOT Gates) | 6 | NOT |
| 7408 | Quad 2-Input AND Gates | 4 | AND |
| 7432 | Quad 2-Input OR Gates | 4 | OR |
| 7486 | Quad 2-Input XOR Gates | 4 | XOR |
| 7410 | Triple 3-Input NAND Gates | 3 | NAND |
| 7420 | Dual 4-Input NAND Gates | 2 | NAND |
| 7430 | Single 8-Input NAND Gate | 1 | NAND |

## Quick Start

```python
from IC.ic_7400 import IC7400

# Create a 7400 IC (Quad NAND)
ic = IC7400()

# Connect power (VCC=1, GND=0)
ic.connect_power()

# Test a specific gate
output = ic.get_gate_output(1, 1, 0)  # Gate 1: 1 NAND 0 = 1
print(f"Output: {output}")

# Run comprehensive tests
ic.test_ic()

# Show pinout diagram
print(ic.get_pinout_diagram())

# Generate truth table
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
