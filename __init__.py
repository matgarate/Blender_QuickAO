bl_info = {
    "name" : "Quick AO Nodes - BETA",
    "author" : "Matias Garate",
    "description" : "Add an AO and Color ramp node all the materials of the active object (it preserves the Base Color of the object).",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}


import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, FloatVectorProperty
from mathutils import Vector



def Add_AO_Nodes(self, context, AO_distance, ramp_left_position, ramp_right_position, ramp_black_color):
        
    active_object = context.active_object
    for material_slot in active_object.material_slots:
        
        # Read the Node Tree
        try:
            node_tree = material_slot.material.node_tree
        except:
            # If the maetrial slot is empty then mode on.
            continue
        
        # Obtain the node connected to the Material Output
        # It should be a Principled Shader
        main_node = node_tree.nodes['Material Output'].inputs[0].links[0].from_node    
        base_color = main_node.inputs[0].default_value
        
        # Create the ColorRamp
        ramp_node = node_tree.nodes.new('ShaderNodeValToRGB')

        ramp_node.color_ramp.elements[0].position = ramp_left_position    
        ramp_node.color_ramp.elements[1].position = ramp_right_position
        ramp_node.color_ramp.elements[0].color = (ramp_black_color[0], ramp_black_color[1],ramp_black_color[2], 1.0)  
        ramp_node.color_ramp.elements[1].color = base_color
        
        # Create the AO Node
        AO_node = node_tree.nodes.new('ShaderNodeAmbientOcclusion')
        AO_node.inputs['Distance'].default_value = AO_distance
        
        
        # Link the Color Ramp Color to the Principled BSDF
        # Link the AO to the Color Ramp
        node_tree.links.new(ramp_node.outputs[0], main_node.inputs[0])
        node_tree.links.new(AO_node.outputs[0], ramp_node.inputs[0])


        # Adjust the Color Ramp and AO positions
        ramp_node.location = main_node.location + Vector((-400,0))
        AO_node.location = ramp_node.location + Vector((-300,0))
        



class OBJECT_OT_add_quickAO(Operator):
    """Add an AO and color ramp node to all the materials of the active object"""
    bl_idname = "object.add_quick_ambient_occlusion_nodes"
    bl_label = "Quick AO Nodes"
    bl_options = {'REGISTER', 'UNDO'}



    AO_distance: FloatProperty(
        name="AO distance",
        default=0.1,
        min = 0.0,
        max = 1000.,
        description="AO distance"
    )
    ramp_left_position: FloatProperty(
        name="Ramp Left Position",
        default=0.0,
        min = 0.0,
        max = 1.0,
        description="Color Ramp left handle position"
    )
    ramp_right_position: FloatProperty(
        name="Ramp Right Position",
        default=1.0,
        min = 0.0,
        max = 1.0,
        description="Color Ramp right handle position"
    )
    ramp_black_color: FloatVectorProperty(
        name="AO Black Color",
        subtype= 'COLOR',
        default=(0.0, 0.0, 0.0),
        min=0.0, max=1.0,
        description="Replace the default black color of the color ramp"
    )


    def execute(self, context):

        Add_AO_Nodes(self, context, self.AO_distance, self.ramp_left_position, self.ramp_right_position, self.ramp_black_color)

        return {'FINISHED'}
    
    

def register():
    bpy.utils.register_class(OBJECT_OT_add_quickAO)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_quickAO)

if __name__ == "__main__":
    register()