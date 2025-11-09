<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📡 Multi-Channel SDR System - Dynamic</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
        
        /* --- COSMIC COLOR PALETTE --- */
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0A0A1F; /* Deep Space Black for particle contrast */
            color: #E0E0E0;
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
            position: relative; 
        }

        /* --- PARTICLES.JS CONTAINER --- */
        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            background-color: transparent;
            z-index: -2; 
        }

        /* Ensure content is above particles */
        .container { 
            position: relative; 
            z-index: 1; 
            max-width: 1600px; margin: 0 auto; 
        }
        
        /* Header */
        .header { text-align: center; margin-bottom: 50px; animation: fadeInDown 0.8s ease; }
        @keyframes fadeInDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }
        .header h1 {
            font-size: 3em; font-weight: 800;
            background: linear-gradient(135deg, #00ADB5 0%, #A855F7 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
            margin-bottom: 5px; letter-spacing: -1px;
        }
        .header .subtitle { font-size: 1.3em; color: #9CA3AF; font-weight: 300; }

        /* Glass card effect */
        .glass-card {
            background: rgba(255, 255, 255, 0.05); 
            backdrop-filter: blur(15px); 
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.15); 
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6); 
            padding: 30px; margin-bottom: 25px; transition: all 0.3s ease;
        }
        .glass-card:hover {
            transform: translateY(-5px); 
            box-shadow: 0 16px 50px rgba(0, 0, 0, 0.8); 
            border-color: rgba(0, 173, 181, 0.5); 
        }

        /* Connection Status */
        .connection-status { padding: 20px; border-radius: 16px; font-weight: 700; text-align: center; font-size: 1.2em; display: flex; align-items: center; justify-content: center; gap: 12px; transition: all 0.3s ease; margin-bottom: 30px; }
        .status-dot { width: 14px; height: 14px; border-radius: 50%; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(1.2); } }
        /* Specific Status Colors */
        .connection-status.connected { background: linear-gradient(135deg, #059669, #10B981); border-color: #059669; } 
        .connection-status.disconnected { background: linear-gradient(135deg, #DC2626, #EF4444); } 
        .connection-status.connecting { background: linear-gradient(135deg, #D97706, #F59E0B); } 

        /* Dashboard and Chart Grids */
        .quad-chart-grid { display: grid; grid-template-columns: repeat(2, 1fr); grid-template-rows: repeat(2, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px; }
        @media (max-width: 900px) { .quad-chart-grid { grid-template-columns: 1fr; } }

        .chart-panel { min-height: 220px; display: flex; flex-direction: column; }
        .chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .channel-title { font-size: 1.2em; font-weight: 700; color: #E0E0E0; }
        .channel-data {
            font-size: 1.5em; font-weight: 800;
            background: linear-gradient(135deg, #00ADB5, #00C6CC);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        }

        .alert-indicator { padding: 5px 10px; border-radius: 8px; font-weight: 700; font-size: 0.9em; transition: all 0.3s; }
        .alert-indicator.inactive { background: rgba(107, 114, 128, 0.2); color: #9CA3AF; }
        .alert-indicator.active {
            background: #A855F7; 
            color: #0A0A1F;
            animation: flash 1s infinite alternate;
            box-shadow: 0 0 10px #A855F7;
        }
        
        @keyframes flash {
            from { opacity: 1; }
            to { opacity: 0.5; }
        }
        
        /* Stats Grid Row */
        .stats-grid-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        @media (max-width: 1200px) { .stats-grid-row { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 600px) { .stats-grid-row { grid-template-columns: 1fr; } }

        .stat-box { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center; }
        .stat-label { font-size: 0.9em; color: #94A3B8; margin-bottom: 6px; text-transform: uppercase; font-weight: 600; }
        .stat-value {
            font-size: 2.2em; font-weight: 800;
            background: linear-gradient(135deg, #A855F7, #D8B4FE);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        }
        
        .chart-container { position: relative; height: 150px; }
        
        /* Controls Section */
        .controls-section h3 { font-size: 1.5em; font-weight: 800; margin-bottom: 25px; color: #E0E0E0; }
        .button-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 15px; margin-bottom: 30px; }

        button { padding: 18px 24px; border: none; border-radius: 14px; font-size: 1.1em; font-weight: 700; cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); text-transform: uppercase; letter-spacing: 0.5px; position: relative; overflow: hidden; }

        /* Button Colors */
        .btn-primary { 
            background: linear-gradient(135deg, #A855F7, #D8B4FE); 
            color: #0A0A1F;
            box-shadow: 0 4px 20px rgba(168, 85, 247, 0.5); 
        }
        .btn-primary:hover { transform: translateY(-4px); box-shadow: 0 8px 30px rgba(168, 85, 247, 0.7); }
        .btn-danger { background: linear-gradient(135deg, #DC2626, #EF4444); color: white; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.5); }
        .btn-secondary { 
            background: rgba(255, 255, 255, 0.1); 
            color: #E0E0E0; 
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .btn-secondary:hover { background: rgba(0, 173, 181, 0.2); transform: translateY(-3px); }

        /* Input styling */
        .input-group label { 
            color: #E0E0E0; 
            display: flex; 
            align-items: center;
            gap: 8px; 
            margin-bottom: 8px;
            font-weight: 600;
            font-size: 0.95em;
        }

        .input-group input, .input-group select {
            /* Input Size & Aesthetics */
            width: 100%;
            padding: 14px 18px; 
            font-size: 1.1em; 
            font-weight: 500;
            border-radius: 10px;
            
            /* Color and Style */
            background: rgba(255, 255, 255, 0.08); 
            backdrop-filter: blur(5px); 
            border: 1px solid rgba(255, 255, 255, 0.2); 
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3); 
            color: #E0E0E0; 
            transition: all 0.3s ease;
            
            /* Sizing Fixes */
            max-width: 300px; 
            min-width: 150px;
        }
        
        @media (max-width: 768px) {
            .input-group input, .input-group select {
                max-width: 100%; 
            }
        }
        
        .input-group input:focus, .input-group select:focus {
            border-color: #00ADB5; 
            background: rgba(255, 255, 255, 0.15); 
            box-shadow: 0 0 0 4px rgba(0, 173, 181, 0.2), inset 0 2px 4px rgba(0, 0, 0, 0.5); 
        }

        /* Log console styling */
        .log-console-header {
            font-size: 1.1em;
            font-weight: 700;
            color: #00ADB5; 
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 2px solid rgba(0, 173, 181, 0.3);
        }

        .log-container { 
            background: rgba(0, 0, 0, 0.4); 
            border: 1px solid rgba(255, 255, 255, 0.1); 
            border-radius: 12px;
            padding: 20px;
            max-height: 250px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            margin-top: 30px; 
            color: #E0E0E0; 
        }

        .log-entry { padding: 6px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); animation: fadeIn 0.3s ease; }
        .log-entry.info { color: #00ADB5; } 
        .log-entry.error { color: #F87171; }
        .log-entry.warning { color: #FFD700; } 
        .log-entry.success { color: #059669; } 

        /* Setup Guide */
        .setup-guide {
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(0, 173, 181, 0.1));
            border: 2px solid rgba(0, 173, 181, 0.5);
        }
        .step-card { 
            background: rgba(255, 255, 255, 0.05); 
            border-left: 5px solid #A855F7; 
            padding: 20px 25px; 
        } 
        .step-card h4 { color: #00ADB5; } 
        .step-card ol { 
            list-style: none; 
            counter-reset: step-counter; 
            margin: 0;
            padding: 0;
        }
        .step-card ol li {
            counter-increment: step-counter; 
            line-height: 1.4;
            color: #d1d5db; 
            padding: 10px 0; 
            border-bottom: 1px dashed rgba(255, 255, 255, 0.05); 
            display: flex; 
            align-items: flex-start;
        }
        .step-card ol li:last-child {
            border-bottom: none;
        }

        .step-card ol li::before {
            content: counter(step-counter) ".";
            font-weight: 800;
            font-size: 1.1em;
            color: #A855F7; 
            margin-right: 15px;
            flex-shrink: 0; 
        }
        
        .step-card code { background: rgba(0, 0, 0, 0.5); color: #059669; }
    </style>
</head>
<body>
    
    <div id="particles-js"></div>
    
    <div class="container">
        
        <div class="header">
            <h1>📡 Remote Sensing using Software Defined Radio</h1>
            <p class="subtitle">Disaster Detection System for Hazardous Environments</p>
        </div>

        <div class="setup-guide glass-card">
            <h3>🚀 System Setup Guide</h3>
            <div class="setup-steps">
                <div class="step-card">
                    <h4>💻 Laptop 1 - Transmitter (Hotspot)</h4>
                    <ol>
                        <li>Create a dedicated **WiFi Hotspot**.</li>
                        <li>Name the hotspot: <code>MotionDetect</code> (or your custom SSID).</li>
                        <li>Set a password and ensure the hotspot remains **ON**.</li>
                        <li>**Position:** Place this laptop across the area you intend to monitor (the "Trip Wire").</li>
                    </ol>
                </div>
                <div class="step-card">
                    <h4>📡 Laptop 2 - Monitor (Receiver & Analyzer)</h4>
                    <ol>
                        <li>Connect this device to the **Hotspot** created by Laptop 1.</li>
                        <li>Run the RSSI server script: <code>python laptop2_rssi_server.py</code></li>
                        <li>Enter the Hotspot **SSID** in the control panel below.</li>
                        <li>Click **Start** and observe the baseline signal before introducing motion.</li>
                    </ol>
                </div>
            </div>
        </div>

        <div id="connectionStatus" class="connection-status disconnected glass-card">
            <span class="status-dot"></span>
            <span>System Ready - Configure & Start</span>
        </div>
        
        <div class="glass-card">
             <h3 class="chart-title">📊 Multi-Channel SDR Analysis</h3>
            
            <div class="stats-grid-row">
                <div class="stat-box">
                    <div class="stat-label">MAX ST. DEVIATION (σ)</div>
                    <div class="stat-value" id="maxStdDev">--</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">TOTAL ALERTS</div>
                    <div class="stat-value" id="motionCount">0</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">TOTAL SAMPLES</div>
                    <div class="stat-value" id="sampleCount">0</div>
                </div>
                 <div class="stat-box">
                    <div class="stat-label">AVG POWER (dBm)</div>
                    <div class="stat-value" id="avgRssi">--</div>
                </div>
            </div>
            
            <div class="quad-chart-grid">
                
                <div class="glass-card chart-panel">
                    <div class="chart-header">
                        <div>
                            <span class="channel-title">CH 1: 2412 MHz</span>
                            <div class="channel-data" id="freq1Value">-- dBm</div>
                        </div>
                         <div id="alertIndicator1" class="alert-indicator inactive" data-was-active="false">NO MOTION</div>
                    </div>
                    <div class="chart-container"><canvas id="rssiChart1"></canvas></div>
                </div>
                
                <div class="glass-card chart-panel">
                    <div class="chart-header">
                        <div>
                            <span class="channel-title">CH 6: 2437 MHz</span>
                            <div class="channel-data" id="freq2Value">-- dBm</div>
                        </div>
                        <div id="alertIndicator2" class="alert-indicator inactive" data-was-active="false">NO MOTION</div>
                    </div>
                    <div class="chart-container"><canvas id="rssiChart2"></canvas></div>
                </div>
                
                <div class="glass-card chart-panel">
                    <div class="chart-header">
                        <div>
                            <span class="channel-title">CH 11: 2462 MHz</span>
                            <div class="channel-data" id="freq3Value">-- dBm</div>
                        </div>
                        <div id="alertIndicator3" class="alert-indicator inactive" data-was-active="false">NO MOTION</div>
                    </div>
                    <div class="chart-container"><canvas id="rssiChart3"></canvas></div>
                </div>
                
                <div class="glass-card chart-panel">
                    <div class="chart-header">
                        <div>
                            <span class="channel-title">SDR: 433 MHz</span>
                            <div class="channel-data" id="freq4Value">-- dBm</div>
                        </div>
                        <div id="alertIndicator4" class="alert-indicator inactive" data-was-active="false">NO MOTION</div>
                    </div>
                    <div class="chart-container"><canvas id="rssiChart4"></canvas></div>
                </div>
                
            </div>
            
        </div>
        
        <div class="glass-card controls-section">
            <h3>⚙ Control Center</h3>
            
            <div class="button-grid">
                <button class="btn-primary" id="startBtn" onclick="startMonitoring()">
                    🚀 START MONITORING
                </button>
                <button class="btn-danger" onclick="stopMonitoring()">
                    ⏹ STOP
                </button>
                <button class="btn-secondary" onclick="calibrate()">
                    🎯 CALIBRATE BASELINE
                </button>
                <button class="btn-secondary" onclick="resetData()">
                    🔄 RESET DATA
                </button>
            </div>

            <div class="input-grid">
                <div class="input-group">
                    <label for="ssidName">📡 Signal Transmitter Name (SSID)</label>
                    <input type="text" id="ssidName" value="MotionDetect" placeholder="Enter hotspot name">
                </div>
                
                <div class="input-group">
                    <label for="threshold">🎚 Motion Threshold (Std Dev in dB)</label>
                    <input type="number" id="threshold" value="3.0" min="0.5" max="15" step="0.5">
                </div>
                
                <div class="input-group">
                    <label for="windowSize">📏 Analysis Window (Samples)</label>
                    <input type="number" id="windowSize" value="8" min="4" max="30">
                </div>
                
                <div class="input-group">
                    <label for="updateRate">⏱ Update Rate (ms)</label>
                    <input type="number" id="updateRate" value="500" min="100" max="2000" step="100">
                </div>
            </div>

            <div class="log-console-group">
                 <div class="log-console-header">📜 System Console Log</div>
                 <div class="log-container" id="logContainer">
                    <div class="log-entry success">🟢 System initialized and ready</div>
                    <div class="log-entry info">💡 Tip: Use <kbd>Ctrl</kbd> + <kbd>Space</kbd> for quick start/stop</div>
                </div>
            </div>
           
        </div>
    </div>

    <script>
        // --- PARTICLES.JS INITIALIZATION SCRIPT ---
        particlesJS('particles-js', {
            "particles": {
                "number": {
                    "value": 80,
                    "density": {
                        "enable": true,
                        "value_area": 800
                    }
                },
                "color": {
                    "value": ["#00ADB5", "#A855F7", "#059669"] /* Teal, Purple, Green */
                },
                "shape": {
                    "type": "circle",
                    "stroke": {
                        "width": 0,
                        "color": "#000000"
                    },
                    "polygon": {
                        "nb_sides": 5
                    }
                },
                "opacity": {
                    "value": 0.5,
                    "random": false,
                    "anim": {
                        "enable": false,
                        "speed": 1,
                        "opacity_min": 0.1,
                        "sync": false
                    }
                },
                "size": {
                    "value": 3,
                    "random": true,
                    "anim": {
                        "enable": false,
                        "speed": 40,
                        "size_min": 0.1,
                        "sync": false
                    }
                },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#00ADB5", /* Teal lines */
                    "opacity": 0.4,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": 2,
                    "direction": "none",
                    "random": false,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false,
                    "attract": {
                        "enable": false,
                        "rotateX": 600,
                        "rotateY": 1200
                    }
                }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": {
                        "enable": true,
                        "mode": "grab"
                    },
                    "onclick": {
                        "enable": true,
                        "mode": "push"
                    },
                    "resize": true
                },
                "modes": {
                    "grab": {
                        "distance": 140,
                        "line_linked": {
                            "opacity": 1
                        }
                    },
                    "bubble": {
                        "distance": 400,
                        "size": 40,
                        "duration": 2,
                        "opacity": 8,
                        "speed": 3
                    },
                    "repulse": {
                        "distance": 200,
                        "duration": 0.4
                    },
                    "push": {
                        "particles_nb": 4
                    },
                    "remove": {
                        "particles_nb": 2
                    }
                }
            },
            "retina_detect": true
        });

        // --- MULTI-CHANNEL DATA STRUCTURE (Existing Logic Below) ---
        let channelData = {
            1: { freq: 2412, data: [], chart: null, elementId: 'rssiChart1', valueId: 'freq1Value', alertId: 'alertIndicator1', baseline: -45 - Math.random() * 10 },
            2: { freq: 2437, data: [], chart: null, elementId: 'rssiChart2', valueId: 'freq2Value', alertId: 'alertIndicator2', baseline: -45 - Math.random() * 10 },
            3: { freq: 2462, data: [], chart: null, elementId: 'rssiChart3', valueId: 'freq3Value', alertId: 'alertIndicator3', baseline: -45 - Math.random() * 10 },
            4: { freq: 433,  data: [], chart: null, elementId: 'rssiChart4', valueId: 'freq4Value', alertId: 'alertIndicator4', baseline: -45 - Math.random() * 10 }
        };
        let timeLabels = [];
        let maxDataPoints = 60;
        let monitoringInterval;
        let sampleCount = 0;
        let motionCount = 0;
        
        // Helper function for Chart setup
        function createChart(ctx, data, color) {
            const gradient = ctx.createLinearGradient(0, 0, 0, 150);
            gradient.addColorStop(0, `${color}66`); 
            gradient.addColorStop(1, `${color}00`); 

            return new Chart(ctx, {
                type: 'line',
                data: {
                    datasets: [{
                        data: data,
                        borderColor: color,
                        backgroundColor: gradient,
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true,
                        pointRadius: 0,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: { duration: 100 },
                    plugins: { legend: { display: false }, tooltip: { enabled: false } },
                    scales: {
                        y: { 
                            display: false,
                            min: -85, 
                            max: -30,
                        },
                        x: { display: false }
                    },
                    layout: { padding: 0 }
                }
            });
        }
        
        // Initialize all 4 charts
        Object.keys(channelData).forEach(key => {
            const channel = channelData[key];
            const ctx = document.getElementById(channel.elementId).getContext('2d');
            
            // Cosmic Chart Colors
            let color;
            if (key === '1') color = '#00ADB5'; // Teal
            else if (key === '2') color = '#A855F7'; // Purple
            else if (key === '3') color = '#059669'; // Green
            else if (key === '4') color = '#FFD700'; // Gold/Yellow
            
            channel.chart = createChart(ctx, channel.data, color);
        });

        // --- CORE LOGIC ---
        
        function addLog(message, type = 'info') {
            const logContainer = document.getElementById('logContainer');
            const entry = document.createElement('div');
            entry.className = `log-entry ${type}`;
            const timestamp = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            const icon = { info: '🔵', error: '🔴', warning: '🟡', success: '🟢' }[type] || '🔵';
            entry.textContent = `${icon} [${timestamp}] ${message}`;
            logContainer.insertBefore(entry, logContainer.firstChild);
            
            while (logContainer.children.length > 25) { logContainer.removeChild(logContainer.lastChild); }
        }

        async function getRSSI(channelIndex) {
            return getSimulatedRSSI(channelIndex);
        }

        function getSimulatedRSSI(channelIndex) {
            const channel = channelData[channelIndex];
            
            let bias = 0;
            if (channel.freq === 433) bias = -10;
            
            let rssi = channel.baseline + bias + (Math.random() - 0.5) * 3;
            
            if (Math.random() > 0.95 && channelIndex === 1) {
                rssi -= 10 + Math.random() * 15;
            } else if (Math.random() > 0.98) {
                rssi -= 5 + Math.random() * 5;
            }
            
            return rssi; 
        }
        
        async function addDataPoint() {
            const now = new Date();
            const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            
            timeLabels.push(timeStr);
            sampleCount++;
            
            let totalRssi = 0;
            let maxStdDev = 0;

            for (const key in channelData) {
                const channel = channelData[key];
                const rssi = await getRSSI(key); 
                
                channel.data.push(rssi);
                totalRssi += rssi;
                
                if (channel.data.length > maxDataPoints) {
                    channel.data.shift();
                }

                // Update chart labels/data
                channel.chart.data.labels = timeLabels;
                channel.chart.update('none');

                const stdDev = detectMotion(key);
                document.getElementById(channel.valueId).textContent = `${rssi.toFixed(1)} dBm`;
                
                if (stdDev > maxStdDev) maxStdDev = stdDev;
            }
            
            if (timeLabels.length > maxDataPoints) {
                timeLabels.shift();
            }

            document.getElementById('sampleCount').textContent = sampleCount;
            document.getElementById('avgRssi').textContent = `${(totalRssi / 4).toFixed(1)} dBm`;
            document.getElementById('maxStdDev').textContent = maxStdDev.toFixed(2);
        }
        
        function detectMotion(channelKey) {
            const channel = channelData[channelKey];
            const windowSize = parseInt(document.getElementById('windowSize').value);
            const threshold = parseFloat(document.getElementById('threshold').value);
            
            if (channel.data.length < windowSize) return 0;
            
            const recentData = channel.data.slice(-windowSize);
            const mean = recentData.reduce((a, b) => a + b) / recentData.length;
            const variance = recentData.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / recentData.length;
            const stdDev = Math.sqrt(variance); 
            
            const recentDrop = mean - channel.data[channel.data.length - 1];
            
            const isMotion = (stdDev > threshold) || (recentDrop > threshold * 1.5);

            const alertIndicator = document.getElementById(channel.alertId);
            
            if (isMotion) {
                alertIndicator.classList.remove('inactive');
                alertIndicator.classList.add('active');
                alertIndicator.textContent = 'ALERT!';
                
                if (alertIndicator.dataset.wasActive !== 'true') {
                    motionCount++;
                    document.getElementById('motionCount').textContent = motionCount;
                    addLog(`[${channel.freq} MHz] ALERT! Std Dev: ${stdDev.toFixed(2)} > Threshold: ${threshold}`, 'error');
                }
                alertIndicator.dataset.wasActive = 'true';
            } else {
                alertIndicator.classList.remove('active');
                alertIndicator.classList.add('inactive');
                alertIndicator.textContent = 'NO MOTION';
                alertIndicator.dataset.wasActive = 'false';
            }
            
            return stdDev;
        }
        
        // --- CONTROL FUNCTIONS (Start/Stop/Reset/Calibrate) ---

        function updateConnectionStatus(status) {
            const statusEl = document.getElementById('connectionStatus');
            const statusText = statusEl.querySelector('span:last-child');
            statusEl.className = 'connection-status glass-card ' + status;
            
            if (status === 'connected') {
                statusText.textContent = 'Connected & Monitoring Active';
            } else if (status === 'connecting') {
                statusText.textContent = 'Attempting Connection...';
            } else {
                statusText.textContent = 'System Ready - Configure & Start';
            }
        }
        
        async function startMonitoring() {
            const ssid = document.getElementById('ssidName').value.trim();
            
            if (!ssid) { addLog('Please enter Signal Transmitter Name (SSID)!', 'error'); return; }
            stopMonitoring();
            
            addLog(`Starting multi-channel monitoring...`, 'info');
            updateConnectionStatus('connecting');
            
            setTimeout(() => {
                updateConnectionStatus('connected');
                addLog(`Monitoring started! Observing 4 channels.`, 'success');
                
                const updateRate = parseInt(document.getElementById('updateRate').value);
                
                monitoringInterval = setInterval(addDataPoint, updateRate);
                
                document.getElementById('startBtn').disabled = true;
            }, 1500); 
        }
        
        function stopMonitoring() {
            if (monitoringInterval) {
                clearInterval(monitoringInterval);
                monitoringInterval = null;
            }
            updateConnectionStatus('disconnected');
            document.getElementById('startBtn').disabled = false;
            addLog('Monitoring stopped by user.', 'warning');
        }
        
        function resetData() {
            stopMonitoring();
            
            Object.keys(channelData).forEach(key => {
                channelData[key].data = [];
                channelData[key].chart.update();
                document.getElementById(channelData[key].valueId).textContent = '-- dBm';
                document.getElementById(channelData[key].alertId).classList.remove('active');
                document.getElementById(channelData[key].alertId).classList.add('inactive');
                document.getElementById(channelData[key].alertId).textContent = 'NO MOTION';
                document.getElementById(channelData[key].alertId).dataset.wasActive = 'false';
                channelData[key].baseline = -45 - Math.random() * 10;
            });

            timeLabels = [];
            sampleCount = 0;
            motionCount = 0;
            
            document.getElementById('maxStdDev').textContent = '--';
            document.getElementById('avgRssi').textContent = '--';
            document.getElementById('sampleCount').textContent = '0';
            document.getElementById('motionCount').textContent = '0';
            
            addLog('System reset - all data cleared', 'info');
        }

        function calibrate() {
            addLog('Calibrating baseline for all channels... Keep hands clear!', 'warning');
            isCalibrating = true;
            
            setTimeout(() => {
                Object.keys(channelData).forEach(key => {
                    const channel = channelData[key];
                    const recent = channel.data.slice(-10);
                    if (recent.length > 0) {
                        const newBaseline = recent.reduce((a, b) => a + b) / recent.length;
                        channel.baseline = newBaseline;
                    }
                });
                addLog('✅ Calibration complete! New baselines set.', 'success');
                isCalibrating = false;
            }, 2500);
        }


        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === ' ') { e.preventDefault(); if (monitoringInterval) { stopMonitoring(); } else { startMonitoring(); } }
            if (e.ctrlKey && e.key === 'r') { e.preventDefault(); resetData(); }
        });

        // Auto-adjust chart on window resize
        window.addEventListener('resize', () => {
            Object.keys(channelData).forEach(key => channelData[key].chart.resize());
        });

        // Welcome message
        setTimeout(() => {
            addLog('Pro Tip: Use Ctrl+Space to start/stop quickly', 'info');
        }, 2000);
    </script>
</body>
</html>