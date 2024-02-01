import bpy
from core.translations import t

class OtherOptionsSubMenu(bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_RINA_OtherOptions'
    bl_label = t('RinasBlenderToolsPanel.OtherOptions')

    def draw(self, context):
        scene = context.scene
        layout = self.layout
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
        row.operator("rinasplugin.separate_by_mesh")
        row.operator("rinasplugin.separate_loose_parts")
        col.separator()
        col.separator()

