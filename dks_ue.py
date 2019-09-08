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
from distutils import dir_util
import json
from pathlib import Path as pathlib_path

_preferences={}

def dks_ue_get_export_sub():
 
    global _preferences
    
    _file_name = bpy.context.blend_data.filepath
    _file_path = _file_name[0:len(_file_name)-len(bpy.path.basename(_file_name))]
    _file_sub = _file_path[len(_preferences["option_ue_src"]):]
    
    return _file_sub

def dks_ue_get_export_path():
    
    global _preferences

    _file_sub = dks_ue_get_export_sub()
    _export_path = _preferences["option_ue_dst"]+_file_sub

    if not path.exists(_export_path):
        makedirs(_export_path)

    return _export_path

def dks_ue_get_file_name():

    return bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')

def dks_ue_filename():

    _object_name = dks_ue_get_file_name()
    _export_path = dks_ue_get_export_path()
    _export_file = _export_path + _object_name + '.fbx'
 
    return _export_file

def screenshot(self, context):
    
    global _preferences

    _object_name = dks_ue_get_file_name()
    _object_file = dks_ue_get_export_path() + _object_name + '_Icon.png'

    if _preferences["option_override_camera"]:

        bpy.context.scene.camera.location = _preferences["option_camera_location"]
        bpy.context.scene.camera.rotation_euler = _preferences["option_camera_rotation"]

    bpy.ops.render.render(use_viewport=True)

    bpy.data.scenes["Scene"].render.filepath = _object_file
    bpy.context.scene.render.image_settings.file_format='PNG'
    bpy.context.scene.render.filepath = _object_file
    bpy.context.scene.render.resolution_x = _preferences["option_icon_resolution_x"]
    bpy.context.scene.render.resolution_y = _preferences["option_icon_resolution_y"]
    bpy.context.scene.render.resolution_percentage = 100

    bpy.context.scene.cycles.film_transparent = True

    bpy.ops.render.render()
    
    bpy.data.images["Render Result"].save_render(_object_file)

def dks_ue_fbx_export(self, context):

    _export_file = dks_ue_filename()

    bpy.ops.export_scene.fbx(filepath=_export_file, use_selection=False, check_existing=False, axis_forward='Y', axis_up='Z', filter_glob="*.fbx", global_scale=1.0, apply_unit_scale=True, bake_space_transform=False, object_types={'EMPTY','MESH','ARMATURE'}, use_mesh_modifiers=True, mesh_smooth_type='EDGE', use_mesh_edges=False, use_tspace=False, use_custom_props=False, add_leaf_bones=False, primary_bone_axis='Y', secondary_bone_axis='X', use_armature_deform_only=False, bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=1.0, embed_textures=False, batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)

    return _export_file

def dks_ue_folder_crawl(directory):
    
    found=""

    path_check=path.join(directory, "blender_addon_ue.json")

    if path.exists(path_check):
        found=path_check
    else:        
        path_parent=pathlib_path(directory).parent
        if path_parent!=directory:
            found=dks_ue_folder_crawl(path_parent)
    
    return found

def dks_ue_get_texture_file(texture_path,mesh_name,mat_name,texture_name,texture_ext):

    if path.exists(texture_path+mesh_name+'_'+mat_name+'_'+texture_name+'.'+texture_ext):
        return texture_path+mesh_name+'_'+mat_name+'_'+texture_name+'.'+texture_ext
    elif path.exists(texture_path+mat_name+'_'+texture_name+'.'+texture_ext):
        return texture_path+mat_name+'_'+texture_name+'.'+texture_ext
    else:
        _blend=dks_ue_get_file_name()
        if path.exists(texture_path+_blend+'_'+mesh_name+'_'+texture_name+'.'+texture_ext):
            return texture_path+_blend+'_'+mesh_name+'_'+texture_name+'.'+texture_ext
        elif path.exists(texture_path+_blend+'_'+mat_name+'_'+texture_name+'.'+texture_ext):
            return texture_path+_blend+'_'+mat_name+'_'+texture_name+'.'+texture_ext
        else:
            return ""

class dks_ue_export(bpy.types.Operator):

    bl_idname = "dks_ue.export"
    bl_label = "UE"
    bl_description = "Export to UE"

    def execute(self, context):
        
        global _preferences

        if bpy.context.preferences.addons[__package__].preferences.option_save_before_export:
            bpy.ops.wm.save_mainfile()

        _file_name = bpy.context.blend_data.filepath
        _file_path = _file_name[0:len(_file_name)-len(bpy.path.basename(_file_name))]
        
        _file_json=dks_ue_folder_crawl(_file_path)
        
        if _file_json!="":
                
            try:
                with open(_file_json) as _file_json_data:
                    _preferences = json.load(_file_json_data)
            except Exception as e:
                print("blender_addon_ue.json is invalid: ",str(e.reason))
                return {'FINISHED'}
            
            if "option_ue_src" not in _preferences:
                _preferences["option_ue_src"]=bpy.context.preferences.addons[__package__].preferences.option_ue_src
            
            if "option_ue_dst" not in _preferences:
                _preferences["option_ue_dst"]=bpy.context.preferences.addons[__package__].preferences.option_ue_dst

            if "option_create_icon" not in _preferences:
                _preferences["option_create_icon"]=bpy.context.preferences.addons[__package__].preferences.option_create_icon

            if "option_override_camera" not in _preferences:
                _preferences["option_override_camera"]=bpy.context.preferences.addons[__package__].preferences.option_override_camera

            if "option_icon_resolution_x" not in _preferences:
                _preferences["option_icon_resolution_x"]=bpy.context.preferences.addons[__package__].preferences.option_icon_resolution_x

            if "option_icon_resolution_y" not in _preferences:
                _preferences["option_icon_resolution_y"]=bpy.context.preferences.addons[__package__].preferences.option_icon_resolution_y

            if "option_camera_location" in _preferences:
                _preferences["option_camera_location"]=(_preferences["option_camera_location"]["x"],_preferences["option_camera_location"]["y"],_preferences["option_camera_location"]["z"])
            else:
                _preferences["option_camera_location"] = bpy.context.preferences.addons[__package__].preferences.option_camera_location

            if "option_camera_rotation" in _preferences:
                _preferences["option_camera_rotation"]=(math.radians(_preferences["option_camera_rotation"]["x"]),math.radians(_preferences["option_camera_rotation"]["y"]),math.radians(_preferences["option_camera_rotation"]["z"]))
            else:
                _preferences["option_camera_rotation"] = (math.radians(bpy.context.preferences.addons[__package__].preferences.option_camera_rotation[0]),math.radians(bpy.context.preferences.addons[__package__].preferences.option_camera_rotation[1]),math.radians(bpy.context.preferences.addons[__package__].preferences.option_camera_rotation[2]))

            if "option_create_icon" not in _preferences:
                _preferences["option_create_icon"]=bpy.context.preferences.addons[__package__].preferences.option_create_icon

            if "option_textures_folder" not in _preferences:
                _preferences["option_textures_folder"]=bpy.context.preferences.addons[__package__].preferences.option_textures_folder

            if "option_ue_json" not in _preferences:
                _preferences["option_ue_json"]=bpy.context.preferences.addons[__package__].preferences.option_ue_json

        else:

            _preferences["option_ue_src"]=bpy.context.preferences.addons[__package__].preferences.option_ue_src
            _preferences["option_ue_dst"]=bpy.context.preferences.addons[__package__].preferences.option_ue_dst
            _preferences["option_create_icon"]=bpy.context.preferences.addons[__package__].preferences.option_create_icon
            _preferences["option_override_camera"]=bpy.context.preferences.addons[__package__].preferences.option_override_camera
            _preferences["option_icon_resolution_x"]=bpy.context.preferences.addons[__package__].preferences.option_icon_resolution_x
            _preferences["option_icon_resolution_y"]=bpy.context.preferences.addons[__package__].preferences.option_icon_resolution_y
            _preferences["option_camera_location"] = bpy.context.preferences.addons[__package__].preferences.option_camera_location
            _preferences["option_camera_rotation"] = (math.radians(bpy.context.preferences.addons[__package__].preferences.option_camera_rotation[0]),math.radians(bpy.context.preferences.addons[__package__].preferences.option_camera_rotation[1]),math.radians(bpy.context.preferences.addons[__package__].preferences.option_camera_rotation[2]))
            _preferences["option_copy_textures"]=bpy.context.preferences.addons[__package__].preferences.option_copy_textures
            _preferences["option_textures_folder"]=bpy.context.preferences.addons[__package__].preferences.option_textures_folder
            _preferences["option_ue_json"]=bpy.context.preferences.addons[__package__].preferences.option_ue_json

        if _preferences["option_create_icon"]:

            screenshot(self, context)

        _export_file = dks_ue_fbx_export(self, context)

        if _preferences["option_copy_textures"]:

            _path_textures_from = bpy.path.abspath('//') + _preferences["option_textures_folder"] + sep
            _path_textures_to = dks_ue_get_export_path() + _preferences["option_textures_folder"] + sep

            if path.exists(_path_textures_from):
                dir_util.copy_tree(_path_textures_from, _path_textures_to)

            blender_data = {}
            blender_data['path']=dks_ue_get_export_sub().replace("\\","/")
            blender_data['options'] = {}
            
            blender_data['options']['ImportMaterials']=True;
            blender_data['options']['ImportAnimations']=True;
            blender_data['options']['CreatePhysicsAsset']=True;
            
            blender_data['materials'] = []

            _objects = bpy.context.scene.objects
            _texture_ext="png"

            for _obj in _objects:

                if _obj.type=='MESH':

                    _obj_name = _obj.name

                    _materials = _obj.data.materials

                    for _material in _materials:

                        _material_name = _material.name
                        
                        _material_data = {}
                        _material_data["name"]=_material_name

                        _file_Base_Color = dks_ue_get_texture_file(_path_textures_from,_obj_name,_material_name,'Base_Color',_texture_ext)
                        if _file_Base_Color=="":
                            _file_Base_Color = dks_ue_get_texture_file(_path_textures_from,_obj_name,_material_name,'BaseColor',_texture_ext)
                        _file_Ambient_occlusion = dks_ue_get_texture_file(_path_textures_from,_obj_name,_material_name,'Ambient_occlusion',_texture_ext)
                        _file_Metallic = dks_ue_get_texture_file(_path_textures_from,_obj_name,_material_name,'Metallic',_texture_ext)
                        _file_Roughness = dks_ue_get_texture_file(_path_textures_from,_obj_name,_material_name,'Roughness',_texture_ext)
                        _file_ORM = dks_ue_get_texture_file(_path_textures_from,_obj_name,_material_name,'OcclusionRoughnessMetallic',_texture_ext)
                        _file_Opacity = dks_ue_get_texture_file(_path_textures_from,_obj_name,_material_name,'Opacity',_texture_ext)
                        _file_Normal = dks_ue_get_texture_file(_path_textures_from,_obj_name,_material_name,'Normal',_texture_ext)
                        if _file_Normal=="":
                            _file_Normal = dks_ue_get_texture_file(_path_textures_from,_obj_name,_material_name,'Normal_OpenGL',_texture_ext)
                        _file_Emissive = dks_ue_get_texture_file(_path_textures_from,_obj_name,_material_name,'Emissive',_texture_ext)

                        _material_data['base_color']=_file_Base_Color[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                        _material_data['normal']=_file_Normal[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                        _material_data['orm']=_file_ORM[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                        _material_data['opacity']=_file_Opacity[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                        _material_data['ambient_occlusion']=_file_Ambient_occlusion[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                        _material_data['metallic']=_file_Metallic[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                        _material_data['roughness']=_file_Roughness[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                        _material_data['emissive']=_file_Emissive[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                        
                        blender_data['materials'].append(_material_data)
            
            json_data = json.dumps(blender_data, sort_keys=False, indent=3)
            json_data_filename = dks_ue_filename().replace(".fbx",".bjd")
            
            with open(json_data_filename, 'w') as f:
                json.dump(blender_data, f)
        
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

