"""
Flask Application Factory
Digital Logic Design IC Library - Web Frontend
"""

import os
from flask import Flask
from flask_socketio import SocketIO

# Global SocketIO instance
socketio = SocketIO()

def create_app(config_name='development'):
    """Create and configure Flask application"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Load configuration
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register blueprints
    from .routes.main import main_bp
    from .routes.api import api_bp
    from .routes.simulator import simulator_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(simulator_bp, url_prefix='/simulator')
    
    # Register socket handlers
    from .routes import socket_handlers
    
    return app
