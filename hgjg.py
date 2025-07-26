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