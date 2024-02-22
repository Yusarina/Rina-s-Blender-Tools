import bpy
from core.translations import t
import addon_updater_ops

class QuickAccessSubMenu(bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_RINA_QuickAccess'
    bl_label = t('QuickAccessSubMenu.label')
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        addon_updater_ops.check_for_update_background()
        box = layout.box()
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5
    

        col.separator()
        col.separator()
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.1
        row.operator("rinasplugin.join_all_meshes")
        row.operator("rinasplugin.combine_materials")
        col.separator()
        col.separator()
        addon_updater_ops.update_notice_box_ui(self, context)