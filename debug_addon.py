#!/usr/bin/env python3
"""
Debug script to test addon registration in Blender
Run this in Blender's Python console (Window > Toggle System Console)
"""

import bpy

def debug_addon():
    """Debug addon registration"""
    print("🔍 Debugging addon registration...")
    
    # Check if our addon is enabled
    addon_name = "camera_motion_receiver"
    if addon_name in bpy.context.preferences.addons:
        print(f"✅ Addon '{addon_name}' is enabled")
    else:
        print(f"❌ Addon '{addon_name}' is NOT enabled")
        print("   Please enable it in Edit > Preferences > Add-ons")
        return False
    
    # Check if panel class is registered
    panel_class = "CAMERA_MOTION_PT_main_panel"
    if hasattr(bpy.types, panel_class):
        print(f"✅ Panel class '{panel_class}' is registered")
    else:
        print(f"❌ Panel class '{panel_class}' is NOT registered")
        return False
    
    # Check if operator classes are registered
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
    
    # List all registered panel classes
    print("\n📋 All registered panel classes:")
    for attr in dir(bpy.types):
        if 'PT_' in attr and 'Panel' in str(type(getattr(bpy.types, attr))):
            print(f"  - {attr}")
    
    # List all UI categories in VIEW_3D
    print("\n📋 All UI categories in VIEW_3D:")
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'UI':
                    print(f"  - Region: {region.type}")
                    # This is a bit complex to get categories, but we can try
    
    print("\n🎉 Debug complete!")
    return True

# Run the debug function
debug_addon()
