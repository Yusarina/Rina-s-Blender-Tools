import bpy
import functions.bones
from core.translations import t
from core.addonpreferences import AddonPreferences
from functions.bones import get_bone_items, MergeBones
from bpy.props import StringProperty, EnumProperty

class RinasPluginProps(bpy.types.PropertyGroup):
    merge_base_bone: bpy.props.EnumProperty(items=get_bone_items)

class OptimizationSubMenu(bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_RINA_Optimization'
    bl_label = t('OptimizationSubMenu.label')

    merge_base_bone: bpy.props.EnumProperty()

    def draw(self, context):
        self.merge_base_bone = context.scene.rinas_plugin.merge_base_bone
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

        box = layout.box()
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5

        col.separator()
        col.separator()  
        layout.prop(scene.rinas_plugin, "merge_base_bone")
        self.merge_base_bone = context.scene.rinas_plugin.merge_base_bone
        # print("Selected bone:", self.merge_base_bone)  # Add this line to check the selected bone
        layout.prop(context.scene, "merge_ratio")
        
        layout.operator("rinasplugin.merge_bones_main")
        col.separator()  
        layout.operator("rinasplugin.remove_zero_weight_bones")
