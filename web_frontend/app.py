"""
Digital Logic Design IC Library - Web Frontend
Interactive web application for visualizing and testing ICs
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit

# Import IC classes
from IC.ic_7400 import IC7400
from IC.ic_7402 import IC7402
from IC.ic_7404 import IC7404
from IC.ic_7408 import IC7408
from IC.ic_7410 import IC7410
from IC.ic_7420 import IC7420
from IC.ic_7430 import IC7430
from IC.ic_7432 import IC7432
from IC.ic_7486 import IC7486
from IC.ic_74138 import IC74138
from IC.ic_74139 import IC74139
from IC.ic_74147 import IC74147
from IC.ic_74148 import IC74148
from IC.ic_74150 import IC74150
from IC.ic_74151 import IC74151
from IC.ic_74153 import IC74153
from IC.ic_74157 import IC74157

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dld_ic_library_2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# IC Registry
IC_CLASSES = {
    '7400': IC7400,
    '7402': IC7402,
    '7404': IC7404,
    '7408': IC7408,
    '7410': IC7410,
    '7420': IC7420,
    '7430': IC7430,
    '7432': IC7432,
    '7486': IC7486,
    '74138': IC74138,
    '74139': IC74139,
    '74147': IC74147,
    '74148': IC74148,
    '74150': IC74150,
    '74151': IC74151,
    '74153': IC74153,
    '74157': IC74157,
}

# IC Categories
IC_CATEGORIES = {
    'Logic Gates': ['7400', '7402', '7404', '7408', '7410', '7420', '7430', '7432', '7486'],
    'Decoders': ['74138', '74139'],
    'Encoders': ['74147', '74148'],
    'Multiplexers': ['74150', '74151', '74153', '74157']
}

# Active IC instances (for simulation state)
active_ics = {}

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', 
                         ic_categories=IC_CATEGORIES, 
                         ic_classes=IC_CLASSES)

@app.route('/ic/<ic_type>')
def ic_detail(ic_type):
    """IC detail page"""
    if ic_type not in IC_CLASSES:
        return "IC not found", 404
    
    # Create IC instance for info
    ic_class = IC_CLASSES[ic_type]
    ic = ic_class()
    ic.connect_power()
    
    ic_info = {
        'type': ic_type,
        'description': ic.description,
        'package': ic.package_type,
        'pins': ic.num_pins,
        'pinout': ic.get_pinout_diagram() if hasattr(ic, 'get_pinout_diagram') else None,
        'truth_table': ic.get_truth_table() if hasattr(ic, 'get_truth_table') else None
    }
    
    return render_template('ic_detail.html', ic_info=ic_info)

@app.route('/simulator')
def simulator():
    """IC Simulator page"""
    return render_template('simulator.html', 
                         ic_categories=IC_CATEGORIES)

@app.route('/circuit_designer')
def circuit_designer():
    """Circuit Designer page"""
    return render_template('circuit_designer.html')

@app.route('/api/ic/<ic_type>/info')
def get_ic_info(ic_type):
    """Get IC information"""
    if ic_type not in IC_CLASSES:
        return jsonify({'error': 'IC not found'}), 404
    
    try:
        ic_class = IC_CLASSES[ic_type]
        ic = ic_class()
        ic.connect_power()
        
        info = {
            'type': ic_type,
            'description': ic.description,
            'package': ic.package_type,
            'pins': ic.num_pins,
            'powered': ic.is_powered(),
            'pin_mapping': getattr(ic, 'pin_mapping', {}),
            'gates': getattr(ic, 'num_gates', 0) if hasattr(ic, 'num_gates') else len(getattr(ic, 'gates', {}))
        }
        
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ic/<ic_type>/test')
def test_ic(ic_type):
    """Test IC functionality"""
    if ic_type not in IC_CLASSES:
        return jsonify({'error': 'IC not found'}), 404
    
    try:
        ic_class = IC_CLASSES[ic_type]
        ic = ic_class()
        ic.connect_power()
        
        test_result = ic.test_ic()
        
        return jsonify({
            'type': ic_type,
            'test_passed': test_result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ic/<ic_type>/pinout')
def get_pinout(ic_type):
    """Get IC pinout diagram"""
    if ic_type not in IC_CLASSES:
        return jsonify({'error': 'IC not found'}), 404
    
    try:
        ic_class = IC_CLASSES[ic_type]
        ic = ic_class()
        
        pinout = ic.get_pinout_diagram() if hasattr(ic, 'get_pinout_diagram') else "Pinout not available"
        
        return jsonify({
            'type': ic_type,
            'pinout': pinout
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to DLD IC Library server'})

@socketio.on('create_ic')
def handle_create_ic(data):
    """Create IC instance for simulation"""
    ic_type = data.get('type')
    instance_id = data.get('id', f"{ic_type}_{len(active_ics)}")
    
    if ic_type not in IC_CLASSES:
        emit('error', {'message': f'IC type {ic_type} not found'})
        return
    
    try:
        ic_class = IC_CLASSES[ic_type]
        ic = ic_class()
        ic.connect_power()
        
        active_ics[instance_id] = ic
        
        emit('ic_created', {
            'id': instance_id,
            'type': ic_type,
            'description': ic.description,
            'pins': ic.num_pins,
            'powered': ic.is_powered()
        })
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('simulate_gate')
def handle_simulate_gate(data):
    """Simulate gate operation"""
    instance_id = data.get('id')
    gate_number = data.get('gate', 1)
    inputs = data.get('inputs', [])
    
    if instance_id not in active_ics:
        emit('error', {'message': 'IC instance not found'})
        return
    
    try:
        ic = active_ics[instance_id]
        
        if hasattr(ic, 'get_gate_output'):
            output = ic.get_gate_output(gate_number, *inputs)
            
            emit('gate_result', {
                'id': instance_id,
                'gate': gate_number,
                'inputs': inputs,
                'output': output,
                'timestamp': datetime.now().isoformat()
            })
        else:
            emit('error', {'message': 'IC does not support gate simulation'})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('simulate_decoder')
def handle_simulate_decoder(data):
    """Simulate decoder operation"""
    instance_id = data.get('id')
    address_bits = data.get('address', [])
    enable_bits = data.get('enable', [0, 0, 1])  # Default enable for 74138
    
    if instance_id not in active_ics:
        emit('error', {'message': 'IC instance not found'})
        return
    
    try:
        ic = active_ics[instance_id]
        
        if hasattr(ic, 'decode'):
            if len(address_bits) == 3:  # 74138
                outputs = ic.decode(*address_bits, *enable_bits)
            elif len(address_bits) == 2:  # 74139
                outputs = ic.decode_1(*address_bits, enable_bits[0])
            else:
                emit('error', {'message': 'Invalid address bits for decoder'})
                return
            
            emit('decoder_result', {
                'id': instance_id,
                'address': address_bits,
                'enable': enable_bits,
                'outputs': outputs,
                'active_output': outputs.index(0) if 0 in outputs else -1,
                'timestamp': datetime.now().isoformat()
            })
        else:
            emit('error', {'message': 'IC does not support decoder simulation'})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('simulate_encoder')
def handle_simulate_encoder(data):
    """Simulate encoder operation"""
    instance_id = data.get('id')
    inputs = data.get('inputs', {})
    
    if instance_id not in active_ics:
        emit('error', {'message': 'IC instance not found'})
        return
    
    try:
        ic = active_ics[instance_id]
        
        if hasattr(ic, 'encode_decimal'):  # 74147
            output = ic.encode_decimal(inputs)
            decimal_value = ic.get_bcd_output()
            
            emit('encoder_result', {
                'id': instance_id,
                'inputs': inputs,
                'bcd_output': output,
                'decimal_value': decimal_value,
                'timestamp': datetime.now().isoformat()
            })
        elif hasattr(ic, 'encode_inputs'):  # 74148
            result = ic.encode_inputs(inputs, enable_input=0)
            a2, a1, a0, gs, eo = result
            
            emit('encoder_result', {
                'id': instance_id,
                'inputs': inputs,
                'output_code': [a2, a1, a0],
                'group_select': gs,
                'enable_output': eo,
                'timestamp': datetime.now().isoformat()
            })
        else:
            emit('error', {'message': 'IC does not support encoder simulation'})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('simulate_multiplexer')
def handle_simulate_multiplexer(data):
    """Simulate multiplexer operation"""
    instance_id = data.get('id')
    address = data.get('address', 0)
    data_inputs = data.get('data', [])
    
    if instance_id not in active_ics:
        emit('error', {'message': 'IC instance not found'})
        return
    
    try:
        ic = active_ics[instance_id]
        
        if hasattr(ic, 'select_input'):
            output = ic.select_input(address, data_inputs)
            
            emit('multiplexer_result', {
                'id': instance_id,
                'address': address,
                'data_inputs': data_inputs,
                'output': output,
                'timestamp': datetime.now().isoformat()
            })
        else:
            emit('error', {'message': 'IC does not support multiplexer simulation'})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('remove_ic')
def handle_remove_ic(data):
    """Remove IC instance"""
    instance_id = data.get('id')
    
    if instance_id in active_ics:
        del active_ics[instance_id]
        emit('ic_removed', {'id': instance_id})
    else:
        emit('error', {'message': 'IC instance not found'})

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("🌐 Starting Digital Logic Design IC Library Web Server")
    print("=" * 50)
    print("📱 Open your browser to: http://localhost:5000")
    print("🔌 IC Simulator: http://localhost:5000/simulator")
    print("🛠️  Circuit Designer: http://localhost:5000/circuit_designer")
    print("=" * 50)
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
