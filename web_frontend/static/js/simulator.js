// Digital Logic Design IC Library - Simulator JavaScript

let activeICs = new Map();
let connections = [];
let selectedPin = null;
let draggedIC = null;
let operationCounter = 0;
let performanceTimer = null;

// Initialize simulator
document.addEventListener('DOMContentLoaded', function() {
    initializeSimulator();
    
    // Check if there's a pre-selected IC from the main page
    const selectedIC = sessionStorage.getItem('selectedIC');
    if (selectedIC) {
        addIC(selectedIC);
        sessionStorage.removeItem('selectedIC');
    }
});

function initializeSimulator() {
    // Initialize socket connection
    if (typeof io !== 'undefined') {
        window.socket = io();
        setupSocketListeners();
    }
    
    // Setup workspace
    setupWorkspace();
    
    // Start performance monitoring
    startPerformanceMonitoring();
    
    console.log('Simulator initialized');
}

function setupSocketListeners() {
    const socket = window.socket;
    
    socket.on('connect', function() {
        updateConnectionStatus('connected');
        addToLog('Connected to simulation server', 'success');
    });
    
    socket.on('disconnect', function() {
        updateConnectionStatus('disconnected');
        addToLog('Disconnected from server', 'warning');
    });
    
    socket.on('ic_created', function(data) {
        createICInstance(data);
        addToLog(`Created ${data.type} (${data.id})`, 'success');
    });
    
    socket.on('gate_result', function(data) {
        updateGateOutput(data);
        operationCounter++;
    });
    
    socket.on('decoder_result', function(data) {
        updateDecoderOutput(data);
        operationCounter++;
    });
    
    socket.on('encoder_result', function(data) {
        updateEncoderOutput(data);
        operationCounter++;
    });
    
    socket.on('multiplexer_result', function(data) {
        updateMultiplexerOutput(data);
        operationCounter++;
    });
    
    socket.on('error', function(data) {
        addToLog(`Error: ${data.message}`, 'error');
    });
}

function setupWorkspace() {
    const workspace = document.getElementById('workspace');
    
    // Make workspace droppable
    workspace.addEventListener('dragover', function(e) {
        e.preventDefault();
    });
    
    workspace.addEventListener('drop', function(e) {
        e.preventDefault();
        // Handle drop events if needed
    });
    
    // Add click handler for deselecting
    workspace.addEventListener('click', function(e) {
        if (e.target === workspace) {
            deselectAll();
        }
    });
}

function addIC(icType) {
    const icId = `${icType}_${Date.now()}`;
    
    if (window.socket) {
        window.socket.emit('create_ic', {
            type: icType,
            id: icId
        });
    } else {
        // Fallback for when socket is not available
        createICInstance({
            id: icId,
            type: icType,
            description: `${icType} IC`,
            pins: 14,
            powered: true
        });
    }
    
    // Hide welcome message
    const welcomeMsg = document.getElementById('welcome-message');
    if (welcomeMsg) {
        welcomeMsg.style.display = 'none';
    }
}

function createICInstance(icData) {
    const workspace = document.getElementById('workspace');
    const icElement = document.createElement('div');
    icElement.className = 'ic-instance';
    icElement.id = icData.id;
    icElement.style.left = (Math.random() * (workspace.clientWidth - 200)) + 'px';
    icElement.style.top = (Math.random() * (workspace.clientHeight - 150)) + 'px';
    
    // Generate pin layout based on IC type
    const pinLayout = generatePinLayout(icData);
    
    icElement.innerHTML = `
        <div class="ic-header">
            ${icData.type}
            <button class="btn btn-sm btn-outline-danger float-end" onclick="removeIC('${icData.id}')" title="Remove IC">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="ic-body">
            ${pinLayout}
        </div>
        <div class="ic-controls mt-2">
            <button class="btn btn-sm btn-primary" onclick="configureIC('${icData.id}')" title="Configure">
                <i class="fas fa-cog"></i>
            </button>
            <button class="btn btn-sm btn-success" onclick="testIC('${icData.id}')" title="Test">
                <i class="fas fa-check"></i>
            </button>
        </div>
    `;
    
    // Make draggable
    makeDraggable(icElement);
    
    // Add to workspace
    workspace.appendChild(icElement);
    
    // Store in active ICs
    activeICs.set(icData.id, {
        ...icData,
        element: icElement,
        pins: generatePinData(icData)
    });
    
    updateStats();
}

function generatePinLayout(icData) {
    const pinCount = icData.pins || 14;
    const pinsPerSide = pinCount / 2;
    
    let leftPins = '';
    let rightPins = '';
    
    for (let i = 1; i <= pinsPerSide; i++) {
        leftPins += `
            <div class="ic-pins">
                <div class="pin input" data-pin="${i}" onclick="selectPin('${icData.id}', ${i})" title="Pin ${i}"></div>
                <span class="pin-label">${i}</span>
                <span class="flex-grow-1"></span>
            </div>
        `;
    }
    
    for (let i = pinCount; i > pinsPerSide; i--) {
        rightPins += `
            <div class="ic-pins">
                <span class="flex-grow-1"></span>
                <span class="pin-label">${i}</span>
                <div class="pin output" data-pin="${i}" onclick="selectPin('${icData.id}', ${i})" title="Pin ${i}"></div>
            </div>
        `;
    }
    
    return `
        <div class="row">
            <div class="col-6">
                ${leftPins}
            </div>
            <div class="col-6">
                ${rightPins}
            </div>
        </div>
    `;
}

function generatePinData(icData) {
    const pins = {};
    const pinCount = icData.pins || 14;
    
    for (let i = 1; i <= pinCount; i++) {
        pins[i] = {
            number: i,
            value: 0,
            type: i <= pinCount/2 ? 'input' : 'output',
            connected: false
        };
    }
    
    return pins;
}

function makeDraggable(element) {
    let isDragging = false;
    let startX, startY, initialX, initialY;
    
    element.addEventListener('mousedown', function(e) {
        if (e.target.classList.contains('pin') || e.target.tagName === 'BUTTON') {
            return;
        }
        
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        initialX = element.offsetLeft;
        initialY = element.offsetTop;
        
        element.classList.add('dragging');
        e.preventDefault();
    });
    
    document.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        
        element.style.left = (initialX + dx) + 'px';
        element.style.top = (initialY + dy) + 'px';
        
        updateConnections();
    });
    
    document.addEventListener('mouseup', function() {
        if (isDragging) {
            isDragging = false;
            element.classList.remove('dragging');
        }
    });
}

function selectPin(icId, pinNumber) {
    const pin = document.querySelector(`#${icId} .pin[data-pin="${pinNumber}"]`);
    
    if (selectedPin) {
        // Create connection if different IC or pin
        if (selectedPin.icId !== icId || selectedPin.pinNumber !== pinNumber) {
            createConnection(selectedPin, { icId, pinNumber, element: pin });
        }
        
        // Deselect previous pin
        document.querySelector(`#${selectedPin.icId} .pin[data-pin="${selectedPin.pinNumber}"]`)
            .classList.remove('selected');
        selectedPin = null;
    } else {
        // Select this pin
        pin.classList.add('selected');
        selectedPin = { icId, pinNumber, element: pin };
    }
}

function createConnection(pin1, pin2) {
    const connection = {
        id: `conn_${Date.now()}`,
        from: pin1,
        to: pin2,
        active: false
    };
    
    connections.push(connection);
    drawConnection(connection);
    updateStats();
    
    addToLog(`Connected ${pin1.icId}:${pin1.pinNumber} to ${pin2.icId}:${pin2.pinNumber}`, 'info');
}

function drawConnection(connection) {
    const workspace = document.getElementById('workspace');
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.className = 'connection-line';
    svg.setAttribute('id', connection.id);
    svg.style.position = 'absolute';
    svg.style.top = '0';
    svg.style.left = '0';
    svg.style.width = '100%';
    svg.style.height = '100%';
    svg.style.pointerEvents = 'none';
    svg.style.zIndex = '1';
    
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    
    const pin1Rect = connection.from.element.getBoundingClientRect();
    const pin2Rect = connection.to.element.getBoundingClientRect();
    const workspaceRect = workspace.getBoundingClientRect();
    
    line.setAttribute('x1', pin1Rect.left + pin1Rect.width/2 - workspaceRect.left);
    line.setAttribute('y1', pin1Rect.top + pin1Rect.height/2 - workspaceRect.top);
    line.setAttribute('x2', pin2Rect.left + pin2Rect.width/2 - workspaceRect.left);
    line.setAttribute('y2', pin2Rect.top + pin2Rect.height/2 - workspaceRect.top);
    
    svg.appendChild(line);
    workspace.appendChild(svg);
}

function updateConnections() {
    connections.forEach(connection => {
        const svgElement = document.getElementById(connection.id);
        if (svgElement) {
            const line = svgElement.querySelector('line');
            const workspace = document.getElementById('workspace');
            
            const pin1Rect = connection.from.element.getBoundingClientRect();
            const pin2Rect = connection.to.element.getBoundingClientRect();
            const workspaceRect = workspace.getBoundingClientRect();
            
            line.setAttribute('x1', pin1Rect.left + pin1Rect.width/2 - workspaceRect.left);
            line.setAttribute('y1', pin1Rect.top + pin1Rect.height/2 - workspaceRect.top);
            line.setAttribute('x2', pin2Rect.left + pin2Rect.width/2 - workspaceRect.left);
            line.setAttribute('y2', pin2Rect.top + pin2Rect.height/2 - workspaceRect.top);
        }
    });
}

function removeIC(icId) {
    const icElement = document.getElementById(icId);
    if (icElement) {
        // Remove connections
        connections = connections.filter(conn => {
            if (conn.from.icId === icId || conn.to.icId === icId) {
                const svgElement = document.getElementById(conn.id);
                if (svgElement) {
                    svgElement.remove();
                }
                return false;
            }
            return true;
        });
        
        // Remove IC element
        icElement.remove();
        
        // Remove from active ICs
        activeICs.delete(icId);
        
        // Emit removal to server
        if (window.socket) {
            window.socket.emit('remove_ic', { id: icId });
        }
        
        updateStats();
        addToLog(`Removed IC ${icId}`, 'warning');
    }
}

function configureIC(icId) {
    const ic = activeICs.get(icId);
    if (!ic) return;
    
    // Generate configuration interface based on IC type
    const configContent = generateConfigInterface(ic);
    
    document.getElementById('configModalTitle').innerHTML = 
        `<i class="fas fa-cog me-2"></i>Configure ${ic.type}`;
    document.getElementById('configModalBody').innerHTML = configContent;
    
    const modal = new bootstrap.Modal(document.getElementById('icConfigModal'));
    modal.show();
    
    // Store current IC for configuration
    window.currentConfigIC = icId;
}

function generateConfigInterface(ic) {
    let interface = '';
    
    // Common controls
    interface += `
        <div class="row mb-3">
            <div class="col-md-6">
                <label class="form-label">IC Type:</label>
                <input type="text" class="form-control" value="${ic.type}" readonly>
            </div>
            <div class="col-md-6">
                <label class="form-label">Power Status:</label>
                <select class="form-control" id="powerStatus">
                    <option value="1" ${ic.powered ? 'selected' : ''}>Powered</option>
                    <option value="0" ${!ic.powered ? 'selected' : ''}>Unpowered</option>
                </select>
            </div>
        </div>
    `;
    
    // Type-specific controls
    if (ic.type.includes('740') && ic.type.length === 4) {
        // Logic gates
        interface += generateGateControls(ic);
    } else if (ic.type.includes('7413') || ic.type.includes('7414')) {
        // Decoders/Encoders
        interface += generateDecoderControls(ic);
    } else if (ic.type.includes('7415')) {
        // Multiplexers
        interface += generateMuxControls(ic);
    }
    
    return interface;
}

function generateGateControls(ic) {
    return `
        <div class="mb-3">
            <h6><i class="fas fa-logic me-2"></i>Gate Testing</h6>
            <div class="row">
                <div class="col-md-6">
                    <label class="form-label">Input A:</label>
                    <select class="form-control" id="inputA">
                        <option value="0">0 (Low)</option>
                        <option value="1">1 (High)</option>
                    </select>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Input B:</label>
                    <select class="form-control" id="inputB">
                        <option value="0">0 (Low)</option>
                        <option value="1">1 (High)</option>
                    </select>
                </div>
            </div>
            <div class="mt-2">
                <button class="btn btn-primary" onclick="simulateGate()">
                    <i class="fas fa-play me-2"></i>Test Gate
                </button>
            </div>
        </div>
    `;
}

function generateDecoderControls(ic) {
    return `
        <div class="mb-3">
            <h6><i class="fas fa-code me-2"></i>Decoder Testing</h6>
            <p class="small text-muted">Enter address bits to decode:</p>
            <div class="row">
                <div class="col-4">
                    <label class="form-label">A2:</label>
                    <select class="form-control" id="addrA2">
                        <option value="0">0</option>
                        <option value="1">1</option>
                    </select>
                </div>
                <div class="col-4">
                    <label class="form-label">A1:</label>
                    <select class="form-control" id="addrA1">
                        <option value="0">0</option>
                        <option value="1">1</option>
                    </select>
                </div>
                <div class="col-4">
                    <label class="form-label">A0:</label>
                    <select class="form-control" id="addrA0">
                        <option value="0">0</option>
                        <option value="1">1</option>
                    </select>
                </div>
            </div>
            <div class="mt-2">
                <button class="btn btn-primary" onclick="simulateDecoder()">
                    <i class="fas fa-play me-2"></i>Test Decoder
                </button>
            </div>
        </div>
    `;
}

function generateMuxControls(ic) {
    return `
        <div class="mb-3">
            <h6><i class="fas fa-random me-2"></i>Multiplexer Testing</h6>
            <div class="row">
                <div class="col-md-6">
                    <label class="form-label">Select Address:</label>
                    <select class="form-control" id="muxAddress">
                        <option value="0">0</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                    </select>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Data Pattern:</label>
                    <input type="text" class="form-control" id="muxData" placeholder="e.g., 1,0,1,1" value="1,0,1,1">
                </div>
            </div>
            <div class="mt-2">
                <button class="btn btn-primary" onclick="simulateMultiplexer()">
                    <i class="fas fa-play me-2"></i>Test Multiplexer
                </button>
            </div>
        </div>
    `;
}

function simulateGate() {
    const icId = window.currentConfigIC;
    const inputA = parseInt(document.getElementById('inputA').value);
    const inputB = parseInt(document.getElementById('inputB').value);
    
    if (window.socket) {
        window.socket.emit('simulate_gate', {
            id: icId,
            gate: 1,
            inputs: [inputA, inputB]
        });
    }
}

function simulateDecoder() {
    const icId = window.currentConfigIC;
    const a2 = parseInt(document.getElementById('addrA2').value);
    const a1 = parseInt(document.getElementById('addrA1').value);
    const a0 = parseInt(document.getElementById('addrA0').value);
    
    if (window.socket) {
        window.socket.emit('simulate_decoder', {
            id: icId,
            address: [a2, a1, a0],
            enable: [0, 0, 1]
        });
    }
}

function simulateMultiplexer() {
    const icId = window.currentConfigIC;
    const address = parseInt(document.getElementById('muxAddress').value);
    const dataStr = document.getElementById('muxData').value;
    const data = dataStr.split(',').map(x => parseInt(x.trim()));
    
    if (window.socket) {
        window.socket.emit('simulate_multiplexer', {
            id: icId,
            address: address,
            data: data
        });
    }
}

function updateGateOutput(data) {
    addToLog(`Gate ${data.gate} output: ${data.inputs.join(',')} → ${data.output}`, 'success');
    
    // Update visual feedback on IC
    const ic = activeICs.get(data.id);
    if (ic && ic.element) {
        // Flash the IC to show activity
        ic.element.classList.add('pulse');
        setTimeout(() => ic.element.classList.remove('pulse'), 1000);
    }
}

function updateDecoderOutput(data) {
    const activeOutput = data.active_output;
    addToLog(`Decoder output: Address ${data.address.join('')} → Y${activeOutput} active`, 'success');
}

function updateEncoderOutput(data) {
    if (data.decimal_value !== undefined) {
        addToLog(`Encoder output: Input → ${data.decimal_value} (BCD: ${data.bcd_output.join('')})`, 'success');
    } else {
        addToLog(`Encoder output: Code ${data.output_code.join('')}, GS=${data.group_select}`, 'success');
    }
}

function updateMultiplexerOutput(data) {
    addToLog(`Multiplexer output: Address ${data.address} → ${data.output}`, 'success');
}

function testIC(icId) {
    const ic = activeICs.get(icId);
    if (!ic) return;
    
    // Visual feedback
    const testBtn = document.querySelector(`#${icId} .btn-success`);
    testBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    
    // Simulate basic test
    setTimeout(() => {
        const passed = Math.random() > 0.1; // 90% pass rate
        const resultClass = passed ? 'text-success' : 'text-danger';
        const resultIcon = passed ? 'fa-check' : 'fa-times';
        
        testBtn.innerHTML = `<i class="fas ${resultIcon}"></i>`;
        testBtn.className = `btn btn-sm ${passed ? 'btn-success' : 'btn-danger'}`;
        
        addToLog(`Test ${ic.type}: ${passed ? 'PASS' : 'FAIL'}`, passed ? 'success' : 'error');
        
        // Reset button after delay
        setTimeout(() => {
            testBtn.innerHTML = '<i class="fas fa-check"></i>';
            testBtn.className = 'btn btn-sm btn-success';
        }, 2000);
    }, 1000);
}

function runAllTests() {
    addToLog('Running comprehensive test suite...', 'info');
    
    let passCount = 0;
    let totalCount = activeICs.size;
    
    activeICs.forEach((ic, icId) => {
        setTimeout(() => {
            testIC(icId);
            passCount++;
            
            if (passCount === totalCount) {
                addToLog(`Test suite complete: ${passCount}/${totalCount} ICs tested`, 'success');
            }
        }, passCount * 500);
    });
}

function clearWorkspace() {
    if (confirm('Are you sure you want to clear the workspace?')) {
        // Remove all ICs
        activeICs.forEach((ic, icId) => {
            removeIC(icId);
        });
        
        // Clear connections
        connections = [];
        
        // Show welcome message
        const welcomeMsg = document.getElementById('welcome-message');
        if (welcomeMsg) {
            welcomeMsg.style.display = 'block';
        }
        
        addToLog('Workspace cleared', 'warning');
    }
}

function exportResults() {
    const results = {
        timestamp: new Date().toISOString(),
        activeICs: Array.from(activeICs.keys()),
        connections: connections.length,
        operations: operationCounter
    };
    
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `dld_simulation_${Date.now()}.json`;
    link.click();
    
    addToLog('Results exported successfully', 'success');
}

function toggleFullscreen() {
    const workspace = document.getElementById('workspace');
    if (document.fullscreenElement) {
        document.exitFullscreen();
    } else {
        workspace.requestFullscreen();
    }
}

function deselectAll() {
    if (selectedPin) {
        document.querySelector(`#${selectedPin.icId} .pin[data-pin="${selectedPin.pinNumber}"]`)
            .classList.remove('selected');
        selectedPin = null;
    }
    
    // Remove selected class from all ICs
    document.querySelectorAll('.ic-instance.selected').forEach(el => {
        el.classList.remove('selected');
    });
}

function updateStats() {
    document.getElementById('activeICCount').textContent = activeICs.size;
    document.getElementById('connectionCount').textContent = connections.length;
}

function startPerformanceMonitoring() {
    let lastOperationCount = 0;
    
    performanceTimer = setInterval(() => {
        const opsPerSec = operationCounter - lastOperationCount;
        document.getElementById('operationsPerSec').textContent = opsPerSec;
        lastOperationCount = operationCounter;
    }, 1000);
}

function updateConnectionStatus(status) {
    const statusEl = document.getElementById('connectionStatus');
    if (!statusEl) return;
    
    const statusConfig = {
        'connected': {
            class: 'alert-success',
            icon: 'fa-check-circle',
            text: 'Connected'
        },
        'disconnected': {
            class: 'alert-danger',
            icon: 'fa-times-circle',
            text: 'Disconnected'
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
    
    // Keep only last 50 entries
    while (logEl.children.length > 50) {
        logEl.removeChild(logEl.firstChild);
    }
}

function applyICConfig() {
    // This would apply configuration changes
    const modal = bootstrap.Modal.getInstance(document.getElementById('icConfigModal'));
    modal.hide();
    
    addToLog('Configuration applied', 'success');
}
