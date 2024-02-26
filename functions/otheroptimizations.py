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
            self.report({'ERROR'}, "No mesh object selected!")
            return {'CANCELLED'}
        
        threshold = 0.00001 # set threshold value
        removed_tris = remove_doubles(obj, threshold, save_shapes=True)
        
        self.report({'INFO'}, f"Removed {removed_tris} tris by merging vertices")
        return {'FINISHED'}