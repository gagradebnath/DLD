"""
Main Routes
Handles the main application pages
"""

from flask import Blueprint, render_template
from ..models.ic_registry import IC_CATEGORIES, IC_CLASSES

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main page"""
    return render_template('index.html', 
                         ic_categories=IC_CATEGORIES, 
                         ic_classes=IC_CLASSES)

@main_bp.route('/ic/<ic_type>')
def ic_detail(ic_type):
    """IC detail page"""
    from ..models.ic_registry import create_ic_instance
    
    if ic_type not in IC_CLASSES:
        return "IC not found", 404
    
    # Create IC instance for info
    ic = create_ic_instance(ic_type)
    if not ic:
        return "Failed to create IC instance", 500
    
    ic_info = {
        'type': ic_type,
        'description': ic.description,
        'package': ic.package_type,
        'pins': ic.num_pins,
        'pinout': ic.get_pinout_diagram() if hasattr(ic, 'get_pinout_diagram') else None,
        'truth_table': ic.get_truth_table() if hasattr(ic, 'get_truth_table') else None
    }
    
    return render_template('ic_detail.html', ic_info=ic_info)

@main_bp.route('/circuit_designer')
def circuit_designer():
    """Circuit Designer page"""
    return render_template('circuit_designer.html')
