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

import bpy, math
from bpy.utils import register_class, unregister_class
from subprocess import Popen
from os import system, path, makedirs, sep
import os, sys
import distutils.dir_util

def dks_ue_get_export_path():
    
    _file_name = bpy.context.blend_data.filepath
    _file_path = _file_name[0:len(_file_name)-len(bpy.path.basename(_file_name))]
    _file_sub = _file_path[len(bpy.context.preferences.addons["blender_addon_ue"].preferences.option_ue_src):]
    _export_path = bpy.context.preferences.addons["blender_addon_ue"].preferences.option_ue_dst+_file_sub

    if not path.exists(_export_path):
        makedirs(_export_path)

    return _export_path

def dks_ue_filename(self, context):

    _object_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
    _export_path = dks_ue_get_export_path()
    _export_file = _export_path + _object_name + '.fbx'
 
    if not bpy.context.preferences.addons[__package__].preferences.option_save_before_export:
        bpy.ops.wm.save_mainfile()

    return _export_file


def screenshot(self, context):
    
    _object_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
    _object_file = dks_ue_get_export_path() + _object_name + '_Icon.png'
    
    if bpy.context.preferences.addons[__package__].preferences.option_override_camera:

        bpy.context.scene.camera.location = bpy.context.preferences.addons[__package__].preferences.option_camera_location
        bpy.context.scene.camera.rotation_euler = bpy.context.preferences.addons[__package__].preferences.option_camera_rotation


    bpy.ops.render.render(use_viewport=True)

    bpy.data.scenes["Scene"].render.filepath = _object_file
    bpy.context.scene.render.image_settings.file_format='PNG'
    bpy.context.scene.render.filepath = _object_file
    bpy.context.scene.render.resolution_x = bpy.context.preferences.addons[__package__].preferences.option_icon_resolution_x
    bpy.context.scene.render.resolution_y = bpy.context.preferences.addons[__package__].preferences.option_icon_resolution_y
    bpy.context.scene.render.resolution_percentage = 100

    bpy.context.scene.cycles.film_transparent = True

    bpy.ops.render.render()
    
    bpy.data.images["Render Result"].save_render(_object_file)

def dks_ue_fbx_export(self, context):

    _export_file = dks_ue_filename(self, context)

    bpy.ops.export_scene.fbx(filepath=_export_file, use_selection=False, check_existing=False, axis_forward='Y', axis_up='Z', filter_glob="*.fbx", global_scale=1.0, apply_unit_scale=True, bake_space_transform=False, object_types={'EMPTY','MESH','ARMATURE'}, use_mesh_modifiers=True, mesh_smooth_type='EDGE', use_mesh_edges=False, use_tspace=False, use_custom_props=False, add_leaf_bones=False, primary_bone_axis='Y', secondary_bone_axis='X', use_armature_deform_only=False, bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=1.0, embed_textures=False, batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)

    return _export_file

class dks_ue_export(bpy.types.Operator):

    bl_idname = "dks_ue.export"
    bl_label = "UE"
    bl_description = "Export to UE"

    def execute(self, context):

        if bpy.context.preferences.addons[__package__].preferences.option_create_icon:

            screenshot(self, context)

        if bpy.context.preferences.addons[__package__].preferences.option_copy_textures:

            _path_textures_from = bpy.path.abspath('//') + "Textures" + sep
            _path_textures_to = dks_ue_get_export_path() + "Textures" + sep

            if path.exists(_path_textures_from):
                distutils.dir_util.copy_tree(_path_textures_from, _path_textures_to)

        _export_file = dks_ue_fbx_export(self, context)

        return {'FINISHED'}

classes = (
    dks_ue_export,
)

def register():

    for cls in classes:
        register_class(cls)

def unregister():

    for cls in reversed(classes):
        unregister_class(cls)

