import bpy 

def separate_by_mesh():
    # Code to take the active object and separate it into 
    # separate mesh objects for each mesh
    pass

class SeparateByMesh(bpy.types.Operator):
    bl_label = "Separate By Mesh"
    bl_idname = "rinasplugin.separate_by_mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        separate_by_mesh.separate_by_mesh()
        return {'FINISHED'}
