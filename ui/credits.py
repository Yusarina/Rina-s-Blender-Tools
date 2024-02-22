import bpy
from core.translations import t

class CreditsSubMenu(bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_RINA_Credits'
    bl_label = t('CreditsSubMenu.label')

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

        sub.label(text=t("CreditsSubMenu.CreditsTitle")) 
        
        col.separator()
        col.separator()
        
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        sub.scale_y = 0.75
        sub.label(text=t("CreditsSubMenu.ForTheCommunity1")) 
        sub.label(text=t("CreditsSubMenu.ForTheCommunity2"))  

        col.separator()

        split = box.split()
        row = split.row()
        row.scale_y = 1.1
        row.operator("wm.url_open", text=t('CreditsSubMenu.YusarinaWebsite'), icon='INFO').url = "https://yusarina.xyz"
        split = box.split()
        row = split.row()
        row.operator("wm.url_open", text=t('CreditsSubMenu.Yusarinakofi'), icon='INFO').url = "https://ko-fi.com/yusarina"