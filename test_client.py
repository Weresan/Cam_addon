#!/usr/bin/env python3
"""
Test client for the Camera Motion Receiver add-on
This script sends camera motion data to the WebSocket server running in Blender
"""

import json
import time
import socket
import struct
import threading
import math

class CameraMotionTestClient:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        
    def connect(self):
        """Connect to the WebSocket server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connected to server at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the server"""
        if self.socket:
            self.socket.close()
            self.socket = None
        self.connected = False
        print("Disconnected from server")
    
    def send_camera_data(self, x, y, z, rot_x, rot_y, rot_z):
        """Send camera motion data to the server"""
        if not self.connected:
            print("Not connected to server")
            return False
        
        try:
            # Create JSON data
            data = {
                "X": x,
                "Y": y,
                "Z": z,
                "ROT_X": rot_x,
                "ROT_Y": rot_y,
                "ROT_Z": rot_z
            }
            
            # Convert to JSON string
            json_data = json.dumps(data)
            message = json_data.encode('utf-8')
            
            # Send data length first (4 bytes)
            length = struct.pack('!I', len(message))
            self.socket.send(length)
            
            # Send the actual data
            self.socket.send(message)
            
            print(f"Sent camera data: {data}")
            return True
            
        except Exception as e:
            print(f"Failed to send data: {e}")
            self.connected = False
            return False
    
    def send_animated_motion(self, duration=10, fps=30):
        """Send animated camera motion for testing"""
        if not self.connect():
            return
        
        try:
            print(f"Starting animated camera motion for {duration} seconds at {fps} FPS")
            
            start_time = time.time()
            frame_count = 0
            
            while time.time() - start_time < duration:
                # Calculate time-based animation
                t = (time.time() - start_time) / duration
                
                # Create a circular motion
                radius = 5.0
                x = radius * math.cos(t * 2 * math.pi)
                y = radius * math.sin(t * 2 * math.pi)
                z = 2.0 + math.sin(t * 4 * math.pi) * 1.0
                
                # Rotation follows the motion
                rot_x = 0.0
                rot_y = 0.0
                rot_z = t * 2 * math.pi
                
                # Send the data
                self.send_camera_data(x, y, z, rot_x, rot_y, rot_z)
                
                frame_count += 1
                time.sleep(1.0 / fps)
            
            print(f"Animation complete. Sent {frame_count} frames")
            
        finally:
            self.disconnect()
    
    def send_test_sequence(self):
        """Send a sequence of test positions"""
        if not self.connect():
            return
        
        try:
            # Test positions
            test_positions = [
                (0, 0, 0, 0, 0, 0),      # Origin
                (5, 0, 0, 0, 0, 0),      # Right
                (0, 5, 0, 0, 0, 0),      # Forward
                (0, 0, 5, 0, 0, 0),      # Up
                (5, 5, 5, 0, 0, 0),      # Diagonal
                (0, 0, 0, 0, 0, math.pi/2),  # Rotated 90 degrees
                (0, 0, 0, 0, 0, math.pi),    # Rotated 180 degrees
                (0, 0, 0, 0, 0, 0),      # Back to origin
            ]
            
            for i, (x, y, z, rot_x, rot_y, rot_z) in enumerate(test_positions):
                print(f"Test position {i+1}/{len(test_positions)}")
                self.send_camera_data(x, y, z, rot_x, rot_y, rot_z)
                time.sleep(1.0)  # Wait 1 second between positions
            
            print("Test sequence complete")
            
        finally:
            self.disconnect()

def main():
    """Main function to run the test client"""
    client = CameraMotionTestClient()
    
    print("Camera Motion Test Client")
    print("1. Send animated motion")
    print("2. Send test sequence")
    print("3. Send single position")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                duration = float(input("Enter animation duration (seconds): "))
                client.send_animated_motion(duration=duration)
                
            elif choice == '2':
                client.send_test_sequence()
                
            elif choice == '3':
                print("Enter camera position and rotation:")
                x = float(input("X position: "))
                y = float(input("Y position: "))
                z = float(input("Z position: "))
                rot_x = float(input("X rotation (radians): "))
                rot_y = float(input("Y rotation (radians): "))
                rot_z = float(input("Z rotation (radians): "))
                
                if client.connect():
                    client.send_camera_data(x, y, z, rot_x, rot_y, rot_z)
                    client.disconnect()
                    
            elif choice == '4':
                break
                
            else:
                print("Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
