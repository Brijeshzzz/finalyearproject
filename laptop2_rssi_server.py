# laptop2_rssi_server.py
# Install: pip install flask flask-cors pywifi

from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import re
import time
import platform

app = Flask(__name__)
CORS(app)

def get_rssi_windows(ssid):
    try:
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], 
                                        encoding='utf-8', errors='ignore')
        
        if ssid in result:
            signal_match = re.search(r'Signal\s+:\s+(\d+)%', result)
            if signal_match:
                percentage = int(signal_match.group(1))
                # Convert percentage to dBm (approximate)
                rssi = (percentage / 2) - 100
                return rssi
    except:
        pass
    return None

def get_rssi_linux(ssid):
    try:
        result = subprocess.check_output(['iwconfig'], encoding='utf-8', errors='ignore')
        if 'Signal level' in result:
            signal_match = re.search(r'Signal level=(-?\d+)', result)
            if signal_match:
                return int(signal_match.group(1))
    except:
        pass
    return None

def get_rssi_mac(ssid):
    try:
        result = subprocess.check_output(
            ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'],
            encoding='utf-8'
        )
        if ssid in result:
            rssi_match = re.search(r'agrCtlRSSI: (-?\d+)', result)
            if rssi_match:
                return int(rssi_match.group(1))
    except:
        pass
    return None

@app.route('/rssi/<ssid>')
def get_rssi(ssid):
    system = platform.system()
    
    if system == 'Windows':
        rssi = get_rssi_windows(ssid)
    elif system == 'Linux':
        rssi = get_rssi_linux(ssid)
    elif system == 'Darwin':  # macOS
        rssi = get_rssi_mac(ssid)
    else:
        rssi = None
    
    if rssi is not None:
        return jsonify({'rssi': rssi, 'timestamp': time.time()})
    else:
        return jsonify({'error': 'Could not read RSSI'}), 404

if __name__ == '__main__':
    print("RSSI Server running on http://localhost:5000")
    print("Access: http://localhost:5000/rssi/YOUR_HOTSPOT_NAME")
    app.run(host='0.0.0.0', port=5000, debug=True)