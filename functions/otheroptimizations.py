import bpy 
from core.translations import t
from core.common import remove_doubles

class RemoveDoubles(bpy.types.Operator):
    bl_idname = "rinasplugin.remove_doubles"
    bl_label = t("RemoveDoubles.label")
    bl_description = t('RemoveDoubles.description')
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, t('RemoveDoubles.Error.nomesh'))
            return {'CANCELLED'}
        
        threshold = 0.00001 # set threshold value
        removed_tris = remove_doubles(obj, threshold, save_shapes=True)
        
        self.report({'INFO'}, t('RemoveDoubles.info.remove_doubles').format(count=removed_tris))
        return {'FINISHED'}