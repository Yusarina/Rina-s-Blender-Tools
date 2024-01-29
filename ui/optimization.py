import bpy

class OptimizationSubMenu(bpy.types.Menu):
    bl_idname = 'VIEW3D_RINA_Optimization'
    bl_label = "Optimization"

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
        row.operator("rinasplugin.join_all_meshes")
        row.operator("rinasplugin.join_selected_meshes")
        col.separator()
        col.separator()
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.1
        row.operator("rinasplugin.combine_materials")
        col.separator()
        col.separator()