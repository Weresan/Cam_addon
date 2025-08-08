#!/usr/bin/env python3
"""
Installation script for the Camera Motion Receiver add-on
This script helps create the proper zip file for Blender installation
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_addon_zip():
    """Create the add-on zip file for Blender installation"""
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Define the add-on name
    addon_name = "camera_motion_receiver"
    
    # Create the zip file
    zip_path = current_dir / f"{addon_name}.zip"
    
    # Files to include in the add-on
    addon_files = [
        "__init__.py",
        "websocket_server.py", 
        "camera_controller.py",
        "README.md"
    ]
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_name in addon_files:
                file_path = current_dir / file_name
                if file_path.exists():
                    # Add file to zip with the addon_name prefix
                    zipf.write(file_path, f"{addon_name}/{file_name}")
                    print(f"Added {file_name} to zip")
                else:
                    print(f"Warning: {file_name} not found")
        
        print(f"\n✅ Add-on zip created successfully: {zip_path}")
        print(f"📦 File size: {zip_path.stat().st_size / 1024:.1f} KB")
        
        return zip_path
        
    except Exception as e:
        print(f"❌ Error creating zip file: {e}")
        return None

def print_installation_instructions():
    """Print installation instructions"""
    
    print("\n" + "="*60)
    print("📦 CAMERA MOTION RECEIVER - INSTALLATION INSTRUCTIONS")
    print("="*60)
    
    print("\n1️⃣ Install the add-on in Blender:")
    print("   • Open Blender")
    print("   • Go to Edit > Preferences > Add-ons")
    print("   • Click 'Install...' and select the zip file")
    print("   • Enable the add-on by checking the box")
    
    print("\n2️⃣ Use the add-on:")
    print("   • Open the 3D Viewport")
    print("   • Press N to open the sidebar")
    print("   • Find the 'Camera Motion' panel")
    print("   • Click 'Start Server' to begin")
    
    print("\n3️⃣ Test the add-on:")
    print("   • Run: python test_client.py")
    print("   • Choose option 1 for animated motion")
    print("   • Watch the camera move in Blender!")
    
    print("\n4️⃣ Send your own data:")
    print("   • Connect to localhost:8765")
    print("   • Send JSON data in this format:")
    print("""
   {
       "X": 0.0,
       "Y": 0.0, 
       "Z": 0.0,
       "ROT_X": 0.0,
       "ROT_Y": 0.0,
       "ROT_Z": 0.0
   }
   """)
    
    print("\n📚 For more information, see README.md")
    print("="*60)

def main():
    """Main installation function"""
    
    print("🔧 Camera Motion Receiver - Installation Script")
    print("Creating add-on zip file...")
    
    # Create the zip file
    zip_path = create_addon_zip()
    
    if zip_path:
        print_installation_instructions()
        
        # Check if test client exists
        test_client_path = Path(__file__).parent / "test_client.py"
        if test_client_path.exists():
            print(f"\n✅ Test client available: {test_client_path}")
        else:
            print(f"\n⚠️  Test client not found: {test_client_path}")
            
        # Check if README exists
        readme_path = Path(__file__).parent / "README.md"
        if readme_path.exists():
            print(f"✅ Documentation available: {readme_path}")
        else:
            print(f"⚠️  Documentation not found: {readme_path}")
            
    else:
        print("\n❌ Failed to create add-on zip file")
        print("Please check that all required files exist in the current directory")

if __name__ == "__main__":
    main()
