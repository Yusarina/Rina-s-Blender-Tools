import bpy
from core.common import fix_uv_coordinates
from core.translations import t

class JoinAllMeshes(bpy.types.Operator):
    bl_idname = "rinasplugin.join_all_meshes"    
    bl_label = t("CombineMaterials.label")
    bl_description = t('JoinAllMeshes.description')
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        self.join_all_meshes(context)
        return {'FINISHED'}

    # Join all meshes in the scene and perform various operations on the joined mesh.
    def join_all_meshes(self, context):
        # Check if there is an active object
        if context.active_object is None:
            self.report({'WARNING'}, "No active object. No mesh objects selected for joining")
            return

        # Switch to Object Mode to ensure correct context
        bpy.ops.object.mode_set(mode='OBJECT')

        # Deselect all objects
        bpy.context.view_layer.objects.active = None
        bpy.ops.object.select_all(action='DESELECT')

        # Select all mesh objects
        bpy.ops.object.select_by_type(type='MESH')

        # Check if there are selected objects before joining
        selected_objects = bpy.context.selected_objects
        if selected_objects:
            # Join selected meshes
            bpy.context.view_layer.objects.active = selected_objects[0]
            bpy.ops.object.join()

            # Apply all transforms
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
            # Fix UV coordinates
            fix_uv_coordinates(context)

            # Switch back to Object Mode
            bpy.ops.object.mode_set(mode='OBJECT')

            # Report success message
            self.report({'INFO'}, "Meshes joined successfully")
        else:
            # Report message if no mesh objects are selected
            self.report({'WARNING'}, "No mesh objects selected for joining")

class JoinSelectedMeshes(bpy.types.Operator):
    bl_idname = "rinasplugin.join_selected_meshes"
    bl_label = t("CombineMaterials.label")
    bl_description = t("CombineMaterials.description")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        self.join_selected_meshes(context)
        return {'FINISHED'}

    # Join selected meshes.
    def join_selected_meshes(self, context):
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        if not selected_objects:
            # Report message if no mesh objects are selected
            self.report({'WARNING'}, "No mesh objects selected for joining")
            return

        # Switch to Object Mode to ensure correct context
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Check if there is an active object
        if context.active_object is None:
            self.report({'WARNING'}, "No active object. No mesh objects selected for joining")
            return

        # Deselect all objects
        bpy.context.view_layer.objects.active = None
        bpy.ops.object.select_all(action='DESELECT')

        # Select the selected mesh objects
        for obj in selected_objects:
            obj.select_set(True)

        # Check if there are selected objects before joining
        if bpy.context.selected_objects:
            # Join selected meshes
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
            bpy.ops.object.join()

            # Apply all transforms
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

            # Fix UV coordinates
            fix_uv_coordinates(context)

            # Switch back to Object Mode
            bpy.ops.object.mode_set(mode='OBJECT')

            # Report success message
            self.report({'INFO'}, "Meshes joined successfully")
        else:
            # Report message if no mesh objects are selected (after deselecting all)
            self.report({'WARNING'}, "No mesh objects selected for joining")
            