import bpy
import re
from core.common import get_objects, get_meshes, get_armature, unselect_all, select
from core.translations import t
from bpy.props import EnumProperty

exclude_bones = ['Hips', 'Chest', 'Thumb', 'Head', 'Neck', 'Spine', 'Twist', 'Eye', 'Tongue', 'Finger', 'Shoulder', 'Arm', 'Elbow', 'Wrist', 'Leg', 'Knee', 'Ankle', 'Toe', 'Teeth', 'Hand', 'BreastUpper2']

def bone_is_excluded(bone_name):

    bone_name = bone_name.lower()
    
    # Check against exclude list
    if any(exclude.lower() in bone_name for exclude in exclude_bones):
        return True

    if re.search(r'([\._]_*\d{3,})', bone_name):
        return True

    if re.search(r'[\._]?\d{3,}[_.]?[LR]', bone_name):
        return True
    
    if re.search(r'\d', bone_name):
        return True
    
def get_bone_items(self, context):

    armature = get_armature(context)
    if not armature:
        return []

    items = []
    for bone in armature.data.bones:
        if not bone_is_excluded(bone.name):
            # print(f"Letting through: {bone.name}") 
            items.append((bone.name, bone.name, ""))

    return items

# The Below is from Cat's Blender Plugin, please note that it is under the GPL/ MIT license. Used it has my version just didn't work, full credit to them!

def mix_weights(mesh, vg_from, vg_to, mix_strength=1.0, mix_mode='ADD', delete_old_vg=True):
    mesh.active_shape_key_index = 0
    mod = mesh.modifiers.new("VertexWeightMix", 'VERTEX_WEIGHT_MIX')
    mod.vertex_group_a = vg_to
    mod.vertex_group_b = vg_from
    mod.mix_mode = mix_mode
    mod.mix_set = 'B'
    mod.mask_constant = mix_strength
    apply_modifier(mod)
    if delete_old_vg:
        mesh.vertex_groups.remove(mesh.vertex_groups.get(vg_from))
    mesh.active_shape_key_index = 0  # This line fixes a visual bug in 2.80 which causes random weights to be stuck after being merged

def apply_modifier(mod, as_shapekey=False):
    if as_shapekey:
        bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=False, modifier=mod.name)
    else:
        bpy.ops.object.modifier_apply(modifier=mod.name)

# End of code from Cats Blender Plugin

def connect_bones_to_children(armature):
    if armature and armature.type == 'ARMATURE':
        bpy.ops.object.mode_set(mode='EDIT')
        for bone in armature.data.edit_bones:
            if bone.parent:
                # Store the original head and tail positions
                original_head = bone.head.copy()
                original_tail = bone.tail.copy()

                # Connect the bone to its parent
                bone.use_connect = True

                # Restore the original head and tail positions
                bone.head = original_head
                bone.tail = original_tail

        bpy.ops.object.mode_set(mode='OBJECT')
        return True
    return False

def delete_zero_weight(armature):
    bpy.ops.object.mode_set(mode='EDIT')
    unselect_all()

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

def remove_constraints(context):
    armature = get_armature(context)
    
    if armature and armature.type == 'ARMATURE':
        removed = False
        for bone in armature.pose.bones:
            for con in bone.constraints:
                bone.constraints.remove(con)
                removed = True

    return {'FINISHED'} if removed else {'CANCELLED'}

def merge_weights(armature, parent_list, keep_merged_bones):
    bpy.ops.object.mode_set(mode='OBJECT')
    # Merge the weights on the meshes
    for mesh in get_meshes(armature):
        select(mesh)

        for bone, parent in parent_list.items():
            if not mesh.vertex_groups.get(bone):
                continue
            if not mesh.vertex_groups.get(parent):
                mesh.vertex_groups.new(name=parent)
            mix_weights(mesh, bone, parent)

    # Select armature
    unselect_all()
    select(armature)
    bpy.ops.object.mode_set(mode='EDIT')

    # Delete merged bones if not keeping them
    if not keep_merged_bones:
        for bone in parent_list.keys():
            armature.data.edit_bones.remove(armature.data.edit_bones.get(bone))

class MergeBones(bpy.types.Operator):
    bl_idname = "rinasplugin.merge_bones_main"
    bl_label = t("MergeBones.label")
    bl_description = t("MergeBones.description")
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        scene = context.scene
        base_bone_name = context.scene.rinas_plugin.merge_base_bone

        if not base_bone_name:
            self.report({'ERROR'}, t('MergeBones.error.no_base_bone'))
            return {'CANCELLED'}    

        armature_obj = context.active_object

        if not armature_obj or armature_obj.type != 'ARMATURE':
            self.report({'ERROR'}, t('MergeBones.error.no_armature'))
            return {"CANCELLED"}
        
        armature = armature_obj.data

        if not armature:
            self.report({'ERROR'}, t('MergeBones.error.invalid_armature'))
            return {"CANCELLED"}

        # print("All bones in the armature:")
        # for bone in armature.bones:
            # print(bone.name)

        # print(f"Base bone name: {base_bone_name}")
        base_bone = armature.bones.get(base_bone_name)

        if not base_bone:
            self.report({'ERROR'}, t('MergeBones.error.invalid_base_bone'))
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
                self.report({'ERROR'}, t('MergeBones.error.parent_bone_not_found').format(bone_name=edit_bone.name))
                return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, t('MergeBones.info.merged_bones').format(count=num_merged))

        return {'FINISHED'}

class RemoveZeroWeightBones(bpy.types.Operator):
    bl_idname = "rinasplugin.remove_zero_weight_bones"
    bl_label = t("RemoveZeroWeightBones.label")
    bl_description = t("RemoveZeroWeightBones.description")
    bl_options = {'REGISTER', 'UNDO'} 
    
    def execute(self, context):
        armature = get_armature(context)
        deleted_bones = delete_zero_weight(armature)
        
        if deleted_bones == 0:
            self.report({'INFO'}, t('RemoveZeroWeightBones.info.no_bones_found'))
        else:
            self.report({'INFO'}, t('RemoveZeroWeightBones.info.removed_zero_bones').format(count=deleted_bones))
                
        return {'FINISHED'}

class RemoveConstraints(bpy.types.Operator):
    bl_idname = "rinasplugin.remove_constraints"
    bl_label = t("RemoveConstraints.label")
    bl_description = t("RemoveConstraints.description")
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        result = remove_constraints(context)
        
        if result == {'FINISHED'}:
            self.report({'INFO'}, t('RemoveConstraints.info.success'))
        else:
            self.report({'INFO'}, t('RemoveConstraints.info.no_constraints'))
            
        return result

class MergeBoneWeightsToParent(bpy.types.Operator):
    bl_idname = "rinasplugin.merge_bone_weights_to_parent"
    bl_label = "Merge Bone Weights to Parent"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_ARMATURE' and context.selected_editable_bones

    def execute(self, context):
        armature = context.active_object
        keep_merged_bones = context.scene.keep_merged_bones

        # Find which bones to work on and put their name and their parent in a list
        parent_list = {}
        for bone in context.selected_editable_bones:
            parent = bone.parent
            if parent:
                parent_list[bone.name] = parent.name

        # Merge all the bones in the parenting list
        merge_weights(armature, parent_list, keep_merged_bones)

        self.report({'INFO'}, f"Merged weights of {len(parent_list)} bones to their parents.")
        return {'FINISHED'}

class MergeBoneWeightsToActive(bpy.types.Operator):
    bl_idname = "rinasplugin.merge_bone_weights_to_active"
    bl_label = "Merge Bone Weights to Active"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_ARMATURE' and context.selected_editable_bones and len(context.selected_editable_bones) > 1 and context.active_bone in context.selected_editable_bones

    def execute(self, context):
        armature = context.active_object
        keep_merged_bones = context.scene.keep_merged_bones

        # Find which bones to work on and put their name and the active bone's name in a list
        parent_list = {}
        for bone in context.selected_editable_bones:
            if bone != context.active_bone:
                parent_list[bone.name] = context.active_bone.name

        # Merge all the bones in the parenting list
        merge_weights(armature, parent_list, keep_merged_bones)

        self.report({'INFO'}, f"Merged weights of {len(parent_list)} bones to the active bone.")
        return {'FINISHED'}

class ConnectBonesToChildren(bpy.types.Operator):
    bl_idname = "rinasplugin.connect_bones_to_children"
    bl_label = "Connect Bones to Children"
    bl_description = "Connect all bones to their respective children"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = get_armature(context)
        if connect_bones_to_children(armature):
            self.report({'INFO'}, "Connected bones to their children")
        else:
            self.report({'WARNING'}, "No armature found in the scene")
        return {'FINISHED'}