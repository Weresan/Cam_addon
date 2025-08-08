#!/usr/bin/env python3
"""
Phone server for Camera Motion Receiver add-on
This script serves the phone test HTML file and provides network access
"""

import http.server
import socketserver
import socket
import threading
import webbrowser
import os
import json
from pathlib import Path

# Import our standalone WebSocket server
from standalone_websocket_server import start_websocket_server, stop_websocket_server

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def forward_to_blender(self, data):
        """Forward camera data to Blender's server on port 8765"""
        try:
            # Create a socket connection to Blender's server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(1.0)  # 1 second timeout
            client_socket.connect(('localhost', 8765))
            
            # Send the JSON data to Blender
            json_data = json.dumps(data)
            client_socket.send(json_data.encode('utf-8'))
            
            # Close the connection
            client_socket.close()
            print(f"✅ Forwarded data to Blender: {data}")
            
        except Exception as e:
            print(f"⚠️  Could not forward to Blender: {e}")
    
    def do_POST(self):
        """Handle POST requests for camera data"""
        if self.path == '/send_data':
            try:
                # Get the content length
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # Parse JSON data
                data = json.loads(post_data.decode('utf-8'))
                
                # Print the received data
                print(f"📱 Received camera data via HTTP: {data}")
                
                # Forward the data to Blender's server
                self.forward_to_blender(data)
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                
                response = {'status': 'success', 'message': 'Data received'}
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"❌ Error handling POST request: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {'status': 'error', 'message': str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

class PhoneServer:
    def __init__(self, port=8000, websocket_port=8765):
        self.http_port = port
        self.websocket_port = websocket_port
        self.http_server = None
        self.websocket_running = False
        
    def get_local_ip(self):
        """Get the local IP address of this machine"""
        try:
            # Connect to a remote address to determine local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    def start_http_server(self):
        """Start the HTTP server to serve the phone test page"""
        try:
            # Change to the directory containing this script
            script_dir = Path(__file__).parent
            os.chdir(script_dir)
            
            # Update the HTML file with the correct IP address
            self.update_html_with_ip()
            
            # Create HTTP server with custom handler
            handler = CustomHTTPRequestHandler
            
            with socketserver.TCPServer(("", self.http_port), handler) as httpd:
                print(f"🌐 HTTP server started on port {self.http_port}")
                print(f"📱 Phone test page available at: http://{self.get_local_ip()}:{self.http_port}/phone_test.html")
                print(f"💻 Local access: http://localhost:{self.http_port}/phone_test.html")
                
                # Start WebSocket server in a separate thread
                self.start_websocket_server()
                
                # Start HTTP server
                httpd.serve_forever()
                
        except Exception as e:
            print(f"❌ Failed to start HTTP server: {e}")
    
    def update_html_with_ip(self):
        """Update the HTML file with the correct IP address"""
        try:
            html_file = Path("phone_test.html")
            if html_file.exists():
                # Read the HTML file
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Get the local IP address
                local_ip = self.get_local_ip()
                
                # Update the IP address in the HTML
                updated_content = content.replace('value="192.168.100.59"', f'value="{local_ip}"')
                
                # Write the updated content back
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"✅ Updated phone_test.html with IP address: {local_ip}")
                
        except Exception as e:
            print(f"⚠️  Could not update HTML file: {e}")
    
    def start_websocket_server(self):
        """Start the WebSocket server for phone connections"""
        try:
            # Start the standalone WebSocket server
            start_websocket_server()
            self.websocket_running = True
            print(f"🔌 WebSocket server started on port {self.websocket_port}")
            print(f"📡 Accepting connections from any IP address")
            
        except Exception as e:
            print(f"❌ Failed to start WebSocket server: {e}")
    
    def stop_servers(self):
        """Stop both HTTP and WebSocket servers"""
        try:
            if self.websocket_running:
                stop_websocket_server()
                self.websocket_running = False
                print("🔌 WebSocket server stopped")
        except Exception as e:
            print(f"❌ Error stopping WebSocket server: {e}")
    
    def print_instructions(self):
        """Print setup instructions"""
        local_ip = self.get_local_ip()
        
        print("\n" + "="*60)
        print("📱 PHONE TEST SETUP INSTRUCTIONS")
        print("="*60)
        
        print(f"\n1️⃣ Start the phone server:")
        print(f"   python3 phone_server.py")
        
        print(f"\n2️⃣ On your phone:")
        print(f"   • Open your web browser")
        print(f"   • Go to: http://{local_ip}:8000/phone_test.html")
        print(f"   • Make sure your phone is on the same WiFi network")
        
        print(f"\n3️⃣ In the phone app:")
        print(f"   • Enter server IP: {local_ip}")
        print(f"   • Enter port: 8000")
        print(f"   • Click 'Connect'")
        
        print(f"\n4️⃣ In Blender:")
        print(f"   • Enable the Camera Motion Receiver add-on")
        print(f"   • The WebSocket server should start automatically")
        print(f"   • Or manually start it from the UI panel")
        print(f"   • Make sure Blender is running and the add-on is enabled!")
        
        print(f"\n5️⃣ Test the connection:")
        print(f"   • Use the sliders to move the camera")
        print(f"   • Try the 'Auto Motion' feature")
        print(f"   • Watch the camera move in Blender!")
        
        print(f"\n🔧 Troubleshooting:")
        print(f"   • Make sure both devices are on the same network")
        print(f"   • Check that port 8765 is not blocked by firewall")
        print(f"   • Try using the computer's IP address if localhost doesn't work")
        
        print("="*60)
    
    def open_browser(self):
        """Open the phone test page in the default browser"""
        try:
            url = f"http://localhost:{self.http_port}/phone_test.html"
            webbrowser.open(url)
            print(f"🌐 Opened phone test page in browser: {url}")
        except Exception as e:
            print(f"❌ Failed to open browser: {e}")

def main():
    """Main function"""
    print("📱 Camera Motion Receiver - Phone Server")
    print("Starting servers for phone testing...")
    
    # Create and start the phone server
    server = PhoneServer()
    
    # Print instructions
    server.print_instructions()
    
    # Ask if user wants to open browser
    try:
        response = input("\nOpen phone test page in browser? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            server.open_browser()
    except KeyboardInterrupt:
        pass
    
    try:
        # Start the HTTP server (this will block)
        server.start_http_server()
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        server.stop_servers()
        print("✅ Servers stopped")

if __name__ == "__main__":
    main()
