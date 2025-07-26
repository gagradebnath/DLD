"""
IC Simulation Service
Handles IC instance management and simulation operations
"""

from datetime import datetime
from ..models.ic_registry import create_ic_instance, get_ic_class

class ICSimulationService:
    """Service for managing IC simulation instances"""
    
    def __init__(self):
        self.active_ics = {}
        self.operation_count = 0
    
    def create_ic(self, ic_type, instance_id=None):
        """Create a new IC instance"""
        if instance_id is None:
            instance_id = f"{ic_type}_{len(self.active_ics)}"
        
        ic = create_ic_instance(ic_type)
        if ic:
            self.active_ics[instance_id] = ic
            return instance_id, ic
        return None, None
    
    def get_ic(self, instance_id):
        """Get IC instance by ID"""
        return self.active_ics.get(instance_id)
    
    def remove_ic(self, instance_id):
        """Remove IC instance"""
        if instance_id in self.active_ics:
            del self.active_ics[instance_id]
            return True
        return False
    
    def clear_all(self):
        """Clear all IC instances"""
        self.active_ics.clear()
        self.operation_count = 0
    
    def get_stats(self):
        """Get simulation statistics"""
        return {
            'active_ics': len(self.active_ics),
            'total_operations': self.operation_count,
            'timestamp': datetime.now().isoformat()
        }
    
    def simulate_gate(self, instance_id, gate_number, inputs):
        """Simulate gate operation"""
        ic = self.get_ic(instance_id)
        if not ic or not hasattr(ic, 'get_gate_output'):
            return None
        
        try:
            output = ic.get_gate_output(gate_number, *inputs)
            self.operation_count += 1
            return {
                'id': instance_id,
                'gate': gate_number,
                'inputs': inputs,
                'output': output,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def simulate_decoder(self, instance_id, address_bits, enable_bits):
        """Simulate decoder operation"""
        ic = self.get_ic(instance_id)
        if not ic or not hasattr(ic, 'decode'):
            return None
        
        try:
            if len(address_bits) == 3:  # 74138
                outputs = ic.decode(*address_bits, *enable_bits)
            elif len(address_bits) == 2:  # 74139
                outputs = ic.decode_1(*address_bits, enable_bits[0])
            else:
                return {'error': 'Invalid address bits for decoder'}
            
            self.operation_count += 1
            return {
                'id': instance_id,
                'address': address_bits,
                'enable': enable_bits,
                'outputs': outputs,
                'active_output': outputs.index(0) if 0 in outputs else -1,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def simulate_encoder(self, instance_id, inputs):
        """Simulate encoder operation"""
        ic = self.get_ic(instance_id)
        if not ic:
            return None
        
        try:
            if hasattr(ic, 'encode_decimal'):  # 74147
                output = ic.encode_decimal(inputs)
                decimal_value = ic.get_bcd_output()
                self.operation_count += 1
                return {
                    'id': instance_id,
                    'inputs': inputs,
                    'bcd_output': output,
                    'decimal_value': decimal_value,
                    'timestamp': datetime.now().isoformat()
                }
            elif hasattr(ic, 'encode_inputs'):  # 74148
                result = ic.encode_inputs(inputs, enable_input=0)
                a2, a1, a0, gs, eo = result
                self.operation_count += 1
                return {
                    'id': instance_id,
                    'inputs': inputs,
                    'output_code': [a2, a1, a0],
                    'group_select': gs,
                    'enable_output': eo,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {'error': 'IC does not support encoder simulation'}
        except Exception as e:
            return {'error': str(e)}
    
    def simulate_multiplexer(self, instance_id, address, data_inputs):
        """Simulate multiplexer operation"""
        ic = self.get_ic(instance_id)
        if not ic or not hasattr(ic, 'select_input'):
            return None
        
        try:
            output = ic.select_input(address, data_inputs)
            self.operation_count += 1
            return {
                'id': instance_id,
                'address': address,
                'data_inputs': data_inputs,
                'output': output,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}

# Global simulation service instance
simulation_service = ICSimulationService()
