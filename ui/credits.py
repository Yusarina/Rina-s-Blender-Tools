import bpy

class CreditsSubMenu(bpy.types.Menu):
    bl_idname = 'VIEW3D_RINA_Credits'
    bl_label = "Credits"

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

        sub.label(text="Rina's Blender Tools Credits!")
        
        col.separator()
        col.separator()
        
        split = col.row(align=True)
        row = split.row(align=True)
        sub = col.column(align=True)
        sub.scale_y = 0.75
        sub.label(text="Made by Yusarina for the VRChat")
        sub.label(text="and blender community")  

        col.separator()

        split = box.split() # Split to align
        row = split.row()
        row.scale_y = 1.1
        row.operator("wm.url_open", text="Yusarina's Website", icon='INFO').url = "https://yusarina.xyz"
