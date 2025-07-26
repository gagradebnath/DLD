"""
API Routes
Handles REST API endpoints for IC operations
"""

from flask import Blueprint, jsonify
from datetime import datetime
from ..models.ic_registry import IC_CLASSES, create_ic_instance

api_bp = Blueprint('api', __name__)

@api_bp.route('/ic/<ic_type>/info')
def get_ic_info(ic_type):
    """Get IC information"""
    if ic_type not in IC_CLASSES:
        return jsonify({'error': 'IC not found'}), 404
    
    try:
        ic = create_ic_instance(ic_type)
        if not ic:
            return jsonify({'error': 'Failed to create IC instance'}), 500
        
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

@api_bp.route('/ic/<ic_type>/test')
def test_ic(ic_type):
    """Test IC functionality"""
    if ic_type not in IC_CLASSES:
        return jsonify({'error': 'IC not found'}), 404
    
    try:
        ic = create_ic_instance(ic_type)
        if not ic:
            return jsonify({'error': 'Failed to create IC instance'}), 500
        
        test_result = ic.test_ic()
        
        return jsonify({
            'type': ic_type,
            'test_passed': test_result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/ic/<ic_type>/pinout')
def get_pinout(ic_type):
    """Get IC pinout diagram"""
    if ic_type not in IC_CLASSES:
        return jsonify({'error': 'IC not found'}), 404
    
    try:
        ic = create_ic_instance(ic_type)
        if not ic:
            return jsonify({'error': 'Failed to create IC instance'}), 500
        
        pinout = ic.get_pinout_diagram() if hasattr(ic, 'get_pinout_diagram') else "Pinout not available"
        
        return jsonify({
            'type': ic_type,
            'pinout': pinout
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/stats')
def get_stats():
    """Get application statistics"""
    from ..services.simulation_service import simulation_service
    
    stats = simulation_service.get_stats()
    stats.update({
        'total_ic_types': len(IC_CLASSES),
        'categories': len(IC_CLASSES)
    })
    
    return jsonify(stats)
