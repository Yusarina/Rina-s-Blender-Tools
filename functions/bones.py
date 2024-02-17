import bpy
from bpy.props import StringProperty, FloatProperty
from core.common import get_armature

class MergeBones(bpy.types.Operator):
    bl_idname = "rinasplugin.merge_bones"
    bl_label =  "Merge Bones"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        armature = get_armature(context)

        base_bone_name = scene.merge_base_bone
        ratio = context.scene.merge_ratio / 100.0

        bpy.ops.object.mode_set(mode='EDIT')
        
        base_bone = armature.data.edit_bones[base_bone_name]
        base_children = base_bone.children_recursive
        
        num_to_merge = int(len(base_children) * ratio)
        merge_bones = base_children[:num_to_merge]
        

        # Merge the bones
        for pose_bone in merge_bones:
            edit_bone = armature.data.edit_bones[pose_bone.name]
            armature.data.edit_bones.remove(edit_bone)
            pose_bone.parent = base_bone
            
        armature.data.edit_bones.remove(base_bone)

        bpy.ops.object.mode_set(mode='OBJECT')
        
        return {'FINISHED'}