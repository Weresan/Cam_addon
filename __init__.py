bl_info = {
    "name": "Camera Motion Receiver",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (3, 3, 0),
    "location": "View3D > Sidebar > Camera Motion",
    "description": "Receives camera motion data via WebSocket and applies it to the active camera",
    "warning": "",
    "doc_url": "",
    "category": "Camera",
}

import bpy
from bpy.props import BoolProperty
from bpy.types import Panel, Operator

# Import our modules
from . import websocket_server
from . import camera_controller

# Global variable to track server state
server_running = False

class CAMERA_MOTION_PT_main_panel(Panel):
    bl_label = "Camera Motion Receiver"
    bl_idname = "CAMERA_MOTION_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Camera Motion'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Server status
        box = layout.box()
        box.label(text="WebSocket Server Status:")
        
        if server_running:
            box.label(text="🟢 Running on localhost:8765", icon='PLAY')
        else:
            box.label(text="🔴 Stopped", icon='PAUSE')
        
        # Control buttons
        row = layout.row()
        if not server_running:
            row.operator("camera_motion.start_server", text="Start Server", icon='PLAY')
        else:
            row.operator("camera_motion.stop_server", text="Stop Server", icon='PAUSE')
        
        # Camera info
        box = layout.box()
        box.label(text="Active Camera:")
        
        if context.scene.camera:
            camera = context.scene.camera
            box.label(text=f"Name: {camera.name}")
            box.label(text=f"Location: ({camera.location.x:.2f}, {camera.location.y:.2f}, {camera.location.z:.2f})")
            box.label(text=f"Rotation: ({camera.rotation_euler.x:.2f}, {camera.rotation_euler.y:.2f}, {camera.rotation_euler.z:.2f})")
        else:
            box.label(text="No active camera", icon='ERROR')

class CAMERA_MOTION_OT_start_server(Operator):
    bl_idname = "camera_motion.start_server"
    bl_label = "Start WebSocket Server"
    bl_description = "Start the WebSocket server to receive camera motion data"
    
    def execute(self, context):
        global server_running
        if not server_running:
            try:
                websocket_server.start_server()
                server_running = True
                self.report({'INFO'}, "WebSocket server started on localhost:8765")
            except Exception as e:
                self.report({'ERROR'}, f"Failed to start server: {str(e)}")
        return {'FINISHED'}

class CAMERA_MOTION_OT_stop_server(Operator):
    bl_idname = "camera_motion.stop_server"
    bl_label = "Stop WebSocket Server"
    bl_description = "Stop the WebSocket server"
    
    def execute(self, context):
        global server_running
        if server_running:
            try:
                websocket_server.stop_server()
                server_running = False
                self.report({'INFO'}, "WebSocket server stopped")
            except Exception as e:
                self.report({'ERROR'}, f"Failed to stop server: {str(e)}")
        return {'FINISHED'}

# Registration
classes = [
    CAMERA_MOTION_PT_main_panel,
    CAMERA_MOTION_OT_start_server,
    CAMERA_MOTION_OT_stop_server,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Start server automatically when add-on is enabled
    global server_running
    if not server_running:
        try:
            websocket_server.start_server()
            server_running = True
        except Exception as e:
            print(f"Failed to start WebSocket server: {e}")

def unregister():
    # Stop server when add-on is disabled
    global server_running
    if server_running:
        try:
            websocket_server.stop_server()
            server_running = False
        except Exception as e:
            print(f"Failed to stop WebSocket server: {e}")
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
