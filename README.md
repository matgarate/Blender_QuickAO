# Blender_QuickAO
Add-on for Blender 2.8 to add an AO and color ramp node to all materials assigned to the active object. 
The node preserves the base color of the material. 
Desgined to save time when importing objects from AssetForge.


How to use:
1. Select an object that has multiple materials assigned.*
2. Hit F3, and search for the command "Quick AO Nodes"
3. Hit Enter, and adjust the AO distance and color ramp properties in the operator panel on the bottom left of the 3D viewport.

* So  far it has only been tested with materials that have a Principled BSDF Node connected to the Material Output Node. It may throw an error if no Shader Node is connected.
