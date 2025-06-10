// Initialize the map and global variables
let map;
let drawnItems;
let drawnPolygon = null;
let environmentalLayers = {};
let heatmapLayer = null;
let legendControl = null;
let activeEnvLayer = null;

// Initialize the map when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    setupVisualizationLayers();
});

// Initialize Leaflet map
function initializeMap() {
    // Create the map centered on India (you can change this to your preferred location)
    map = L.map("map").setView([20.0, 77.0], 5);

    // Add a dark-themed tile layer
    L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // Initialize drawing tools
    drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);
    
    const drawControl = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems,
            edit: true
        },
        draw: {
            polygon: {
                allowIntersection: false,
                drawError: {
                    color: '#e1e100',
                    message: '<strong>Error:</strong> Polygon edges cannot cross!'
                },
                shapeOptions: {
                    color: '#16a32a'
                }
            },
            rectangle: false,
            circle: false,
            polyline: false,
            circlemarker: false,
            marker: false
        }
    });
    
    map.addControl(drawControl);

    // Handle new drawings
    map.on(L.Draw.Event.CREATED, function(e) {
        drawnItems.clearLayers();
        
        const layer = e.layer;
        drawnItems.addLayer(layer);
        
        drawnPolygon = layer.getLatLngs()[0].map(point => [point.lat, point.lng]);
        
        clearVisualizationLayers();
        document.getElementById('predict-button').disabled = false;
    });

    // Handle edited shapes
    map.on(L.Draw.Event.EDITED, function(e) {
        const layers = e.layers;
        layers.eachLayer(function(layer) {
            drawnPolygon = layer.getLatLngs()[0].map(point => [point.lat, point.lng]);
            clearVisualizationLayers();
        });
    });

    // Handle deleted shapes
    map.on(L.Draw.Event.DELETED, function(e) {
        drawnPolygon = null;
        clearVisualizationLayers();
        
        document.getElementById('prediction-results').innerHTML = 
            "<p>Draw a polygon on the map and click \"Get AI Recommendations\" to get crop suggestions.</p>";
        
        document.getElementById('predict-button').disabled = true;
    });
}

// Setup visualization layers (same as before)
function setupVisualizationLayers() {
    const environmentalFactors = {
        'Nitrogen': {
            colorScale: ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026'],
            minValue: 0,
            maxValue: 140,
            unit: 'mg/kg'
        },
        'Phosphorus': {
            colorScale: ['#F7FBFF', '#DEEBF7', '#C6DBEF', '#9ECAE1', '#6BAED6', '#4292C6', '#2171B5', '#084594'],
            minValue: 5,
            maxValue: 145, 
            unit: 'mg/kg'
        },
        'Potassium': {
            colorScale: ['#EFEDF5', '#DADAEB', '#BCBDDC', '#9E9AC8', '#807DBA', '#6A51A3', '#54278F', '#3F007D'],
            minValue: 5,
            maxValue: 205,
            unit: 'mg/kg'
        },
        'Temperature': {
            colorScale: ['#313695', '#4575B4', '#74ADD1', '#ABD9E9', '#FDAE61', '#F46D43', '#D73027', '#A50026'],
            minValue: 8,
            maxValue: 43,
            unit: '°C'
        },
        'Humidity': {
            colorScale: ['#FFFFCC', '#D9F0A3', '#ADDD8E', '#78C679', '#41AB5D', '#238443', '#006837', '#004529'],
            minValue: 14,
            maxValue: 100,
            unit: '%'
        },
        'pH': {
            colorScale: ['#D53E4F', '#FC8D59', '#FEE08B', '#E6F598', '#99D594', '#3288BD'],
            minValue: 3.5,
            maxValue: 9.5,
            unit: ''
        },
        'Rainfall': {
            colorScale: ['#FFFFFF', '#D4E8F2', '#A7D0E4', '#77B7D5', '#4E9BC7', '#2F7EB9', '#1961AC', '#08469C'],
            minValue: 20,
            maxValue: 300,
            unit: 'mm'
        }
    };
    
    for (const factor in environmentalFactors) {
        environmentalLayers[factor] = L.layerGroup();
    }
    
    heatmapLayer = L.layerGroup();
    
    legendControl = L.control({ position: 'bottomright' });
    legendControl.onAdd = function(map) {
        this._div = L.DomUtil.create('div', 'info legend');
        this._div.innerHTML = '<h4>Legend</h4><div id="legend-content">Select a layer to see its legend</div>';
        return this._div;
    };
    legendControl.addTo(map);
    
    // Layer toggle event listeners
    document.getElementById('heatmap-toggle').addEventListener('change', function() {
        if (this.checked) {
            if (heatmapLayer) map.addLayer(heatmapLayer);
            updateLegend('heatmap');
        } else {
            if (heatmapLayer) map.removeLayer(heatmapLayer);
        }
    });
    
    document.getElementById('env-layers-toggle').addEventListener('change', function() {
        if (this.checked) {
            showEnvLayerSelector();
        } else {
            hideEnvLayers();
            const existingSelector = document.getElementById('env-layer-selector');
            if (existingSelector) existingSelector.remove();
        }
    });
}

// Function to predict crop using AI
function predictCrop() {
    if (!drawnPolygon || drawnPolygon.length === 0) {
        alert("Please draw a field area on the map first.");
        return;
    }
    
    // Show loading state
    document.getElementById('prediction-results').innerHTML = '<p>🤖 AI is analyzing the location and environmental data...</p>';
    document.getElementById('predict-button').disabled = true;
    
    // Make the API call
    fetch('/predict_crop', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            polygon_coords: drawnPolygon
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("AI Prediction result:", data);
        
        displayAIPredictionResults(data);
        
        // Update environmental layers
        for (const factor in data.features) {
            updateEnvironmentalLayer(factor, data.features[factor]);
        }
        
        updateCropSuitabilityHeatmap(data.top_predictions);
        document.getElementById('predict-button').disabled = false;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('prediction-results').innerHTML = `<p>❌ Error: ${error.message}</p>`;
        document.getElementById('predict-button').disabled = false;
    });
}

// Function to display AI prediction results
function displayAIPredictionResults(data) {
    const predictionDiv = document.getElementById('prediction-results');
    
    const formatProbability = (prob) => `${(prob * 100).toFixed(1)}%`;
    
    let html = `
        <h3>🤖 AI Recommended Crop: ${data.predicted_crop}</h3>
        <p>AI-powered recommendations based on location and environmental analysis:</p>
    `;
    
    // Add location info if available
    if (data.location_info) {
        html += `
            <div class="location-info">
                <h4>📍 Location Details</h4>
                <p><strong>Region:</strong> ${data.location_info.city}, ${data.location_info.region}, ${data.location_info.country}</p>
                <p><strong>Climate Zone:</strong> ${data.location_info.climate_zone}</p>
            </div>
        `;
    }
    
    // Add top predictions
    html += `<h4>🌾 Top Crop Recommendations</h4>`;
    data.top_predictions.forEach((pred, index) => {
        html += `
            <div class="prediction-item">
                <span>${index + 1}. ${pred[0]}</span>
                <span class="prediction-probability">${formatProbability(pred[1])}</span>
            </div>
        `;
    });
    
    // Add AI reasoning if available
    if (data.ai_reasoning && Array.isArray(data.ai_reasoning)) {
        html += `
            <details class="ai-reasoning">
                <summary>🧠 AI Analysis & Reasoning</summary>
                <div class="reasoning-content">
        `;
        
        data.ai_reasoning.forEach((reasoning, index) => {
            html += `
                <div class="reasoning-item">
                    <h5>${reasoning.crop}</h5>
                    <p><strong>Suitability:</strong> ${reasoning.suitability}%</p>
                    <p><strong>Reason:</strong> ${reasoning.reason}</p>
                </div>
            `;
        });
        
        html += `
                </div>
            </details>
        `;
    }
    
    // Add environmental features details
    html += `
        <details class="features-details">
            <summary>🌡️ Environmental Factors</summary>
            <div class="env-factors">
                <table>
                    <tr>
                        <th>Factor</th>
                        <th>Value</th>
                        <th>Optimal Range</th>
                    </tr>
    `;
    
    for (const factor in data.features) {
        const value = data.features[factor];
        let optimalRange;
        
        switch(factor) {
            case 'Nitrogen':
                optimalRange = '80-120 mg/kg';
                break;
            case 'Phosphorus':
                optimalRange = '60-100 mg/kg';
                break;
            case 'Potassium':
                optimalRange = '80-150 mg/kg';
                break;
            case 'Temperature':
                optimalRange = '20-30 °C';
                break;
            case 'Humidity':
                optimalRange = '60-80 %';
                break;
            case 'pH':
                optimalRange = '6.0-7.5';
                break;
            case 'Rainfall':
                optimalRange = '80-200 mm';
                break;
            default:
                optimalRange = 'Variable';
        }
        
        html += `
            <tr>
                <td>${factor}</td>
                <td>${value.toFixed(2)} ${getUnitForFactor(factor)}</td>
                <td>${optimalRange}</td>
            </tr>
        `;
    }
    
    html += `
                </table>
            </div>
        </details>
        
        <details class="farming-tips">
            <summary>💡 AI Farming Tips for ${data.predicted_crop}</summary>
            <div class="tips-content">
                ${generateFarmingTips(data.predicted_crop)}
            </div>
        </details>
    `;
    
    predictionDiv.innerHTML = html;
}

// Keep all other existing functions (updateEnvironmentalLayer, clearVisualizationLayers, etc.)
// ... [Rest of the functions remain the same as in the original code]

// Updated functions from original code
function clearVisualizationLayers() {
    if (heatmapLayer) {
        heatmapLayer.clearLayers();
        map.removeLayer(heatmapLayer);
    }
    
    for (const factor in environmentalLayers) {
        if (environmentalLayers[factor]) {
            environmentalLayers[factor].clearLayers();
            map.removeLayer(environmentalLayers[factor]);
        }
    }
    
    document.getElementById('heatmap-toggle').checked = true;
    document.getElementById('env-layers-toggle').checked = false;
    
    const existingSelector = document.getElementById('env-layer-selector');
    if (existingSelector) existingSelector.remove();
    
    document.getElementById('legend-content').innerHTML = 'Select a layer to see its legend';
}

function showEnvLayerSelector() {
    const existingSelector = document.getElementById('env-layer-selector');
    if (existingSelector) existingSelector.remove();
    
    const selectorDiv = document.createElement('div');
    selectorDiv.id = 'env-layer-selector';
    selectorDiv.style.marginTop = '10px';
    
    const selector = document.createElement('select');
    selector.style.width = '100%';
    selector.style.padding = '5px';
    selector.style.backgroundColor = '#1a1a1a';
    selector.style.color = '#e0e0e0';
    selector.style.border = '1px solid #333333';
    selector.style.borderRadius = '4px';
    
    const defaultOption = document.createElement('option');
    defaultOption.value = "";
    defaultOption.text = "Select environmental factor";
    selector.appendChild(defaultOption);
    
    for (const factor in environmentalLayers) {
        const option = document.createElement('option');
        option.value = factor;
        option.text = factor;
        selector.appendChild(option);
    }
    
    selector.addEventListener('change', function() {
        hideEnvLayers();
        
        if (this.value) {
            activeEnvLayer = this.value;
            map.addLayer(environmentalLayers[this.value]);
            updateLegend(this.value);
        }
    });
    
    selectorDiv.appendChild(selector);
    document.getElementById('layer-controls').appendChild(selectorDiv);
}

function hideEnvLayers() {
    for (const factor in environmentalLayers) {
        map.removeLayer(environmentalLayers[factor]);
    }
    activeEnvLayer = null;
}

function updateLegend(layerType) {
    const legendContent = document.getElementById('legend-content');
    
    if (layerType === 'heatmap') {
        let legendHTML = `<h4>Crop Suitability</h4>
            <div class="legend-item">
                <i style="background: linear-gradient(to right, blue, cyan, lime, yellow, red)"></i>
                <span>Low to High Suitability</span>
            </div>`;
        legendContent.innerHTML = legendHTML;
    } else {
        // Keep existing environmental factor legend logic
        const factorConfig = {
            'Nitrogen': {
                colorScale: ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026'],
                minValue: 0,
                maxValue: 140,
                unit: 'mg/kg'
            },
            'Phosphorus': {
                colorScale: ['#F7FBFF', '#DEEBF7', '#C6DBEF', '#9ECAE1', '#6BAED6', '#4292C6', '#2171B5', '#084594'],
                minValue: 5,
                maxValue: 145, 
                unit: 'mg/kg'
            },
            'Potassium': {
                colorScale: ['#EFEDF5', '#DADAEB', '#BCBDDC', '#9E9AC8', '#807DBA', '#6A51A3', '#54278F', '#3F007D'],
                minValue: 5,
                maxValue: 205,
                unit: 'mg/kg'
            },
            'Temperature': {
                colorScale: ['#313695', '#4575B4', '#74ADD1', '#ABD9E9', '#FDAE61', '#F46D43', '#D73027', '#A50026'],
                minValue: 8,
                maxValue: 43,
                unit: '°C'
            },
            'Humidity': {
                colorScale: ['#FFFFCC', '#D9F0A3', '#ADDD8E', '#78C679', '#41AB5D', '#238443', '#006837', '#004529'],
                minValue: 14,
                maxValue: 100,
                unit: '%'
            },
            'pH': {
                colorScale: ['#D53E4F', '#FC8D59', '#FEE08B', '#E6F598', '#99D594', '#3288BD'],
                minValue: 3.5,
                maxValue: 9.5,
                unit: ''
            },
            'Rainfall': {
                colorScale: ['#FFFFFF', '#D4E8F2', '#A7D0E4', '#77B7D5', '#4E9BC7', '#2F7EB9', '#1961AC', '#08469C'],
                minValue: 20,
                maxValue: 300,
                unit: 'mm'
            }
        };
        
        const { colorScale, minValue, maxValue, unit } = factorConfig[layerType];
        const step = (maxValue - minValue) / (colorScale.length - 1);
        
        let legendHTML = `<h4>${layerType}</h4>`;
        
        for (let i = 0; i < colorScale.length; i++) {
            const rangeStart = minValue + (i * step);
            const rangeEnd = i < colorScale.length - 1 ? minValue + ((i + 1) * step) : maxValue;
            
            legendHTML += `
                <div class="legend-item">
                    <i style="background:${colorScale[i]}"></i>
                    ${Math.round(rangeStart * 10) / 10} – ${Math.round(rangeEnd * 10) / 10} ${unit}
                </div>
            `;
        }
        
        legendContent.innerHTML = legendHTML;
    }
}

function updateEnvironmentalLayer(factor, data) {
    environmentalLayers[factor].clearLayers();
    
    const factorConfig = {
        'Nitrogen': {
            colorScale: ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026'],
            minValue: 0,
            maxValue: 140,
            unit: 'mg/kg'
        },
        'Phosphorus': {
            colorScale: ['#F7FBFF', '#DEEBF7', '#C6DBEF', '#9ECAE1', '#6BAED6', '#4292C6', '#2171B5', '#084594'],
            minValue: 5,
            maxValue: 145, 
            unit: 'mg/kg'
        },
        'Potassium': {
            colorScale: ['#EFEDF5', '#DADAEB', '#BCBDDC', '#9E9AC8', '#807DBA', '#6A51A3', '#54278F', '#3F007D'],
            minValue: 5,
            maxValue: 205,
            unit: 'mg/kg'
        },
        'Temperature': {
            colorScale: ['#313695', '#4575B4', '#74ADD1', '#ABD9E9', '#FDAE61', '#F46D43', '#D73027', '#A50026'],
            minValue: 8,
            maxValue: 43,
            unit: '°C'
        },
        'Humidity': {
            colorScale: ['#FFFFCC', '#D9F0A3', '#ADDD8E', '#78C679', '#41AB5D', '#238443', '#006837', '#004529'],
            minValue: 14,
            maxValue: 100,
            unit: '%'
        },
        'pH': {
            colorScale: ['#D53E4F', '#FC8D59', '#FEE08B', '#E6F598', '#99D594', '#3288BD'],
            minValue: 3.5,
            maxValue: 9.5,
            unit: ''
        },
        'Rainfall': {
            colorScale: ['#FFFFFF', '#D4E8F2', '#A7D0E4', '#77B7D5', '#4E9BC7', '#2F7EB9', '#1961AC', '#08469C'],
            minValue: 20,
            maxValue: 300,
            unit: 'mm'
        }
    };
    
    function getColor(value, min, max, colorScale) {
        const normalized = Math.min(Math.max((value - min) / (max - min), 0), 0.999);
        const index = Math.floor(normalized * (colorScale.length - 1));
        return colorScale[index];
    }
    
    const baseValue = data;
    const bounds = L.latLngBounds(drawnPolygon);
    const gridSize = 8;
    const latStep = (bounds.getNorth() - bounds.getSouth()) / gridSize;
    const lngStep = (bounds.getEast() - bounds.getWest()) / gridSize;
    
    const polygon = L.polygon(drawnPolygon);
    
    for (let i = 0; i <= gridSize; i++) {
        for (let j = 0; j <= gridSize; j++) {
            const lat = bounds.getSouth() + i * latStep;
            const lng = bounds.getWest() + j * lngStep;
            const point = L.latLng(lat, lng);
            
            if (polygon.getBounds().contains(point) && pointInPolygon(point, drawnPolygon)) {
                const variation = baseValue * 0.2 * (Math.random() - 0.5);
                const value = baseValue + variation;
                
                const color = getColor(
                    value,
                    factorConfig[factor].minValue,
                    factorConfig[factor].maxValue,
                    factorConfig[factor].colorScale
                );
                
                L.circleMarker([lat, lng], {
                    radius: 8,
                    fillColor: color,
                    color: '#333',
                    weight: 1,
                    opacity: 0.8,
                    fillOpacity: 0.7
                })
                .bindPopup(`${factor}: ${value.toFixed(2)} ${factorConfig[factor].unit}`)
                .addTo(environmentalLayers[factor]);
            }
        }
    }
    
    if (activeEnvLayer === factor) {
        map.addLayer(environmentalLayers[factor]);
        updateLegend(factor);
    }
}

function updateCropSuitabilityHeatmap(cropProbabilities) {
    heatmapLayer.clearLayers();
    
    const bounds = L.latLngBounds(drawnPolygon);
    const gridSize = 20;
    const latStep = (bounds.getNorth() - bounds.getSouth()) / gridSize;
    const lngStep = (bounds.getEast() - bounds.getWest()) / gridSize;
    
    const polygon = L.polygon(drawnPolygon);
    
    const heatData = [];
    for (let i = 0; i <= gridSize; i++) {
        for (let j = 0; j <= gridSize; j++) {
            const lat = bounds.getSouth() + i * latStep;
            const lng = bounds.getWest() + j * lngStep;
            const point = L.latLng(lat, lng);
            
            if (polygon.getBounds().contains(point) && pointInPolygon(point, drawnPolygon)) {
                const intensity = 0.7 + (Math.random() * 0.3);
                heatData.push([lat, lng, intensity]);
            }
        }
    }
    
    if (heatData.length > 0) {
        const heat = L.heatLayer(heatData, {
            radius: 25,
            blur: 15,
            maxZoom: 10,
            gradient: {0.4: 'blue', 0.5: 'cyan', 0.6: 'lime', 0.7: 'yellow', 1: 'red'}
        });
        heatmapLayer.addLayer(heat);
        
        if (document.getElementById('heatmap-toggle').checked) {
            map.addLayer(heatmapLayer);
            updateLegend('heatmap');
        }
    }
}

function pointInPolygon(point, polygon) {
    let inside = false;
    const x = point.lat;
    const y = point.lng;
    
    for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
        const xi = polygon[i][0];
        const yi = polygon[i][1];
        const xj = polygon[j][0];
        const yj = polygon[j][1];
        
        const intersect = ((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
    }
    
    return inside;
}

function getUnitForFactor(factor) {
    const units = {
        'Nitrogen': 'mg/kg',
        'Phosphorus': 'mg/kg',
        'Potassium': 'mg/kg',
        'Temperature': '°C',
        'Humidity': '%',
        'pH': '',
        'Rainfall': 'mm'
    };
    
    return units[factor] || '';
}

function generateFarmingTips(crop) {
    const tips = {
        'Rice': `
            <ul>
                <li>Maintain standing water of 5-10 cm during most of the growing period.</li>
                <li>Apply nitrogen fertilizer in split doses.</li>
                <li>Control weeds in the early stages of growth.</li>
                <li>Monitor for rice stem borers and leaf folders.</li>
            </ul>
        `,
        'Wheat': `
            <ul>
                <li>Sow at the optimum time to avoid heat stress during grain filling.</li>
                <li>Ensure adequate irrigation at crown root initiation, tillering, jointing, flowering, and grain filling stages.</li>
                <li>Monitor for rust diseases and aphids.</li>
                <li>Apply nitrogen in split doses for better utilization.</li>
            </ul>
        `,
        'Maize': `
            <ul>
                <li>Plant when soil temperature reaches 12°C for good germination.</li>
                <li>Apply fertilizer in bands 5 cm away from and 5 cm deeper than the seed.</li>
                <li>Maintain soil moisture, especially during tasseling and grain filling.</li>
                <li>Control fall armyworm and stem borers.</li>
            </ul>
        `,
        'Chickpea': `
            <ul>
                <li>Ensure good drainage as the crop is sensitive to waterlogging.</li>
                <li>Inoculate seeds with Rhizobium culture for better nitrogen fixation.</li>
                <li>Monitor for pod borer infestation during flowering and podding stages.</li>
                <li>Avoid excessive irrigation during flowering which can lead to excessive vegetative growth.</li>
            </ul>
        `,
        'Cotton': `
            <ul>
                <li>Plant in well-drained soil with good organic matter content.</li>
                <li>Monitor for bollworm and whitefly infestations.</li>
                <li>Ensure adequate water supply during flowering and boll development.</li>
                <li>Practice crop rotation to maintain soil health.</li>
            </ul>
        `,
        'Soybean': `
            <ul>
                <li>Inoculate seeds with appropriate Rhizobium bacteria.</li>
                <li>Ensure good drainage and avoid waterlogging.</li>
                <li>Monitor for stem fly and leaf-eating caterpillars.</li>
                <li>Harvest when pods rattle and leaves turn yellow.</li>
            </ul>
        `
    };
    
    return tips[crop] || `<p>🌱 General farming tips: Ensure proper soil preparation, optimal seeding time, regular monitoring for pests and diseases, and appropriate irrigation management for ${crop}.</p>`;
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const predictButton = document.getElementById('predict-button');
    if (predictButton) {
        predictButton.addEventListener('click', predictCrop);
    }
    
    const resetButton = document.getElementById('reset-button');
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            drawnItems.clearLayers();
            drawnPolygon = null;
            clearVisualizationLayers();
            
            document.getElementById('prediction-results').innerHTML = 
                "<p>Draw a polygon on the map and click \"Get AI Recommendations\" to get crop suggestions.</p>";
            
            document.getElementById('predict-button').disabled = true;
        });
    }
});
