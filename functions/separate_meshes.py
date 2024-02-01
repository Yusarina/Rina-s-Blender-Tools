import bpy 
from core.translations import t
from core.common import get_armature, get_meshes

class SeparateByMaterials(bpy.types.Operator):
    bl_idname = "rinasplugin.separate_by_mesh"
    bl_label = t("SeparateByMaterial.label")
    bl_description = t("SeparateByMaterial.description")
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return get_armature(context) is not None

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj 
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.separate(type='MATERIAL')
                bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

class SeparateLooseParts(bpy.types.Operator):
    bl_idname = "rinasplugin.separate_loose_parts"
    bl_label = t('SeparateLooseParts.label')
    bl_description = t('SeparateLooseParts.description')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return get_armature(context) is not None

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT') 
                bpy.ops.mesh.separate(type='LOOSE')
                bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}
    