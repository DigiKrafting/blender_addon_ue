# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
        "name": "DKS UE",
        "description": "Export to UE",
        "author": "DigiKrafting.Studio",
        "version": (0, 5, 0),
        "blender": (2, 80, 0),
        "location": "Info Toolbar, File -> Export",
        "wiki_url":    "https://github.com/DigiKrafting/blender_addon_ue/wiki",
        "tracker_url": "https://github.com/DigiKrafting/blender_addon_ue/issues",
        "category": "Import-Export",
}

import bpy
from bpy.utils import register_class, unregister_class
from . import dks_ue

class dks_ue_addon_prefs(bpy.types.AddonPreferences):

        bl_idname = __package__

        option_ue_src : bpy.props.StringProperty(
                name="Source Root Folder",
                subtype="DIR_PATH",
                default="",
        )     
        option_ue_dst : bpy.props.StringProperty(
                name="Destination Root Folder",
                subtype="DIR_PATH",
                default="",
        )     
        option_save_before_export : bpy.props.BoolProperty(
                name="Save Before Export",
                default=True,
        )
        option_create_icon : bpy.props.BoolProperty(
                name="Create Icon",
                default=True,
        )
        option_icon_resolution_x : bpy.props.IntProperty(
                name="Resolution Width",
                default=64,
        )        
        option_icon_resolution_y : bpy.props.IntProperty(
                name="Resolution Height",
                default=64,
        )        
        option_copy_textures : bpy.props.BoolProperty(
                name="Copy Textures Folder",
                default=True,
        )
        option_override_camera : bpy.props.BoolProperty(
                name="Override Camera Location/Rotation",
                default=False,
        )
        option_camera_location : bpy.props.FloatVectorProperty(
                name="Camera Location",
        )                                            
        option_camera_rotation : bpy.props.FloatVectorProperty(
                name="Camera Rotation",
        )                                            
        option_display_type : bpy.props.EnumProperty(
                items=[('Buttons', "Buttons", "Use Buttons"),('Menu', "Menu", "Append a Menu to Main Menu"),('Hide', "Import/Export", "Use only Import/Export Menu's"),],
                name="Display Type",
                default='Buttons',
        )
        option_textures_folder : bpy.props.StringProperty(
                name="Textures Folder Name",
                default="Textures",
        )
        option_ue_json : bpy.props.BoolProperty(
                name="Create UE JSON",
                default=False,
        )                
        def draw(self, context):

                layout = self.layout

                box=layout.box()
                box.prop(self, 'option_display_type')
                box.prop(self, 'option_save_before_export')
                box=layout.box()
                box.prop(self, 'option_ue_src')
                box.prop(self, 'option_ue_dst')
                box=layout.box()
                box.prop(self, 'option_textures_folder')
                box.label(text='Sub folder relative to the saved .blend file. * Do NOT include any "\\".',icon='INFO')
                box=layout.box()
                box.prop(self, 'option_create_icon')
                box.prop(self, 'option_icon_resolution_x')
                box.prop(self, 'option_icon_resolution_y')                
                box.prop(self, 'option_override_camera')
                box.prop(self, 'option_camera_location')
                box.prop(self, 'option_camera_rotation')
                box=layout.box()
                box.prop(self, 'option_copy_textures')
                box=layout.box()
                box.prop(self, 'option_ue_json')
                box.label(text='Creates a "{fbx_file_name}.bjd" for the UE Plugin.',icon='INFO')

class dks_ue_menu(bpy.types.Menu):

    bl_label = " " + bl_info['name']
    bl_idname = "dks_ue.menu"

    def draw(self, context):
            
        layout = self.layout

        self.layout.operator('dks_ue.export',icon="EXPORT")

def draw_dks_ue_menu(self, context):

        layout = self.layout
        layout.menu(dks_ue_menu.bl_idname,icon="COLLAPSEMENU")

def dks_ue_menu_func_export(self, context):
    self.layout.operator(dks_ue_export.bl_idname)

def dks_ue_toolbar_btn_export(self, context):

    if context.region.alignment != 'RIGHT':

        self.layout.operator('dks_ue.export',text="UE",icon="EXPORT")

classes = (
    dks_ue_addon_prefs,
)

def register():

        for cls in classes:
                register_class(cls)

        dks_ue.register()

        bpy.types.TOPBAR_MT_file_export.append(dks_ue_menu_func_export)

        if bpy.context.preferences.addons[__package__].preferences.option_display_type=='Buttons':
    
                bpy.types.TOPBAR_HT_upper_bar.append(dks_ue_toolbar_btn_export)

        elif bpy.context.preferences.addons[__package__].preferences.option_display_type=='Menu':

                register_class(dks_ue_menu)
                bpy.types.TOPBAR_MT_editor_menus.append(draw_dks_ue_menu)

def unregister():

        bpy.types.TOPBAR_MT_file_export.remove(dks_ue_menu_func_export)

        if bpy.context.preferences.addons[__package__].preferences.option_display_type=='Buttons':

                bpy.types.TOPBAR_HT_upper_bar.remove(dks_ue_toolbar_btn_export)

        elif bpy.context.preferences.addons[__package__].preferences.option_display_type=='Menu':

                bpy.types.TOPBAR_MT_editor_menus.remove(draw_dks_ue_menu)
                unregister_class(dks_ue_menu)

        dks_ue.unregister()
                
        for cls in reversed(classes):
                unregister_class(cls)

if __name__ == "__main__":

	register()