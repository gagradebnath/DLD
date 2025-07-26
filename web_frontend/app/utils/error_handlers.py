"""
Error Handlers
Custom error handling for the application
"""

from flask import jsonify, render_template
from flask_socketio import emit

class ICError(Exception):
    """Custom exception for IC-related errors"""
    def __init__(self, message, ic_type=None):
        self.message = message
        self.ic_type = ic_type
        super().__init__(self.message)

class SimulationError(Exception):
    """Custom exception for simulation errors"""
    def __init__(self, message, instance_id=None):
        self.message = message
        self.instance_id = instance_id
        super().__init__(self.message)

def handle_ic_error(error):
    """Handle IC-related errors"""
    response = {
        'error': 'IC Error',
        'message': error.message,
        'type': error.ic_type
    }
    return jsonify(response), 400

def handle_simulation_error(error):
    """Handle simulation errors"""
    response = {
        'error': 'Simulation Error',
        'message': error.message,
        'instance_id': error.instance_id
    }
    return jsonify(response), 400

def handle_404(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404

def handle_500(error):
    """Handle 500 errors"""
    return render_template('errors/500.html'), 500

def emit_error(message, error_type='general'):
    """Emit error via WebSocket"""
    emit('error', {
        'type': error_type,
        'message': message
    })
