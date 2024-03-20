import bpy
import functions.bones
from core.translations import t
from core.addonpreferences import AddonPreferences
from functions.bones import get_bone_items, MergeBones
from bpy.props import StringProperty, EnumProperty
from core.registry import register

@register
class RinasPluginProps(bpy.types.PropertyGroup):
    bl_idname = "rinasplugin.rinapluginprops"
    
    merge_base_bone: bpy.props.EnumProperty(items=get_bone_items)

@register
class OptimizationSubMenu(bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_RINA_Optimization'
    bl_label = t('OptimizationSubMenu.label')

    def draw(self, context):
        
        scene = context.scene
        layout = self.layout

        box = layout.box()
        row = box.row()  
        row.prop(scene, "show_mesh_options", text=t("RinasBlenderToolsPanel.MeshOptions"), icon="TRIA_DOWN" if scene.show_mesh_options else "TRIA_RIGHT", emboss=False)
        if scene.show_mesh_options:
            # Call the submenu class
            MeshOptionsSubMenu.draw(self, context)

        box = layout.box()
        row = box.row()  
        row.prop(scene, "show_bones_options", text=t("RinasBlenderToolsPanel.BoneOptions"), icon="TRIA_DOWN" if scene.show_bones_options else "TRIA_RIGHT", emboss=False)
        if scene.show_bones_options:
            # Call the submenu class
            BoneOptionsSubMenu.draw(self, context)

@register
class MeshOptionsSubMenu(bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_RINA_MeshOptions'
    bl_label = t('RinasBlenderToolsPanel.MeshOptions')

    def draw(self, context):
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
        sub.label(text=t("OptimizationSubMenu.MeshOptions"), icon='NONE') 
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

@register
class BoneOptionsSubMenu(bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_RINA_BoneOptions'
    bl_label = t('OptimizationSubMenu.BoneOptions')

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

        split = col.row(align=True)
        row = split.row(align=True)
        sub.label(text=t("OptimizationSubMenu.BoneOptions"), icon='NONE') 
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        row.scale_y = 1.1
        col.separator()
        row.prop(scene.rinas_plugin, "merge_base_bone", text=t('MergeBones.base_bone'))
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.1 
        col.separator() 
        self.merge_base_bone = context.scene.rinas_plugin.merge_base_bone
        row.prop(context.scene, "merge_ratio", text=t('MergeBones.ratio'))
        
        row.operator("rinasplugin.merge_bones_main")
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.1 
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        sub.label(text=t("OptimizationSubMenu.BoneOptionsDelete"), icon='X')  
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.1 
        col.separator() 
        row.operator("rinasplugin.remove_zero_weight_bones")
        row.operator("rinasplugin.remove_constraints")
        col.separator()
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        row.prop(scene, "keep_merged_bones")
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        row.scale_y = 1.1 
        sub.label(text=t("OptimizationSubMenu.MergeBonesWieghts"), icon='NONE')  
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        row.scale_y = 1.1 
        row.operator("rinasplugin.merge_bone_weights_to_parent")
        row.operator("rinasplugin.merge_bone_weights_to_active")
        col.separator()
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        row.scale_y = 1.1
        row.operator("rinasplugin.connect_bones_to_children")

