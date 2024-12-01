import bpy
import os
from bpy_extras.io_utils import ExportHelper

class Exporter:
    def __init__(self, filepath, preset, export_path):
        self.basedir = os.path.dirname(bpy.data.filepath)
        if not self.basedir:
            raise Exception("Blend file is not saved")
        self.view_layer = bpy.context.view_layer
        self.obj_active = self.view_layer.objects.active
        self.selection = bpy.context.selected_objects
        self.filepath = filepath
        self.preset = preset
        self.export_path = export_path

    def export(self):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in self.selection:
            obj.select_set(True)
            self.view_layer.objects.active = obj
            name = bpy.path.clean_name(obj.name)
            fn = os.path.join(self.export_path, name)
            export_settings = self.get_export_settings(self.preset)
            
            # Move to origin
            obj_original_location = obj.location.copy()
            obj.location = bpy.context.scene.cursor.location
            
            # Export
            bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, **export_settings)
            
            # Move back
            obj.location = obj_original_location
            
            obj.select_set(False)
            print("written:", fn)

        self.view_layer.objects.active = self.obj_active
        for obj in self.selection:
            obj.select_set(True)
    
    def get_export_settings(self, preset):
        presets = {
            'UNREAL_ENGINE_5': {
                'global_scale': 1.0,
                'apply_scale_options': 'FBX_SCALE_NONE',
                # ... other settings
            },
        }
        return presets.get(preset, {})

class SetExportPathOperator(bpy.types.Operator):
    """Set Export Path"""
    bl_idname = "export.set_export_path"
    bl_label = "Select Export Path"

    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def execute(self, context):
        context.scene.simple_export_path = self.directory
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Export Objects"

    preset: bpy.props.EnumProperty(
        name="Export Preset",
        items=[
            ('UNREAL_ENGINE_5', "Unreal Engine 5", ""),
        ]
    )

    def execute(self, context):
        exporter = Exporter(
            os.path.dirname(bpy.data.filepath),
            context.scene.simple_export_preset,
            bpy.path.abspath(context.scene.simple_export_path)
        )
        exporter.export()
        return {'FINISHED'}

class SimplePanel(bpy.types.Panel):
    bl_label = "Mass Export FBX"
    bl_idname = "PT_SimplePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'UE5 Asset Kit Exporter'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        # Preset Dropdown
        row = col.row(align=True)
        row.label(text="Export Preset:")
        row.prop(context.scene, "simple_export_preset", text="")

        # Export Path with Folder Selector
        row = col.row(align=True)
        row.label(text="Export Path:")
        row.prop(context.scene, "simple_export_path", text="")
        col.operator(SetExportPathOperator.bl_idname, text="Select Folder")

        # Export Button
        col.operator(SimpleOperator.bl_idname, text="Export")

def register():
    bpy.utils.register_class(SetExportPathOperator)
    bpy.utils.register_class(SimpleOperator)
    bpy.utils.register_class(SimplePanel)
    
    bpy.types.Scene.simple_export_preset = bpy.props.EnumProperty(
        name="Export Preset",
        items=[
            ('UNREAL_ENGINE_5', "Unreal Engine 5", ""),
        ],
        default='UNREAL_ENGINE_5'
    )
    bpy.types.Scene.simple_export_path = bpy.props.StringProperty(
        name="Export Path",
        description="Folder where the FBX files will be exported",
        default="//"
    )

def unregister():
    bpy.utils.unregister_class(SimplePanel)
    bpy.utils.unregister_class(SimpleOperator)
    bpy.utils.unregister_class(SetExportPathOperator)
    del bpy.types.Scene.simple_export_preset
    del bpy.types.Scene.simple_export_path

if __name__ == "__main__":
    register()
