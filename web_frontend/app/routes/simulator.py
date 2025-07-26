"""
Simulator Routes
Handles simulator-specific routes
"""

from flask import Blueprint, render_template
from ..models.ic_registry import IC_CATEGORIES

simulator_bp = Blueprint('simulator', __name__)

@simulator_bp.route('/')
def simulator_main():
    """IC Simulator page"""
    return render_template('simulator.html', 
                         ic_categories=IC_CATEGORIES)
