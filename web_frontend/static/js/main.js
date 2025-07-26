// Digital Logic Design IC Library - Main JavaScript

let currentIC = null;
let socket = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize socket connection if on simulator page
    if (window.location.pathname === '/simulator') {
        initializeSocket();
    }
    
    // Add event listeners
    setupEventListeners();
    
    console.log('DLD IC Library initialized');
}

function setupEventListeners() {
    // Add any global event listeners here
}

function showICDetails(icType) {
    currentIC = icType;
    
    // Show loading state
    const modal = new bootstrap.Modal(document.getElementById('icDetailsModal'));
    document.getElementById('icModalTitle').innerHTML = `<i class="fas fa-microchip me-2"></i>Loading ${icType}...`;
    document.getElementById('icModalBody').innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
    modal.show();
    
    // Fetch IC details
    fetch(`/api/ic/${icType}/info`)
        .then(response => response.json())
        .then(data => {
            displayICDetails(data);
        })
        .catch(error => {
            console.error('Error fetching IC details:', error);
            document.getElementById('icModalBody').innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Error loading IC details: ${error.message}
                </div>
            `;
        });
}

function displayICDetails(icData) {
    document.getElementById('icModalTitle').innerHTML = 
        `<i class="fas fa-microchip me-2"></i>${icData.type} - ${icData.description}`;
    
    const modalBody = document.getElementById('icModalBody');
    
    let pinoutHtml = '';
    if (icData.pinout) {
        pinoutHtml = `
            <div class="mt-3">
                <h6><i class="fas fa-sitemap me-2"></i>Pinout Diagram</h6>
                <div class="pinout-diagram">${icData.pinout}</div>
            </div>
        `;
    }
    
    modalBody.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <h6><i class="fas fa-info-circle me-2"></i>Specifications</h6>
                <table class="table table-sm">
                    <tr><td><strong>Type:</strong></td><td>${icData.type}</td></tr>
                    <tr><td><strong>Package:</strong></td><td>${icData.package}</td></tr>
                    <tr><td><strong>Pins:</strong></td><td>${icData.pins}</td></tr>
                    <tr><td><strong>Gates:</strong></td><td>${icData.gates || 'N/A'}</td></tr>
                    <tr><td><strong>Powered:</strong></td><td>
                        <span class="badge ${icData.powered ? 'bg-success' : 'bg-danger'}">
                            ${icData.powered ? 'Yes' : 'No'}
                        </span>
                    </td></tr>
                </table>
            </div>
            <div class="col-md-6">
                <h6><i class="fas fa-microchip me-2"></i>IC Visualization</h6>
                <div class="text-center p-3 border rounded">
                    <div class="ic-visual">
                        <i class="fas fa-microchip fa-4x text-primary mb-2"></i>
                        <div class="small text-muted">${icData.description}</div>
                    </div>
                </div>
                
                <div class="mt-3">
                    <button class="btn btn-success btn-sm w-100 mb-2" onclick="testCurrentIC()">
                        <i class="fas fa-check-circle me-2"></i>Test IC
                    </button>
                    <button class="btn btn-info btn-sm w-100" onclick="showPinout()">
                        <i class="fas fa-sitemap me-2"></i>View Pinout
                    </button>
                </div>
            </div>
        </div>
        ${pinoutHtml}
    `;
}

function testCurrentIC() {
    if (!currentIC) return;
    
    const testButton = event.target;
    testButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Testing...';
    testButton.disabled = true;
    
    fetch(`/api/ic/${currentIC}/test`)
        .then(response => response.json())
        .then(data => {
            const resultClass = data.test_passed ? 'success' : 'danger';
            const resultIcon = data.test_passed ? 'check-circle' : 'times-circle';
            const resultText = data.test_passed ? 'PASS' : 'FAIL';
            
            // Show test result
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${resultClass} mt-3`;
            alertDiv.innerHTML = `
                <i class="fas fa-${resultIcon} me-2"></i>
                <strong>Test Result:</strong> ${resultText}
                <div class="small mt-1">Tested at: ${new Date(data.timestamp).toLocaleString()}</div>
            `;
            
            document.getElementById('icModalBody').appendChild(alertDiv);
            
            // Reset button
            testButton.innerHTML = '<i class="fas fa-check-circle me-2"></i>Test IC';
            testButton.disabled = false;
        })
        .catch(error => {
            console.error('Error testing IC:', error);
            testButton.innerHTML = '<i class="fas fa-check-circle me-2"></i>Test IC';
            testButton.disabled = false;
        });
}

function showPinout() {
    if (!currentIC) return;
    
    fetch(`/api/ic/${currentIC}/pinout`)
        .then(response => response.json())
        .then(data => {
            const pinoutModal = document.createElement('div');
            pinoutModal.className = 'modal fade';
            pinoutModal.innerHTML = `
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-sitemap me-2"></i>${data.type} Pinout
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="pinout-diagram">${data.pinout}</div>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(pinoutModal);
            const modal = new bootstrap.Modal(pinoutModal);
            modal.show();
            
            // Clean up modal after hide
            pinoutModal.addEventListener('hidden.bs.modal', function() {
                document.body.removeChild(pinoutModal);
            });
        })
        .catch(error => {
            console.error('Error fetching pinout:', error);
        });
}

function simulateCurrentIC() {
    if (!currentIC) return;
    
    // Close the details modal and redirect to simulator
    const modal = bootstrap.Modal.getInstance(document.getElementById('icDetailsModal'));
    modal.hide();
    
    // Store the IC type for the simulator
    sessionStorage.setItem('selectedIC', currentIC);
    
    // Navigate to simulator
    window.location.href = '/simulator';
}

function showStats() {
    const modal = new bootstrap.Modal(document.getElementById('statsModal'));
    modal.show();
}

// Initialize socket connection for real-time features
function initializeSocket() {
    socket = io();
    
    socket.on('connect', function() {
        console.log('Connected to server');
        updateConnectionStatus('connected');
    });
    
    socket.on('disconnect', function() {
        console.log('Disconnected from server');
        updateConnectionStatus('disconnected');
    });
    
    socket.on('error', function(data) {
        console.error('Server error:', data.message);
        addToLog(`Error: ${data.message}`, 'error');
    });
    
    socket.on('connected', function(data) {
        console.log('Server says:', data.message);
        addToLog(data.message, 'info');
    });
}

function updateConnectionStatus(status) {
    const statusEl = document.getElementById('connectionStatus');
    if (!statusEl) return;
    
    const statusConfig = {
        'connected': {
            class: 'alert-success',
            icon: 'fa-check-circle',
            text: 'Connected to server'
        },
        'disconnected': {
            class: 'alert-danger',
            icon: 'fa-times-circle',
            text: 'Disconnected from server'
        },
        'connecting': {
            class: 'alert-warning',
            icon: 'fa-spinner fa-spin',
            text: 'Connecting to server...'
        }
    };
    
    const config = statusConfig[status] || statusConfig['disconnected'];
    statusEl.className = `alert ${config.class}`;
    statusEl.innerHTML = `<i class="fas ${config.icon} me-2"></i>${config.text}`;
}

function addToLog(message, type = 'info') {
    const logEl = document.getElementById('simulationLog');
    if (!logEl) return;
    
    const timestamp = new Date().toLocaleTimeString();
    const typeConfig = {
        'info': { class: 'text-info', icon: 'fa-info-circle' },
        'success': { class: 'text-success', icon: 'fa-check-circle' },
        'warning': { class: 'text-warning', icon: 'fa-exclamation-triangle' },
        'error': { class: 'text-danger', icon: 'fa-times-circle' }
    };
    
    const config = typeConfig[type] || typeConfig['info'];
    
    const logEntry = document.createElement('div');
    logEntry.className = `${config.class} mb-1`;
    logEntry.innerHTML = `
        <span class="text-muted">[${timestamp}]</span>
        <i class="fas ${config.icon} me-1"></i>
        ${message}
    `;
    
    logEl.appendChild(logEntry);
    logEl.scrollTop = logEl.scrollHeight;
    
    // Keep only last 100 entries
    while (logEl.children.length > 100) {
        logEl.removeChild(logEl.firstChild);
    }
}

// Utility functions
function formatBinary(value, bits = 8) {
    return value.toString(2).padStart(bits, '0');
}

function formatHex(value, bits = 8) {
    const hex = value.toString(16).toUpperCase();
    return '0x' + hex.padStart(Math.ceil(bits / 4), '0');
}

function generateRandomInputs(count) {
    return Array.from({ length: count }, () => Math.random() < 0.5 ? 1 : 0);
}

// Export functions for use in other modules
window.DLD = {
    showICDetails,
    simulateCurrentIC,
    showStats,
    testCurrentIC,
    showPinout,
    addToLog,
    formatBinary,
    formatHex,
    generateRandomInputs
};
