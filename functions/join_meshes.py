import bpy
from core.common import fix_uv_coordinates
from core.translations import t
from core.common import get_armature, get_meshes, unselect_all

class JoinAllMeshes(bpy.types.Operator):
    bl_idname = "rinasplugin.join_all_meshes"    
    bl_label = t("JoinAllMeshes.label")
    bl_description = t('JoinAllMeshes.description')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return get_armature(context) is not None
    
    def execute(self, context):
        self.join_all_meshes(context)
        return {'FINISHED'}

    # Join all meshes in the scene and perform various operations on the joined mesh.
    def join_all_meshes(self, context):
        # Check if there is an active object
        if context.active_object is None:
            self.report({'INFO'}, t('JoinAllMeshes.info.noobject'))
            return

        # Switch to Object Mode to ensure correct context
        bpy.ops.object.mode_set(mode='OBJECT')

        # Deselect all objects
        unselect_all()

        # Select all mesh objects
        meshes = get_meshes(get_armature(context))

        for mesh in meshes:
            mesh.select_set(True)

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

            # Deselect all objects again on end
            unselect_all()

            # Report success message
            self.report({'INFO'}, t('JoinAllMeshes.info.success'))
        else:
            # Report message if no mesh objects are selected
            self.report({'WARNING'}, t('JoinAllMeshes.info.warning'))

class JoinSelectedMeshes(bpy.types.Operator):
    bl_idname = "rinasplugin.join_selected_meshes"
    bl_label = t("JoinSelectedMeshes.label")
    bl_description = t("JoinSelectedMeshes.description")
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return get_armature(context) is not None
    
    def execute(self, context):
        self.join_selected_meshes(context)
        return {'FINISHED'}

    # Join selected meshes.
    def join_selected_meshes(self, context):
        meshes = get_meshes(get_armature(context))
        selected_objects = [m for m in meshes if m.select_get()] 

        if not selected_objects:
            # Report message if no mesh objects are selected
            self.report({'WARNING'}, t('JoinSelectedMeshes.warning.noobject'))
            return

        # Switch to Object Mode to ensure correct context
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Check if there is an active object
        if context.active_object is None:
            self.report({'WARNING'}, t('JoinSelectedMeshes.warning.noslectedmeshs'))
            return

        # Deselect all objects
        unselect_all()

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

            # Deselect all objects again on end
            unselect_all()

            # Report success message
            self.report({'INFO'}, t('JoinSelectedMeshes.info.success'))
        else:
            # Report message if no mesh objects are selected (after deselecting all)
            self.report({'WARNING'}, t('JoinSelectedMeshes.info.warning'))
            