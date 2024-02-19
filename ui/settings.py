import bpy
from core.translations import t

class SettingsSubMenu(bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_RINA_Settings'
    bl_label = "SettingsSubMenu.label"
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        box = layout.box()
        
        col = box.column(align=True)
        col.label(text=t("SettingsSubMenu.LanguageLabel"))

        col.separator()
        
        split = col.row(align=True)
        split.prop(context.scene, 'plugin_language', text='')

        col.separator()
        col.separator()
        