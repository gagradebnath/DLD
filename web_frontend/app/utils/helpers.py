"""
Utility Functions
Helper functions for the application
"""

import json
from datetime import datetime

def format_timestamp():
    """Get formatted timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def serialize_ic_info(ic):
    """Serialize IC instance information"""
    return {
        'description': ic.description,
        'package': ic.package_type,
        'pins': ic.num_pins,
        'powered': ic.is_powered(),
        'timestamp': format_timestamp()
    }

def validate_gate_inputs(inputs, expected_count):
    """Validate gate input parameters"""
    if not isinstance(inputs, list):
        return False, "Inputs must be a list"
    
    if len(inputs) != expected_count:
        return False, f"Expected {expected_count} inputs, got {len(inputs)}"
    
    for inp in inputs:
        if inp not in [0, 1]:
            return False, "Inputs must be 0 or 1"
    
    return True, None

def validate_address_bits(address, max_bits):
    """Validate address bits for decoders/multiplexers"""
    if not isinstance(address, (int, list)):
        return False, "Address must be an integer or list"
    
    if isinstance(address, int):
        if address < 0 or address >= (2 ** max_bits):
            return False, f"Address out of range for {max_bits}-bit address"
    
    return True, None

class ConfigManager:
    """Configuration management utilities"""
    
    @staticmethod
    def load_config(config_file='config.json'):
        """Load configuration from file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    @staticmethod
    def save_config(config, config_file='config.json'):
        """Save configuration to file"""
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
