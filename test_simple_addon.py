bl_info = {
    "name": "Test Simple Addon",
    "author": "Test",
    "version": (1, 0, 0),
    "blender": (3, 3, 0),
    "location": "View3D > Sidebar > Test",
    "description": "A simple test addon",
    "warning": "",
    "doc_url": "",
    "category": "Test",
}

import bpy
from bpy.types import Panel

class TEST_PT_main_panel(Panel):
    bl_label = "Test Panel"
    bl_idname = "TEST_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Test'

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a test panel!")
        layout.label(text="If you can see this, panels work!")

classes = [TEST_PT_main_panel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    print("Test addon registered successfully!")

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("Test addon unregistered!")

if __name__ == "__main__":
    register()
