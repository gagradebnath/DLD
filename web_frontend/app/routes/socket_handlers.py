"""
Socket Event Handlers
Handles WebSocket events for real-time simulation
"""

from flask_socketio import emit
from .. import socketio
from ..services.simulation_service import simulation_service

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to DLD IC Library server'})

@socketio.on('create_ic')
def handle_create_ic(data):
    """Create IC instance for simulation"""
    ic_type = data.get('type')
    instance_id = data.get('id')
    
    try:
        instance_id, ic = simulation_service.create_ic(ic_type, instance_id)
        if ic:
            emit('ic_created', {
                'id': instance_id,
                'type': ic_type,
                'description': ic.description,
                'pins': ic.num_pins,
                'powered': ic.is_powered()
            })
        else:
            emit('error', {'message': f'Failed to create IC {ic_type}'})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('simulate_gate')
def handle_simulate_gate(data):
    """Simulate gate operation"""
    instance_id = data.get('id')
    gate_number = data.get('gate', 1)
    inputs = data.get('inputs', [])
    
    try:
        result = simulation_service.simulate_gate(instance_id, gate_number, inputs)
        if result:
            if 'error' in result:
                emit('error', {'message': result['error']})
            else:
                emit('gate_result', result)
        else:
            emit('error', {'message': 'IC instance not found or does not support gate simulation'})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('simulate_decoder')
def handle_simulate_decoder(data):
    """Simulate decoder operation"""
    instance_id = data.get('id')
    address_bits = data.get('address', [])
    enable_bits = data.get('enable', [0, 0, 1])  # Default enable for 74138
    
    try:
        result = simulation_service.simulate_decoder(instance_id, address_bits, enable_bits)
        if result:
            if 'error' in result:
                emit('error', {'message': result['error']})
            else:
                emit('decoder_result', result)
        else:
            emit('error', {'message': 'IC instance not found or does not support decoder simulation'})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('simulate_encoder')
def handle_simulate_encoder(data):
    """Simulate encoder operation"""
    instance_id = data.get('id')
    inputs = data.get('inputs', {})
    
    try:
        result = simulation_service.simulate_encoder(instance_id, inputs)
        if result:
            if 'error' in result:
                emit('error', {'message': result['error']})
            else:
                emit('encoder_result', result)
        else:
            emit('error', {'message': 'IC instance not found or does not support encoder simulation'})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('simulate_multiplexer')
def handle_simulate_multiplexer(data):
    """Simulate multiplexer operation"""
    instance_id = data.get('id')
    address = data.get('address', 0)
    data_inputs = data.get('data', [])
    
    try:
        result = simulation_service.simulate_multiplexer(instance_id, address, data_inputs)
        if result:
            if 'error' in result:
                emit('error', {'message': result['error']})
            else:
                emit('multiplexer_result', result)
        else:
            emit('error', {'message': 'IC instance not found or does not support multiplexer simulation'})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('remove_ic')
def handle_remove_ic(data):
    """Remove IC instance"""
    instance_id = data.get('id')
    
    try:
        if simulation_service.remove_ic(instance_id):
            emit('ic_removed', {'id': instance_id})
        else:
            emit('error', {'message': 'IC instance not found'})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('get_stats')
def handle_get_stats():
    """Get simulation statistics"""
    try:
        stats = simulation_service.get_stats()
        emit('stats_update', stats)
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('clear_workspace')
def handle_clear_workspace():
    """Clear all IC instances"""
    try:
        simulation_service.clear_all()
        emit('workspace_cleared', {'message': 'All ICs removed'})
    except Exception as e:
        emit('error', {'message': str(e)})
