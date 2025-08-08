import bpy
import math
import mathutils
from mathutils import Vector, Euler

class CameraController:
    """Handles camera manipulation and provides utility functions"""
    
    @staticmethod
    def get_active_camera():
        """Get the active camera in the current scene"""
        scene = bpy.context.scene
        return scene.camera
    
    @staticmethod
    def set_camera_location(camera, x, y, z):
        """Set camera location"""
        if camera:
            camera.location = (x, y, z)
            return True
        return False
    
    @staticmethod
    def set_camera_rotation(camera, rot_x, rot_y, rot_z):
        """Set camera rotation in radians"""
        if camera:
            camera.rotation_euler = (rot_x, rot_y, rot_z)
            return True
        return False
    
    @staticmethod
    def set_camera_transform(camera, location, rotation):
        """Set both camera location and rotation"""
        if camera:
            camera.location = location
            camera.rotation_euler = rotation
            return True
        return False
    
    @staticmethod
    def create_camera_if_needed():
        """Create a camera if none exists in the scene"""
        scene = bpy.context.scene
        
        if not scene.camera:
            # Create a new camera
            bpy.ops.object.camera_add(location=(0, 0, 0))
            camera = bpy.context.active_object
            
            # Set it as the active camera
            scene.camera = camera
            
            print(f"Created new camera: {camera.name}")
            return camera
        
        return scene.camera
    
    @staticmethod
    def get_camera_info(camera):
        """Get formatted camera information"""
        if not camera:
            return "No camera"
        
        loc = camera.location
        rot = camera.rotation_euler
        
        return {
            'name': camera.name,
            'location': (loc.x, loc.y, loc.z),
            'rotation': (rot.x, rot.y, rot.z),
            'location_degrees': (math.degrees(rot.x), math.degrees(rot.y), math.degrees(rot.z))
        }
    
    @staticmethod
    def validate_camera_data(data):
        """Validate incoming camera motion data"""
        required_fields = ['X', 'Y', 'Z', 'ROT_X', 'ROT_Y', 'ROT_Z']
        
        # Check if all required fields are present
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Check if all values are numeric
        try:
            for field in required_fields:
                float(data[field])
        except (ValueError, TypeError):
            return False, f"Invalid numeric value in field: {field}"
        
        return True, "Valid data"
    
    @staticmethod
    def apply_camera_motion(data):
        """Apply camera motion data to the active camera"""
        # Validate data
        is_valid, message = CameraController.validate_camera_data(data)
        if not is_valid:
            print(f"Invalid camera data: {message}")
            return False
        
        # Get or create camera
        camera = CameraController.get_active_camera()
        if not camera:
            camera = CameraController.create_camera_if_needed()
            if not camera:
                print("Failed to create camera")
                return False
        
        # Convert data to float
        try:
            location = (float(data['X']), float(data['Y']), float(data['Z']))
            rotation = (float(data['ROT_X']), float(data['ROT_Y']), float(data['ROT_Z']))
        except (ValueError, TypeError) as e:
            print(f"Error converting data to float: {e}")
            return False
        
        # Apply transform
        success = CameraController.set_camera_transform(camera, location, rotation)
        
        if success:
            # Update viewport
            CameraController.update_viewport()
            print(f"Applied camera motion: Location={location}, Rotation={rotation}")
        
        return success
    
    @staticmethod
    def update_viewport():
        """Update the 3D viewport to reflect camera changes"""
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
    
    @staticmethod
    def reset_camera():
        """Reset camera to default position"""
        camera = CameraController.get_active_camera()
        if camera:
            camera.location = (0, 0, 0)
            camera.rotation_euler = (0, 0, 0)
            CameraController.update_viewport()
            print("Camera reset to default position")
            return True
        return False

# Utility functions for easy access
def get_active_camera():
    """Get the active camera"""
    return CameraController.get_active_camera()

def create_camera_if_needed():
    """Create a camera if none exists"""
    return CameraController.create_camera_if_needed()

def apply_camera_motion(data):
    """Apply camera motion data"""
    return CameraController.apply_camera_motion(data)

def reset_camera():
    """Reset camera to default position"""
    return CameraController.reset_camera()

def validate_camera_data(data):
    """Validate camera motion data"""
    return CameraController.validate_camera_data(data)
