import bpy
from mathutils import Vector
from core.common import get_armature

EXCLUDE_BONES = ["Head", "LeftArm", "RightArm", "LeftLeg", "RightLeg"]  

def get_parent_bones(self, context):
    armature = context.active_object
    bones = armature.data.bones
    parent_bones = []

    armature = None
    for ob in context.scene.objects:
        if ob.type == 'ARMATURE':
            armature = ob
            break

    if not armature:
        return []
    
    for bone in bones:
        if bone.parent is None and bone.name not in EXCLUDE_BONES:
            parent_bones.append((bone.name, bone.name, "")) 

    return parent_bones

class MergeArmatureBones(bpy.types.Operator):
    bl_idname = "rinasplugin.merge_bones"
    bl_label = "Merge Bones"

    bone_parents: bpy.props.EnumProperty(
        items=get_parent_bones,
        name="Parent Bone"
    )

    merge_ratio: bpy.props.FloatProperty(
        name="Merge Ratio",
        default=0.5,
        min=0.1, 
        max=1.0
    )

    merged_bones = 0

    def execute(self, context):
        ratio = context.scene.rinas_props.merge_ratio
        armature = context.active_object

        armature = get_armature(context)

        if not armature:
            self.report({'ERROR'}, "No active armature found")
            return {'CANCELLED'}
        
        child_bones = get_child_bones(armature, self.bone_parents, self.merge_ratio)
            
        for bone in child_bones:
            self.merged_bones = merge_bone(bone, armature, self.merged_bones)

        self.report({'INFO'}, f"Merged {self.merged_bones} bones.")  
    
        return {'FINISHED'}
    
def get_child_bones(armature, parent_name, ratio):

    child_bones = []
    
    bones = armature.data.bones
    parent_bone = bones[parent_name]
    
    if parent_bone.children:
        sorted_children = sorted(parent_bone.children, key=lambda b: b.length)  
        
        num_to_merge = int(len(sorted_children) * ratio)
        
        for bone in sorted_children[:num_to_merge]:
            if bone.name not in EXCLUDE_BONES:
                child_bones.append(bone)

    return child_bones

def merge_bone(bone, armature, merged_bones):

    bpy.ops.object.mode_set(mode='EDIT')

    edit_bones = armature.data.edit_bones
    parent = edit_bones[bone.parent.name]
    bone_eb = edit_bones[bone.name]
    
    bone_vec = bone_eb.tail - bone_eb.head 
    bone_len = bone_vec.length
    
    new_tail = parent.tail + bone_vec
    
    parent.tail = new_tail
    
    # Offset and parent change
    for child in bone.children:
        if child.name in edit_bones:
            child_eb = edit_bones[child.name]  
            child_eb.head += Vector((0, bone_len, 0)) 
            child_eb.parent = parent

    # Remove merged bone 
    edit_bones.remove(bone_eb) 

    bpy.ops.object.mode_set(mode='OBJECT')

    merged_bones += 1
    
    return merged_bones
    