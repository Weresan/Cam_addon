import json
import threading
import time
import bpy
from bpy.app.handlers import persistent

# WebSocket server variables
server_thread = None
server_running = False
websocket_server = None

def on_message(websocket, message):
    """Handle incoming WebSocket messages with camera motion data"""
    try:
        # Parse JSON data
        data = json.loads(message)
        
        # Validate required fields
        required_fields = ['X', 'Y', 'Z', 'ROT_X', 'ROT_Y', 'ROT_Z']
        for field in required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return
        
        # Convert string values to float if needed
        camera_data = {
            'X': float(data['X']),
            'Y': float(data['Y']),
            'Z': float(data['Z']),
            'ROT_X': float(data['ROT_X']),
            'ROT_Y': float(data['ROT_Y']),
            'ROT_Z': float(data['ROT_Z'])
        }
        
        # Apply camera motion in Blender's main thread
        bpy.app.timers.register(lambda: apply_camera_motion(camera_data))
        
        print(f"Received camera motion: {camera_data}")
        
    except json.JSONDecodeError as e:
        print(f"Invalid JSON data: {e}")
    except ValueError as e:
        print(f"Invalid numeric data: {e}")
    except Exception as e:
        print(f"Error processing message: {e}")

def apply_camera_motion(data):
    """Apply camera motion data to the active camera"""
    try:
        scene = bpy.context.scene
        if not scene.camera:
            print("No active camera in scene")
            return
        
        camera = scene.camera
        
        # Set location
        camera.location = (data['X'], data['Y'], data['Z'])
        
        # Set rotation (in radians)
        camera.rotation_euler = (data['ROT_X'], data['ROT_Y'], data['ROT_Z'])
        
        # Update the viewport
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        
        print(f"Applied camera motion: Location={camera.location}, Rotation={camera.rotation_euler}")
        
    except Exception as e:
        print(f"Error applying camera motion: {e}")

def start_websocket_server():
    """Start the WebSocket server in a separate thread"""
    global server_thread, server_running, websocket_server
    
    if server_running:
        print("WebSocket server is already running")
        return
    
    try:
        # Import websocket library (available in Blender's Python)
        import websocket
        from websocket import WebSocketServer
        
        def server_handler(websocket, path):
            """Handle WebSocket connections"""
            print(f"Client connected from {websocket.remote_address}")
            try:
                while True:
                    message = websocket.recv()
                    if message is None:
                        break
                    on_message(websocket, message)
            except websocket.WebSocketConnectionClosedException:
                print("Client disconnected")
            except Exception as e:
                print(f"WebSocket error: {e}")
        
        # Start server in a separate thread
        def run_server():
            global websocket_server
            try:
                websocket_server = WebSocketServer("0.0.0.0", 8765)
                websocket_server.set_fn_new_client(server_handler)
                websocket_server.run_forever()
            except Exception as e:
                print(f"WebSocket server error: {e}")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        server_running = True
        print("WebSocket server started on localhost:8765")
        
    except ImportError:
        print("WebSocket library not available. Please install 'websocket-client' package.")
        # Fallback to a simple socket server
        start_simple_server()

def start_simple_server():
    """Fallback to a simple socket server if WebSocket library is not available"""
    global server_thread, server_running
    
    import socket
    import struct
    
    def simple_server():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('0.0.0.0', 8765))
            sock.listen(1)
            print("Simple socket server started on 0.0.0.0:8765 (accepting connections from any IP)")
            
            while server_running:
                try:
                    conn, addr = sock.accept()
                    print(f"Client connected from {addr}")
                    
                    with conn:
                        while server_running:
                            try:
                                # Receive data length (4 bytes)
                                data_len = conn.recv(4)
                                if not data_len:
                                    break
                                
                                length = struct.unpack('!I', data_len)[0]
                                
                                # Receive JSON data
                                data = conn.recv(length)
                                if not data:
                                    break
                                
                                message = data.decode('utf-8')
                                on_message(None, message)
                                
                            except Exception as e:
                                print(f"Error handling client: {e}")
                                break
                                
                except Exception as e:
                    if server_running:
                        print(f"Server error: {e}")
                    break
            
            sock.close()
            
        except Exception as e:
            print(f"Failed to start simple server: {e}")
    
    server_thread = threading.Thread(target=simple_server, daemon=True)
    server_thread.start()
    server_running = True

def stop_websocket_server():
    """Stop the WebSocket server"""
    global server_running, websocket_server
    
    server_running = False
    
    if websocket_server:
        try:
            websocket_server.close()
        except:
            pass
        websocket_server = None
    
    if server_thread and server_thread.is_alive():
        server_thread.join(timeout=1.0)
    
    print("WebSocket server stopped")

# Convenience functions for the main add-on
def start_server():
    """Start the WebSocket server"""
    start_websocket_server()

def stop_server():
    """Stop the WebSocket server"""
    stop_websocket_server()

# Cleanup on Blender exit
@persistent
def cleanup_on_exit(scene):
    """Cleanup when Blender exits"""
    if server_running:
        stop_websocket_server()

# Register cleanup handler
if cleanup_on_exit not in bpy.app.handlers.depsgraph_update_post:
    bpy.app.handlers.depsgraph_update_post.append(cleanup_on_exit)
