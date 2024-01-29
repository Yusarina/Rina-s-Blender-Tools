import bpy
from ui.quick_access import QuickAccessSubMenu
from ui.optimization import OptimizationSubMenu
from ui.credits import CreditsSubMenu


class RinasBlenderToolsPanel(bpy.types.Panel):
    bl_label = "Rina's Blender Tools"
    bl_idname = '3D_VIEW_RinasPluginPanel'
    bl_category = "Rina's Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
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

        sub.label(text="Thank you for using rina's", icon='INFO')
        sub.label(text="blender tools, if you need help", icon='NONE') 
        sub.label(text="help please visit the wiki below!", icon='NONE')

        col.separator()
        col.separator()

        split = box.split() # Split to align
        row = split.row()
        row.scale_y = 1.1
        row.operator("wm.url_open", text="Wiki", icon='INFO').url = "https://github.com/Yusarina/Rina-s-Blender-Tools/wiki"

        box = layout.box()
        row = box.row()  
        row.prop(scene, "show_quick_access", text="Quick Access", icon="TRIA_DOWN" if scene.show_quick_access else "TRIA_RIGHT", emboss=False)
        if scene.show_quick_access:
            # Call the submenu class
            QuickAccessSubMenu.draw(self, context)

        box = layout.box()
        row = box.row()  
        row.prop(scene, "show_optimization", text="Optimization", icon="TRIA_DOWN" if scene.show_optimization else "TRIA_RIGHT", emboss=False)
        if scene.show_optimization:
            # Call the submenu class
            OptimizationSubMenu.draw(self, context)

        box = layout.box()
        row = box.row()  
        row.prop(scene, "show_credits", text="Credits", icon="TRIA_DOWN" if scene.show_credits else "TRIA_RIGHT", emboss=False)
        if scene.show_credits:
            # Call the submenu class
            CreditsSubMenu.draw(self, context)

        
