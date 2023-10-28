import bpy
import os
from bpy_extras.io_utils import ExportHelper

class Exporter:
    def __init__(self, filepath, preset):
        self.basedir = os.path.dirname(bpy.data.filepath)
        if not self.basedir:
            raise Exception("Blend file is not saved")
        self.view_layer = bpy.context.view_layer
        self.obj_active = self.view_layer.objects.active
        self.selection = bpy.context.selected_objects
        self.filepath = filepath
        self.preset = preset

    def export(self):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in self.selection:
            obj.select_set(True)
            self.view_layer.objects.active = obj
            name = bpy.path.clean_name(obj.name)
            fn = os.path.join(self.filepath, name)  # Adjusted filepath
            export_settings = self.get_export_settings(self.preset)
            
            # move to orign
            obj_original_location = obj.location.copy()
            obj.location = bpy.context.scene.cursor.location
            
            #export
            bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, **export_settings)
            
            #move back
            obj.location = obj_original_location
            
            obj.select_set(False)
            print("written:", fn)

        self.view_layer.objects.active = self.obj_active
        for obj in self.selection:
            obj.select_set(True)
    
    def get_export_settings(self, preset):
        # Define preset settings
        presets = {
            'UNREAL_ENGINE_5': {
                'global_scale': 1.0,
                'apply_scale_options': 'FBX_SCALE_NONE',
                # ... other settings
            },
            # ... other presets
        }
        return presets.get(preset, {})

class SimpleOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "object.simple_operator"
    bl_label = "Export To Location"
    bl_options = {'PRESET'}
    
    filename_ext = ".fbx"  # The expected file extension

    preset: bpy.props.EnumProperty(
        name="Export Preset",
        items=[
            ('UNREAL_ENGINE_5', "Unreal Engine 5", ""),
            # ... add more presets as needed
        ]
    )

    def execute(self, context):
        exporter = Exporter(os.path.dirname(self.filepath), self.preset)  # Pass the directory and preset to the Exporter
        exporter.export()
        return {'FINISHED'}

class SimplePanel(bpy.types.Panel):
    bl_label = "Mass Export FBX"
    bl_idname = "PT_SimplePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout
        layout.operator_menu_enum(SimpleOperator.bl_idname, "preset")  # Adjusted to use operator_menu_enum for preset selection

def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.utils.register_class(SimplePanel)

def unregister():
    bpy.utils.unregister_class(SimplePanel)
    bpy.utils.unregister_class(SimpleOperator)

if __name__ == "__main__":
    register()
