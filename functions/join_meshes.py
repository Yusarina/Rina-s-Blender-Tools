import bpy
from core.common import unlock_transforms

class JoinAllMeshes(bpy.types.Operator):
    bl_label = "Join All Meshes"
    bl_idname = "rinasplugin.join_all_meshes"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        self.join_all_meshes()
        return {'FINISHED'}

    def join_all_meshes(self):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.join()


class JoinSelectedMeshes(bpy.types.Operator):
    bl_label = "Join Selected Meshes"
    bl_idname = "rinasplugin.join_selected_meshes"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        self.join_selected_meshes(context)
        return {'FINISHED'}

    def join_selected_meshes(self, context):
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        if len(selected_objects) > 1:
            bpy.context.view_layer.objects.active = selected_objects[0]
            bpy.ops.object.join()

