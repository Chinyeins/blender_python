bl_info = {
    "name": "Mass Export FBX with Collisions for Blender | Unreal Engine",
    "author": "Christopher-Robin Fey",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "3D View > Tool Shelf > UE5 Asset Kit Exporter",
    "description": "Export selected objects and their collision meshes as FBX files for Unreal Engine.",
    "warning": "",
    "wiki_url": "https://github.com/Chinyeins/blender_python",
    "tracker_url": "https://github.com/Chinyeins/blender_python",
    "category": "Import-Export",
}

import bpy
import os

class Exporter:
    def __init__(self, preset, export_path):
        self.view_layer = bpy.context.view_layer
        self.selection = bpy.context.selected_objects
        self.preset = preset
        self.export_path = export_path
        self.valid_prefixes = ["UCX_", "UBX_", "USP_"]  # Collision prefixes for Unreal Engine.

    def find_collision_meshes(self, base_object):
        """Find collision meshes for the given base object."""
        collisions = []
        base_name = base_object.name
        for obj in bpy.data.objects:
            if obj.name.startswith(tuple(self.valid_prefixes)) and obj.name.endswith(base_name):
                collisions.append(obj)
        return collisions

    def move_to_cursor_with_offset(self, obj, cursor_location, base_location):
        """Move an object to the cursor location while maintaining its offset from the base object."""
        offset = obj.location - base_location
        obj.location = cursor_location + offset

    def restore_location(self, obj, original_location):
        """Restore an object's original location."""
        obj.location = original_location

    def export(self):
        """Export selected objects with their collision meshes."""
        cursor_location = bpy.context.scene.cursor.location.copy()

        for base_obj in self.selection:
            if not base_obj.select_get():
                continue

            # Collect original locations for restoration
            original_locations = {obj: obj.location.copy() for obj in bpy.data.objects}

            # Find collision meshes
            collision_meshes = self.find_collision_meshes(base_obj)

            # Move base object to origin cursor
            base_obj_original_location = base_obj.location.copy()
            base_obj.location = cursor_location

            # Move collision meshes relative to the base object
            for coll in collision_meshes:
                self.move_to_cursor_with_offset(coll, cursor_location, base_obj_original_location)

            # Select base object and collision meshes
            bpy.ops.object.select_all(action='DESELECT')
            base_obj.select_set(True)
            for coll in collision_meshes:
                coll.select_set(True)

            # Export as FBX
            export_file = os.path.join(self.export_path, f"{base_obj.name}.fbx")
            bpy.ops.export_scene.fbx(filepath=export_file, use_selection=True)
            print(f"Exported: {export_file}")

            # Restore original locations
            for obj, loc in original_locations.items():
                self.restore_location(obj, loc)

        print("Export complete.")

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

    def execute(self, context):
        export_path = bpy.path.abspath(context.scene.simple_export_path)
        preset = context.scene.simple_export_preset

        exporter = Exporter(preset, export_path)
        exporter.export()

        # Show a completion message
        self.report({'INFO'}, f"Export completed! Files saved to: {export_path}")
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

class CreditsPanel(bpy.types.Panel):
    bl_label = "Credits"
    bl_idname = "PT_CreditsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'UE5 Asset Kit Exporter'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Mass Export FBX Addon")
        layout.label(text="Created by: ChinyONE")
        layout.label(text="GitHub: github.com/Chinyeins")


def register():
    bpy.utils.register_class(CreditsPanel)
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
    bpy.utils.unregister_class(CreditsPanel)
    bpy.utils.unregister_class(SimplePanel)
    bpy.utils.unregister_class(SimpleOperator)
    bpy.utils.unregister_class(SetExportPathOperator)
    del bpy.types.Scene.simple_export_preset
    del bpy.types.Scene.simple_export_path

if __name__ == "__main__":
    register()
