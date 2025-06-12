# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Mass KeyFrame",
    "blender": (4,4,2),
    "category": "Animation",
    "author": "StratosDerg",
    "warning": "",
    "description": "Support for adding and duplicating keyframes to properties."
}

import bpy # type: ignore
from mathutils import * # type: ignore

D = bpy.data
C = bpy.context

class MassKeyframe(bpy.types.Operator):
    """Duplicate a property and add a keyframe to all selected objects"""
    bl_idname = "animation.mass_duplicate_keyframe"
    bl_label = "Dupicate Keyframe to Selected Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.property:
            active = context.property
            block, path, index = active
            value = getattr(block, path)
            masskf(context=context, path=path, index=index, value=value, copy=True)

        return {'FINISHED'}
    
def masskf(context, path, index, value=None, copy=False):
        for obj in context.selected_objects:
            if hasattr(obj, path):
                if copy==True:
                    setattr(obj, path, value)
                obj.keyframe_insert(
                    data_path=path, index=index, frame=context.scene.frame_current
                )

class NoDupe(bpy.types.Operator):
    """Add a keyframe for selected property for all selected objects"""
    bl_idname = "animation.mass_add_keyframe"
    bl_label = "Add Keyframe to Selected Objects"
    bl_options = {'REGISTER','UNDO'}

    def execute(self,context):
        if context.property:
            active = context.property
            block, path, index = active
            masskf(context=context, path=path, index=index, copy=False)
        
        return {'FINISHED'}

def menu_func(self,context):
    layout = self.layout
    layout.separator()
    self.layout.operator(MassKeyframe.bl_idname)
    self.layout.operator(NoDupe.bl_idname)

def register():
    bpy.utils.register_class(MassKeyframe)
    bpy.utils.register_class(NoDupe)
    bpy.types.UI_MT_button_context_menu.append(menu_func)

def unregister():
    bpy.utils.unregister_class(MassKeyframe)
    bpy.utils.unregister_class(NoDupe)
    bpy.types.UI_MT_button_context_menu.remove(menu_func)

if __name__ == "__main__":
    register()
