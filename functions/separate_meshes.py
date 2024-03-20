import bpy 
from core.translations import t
from core.common import get_armature, get_meshes, unselect_all, fix_uv_coordinates
from core.registry import register

@register
class SeparateByMaterials(bpy.types.Operator):
    bl_idname = "rinasplugin.separate_by_materials"
    bl_label = t("SeparateByMaterials.label")
    bl_description = t("SeparateByMaterials.description")
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return get_armature(context) is not None

    def execute(self, context):
        armature = get_armature(context)
        meshes = get_meshes(armature)

        for mesh in meshes:

            unselect_all()

            mesh.select_set(True)
            context.view_layer.objects.active = mesh

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.separate(type='MATERIAL')
            bpy.ops.object.mode_set(mode='OBJECT')

            fix_uv_coordinates(context)

        self.report({'INFO'}, t('SeparateByMaterials.success'))
        return {'FINISHED'}

@register
class SeparateLooseParts(bpy.types.Operator):
    bl_idname = "rinasplugin.separate_loose_parts"
    bl_label = t('SeparateLooseParts.label')
    bl_description = t('SeparateLooseParts.description')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return get_armature(context) is not None

    def execute(self, context):
        armature = get_armature(context)
        meshes = get_meshes(armature)

        for mesh in meshes:

            unselect_all()

            mesh.select_set(True)
            context.view_layer.objects.active = mesh

            bpy.ops.object.mode_set(mode='EDIT') 
            bpy.ops.mesh.separate(type='LOOSE')
            bpy.ops.object.mode_set(mode='OBJECT')

            fix_uv_coordinates(context)

        self.report({'INFO'}, t('SeparateLooseParts.success'))
        return {'FINISHED'}
    