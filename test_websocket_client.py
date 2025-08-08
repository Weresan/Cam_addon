#!/usr/bin/env python3
"""
Simple WebSocket client test for the phone server
"""

import websocket
import json
import time

def test_websocket_connection():
    """Test WebSocket connection to the server"""
    try:
        # Create WebSocket connection
        ws = websocket.create_connection("ws://localhost:8765")
        print("✅ WebSocket connection established!")
        
        # Send test data
        test_data = {
            "X": 1.0,
            "Y": 2.0,
            "Z": 3.0,
            "ROT_X": 0.5,
            "ROT_Y": 1.0,
            "ROT_Z": 1.5
        }
        
        ws.send(json.dumps(test_data))
        print(f"✅ Sent test data: {test_data}")
        
        # Close connection
        ws.close()
        print("✅ Connection closed successfully")
        
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing WebSocket connection...")
    test_websocket_connection()
