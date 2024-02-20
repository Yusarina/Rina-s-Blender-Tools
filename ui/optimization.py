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
        sub = col.column(align=True)
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
        row.operator("rinasplugin.remove_doubles")
        col.separator()
        col.separator()
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.1
        row.operator("rinasplugin.combine_materials")
        col.separator()
        col.separator()

        box = layout.box()
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        row.scale_y = 1.5

        col.separator()
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        sub.label(text=t("OptimizationSubMenu.BoneOptions"), icon='NONE') 
        col.separator()
        row.prop(scene.rinas_plugin, "merge_base_bone", text=t('MergeBones.base_bone'))
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        row.scale_y = 1.1 
        col.separator() 
        self.merge_base_bone = context.scene.rinas_plugin.merge_base_bone
        row.prop(context.scene, "merge_ratio", text=t('MergeBones.ratio'))
        
        row.operator("rinasplugin.merge_bones_main")
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        row.scale_y = 0.3
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        sub.label(text=t("OptimizationSubMenu.BoneOptionsDelete"), icon='X')  
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        col.separator() 
        row.operator("rinasplugin.remove_zero_weight_bones")
        row.operator("rinasplugin.remove_constraints")
        col.separator() 
