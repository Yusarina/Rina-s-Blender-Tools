import bpy
import re
from core.common import get_objects, get_meshes, get_armature, unselect_all
from bpy.props import EnumProperty

exclude_bones = ['Hips', 'Chest', 'Thumb', 'Head', 'Neck', 'Spine', 'Twist', 'Eye', 'Tongue', 'Finger', 'Shoulder', 'Arm', 'Elbow', 'Wrist', 'Leg', 'Knee', 'Ankle', 'Toe', 'Teeth', 'Hand']

def bone_is_excluded(bone_name):

    bone_name = bone_name.lower()
    
    # Check against exclude list
    if any(exclude.lower() in bone_name for exclude in exclude_bones):
        return True

    # Filter out 2+ digits at end
    if re.search(r'\d{2,}$', bone_name):
        return True

    # Filter out .002+, _002+ patterns
    if re.search(r'([\._]_*\d{3,})$', bone_name):
        return True

    # Filter out 002+ patterns after side suffix
    if re.search(r'[\._]?\d{3,}[_.]?[LR]$', bone_name):
        return True
    
    return False

def get_bone_items(self, context):

    armature = context.active_object
    if not armature or armature.type != 'ARMATURE':
        return []

    items = []
    for bone in armature.data.bones:
        if not bone_is_excluded(bone.name):
            items.append((bone.name, bone.name, ""))

    return items

class MergeBones(bpy.types.Operator):
    bl_idname = "rinasplugin.merge_bones_main"
    bl_label =  "Merge Bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        base_bone_name = context.scene.rinas_plugin.merge_base_bone

        if not base_bone_name:
            self.report({'ERROR'}, "No base bone selected")
            return {'CANCELLED'}    

        armature_obj = context.active_object

        if not armature_obj or armature_obj.type != 'ARMATURE':
            self.report({"ERROR"}, "No armature object set")
            return {"CANCELLED"}
        
        armature = armature_obj.data

        if not armature:
            self.report({"ERROR"}, "Invalid armature object")
            return {"CANCELLED"}

        # print("All bones in the armature:")
        # for bone in armature.bones:
            # print(bone.name)

        # print(f"Base bone name: {base_bone_name}")
        base_bone = armature.bones.get(base_bone_name)

        if not base_bone:
            self.report({'ERROR'}, "Invalid base bone") 
            return {'CANCELLED'}
        
        # print(f"Base bone found: {base_bone.name}")

        ratio = context.scene.merge_ratio / 100.0

        bpy.ops.object.mode_set(mode='EDIT') 

        base_bone_name = scene.merge_base_bone
        base_children = base_bone.children_recursive
        num_to_merge = int(len(base_children) * ratio)
        merge_bones = base_children[:num_to_merge]

        bpy.ops.object.mode_set(mode='EDIT') 

        num_merged = len(merge_bones)

        for bone in merge_bones:
            edit_bone = armature.edit_bones.get(bone.name)
            if edit_bone and edit_bone.parent:
                parent_name = edit_bone.parent.name
                # print(f"Parent bone: {parent_name}")
                edit_bone.parent = armature.edit_bones[parent_name] 
                armature.edit_bones.remove(edit_bone)
            else:
                self.report({'ERROR'}, f"Parent bone {edit_bone.name} not found")
                return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, f"Merged {num_merged} bones")

        return {'FINISHED'}

def delete_zero_weight(armature):
    bpy.ops.object.mode_set(mode='EDIT')

    bone_names_to_work_on = {b.name for b in armature.data.edit_bones}
    
    bone_name_to_edit_bone = {}
    for eb in armature.data.edit_bones:
        bone_name_to_edit_bone[eb.name] = eb

    used_vertex_groups = set()
    vgroup_name_to_objects = {}
    for obj in get_meshes(armature):
        vgroup_to_name = {v.index: v.name for v in obj.vertex_groups}
        for v in obj.data.vertices:
            for g in v.groups:
                if g.weight > 0:
                    name = vgroup_to_name.get(g.group)
                    used_vertex_groups.add(name)
                    if name not in vgroup_name_to_objects:
                        vgroup_name_to_objects[name] = set()
                    vgroup_name_to_objects[name].add(obj)

    unused_bones = bone_names_to_work_on - used_vertex_groups

    count = 0
    for name in unused_bones:
        armature.data.edit_bones.remove(bone_name_to_edit_bone[name])
        count += 1
        if name in vgroup_name_to_objects:
            for obj in vgroup_name_to_objects[name]:
                vgroup = obj.vertex_groups.get(name)
                if vgroup:
                    obj.vertex_groups.remove(vgroup)

    bpy.ops.object.mode_set(mode='OBJECT')
    
    return count

class RemoveZeroWeightBones(bpy.types.Operator):
    bl_idname = "rinasplugin.remove_zero_weight_bones"
    bl_label = "Remove Zero Weight Bones"
    bl_options = {'REGISTER', 'UNDO'} 
    
    def execute(self, context):
        armature = get_armature(context)
        deleted_bones = delete_zero_weight(armature)
        
        if deleted_bones == 0:
            self.report({'INFO'}, "No unused bones found")
        else:
            self.report({'INFO'}, f"Deleted {deleted_bones} zero weight bones")
        
        return {'FINISHED'}