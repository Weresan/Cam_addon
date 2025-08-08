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
from pathlib import Path

# Import our WebSocket server
from websocket_server import start_websocket_server, stop_websocket_server

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
            
            # Create HTTP server
            handler = http.server.SimpleHTTPRequestHandler
            
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
    
    def start_websocket_server(self):
        """Start the WebSocket server for phone connections"""
        try:
            # Modify the WebSocket server to bind to all interfaces
            import websocket_server
            
            # Start the WebSocket server
            websocket_server.start_websocket_server()
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
        print(f"   • Enter port: 8765")
        print(f"   • Click 'Connect'")
        
        print(f"\n4️⃣ In Blender:")
        print(f"   • Enable the Camera Motion Receiver add-on")
        print(f"   • The WebSocket server should start automatically")
        print(f"   • Or manually start it from the UI panel")
        
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
