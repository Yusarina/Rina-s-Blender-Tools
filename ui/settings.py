import bpy
from core.translations import t, set_language

class SettingsSubMenu(bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_RINA_Settings'
    bl_label = "SettingsSubMenu.label"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 0.4

        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        sub.scale_y = 0.75

        sub.label(text=t("SettingsSubMenu.LanguageLabel"))
        col.separator()
        col.separator()
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        sub.scale_y = 0.75
        sub.prop(context.scene, "plugin_language")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Callback function for updating the language property
def update_language(self, context):
    set_language(context.scene.plugin_language)
