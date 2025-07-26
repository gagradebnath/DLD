"""
Digital Logic Design IC Library - Web Frontend
Main application entry point
"""

import os
import sys

# Add parent directory to path for IC imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app, socketio

def main():
    """Main application entry point"""
    # Create directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Create Flask app
    app = create_app('development')
    
    print("🌐 Starting Digital Logic Design IC Library Web Server")
    print("=" * 50)
    print("📱 Open your browser to: http://localhost:5000")
    print("🔌 IC Simulator: http://localhost:5000/simulator")
    print("🛠️  Circuit Designer: http://localhost:5000/circuit_designer")
    print("📊 API Docs: http://localhost:5000/api/stats")
    print("=" * 50)
    
    # Run the application
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
