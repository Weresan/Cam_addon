#!/usr/bin/env python3
"""
Test script to check if the Camera Motion Receiver addon is working
"""

import bpy

def test_addon():
    """Test if the addon is properly registered"""
    print("🧪 Testing Camera Motion Receiver Addon...")
    
    # Check if the addon is enabled
    addon_name = "camera_motion_receiver"
    if addon_name in bpy.context.preferences.addons:
        print("✅ Addon is enabled in preferences")
    else:
        print("❌ Addon is NOT enabled in preferences")
        print("   Please enable it in Edit > Preferences > Add-ons")
        return False
    
    # Check if the panel class is registered
    panel_class = "CAMERA_MOTION_PT_main_panel"
    if hasattr(bpy.types, panel_class):
        print(f"✅ Panel class '{panel_class}' is registered")
    else:
        print(f"❌ Panel class '{panel_class}' is NOT registered")
        return False
    
    # Check if the operator classes are registered
    operators = [
        "CAMERA_MOTION_OT_start_server",
        "CAMERA_MOTION_OT_stop_server"
    ]
    
    for op in operators:
        if hasattr(bpy.types, op):
            print(f"✅ Operator '{op}' is registered")
        else:
            print(f"❌ Operator '{op}' is NOT registered")
            return False
    
    # Check if the modules are imported
    try:
        import camera_controller
        print("✅ camera_controller module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import camera_controller: {e}")
        return False
    
    try:
        import websocket_server
        print("✅ websocket_server module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import websocket_server: {e}")
        return False
    
    print("🎉 All tests passed! The addon should be working.")
    return True

if __name__ == "__main__":
    test_addon()
