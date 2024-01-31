import bpy
from core.translations import t

class OptimizationSubMenu(bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_RINA_Optimization'
    bl_label = t('OptimizationSubMenu.label')

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
        row.operator("rinasplugin.join_all_meshes", text=t("JoinAllMeshes.label"))
        row.operator("rinasplugin.join_selected_meshes", text=t("JoinSelectedMeshes.label"))
        col.separator()
        col.separator()
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.1
        row.operator("rinasplugin.remove_doubles", text=t("RemoveDoubles.label"))
        col.separator()
        col.separator()
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.1
        row.operator("rinasplugin.combine_materials", text=t("CombineMaterials.label"))
        col.separator()
        col.separator()
