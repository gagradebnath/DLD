// Digital Logic Design IC Library - Circuit Designer JavaScript

let components = new Map();
let wires = [];
let selectedComponent = null;
let currentTool = 'select';
let zoomLevel = 1;
let panOffset = { x: 0, y: 0 };
let isDragging = false;
let isConnecting = false;
let connectionStart = null;

// Initialize circuit designer
document.addEventListener('DOMContentLoaded', function() {
    initializeDesigner();
});

function initializeDesigner() {
    setupCanvas();
    setupEventListeners();
    updateCircuitProperties();
    
    console.log('Circuit Designer initialized');
}

function setupCanvas() {
    const canvas = document.getElementById('designCanvas');
    const svg = document.getElementById('designSVG');
    
    // Make canvas interactive
    canvas.addEventListener('click', handleCanvasClick);
    canvas.addEventListener('mousedown', handleMouseDown);
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mouseup', handleMouseUp);
    canvas.addEventListener('wheel', handleWheel);
    
    // Prevent context menu
    canvas.addEventListener('contextmenu', e => e.preventDefault());
}

function setupEventListeners() {
    // Tool selection
    document.addEventListener('keydown', handleKeyDown);
    
    // Grid snap toggle
    document.getElementById('gridSnap').addEventListener('change', function() {
        addToDesignLog(`Grid snap ${this.checked ? 'enabled' : 'disabled'}`, 'info');
    });
    
    // Auto-route toggle
    document.getElementById('autoRoute').addEventListener('change', function() {
        addToDesignLog(`Auto-routing ${this.checked ? 'enabled' : 'disabled'}`, 'info');
    });
}

function addComponent(type) {
    currentTool = 'place';
    selectedComponent = type;
    
    // Hide welcome message
    const welcomeMsg = document.getElementById('welcome-designer');
    if (welcomeMsg) {
        welcomeMsg.style.display = 'none';
    }
    
    // Change cursor to indicate placement mode
    document.getElementById('designCanvas').style.cursor = 'crosshair';
    
    addToDesignLog(`Selected ${type} for placement`, 'info');
}

function handleCanvasClick(event) {
    const rect = event.target.getBoundingClientRect();
    const x = (event.clientX - rect.left) / zoomLevel - panOffset.x;
    const y = (event.clientY - rect.top) / zoomLevel - panOffset.y;
    
    if (currentTool === 'place' && selectedComponent) {
        placeComponent(selectedComponent, x, y);
        currentTool = 'select';
        selectedComponent = null;
        document.getElementById('designCanvas').style.cursor = 'default';
    }
}

function placeComponent(type, x, y) {
    const componentId = `${type}_${Date.now()}`;
    
    // Snap to grid if enabled
    if (document.getElementById('gridSnap').checked) {
        x = Math.round(x / 20) * 20;
        y = Math.round(y / 20) * 20;
    }
    
    const component = {
        id: componentId,
        type: type,
        x: x,
        y: y,
        inputs: getComponentInputs(type),
        outputs: getComponentOutputs(type),
        properties: getDefaultProperties(type)
    };
    
    components.set(componentId, component);
    renderComponent(component);
    updateCircuitProperties();
    
    addToDesignLog(`Placed ${type} at (${Math.round(x)}, ${Math.round(y)})`, 'success');
}

function getComponentInputs(type) {
    const inputMap = {
        'AND': 2,
        'OR': 2,
        'NOT': 1,
        'NAND': 2,
        'NOR': 2,
        'XOR': 2,
        'INPUT': 0,
        'OUTPUT': 1,
        'CLOCK': 0,
        'GROUND': 0,
        'VCC': 0,
        '74138': 6,
        '74151': 11,
        '74147': 10,
        '74157': 9
    };
    
    return inputMap[type] || 2;
}

function getComponentOutputs(type) {
    const outputMap = {
        'AND': 1,
        'OR': 1,
        'NOT': 1,
        'NAND': 1,
        'NOR': 1,
        'XOR': 1,
        'INPUT': 1,
        'OUTPUT': 0,
        'CLOCK': 1,
        'GROUND': 1,
        'VCC': 1,
        '74138': 8,
        '74151': 2,
        '74147': 4,
        '74157': 4
    };
    
    return outputMap[type] || 1;
}

function getDefaultProperties(type) {
    return {
        label: type,
        propagationDelay: getTypicalDelay(type),
        powerConsumption: getTypicalPower(type)
    };
}

function getTypicalDelay(type) {
    const delayMap = {
        'AND': 10,
        'OR': 10,
        'NOT': 5,
        'NAND': 8,
        'NOR': 8,
        'XOR': 15,
        'INPUT': 0,
        'OUTPUT': 0,
        'CLOCK': 0,
        'GROUND': 0,
        'VCC': 0,
        '74138': 22,
        '74151': 13,
        '74147': 23,
        '74157': 12
    };
    
    return delayMap[type] || 10;
}

function getTypicalPower(type) {
    const powerMap = {
        'AND': 10,
        'OR': 10,
        'NOT': 5,
        'NAND': 8,
        'NOR': 8,
        'XOR': 12,
        'INPUT': 0,
        'OUTPUT': 2,
        'CLOCK': 15,
        'GROUND': 0,
        'VCC': 0,
        '74138': 60,
        '74151': 45,
        '74147': 75,
        '74157': 50
    };
    
    return powerMap[type] || 10;
}

function renderComponent(component) {
    const svg = document.getElementById('designSVG');
    const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    group.setAttribute('id', component.id);
    group.setAttribute('transform', `translate(${component.x}, ${component.y})`);
    group.style.cursor = 'move';
    
    // Component background
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('width', getComponentWidth(component.type));
    rect.setAttribute('height', getComponentHeight(component.type));
    rect.setAttribute('fill', getComponentColor(component.type));
    rect.setAttribute('stroke', '#333');
    rect.setAttribute('stroke-width', '2');
    rect.setAttribute('rx', '5');
    group.appendChild(rect);
    
    // Component label
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', getComponentWidth(component.type) / 2);
    text.setAttribute('y', getComponentHeight(component.type) / 2 + 5);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('font-family', 'Arial, sans-serif');
    text.setAttribute('font-size', '12');
    text.setAttribute('fill', '#333');
    text.textContent = component.type;
    group.appendChild(text);
    
    // Input pins
    for (let i = 0; i < component.inputs; i++) {
        const pin = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        const pinY = 15 + (i * 20);
        pin.setAttribute('cx', '0');
        pin.setAttribute('cy', pinY);
        pin.setAttribute('r', '4');
        pin.setAttribute('fill', '#4CAF50');
        pin.setAttribute('stroke', '#333');
        pin.setAttribute('stroke-width', '1');
        pin.setAttribute('data-pin-type', 'input');
        pin.setAttribute('data-pin-index', i);
        pin.style.cursor = 'crosshair';
        group.appendChild(pin);
    }
    
    // Output pins
    const componentWidth = getComponentWidth(component.type);
    for (let i = 0; i < component.outputs; i++) {
        const pin = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        const pinY = 15 + (i * 20);
        pin.setAttribute('cx', componentWidth);
        pin.setAttribute('cy', pinY);
        pin.setAttribute('r', '4');
        pin.setAttribute('fill', '#FF9800');
        pin.setAttribute('stroke', '#333');
        pin.setAttribute('stroke-width', '1');
        pin.setAttribute('data-pin-type', 'output');
        pin.setAttribute('data-pin-index', i);
        pin.style.cursor = 'crosshair';
        group.appendChild(pin);
    }
    
    // Add event listeners
    group.addEventListener('mousedown', (e) => handleComponentMouseDown(e, component.id));
    group.addEventListener('dblclick', (e) => editComponentProperties(component.id));
    
    // Add pin click handlers
    group.querySelectorAll('circle').forEach(pin => {
        pin.addEventListener('click', (e) => handlePinClick(e, component.id));
    });
    
    svg.appendChild(group);
}

function getComponentWidth(type) {
    const widthMap = {
        'INPUT': 40,
        'OUTPUT': 40,
        'CLOCK': 50,
        'GROUND': 30,
        'VCC': 30,
        '74138': 100,
        '74151': 100,
        '74147': 100,
        '74157': 100
    };
    
    return widthMap[type] || 60;
}

function getComponentHeight(type) {
    const heightMap = {
        'INPUT': 30,
        'OUTPUT': 30,
        'CLOCK': 30,
        'GROUND': 20,
        'VCC': 20,
        '74138': 120,
        '74151': 160,
        '74147': 140,
        '74157': 120
    };
    
    return heightMap[type] || 40;
}

function getComponentColor(type) {
    const colorMap = {
        'AND': '#E3F2FD',
        'OR': '#E8F5E8',
        'NOT': '#FFF3E0',
        'NAND': '#F3E5F5',
        'NOR': '#E1F5FE',
        'XOR': '#FCE4EC',
        'INPUT': '#C8E6C9',
        'OUTPUT': '#FFCDD2',
        'CLOCK': '#D1C4E9',
        'GROUND': '#BDBDBD',
        'VCC': '#FFAB91',
        '74138': '#B39DDB',
        '74151': '#81C784',
        '74147': '#FFB74D',
        '74157': '#F48FB1'
    };
    
    return colorMap[type] || '#F5F5F5';
}

function handleComponentMouseDown(event, componentId) {
    event.stopPropagation();
    selectedComponent = componentId;
    isDragging = true;
    
    const component = components.get(componentId);
    if (component) {
        const rect = event.target.closest('svg').getBoundingClientRect();
        component.dragOffset = {
            x: (event.clientX - rect.left) / zoomLevel - component.x,
            y: (event.clientY - rect.top) / zoomLevel - component.y
        };
    }
}

function handlePinClick(event, componentId) {
    event.stopPropagation();
    
    const pin = event.target;
    const pinType = pin.getAttribute('data-pin-type');
    const pinIndex = parseInt(pin.getAttribute('data-pin-index'));
    
    const pinInfo = {
        componentId: componentId,
        type: pinType,
        index: pinIndex,
        element: pin
    };
    
    if (!isConnecting) {
        // Start connection
        isConnecting = true;
        connectionStart = pinInfo;
        pin.setAttribute('fill', '#2196F3');
        addToDesignLog(`Starting connection from ${componentId}:${pinType}${pinIndex}`, 'info');
    } else {
        // Complete connection
        if (connectionStart.componentId !== componentId && 
            connectionStart.type !== pinType) {
            createWire(connectionStart, pinInfo);
        } else {
            addToDesignLog('Invalid connection - cannot connect same component or same pin types', 'warning');
        }
        
        // Reset connection state
        isConnecting = false;
        connectionStart.element.setAttribute('fill', connectionStart.type === 'input' ? '#4CAF50' : '#FF9800');
        connectionStart = null;
    }
}

function createWire(startPin, endPin) {
    const wireId = `wire_${Date.now()}`;
    
    const wire = {
        id: wireId,
        start: startPin,
        end: endPin,
        active: false
    };
    
    wires.push(wire);
    renderWire(wire);
    updateCircuitProperties();
    
    addToDesignLog(`Connected ${startPin.componentId}:${startPin.type}${startPin.index} to ${endPin.componentId}:${endPin.type}${endPin.index}`, 'success');
}

function renderWire(wire) {
    const svg = document.getElementById('designSVG');
    
    // Get pin positions
    const startPos = getPinPosition(wire.start);
    const endPos = getPinPosition(wire.end);
    
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('id', wire.id);
    line.setAttribute('x1', startPos.x);
    line.setAttribute('y1', startPos.y);
    line.setAttribute('x2', endPos.x);
    line.setAttribute('y2', endPos.y);
    line.setAttribute('stroke', '#2196F3');
    line.setAttribute('stroke-width', '2');
    line.style.cursor = 'pointer';
    
    // Add click handler for wire selection/deletion
    line.addEventListener('click', (e) => selectWire(wire.id));
    line.addEventListener('dblclick', (e) => deleteWire(wire.id));
    
    svg.appendChild(line);
}

function getPinPosition(pin) {
    const component = components.get(pin.componentId);
    const componentElement = document.getElementById(pin.componentId);
    
    if (!component || !componentElement) {
        return { x: 0, y: 0 };
    }
    
    const pinY = 15 + (pin.index * 20);
    const pinX = pin.type === 'input' ? 0 : getComponentWidth(component.type);
    
    return {
        x: component.x + pinX,
        y: component.y + pinY
    };
}

function handleMouseDown(event) {
    if (event.target.id === 'designSVG' || event.target.id === 'designCanvas') {
        // Start panning
        isDragging = true;
        panOffset.startX = event.clientX - panOffset.x;
        panOffset.startY = event.clientY - panOffset.y;
    }
}

function handleMouseMove(event) {
    if (isDragging && selectedComponent && components.has(selectedComponent)) {
        // Move selected component
        const component = components.get(selectedComponent);
        const rect = event.target.closest('svg').getBoundingClientRect();
        
        let newX = (event.clientX - rect.left) / zoomLevel - component.dragOffset.x;
        let newY = (event.clientY - rect.top) / zoomLevel - component.dragOffset.y;
        
        // Snap to grid if enabled
        if (document.getElementById('gridSnap').checked) {
            newX = Math.round(newX / 20) * 20;
            newY = Math.round(newY / 20) * 20;
        }
        
        component.x = newX;
        component.y = newY;
        
        const element = document.getElementById(component.id);
        element.setAttribute('transform', `translate(${newX}, ${newY})`);
        
        // Update connected wires
        updateWiresForComponent(component.id);
    }
}

function handleMouseUp(event) {
    isDragging = false;
    selectedComponent = null;
}

function handleWheel(event) {
    event.preventDefault();
    
    const scaleFactor = event.deltaY > 0 ? 0.9 : 1.1;
    zoomLevel = Math.max(0.1, Math.min(3, zoomLevel * scaleFactor));
    
    const svg = document.getElementById('designSVG');
    svg.style.transform = `scale(${zoomLevel})`;
}

function handleKeyDown(event) {
    switch (event.key) {
        case 'Delete':
            if (selectedComponent) {
                deleteComponent(selectedComponent);
            }
            break;
        case 'Escape':
            if (isConnecting) {
                isConnecting = false;
                if (connectionStart) {
                    connectionStart.element.setAttribute('fill', 
                        connectionStart.type === 'input' ? '#4CAF50' : '#FF9800');
                    connectionStart = null;
                }
            }
            break;
    }
}

function updateWiresForComponent(componentId) {
    wires.forEach(wire => {
        if (wire.start.componentId === componentId || wire.end.componentId === componentId) {
            const wireElement = document.getElementById(wire.id);
            if (wireElement) {
                const startPos = getPinPosition(wire.start);
                const endPos = getPinPosition(wire.end);
                
                wireElement.setAttribute('x1', startPos.x);
                wireElement.setAttribute('y1', startPos.y);
                wireElement.setAttribute('x2', endPos.x);
                wireElement.setAttribute('y2', endPos.y);
            }
        }
    });
}

function deleteComponent(componentId) {
    const component = components.get(componentId);
    if (!component) return;
    
    // Remove connected wires
    wires = wires.filter(wire => {
        if (wire.start.componentId === componentId || wire.end.componentId === componentId) {
            const wireElement = document.getElementById(wire.id);
            if (wireElement) wireElement.remove();
            return false;
        }
        return true;
    });
    
    // Remove component element
    const element = document.getElementById(componentId);
    if (element) element.remove();
    
    // Remove from components map
    components.delete(componentId);
    
    updateCircuitProperties();
    addToDesignLog(`Deleted component ${componentId}`, 'warning');
}

function deleteWire(wireId) {
    const wireIndex = wires.findIndex(wire => wire.id === wireId);
    if (wireIndex !== -1) {
        const wireElement = document.getElementById(wireId);
        if (wireElement) wireElement.remove();
        
        wires.splice(wireIndex, 1);
        updateCircuitProperties();
        addToDesignLog(`Deleted wire ${wireId}`, 'warning');
    }
}

function selectWire(wireId) {
    // Highlight selected wire
    const wireElement = document.getElementById(wireId);
    if (wireElement) {
        wireElement.setAttribute('stroke', '#FF5722');
        wireElement.setAttribute('stroke-width', '3');
        
        // Reset other wires
        wires.forEach(wire => {
            if (wire.id !== wireId) {
                const element = document.getElementById(wire.id);
                if (element) {
                    element.setAttribute('stroke', '#2196F3');
                    element.setAttribute('stroke-width', '2');
                }
            }
        });
    }
}

function editComponentProperties(componentId) {
    const component = components.get(componentId);
    if (!component) return;
    
    document.getElementById('propertiesModalTitle').innerHTML = 
        `<i class="fas fa-cog me-2"></i>${component.type} Properties`;
    
    const modalBody = document.getElementById('propertiesModalBody');
    modalBody.innerHTML = `
        <div class="mb-3">
            <label class="form-label">Label:</label>
            <input type="text" class="form-control" id="componentLabel" value="${component.properties.label}">
        </div>
        <div class="mb-3">
            <label class="form-label">Propagation Delay (ns):</label>
            <input type="number" class="form-control" id="componentDelay" value="${component.properties.propagationDelay}">
        </div>
        <div class="mb-3">
            <label class="form-label">Power Consumption (mW):</label>
            <input type="number" class="form-control" id="componentPower" value="${component.properties.powerConsumption}">
        </div>
    `;
    
    const modal = new bootstrap.Modal(document.getElementById('componentPropertiesModal'));
    modal.show();
    
    window.currentEditComponent = componentId;
}

function applyComponentProperties() {
    const componentId = window.currentEditComponent;
    const component = components.get(componentId);
    
    if (component) {
        component.properties.label = document.getElementById('componentLabel').value;
        component.properties.propagationDelay = parseFloat(document.getElementById('componentDelay').value);
        component.properties.powerConsumption = parseFloat(document.getElementById('componentPower').value);
        
        // Update component visual
        const element = document.getElementById(componentId);
        const text = element.querySelector('text');
        if (text) {
            text.textContent = component.properties.label;
        }
        
        updateCircuitProperties();
        addToDesignLog(`Updated properties for ${componentId}`, 'info');
    }
    
    const modal = bootstrap.Modal.getInstance(document.getElementById('componentPropertiesModal'));
    modal.hide();
}

function validateCircuit() {
    const issues = [];
    
    // Check for unconnected inputs
    components.forEach((component, id) => {
        if (component.inputs > 0) {
            for (let i = 0; i < component.inputs; i++) {
                const hasConnection = wires.some(wire => 
                    wire.end.componentId === id && wire.end.index === i);
                if (!hasConnection && component.type !== 'INPUT') {
                    issues.push(`${id} input ${i} is not connected`);
                }
            }
        }
    });
    
    // Check for unconnected outputs
    components.forEach((component, id) => {
        if (component.outputs > 0 && component.type !== 'OUTPUT') {
            for (let i = 0; i < component.outputs; i++) {
                const hasConnection = wires.some(wire => 
                    wire.start.componentId === id && wire.start.index === i);
                if (!hasConnection) {
                    issues.push(`${id} output ${i} is not connected`);
                }
            }
        }
    });
    
    if (issues.length === 0) {
        addToDesignLog('Circuit validation passed - no issues found', 'success');
    } else {
        addToDesignLog(`Circuit validation found ${issues.length} issues`, 'warning');
        issues.forEach(issue => addToDesignLog(`  - ${issue}`, 'warning'));
    }
}

function simulateCircuit() {
    addToDesignLog('Starting circuit simulation...', 'info');
    
    // Simple simulation - just propagate signals
    const simulationSteps = 10;
    let step = 0;
    
    const simulate = () => {
        if (step < simulationSteps) {
            // Simulate one step
            wires.forEach(wire => {
                const wireElement = document.getElementById(wire.id);
                if (wireElement) {
                    // Toggle active state for visualization
                    wire.active = !wire.active;
                    wireElement.setAttribute('stroke', wire.active ? '#4CAF50' : '#2196F3');
                }
            });
            
            step++;
            setTimeout(simulate, 200);
        } else {
            // Reset wires
            wires.forEach(wire => {
                const wireElement = document.getElementById(wire.id);
                if (wireElement) {
                    wireElement.setAttribute('stroke', '#2196F3');
                }
            });
            addToDesignLog('Circuit simulation completed', 'success');
        }
    };
    
    simulate();
}

function optimizeCircuit() {
    addToDesignLog('Analyzing circuit for optimization opportunities...', 'info');
    
    // Simple optimization suggestions
    const suggestions = [];
    
    if (components.size > 10) {
        suggestions.push('Consider using complex ICs to reduce component count');
    }
    
    if (wires.length > components.size * 2) {
        suggestions.push('Circuit has many connections - consider using bus structures');
    }
    
    const gateCount = Array.from(components.values()).filter(c => 
        ['AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR'].includes(c.type)).length;
    
    if (gateCount > 6) {
        suggestions.push('Consider consolidating gates into single ICs');
    }
    
    if (suggestions.length === 0) {
        addToDesignLog('Circuit appears to be well optimized', 'success');
    } else {
        addToDesignLog(`Found ${suggestions.length} optimization suggestions:`, 'info');
        suggestions.forEach(suggestion => addToDesignLog(`  - ${suggestion}`, 'info'));
    }
}

function exportCircuit() {
    const circuitData = {
        timestamp: new Date().toISOString(),
        components: Array.from(components.entries()),
        wires: wires,
        properties: {
            componentCount: components.size,
            wireCount: wires.length,
            totalPower: calculateTotalPower(),
            maxDelay: calculateMaxDelay()
        }
    };
    
    const dataStr = JSON.stringify(circuitData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `circuit_design_${Date.now()}.json`;
    link.click();
    
    addToDesignLog('Circuit exported successfully', 'success');
}

function clearDesign() {
    if (confirm('Are you sure you want to clear the entire design?')) {
        // Remove all components
        components.forEach((component, id) => {
            const element = document.getElementById(id);
            if (element) element.remove();
        });
        components.clear();
        
        // Remove all wires
        wires.forEach(wire => {
            const element = document.getElementById(wire.id);
            if (element) element.remove();
        });
        wires = [];
        
        // Show welcome message
        const welcomeMsg = document.getElementById('welcome-designer');
        if (welcomeMsg) {
            welcomeMsg.style.display = 'block';
        }
        
        updateCircuitProperties();
        addToDesignLog('Design cleared', 'warning');
    }
}

function zoomIn() {
    zoomLevel = Math.min(3, zoomLevel * 1.2);
    const svg = document.getElementById('designSVG');
    svg.style.transform = `scale(${zoomLevel})`;
}

function zoomOut() {
    zoomLevel = Math.max(0.1, zoomLevel / 1.2);
    const svg = document.getElementById('designSVG');
    svg.style.transform = `scale(${zoomLevel})`;
}

function resetZoom() {
    zoomLevel = 1;
    panOffset = { x: 0, y: 0 };
    const svg = document.getElementById('designSVG');
    svg.style.transform = 'scale(1)';
}

function updateCircuitProperties() {
    document.getElementById('componentCount').textContent = components.size;
    document.getElementById('wireCount').textContent = wires.length;
    
    const totalPower = calculateTotalPower();
    document.getElementById('powerConsumption').textContent = `${totalPower} mW`;
    
    const maxDelay = calculateMaxDelay();
    document.getElementById('propagationDelay').textContent = `${maxDelay} ns`;
    
    const gateCount = Array.from(components.values()).filter(c => 
        ['AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR'].includes(c.type)).length;
    document.getElementById('gateCount').textContent = gateCount;
    
    // Calculate complexity
    let complexity = 'Low';
    if (components.size > 10 || wires.length > 15) complexity = 'Medium';
    if (components.size > 20 || wires.length > 30) complexity = 'High';
    document.getElementById('complexityScore').textContent = complexity;
}

function calculateTotalPower() {
    return Array.from(components.values())
        .reduce((total, component) => total + component.properties.powerConsumption, 0);
}

function calculateMaxDelay() {
    if (components.size === 0) return 0;
    
    return Math.max(...Array.from(components.values())
        .map(component => component.properties.propagationDelay));
}

function addToDesignLog(message, type = 'info') {
    const logEl = document.getElementById('designLog');
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
