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

_enums={
    "NormalImportMethod":{
        'ComputeNormals':1,
        'ImportNormalsAndTangents':2,
        'ImportNormals':3
    },
    "AnimationLength":{
        'AnimatedKey':1,
        'ExportedTime':2,
        'SetRange':3
    }
}
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

def dks_ue_create_bjd(self, context):

    global _preferences
    
    _dks_ue_options = context.scene.dks_ue_options

    blender_data = {}

    blender_data['Auto']=_dks_ue_options.option_ue_auto
    blender_data['Path']=dks_ue_get_export_sub().replace("\\","/")
    
    blender_data['Options'] = {}
    
    blender_data['Options']['ImportMesh']=_dks_ue_options.ue_ImportMesh;
    blender_data['Options']['ImportMaterials']=_dks_ue_options.ue_ImportMaterials;
    blender_data['Options']['ImportAnimations']=_dks_ue_options.ue_ImportAnimations;
    blender_data['Options']['CreatePhysicsAsset']=_dks_ue_options.ue_CreatePhysicsAsset;
    blender_data['Options']['AutoComputeLodDistances']=_dks_ue_options.ue_AutoComputeLodDistances;
    
    blender_data['Options']['Static_Mesh']={}
    blender_data['Options']['Static_Mesh']['NormalImportMethod']=_dks_ue_options.ue_static_mesh_NormalImportMethod;
    blender_data['Options']['Static_Mesh']['ImportMeshLODs']=_dks_ue_options.ue_static_mesh_ImportMeshLODs;
    blender_data['Options']['Static_Mesh']['CombineMeshes']=_dks_ue_options.ue_static_mesh_CombineMeshes;
    blender_data['Options']['Static_Mesh']['AutoGenerateCollision']=_dks_ue_options.ue_static_mesh_AutoGenerateCollision;
    
    blender_data['Options']['Skeletal_Mesh']={}
    blender_data['Options']['Skeletal_Mesh']['NormalImportMethod']=_dks_ue_options.ue_skeletal_mesh_NormalImportMethod;
    blender_data['Options']['Skeletal_Mesh']['ImportMeshLODs']=_dks_ue_options.ue_skeletal_mesh_ImportMeshLODs;
    blender_data['Options']['Skeletal_Mesh']['UseT0AsRefPose']=_dks_ue_options.ue_skeletal_mesh_UseT0AsRefPose;
    blender_data['Options']['Skeletal_Mesh']['PreserveSmoothingGroups']=_dks_ue_options.ue_skeletal_mesh_PreserveSmoothingGroups;
    blender_data['Options']['Skeletal_Mesh']['ImportMorphTargets']=_dks_ue_options.ue_skeletal_mesh_ImportMorphTargets;
    
    blender_data['Options']['Animation']={}
    blender_data['Options']['Animation']['AnimationLength']=_dks_ue_options.ue_animation_AnimationLength;
    blender_data['Options']['Animation']['FrameRangeMin']=_dks_ue_options.ue_animation_FrameRangeMin;
    blender_data['Options']['Animation']['FrameRangeMax']=_dks_ue_options.ue_animation_FrameRangeMax;
    blender_data['Options']['Animation']['ImportMeshesInBoneHierarchy']=_dks_ue_options.ue_animation_ImportMeshesInBoneHierarchy;
    blender_data['Options']['Animation']['UseDefaultSampleRate']=_dks_ue_options.ue_animation_UseDefaultSampleRate;
    blender_data['Options']['Animation']['CustomSampleRate']=_dks_ue_options.ue_animation_CustomSampleRate;
    blender_data['Options']['Animation']['ConvertScene']=_dks_ue_options.ue_animation_ConvertScene;

    blender_data['Materials'] = []

    if _preferences["option_copy_textures"]:

        _objects = bpy.context.scene.objects
        _texture_ext="png"

        _path_textures_from = bpy.path.abspath('//') + _preferences["option_textures_folder"] + sep
        _path_textures_to = dks_ue_get_export_path() + _preferences["option_textures_folder"] + sep

        for _obj in _objects:

            if _obj.type=='MESH':

                _obj_name = _obj.name

                _materials = _obj.data.materials

                for _material in _materials:

                    _material_name = _material.name
                    
                    _material_data = {}
                    _material_data["Name"]=_material_name

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

                    _material_data['BaseColor']=_file_Base_Color[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                    _material_data['Normal']=_file_Normal[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                    _material_data['ORM']=_file_ORM[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                    _material_data['Opacity']=_file_Opacity[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                    _material_data['AmbientOcclusion']=_file_Ambient_occlusion[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                    _material_data['Metallic']=_file_Metallic[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                    _material_data['Roughness']=_file_Roughness[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                    _material_data['Emissive']=_file_Emissive[len(bpy.path.abspath('//')):].replace("\\","/").replace("."+_texture_ext,"")
                    
                    blender_data['Materials'].append(_material_data)
    
    json_data_filename = dks_ue_filename().replace(".fbx",".bjd")
    
    with open(json_data_filename, 'w') as f:
        json.dump(blender_data, f)

class dks_ue_set_preferences(bpy.types.Operator):

    bl_idname = "dks_ue.set_preferences"
    bl_label = "Set from Preferences"
    bl_context = "scene"

    def execute(self, context):

        _dks_ue_prefs = bpy.context.preferences.addons[__package__].preferences
        _dks_ue_options = context.scene.dks_ue_options

        _dks_ue_options.option_ue_src=_dks_ue_prefs.option_ue_src
        _dks_ue_options.option_ue_dst=_dks_ue_prefs.option_ue_dst

        _dks_ue_options.option_json_search=_dks_ue_prefs.option_json_search
        _dks_ue_options.option_create_icon=_dks_ue_prefs.option_create_icon
        _dks_ue_options.option_icon_resolution_x=_dks_ue_prefs.option_icon_resolution_x
        _dks_ue_options.option_icon_resolution_y=_dks_ue_prefs.option_icon_resolution_y
        _dks_ue_options.option_override_camera=_dks_ue_prefs.option_override_camera
        _dks_ue_options.option_camera_location=_dks_ue_prefs.option_camera_location
        _dks_ue_options.option_camera_rotation=_dks_ue_prefs.option_camera_rotation

        _dks_ue_options.option_copy_textures=_dks_ue_prefs.option_copy_textures

        return {'FINISHED'}

class dks_ue_set_json_preferences(bpy.types.Operator):

    bl_idname = "dks_ue.set_json_preferences"
    bl_label = 'Set from "blender_addon_ue.json"'
    bl_context = "scene"

    def execute(self, context):

        _dks_ue_prefs = bpy.context.preferences.addons[__package__].preferences
        _dks_ue_options = context.scene.dks_ue_options

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

            _dks_ue_options.option_ue_src=_preferences["option_ue_src"]
            _dks_ue_options.option_ue_dst=_preferences["option_ue_dst"]

            _dks_ue_options.option_create_icon=_preferences["option_create_icon"]
            _dks_ue_options.option_icon_resolution_x=_preferences["option_icon_resolution_x"]
            _dks_ue_options.option_icon_resolution_y=_preferences["option_icon_resolution_y"]
            _dks_ue_options.option_override_camera=_preferences["option_override_camera"]
            _dks_ue_options.option_camera_location=_preferences["option_camera_location"]
            _dks_ue_options.option_camera_rotation=_preferences["option_camera_rotation"]

            _dks_ue_options.option_copy_textures=_preferences["option_copy_textures"]

        return {'FINISHED'}

class dks_ue_set_ue_preferences(bpy.types.Operator):

    bl_idname = "dks_ue.set_ue_preferences"
    bl_label = "Set from Preferences"
    bl_context = "scene"

    def execute(self, context):

        _dks_ue_prefs = bpy.context.preferences.addons[__package__].preferences
        _dks_ue_options = context.scene.dks_ue_options

        _dks_ue_options.option_ue_json=_dks_ue_prefs.option_ue_json
        _dks_ue_options.option_ue_auto=_dks_ue_prefs.option_ue_auto

        _dks_ue_options.ue_ImportMesh=_dks_ue_prefs.ue_ImportMesh
        _dks_ue_options.ue_ImportMaterials=_dks_ue_prefs.ue_ImportMaterials
        _dks_ue_options.ue_ImportAnimations=_dks_ue_prefs.ue_ImportAnimations
        _dks_ue_options.ue_CreatePhysicsAsset=_dks_ue_prefs.ue_CreatePhysicsAsset
        _dks_ue_options.ue_AutoComputeLodDistances=_dks_ue_prefs.ue_AutoComputeLodDistances
        
        _dks_ue_options.ue_static_mesh_NormalImportMethod=_dks_ue_prefs.ue_static_mesh_NormalImportMethod
        _dks_ue_options.ue_static_mesh_ImportMeshLODs=_dks_ue_prefs.ue_static_mesh_ImportMeshLODs
        _dks_ue_options.ue_static_mesh_CombineMeshes=_dks_ue_prefs.ue_static_mesh_CombineMeshes
        _dks_ue_options.ue_static_mesh_AutoGenerateCollision=_dks_ue_prefs.ue_static_mesh_AutoGenerateCollision
        
        _dks_ue_options.ue_skeletal_mesh_NormalImportMethod=_dks_ue_prefs.ue_skeletal_mesh_NormalImportMethod
        _dks_ue_options.ue_skeletal_mesh_ImportMeshLODs=_dks_ue_prefs.ue_skeletal_mesh_ImportMeshLODs
        _dks_ue_options.ue_skeletal_mesh_UseT0AsRefPose=_dks_ue_prefs.ue_skeletal_mesh_UseT0AsRefPose
        _dks_ue_options.ue_skeletal_mesh_PreserveSmoothingGroups=_dks_ue_prefs.ue_skeletal_mesh_PreserveSmoothingGroups
        _dks_ue_options.ue_skeletal_mesh_ImportMorphTargets=_dks_ue_prefs.ue_skeletal_mesh_ImportMorphTargets
        
        _dks_ue_options.ue_animation_AnimationLength=_dks_ue_prefs.ue_animation_AnimationLength
        _dks_ue_options.ue_animation_FrameRangeMin=_dks_ue_prefs.ue_animation_FrameRangeMin
        _dks_ue_options.ue_animation_FrameRangeMax=_dks_ue_prefs.ue_animation_FrameRangeMax
        _dks_ue_options.ue_animation_ImportMeshesInBoneHierarchy=_dks_ue_prefs.ue_animation_ImportMeshesInBoneHierarchy
        _dks_ue_options.ue_animation_UseDefaultSampleRate=_dks_ue_prefs.ue_animation_UseDefaultSampleRate
        _dks_ue_options.ue_animation_CustomSampleRate=_dks_ue_prefs.ue_animation_CustomSampleRate
        _dks_ue_options.ue_animation_ConvertScene=_dks_ue_prefs.ue_animation_ConvertScene

        return {'FINISHED'}

class dks_ue_json_create(bpy.types.Operator):

    bl_idname = "dks_ue.json_create"
    bl_label = 'Create "blender_addon_ue.json"'
    bl_context = "scene"

    def execute(self, context):
        
        _dks_ue_options = context.scene.dks_ue_options

        _json_data = {}

        _json_data["option_ue_src"]=_dks_ue_options.option_ue_src
        _json_data["option_ue_dst"]=_dks_ue_options.option_ue_dst
        _json_data["option_create_icon"]=_dks_ue_options.option_create_icon
        _json_data["option_override_camera"]=_dks_ue_options.option_override_camera
        _json_data["option_icon_resolution_x"]=_dks_ue_options.option_icon_resolution_x
        _json_data["option_icon_resolution_y"]=_dks_ue_options.option_icon_resolution_y
        _json_data["option_camera_location"]={}
        _json_data["option_camera_location"]["x"]=_dks_ue_options.option_camera_location[0]
        _json_data["option_camera_location"]["y"]=_dks_ue_options.option_camera_location[1]
        _json_data["option_camera_location"]["z"]=_dks_ue_options.option_camera_location[2]
        _json_data["option_camera_rotation"]={}
        _json_data["option_camera_rotation"]["x"]=_dks_ue_options.option_camera_rotation[0]
        _json_data["option_camera_rotation"]["y"]=_dks_ue_options.option_camera_rotation[1]
        _json_data["option_camera_rotation"]["z"]=_dks_ue_options.option_camera_rotation[2]
        _json_data["option_copy_textures"]=_dks_ue_options.option_copy_textures

        json_data_filename = bpy.path.abspath(_dks_ue_options.option_ue_json_folder)+"blender_addon_ue.json"

        with open(json_data_filename, 'w') as f:
            json.dump(_json_data, f)

        return {'FINISHED'}

class dks_ue_set_camera_location(bpy.types.Operator):

    bl_idname = "dks_ue.set_camera_location"
    bl_label = 'Set from Camera Location'
    bl_context = "scene"

    def execute(self, context):
        
        _dks_ue_options = context.scene.dks_ue_options
        _dks_ue_options.option_camera_location=bpy.context.scene.camera.location

        return {'FINISHED'}

class dks_ue_set_camera_rotation(bpy.types.Operator):

    bl_idname = "dks_ue.set_camera_rotation"
    bl_label = 'Set from Camera Rotation'
    bl_context = "scene"

    def execute(self, context):
        
        _dks_ue_options = context.scene.dks_ue_options
        _dks_ue_options.option_camera_rotation=bpy.context.scene.camera.rotation_euler

        return {'FINISHED'}

# UE Options Panel Properties

class dks_ue_options(bpy.types.PropertyGroup):

    # Preferences

    def get_option_json_search(self):
        if "_option_json_search" not in self:
            self["_option_json_search"]=bpy.context.preferences.addons[__package__].preferences.option_json_search
        return self["_option_json_search"]
    def set_option_json_search(self, value):
        self["_option_json_search"] = value

    option_json_search : bpy.props.BoolProperty(
            name='Search for "blender_addon_ue.json"',
            get = get_option_json_search,
            set = set_option_json_search                
    )

    def get_option_ue_src(self):
        if ("_option_ue_src" not in self):
            self["_option_ue_src"]=bpy.context.preferences.addons[__package__].preferences.option_ue_src
        return self["_option_ue_src"]
    def set_option_ue_src(self, value):
        self["_option_ue_src"] = value

    option_ue_src : bpy.props.StringProperty(
            name="Source Root Folder",
            subtype="DIR_PATH",
            get = get_option_ue_src,
            set = set_option_ue_src                 
    )     

    def get_option_ue_dst(self):
        if ("_option_ue_dst" not in self):
            self["_option_ue_dst"]=bpy.context.preferences.addons[__package__].preferences.option_ue_dst
        return self["_option_ue_dst"]
    def set_option_ue_dst(self, value):
        self["_option_ue_dst"] = value

    option_ue_dst : bpy.props.StringProperty(
            name="Destination Root Folder",
            subtype="DIR_PATH",
            get = get_option_ue_dst,
            set = set_option_ue_dst                 
    )   

    def get_option_create_icon(self):
        if "_option_create_icon" not in self:
            self["_option_create_icon"]=bpy.context.preferences.addons[__package__].preferences.option_create_icon
        return self["_option_create_icon"]
    def set_option_create_icon(self, value):
        self["_option_create_icon"] = value

    option_create_icon : bpy.props.BoolProperty(
            name="Create Icon",
            get = get_option_create_icon,
            set = set_option_create_icon                 
    )

    def get_option_icon_resolution_x(self):
        if "_option_icon_resolution_x" not in self:
            self["_option_icon_resolution_x"]=bpy.context.preferences.addons[__package__].preferences.option_icon_resolution_x
        return self["_option_icon_resolution_x"]
    def set_option_icon_resolution_x(self, value):
        self["_option_icon_resolution_x"] = value

    option_icon_resolution_x : bpy.props.IntProperty(
            name="Resolution Width",
            get = get_option_icon_resolution_x,
            set = set_option_icon_resolution_x                 
    )        

    def get_option_icon_resolution_y(self):
        if "_option_icon_resolution_y" not in self:
            self["_option_icon_resolution_y"]=bpy.context.preferences.addons[__package__].preferences.option_icon_resolution_y
        return self["_option_icon_resolution_y"]
    def set_option_icon_resolution_y(self, value):
        self["_option_icon_resolution_y"] = value

    option_icon_resolution_y : bpy.props.IntProperty(
            name="Resolution Height",
            get = get_option_icon_resolution_y,
            set = set_option_icon_resolution_y                 
    )        

    def get_option_copy_textures(self):
        if "_option_copy_textures" not in self:
            self["_option_copy_textures"]=bpy.context.preferences.addons[__package__].preferences.option_copy_textures
        return self["_option_copy_textures"]
    def set_option_copy_textures(self, value):
        self["_option_copy_textures"] = value

    option_copy_textures : bpy.props.BoolProperty(
            name="Copy Textures Folder",
            get = get_option_copy_textures,
            set = set_option_copy_textures                 
    )

    def get_option_override_camera(self):
        if "_option_override_camera" not in self:
            self["_option_override_camera"]=bpy.context.preferences.addons[__package__].preferences.option_override_camera
        return self["_option_override_camera"]
    def set_option_override_camera(self, value):
        self["_option_override_camera"] = value

    option_override_camera : bpy.props.BoolProperty(
            name="Override Camera Location/Rotation",
            get = get_option_override_camera,
            set = set_option_override_camera                 
    )

    def get_option_camera_location(self):
        if "_option_camera_location" not in self:
            self["_option_camera_location"]=bpy.context.preferences.addons[__package__].preferences.option_camera_location
        return self["_option_camera_location"]
    def set_option_camera_location(self, value):
        self["_option_camera_location"] = value

    option_camera_location : bpy.props.FloatVectorProperty(
            name="Camera Location",
            get = get_option_camera_location,
            set = set_option_camera_location                 
    )                                            

    def get_option_camera_rotation(self):
        if "_option_camera_rotation" not in self:
            self["_option_camera_rotation"]=bpy.context.preferences.addons[__package__].preferences.option_camera_rotation
        return self["_option_camera_rotation"]
    def set_option_camera_rotation(self, value):
        self["_option_camera_rotation"] = value

    option_camera_rotation : bpy.props.FloatVectorProperty(
            name="Camera Rotation",
            get = get_option_camera_rotation,
            set = set_option_camera_rotation                 
    ) 
    
    option_ue_json_folder : bpy.props.StringProperty(
            name="Select Folder",
            subtype="DIR_PATH",
    )   

    # UE JSON Options >

    def get_option_ue_json(self):
        if "_option_ue_json" not in self:
            self["_option_ue_json"]=bpy.context.preferences.addons[__package__].preferences.option_ue_json
        return self["_option_ue_json"]
    def set_option_ue_json(self, value):
        self["_option_ue_json"] = value

    option_ue_json : bpy.props.BoolProperty(
            name="Create UE JSON",
            get = get_option_ue_json,
            set = set_option_ue_json            
    )

    def get_option_ue_auto(self):
        if "_option_ue_auto" not in self:
            self["_option_ue_auto"]=bpy.context.preferences.addons[__package__].preferences.option_ue_auto
        return self["_option_ue_auto"]
    def set_option_ue_auto(self, value):
        self["_option_ue_auto"] = value

    option_ue_auto : bpy.props.BoolProperty(
            name="Auto UE Import",
            get = get_option_ue_auto,
            set = set_option_ue_auto            
    )

    # General

    def get_ue_ImportMesh(self):
        if "_ue_ImportMesh" not in self:
            self["_ue_ImportMesh"]=bpy.context.preferences.addons[__package__].preferences.ue_ImportMesh
        return self["_ue_ImportMesh"]
    def set_ue_ImportMesh(self, value):
        self["_ue_ImportMesh"] = value

    def get_ue_ImportMaterials(self):
        if "_ue_ImportMaterials" not in self:
            self["_ue_ImportMaterials"]=bpy.context.preferences.addons[__package__].preferences.ue_ImportMaterials
        return self["_ue_ImportMaterials"]
    def set_ue_ImportMaterials(self, value):
        self["_ue_ImportMaterials"] = value

    def get_ue_ImportAnimations(self):
        if "_ue_ImportAnimations" not in self:
            self["_ue_ImportAnimations"]=bpy.context.preferences.addons[__package__].preferences.ue_ImportAnimations
        return self["_ue_ImportAnimations"]
    def set_ue_ImportAnimations(self, value):
        self["_ue_ImportAnimations"] = value

    def get_ue_CreatePhysicsAsset(self):
        if "_ue_CreatePhysicsAsset" not in self:
            self["_ue_CreatePhysicsAsset"]=bpy.context.preferences.addons[__package__].preferences.ue_CreatePhysicsAsset
        return self["_ue_CreatePhysicsAsset"]
    def set_ue_CreatePhysicsAsset(self, value):
        self["_ue_CreatePhysicsAsset"] = value

    def get_ue_AutoComputeLodDistances(self):
        if "_ue_AutoComputeLodDistances" not in self:
            self["_ue_AutoComputeLodDistances"]=bpy.context.preferences.addons[__package__].preferences.ue_AutoComputeLodDistances
        return self["_ue_AutoComputeLodDistances"]
    def set_ue_AutoComputeLodDistances(self, value):
        self["_ue_AutoComputeLodDistances"] = value

    ue_ImportMesh : bpy.props.BoolProperty(
            name="Import Mesh",
            get = get_ue_ImportMesh,
            set = set_ue_ImportMesh            
    )
    ue_ImportMaterials : bpy.props.BoolProperty(
            name="Import Materials",
            get = get_ue_ImportMaterials,
            set = set_ue_ImportMaterials            
    )
    ue_ImportAnimations : bpy.props.BoolProperty(
            name="Import Animations",
            get = get_ue_ImportAnimations,
            set = set_ue_ImportAnimations            
    )
    ue_CreatePhysicsAsset : bpy.props.BoolProperty(
            name="Create Physics Asset",
            get = get_ue_CreatePhysicsAsset,
            set = set_ue_CreatePhysicsAsset            
    )
    ue_AutoComputeLodDistances : bpy.props.BoolProperty(
            name="Auto Compute Lod Distances",
            get = get_ue_AutoComputeLodDistances,
            set = set_ue_AutoComputeLodDistances            
    )
    
    # Static Mesh

    def get_ue_static_mesh_NormalImportMethod(self):
        if "_ue_static_mesh_NormalImportMethod" not in self:
            self["_ue_static_mesh_NormalImportMethod"]=_enums["NormalImportMethod"][bpy.context.preferences.addons[__package__].preferences.ue_static_mesh_NormalImportMethod]
        return self["_ue_static_mesh_NormalImportMethod"]
    def set_ue_static_mesh_NormalImportMethod(self, value):
        self["_ue_static_mesh_NormalImportMethod"] = value

    def get_ue_static_mesh_ImportMeshLODs(self):
        if "_ue_static_mesh_ImportMeshLODs" not in self:
            self["_ue_static_mesh_ImportMeshLODs"]=bpy.context.preferences.addons[__package__].preferences.ue_static_mesh_ImportMeshLODs
        return self["_ue_static_mesh_ImportMeshLODs"]
    def set_ue_static_mesh_ImportMeshLODs(self, value):
        self["_ue_static_mesh_ImportMeshLODs"] = value

    def get_ue_static_mesh_CombineMeshes(self):
        if "_ue_static_mesh_CombineMeshes" not in self:
            self["_ue_static_mesh_CombineMeshes"]=bpy.context.preferences.addons[__package__].preferences.ue_static_mesh_CombineMeshes
        return self["_ue_static_mesh_CombineMeshes"]
    def set_ue_static_mesh_CombineMeshes(self, value):
        self["_ue_static_mesh_CombineMeshes"] = value

    def get_ue_static_mesh_AutoGenerateCollision(self):
        if "_ue_static_mesh_AutoGenerateCollision" not in self:
            self["_ue_static_mesh_AutoGenerateCollision"]=bpy.context.preferences.addons[__package__].preferences.ue_static_mesh_AutoGenerateCollision
        return self["_ue_static_mesh_AutoGenerateCollision"]
    def set_ue_static_mesh_AutoGenerateCollision(self, value):
        self["_ue_static_mesh_AutoGenerateCollision"] = value

    ue_static_mesh_NormalImportMethod : bpy.props.EnumProperty(
            items=[('ComputeNormals', "ComputeNormals", "Compute Normals", 1),('ImportNormalsAndTangents', "ImportNormalsAndTangents", "Import Normals And Tangents", 2),('ImportNormals', "ImportNormals", "Import Normals", 3),],
            name="Normal Import Method",
            get = get_ue_static_mesh_NormalImportMethod,
            set = set_ue_static_mesh_NormalImportMethod
    )
    ue_static_mesh_ImportMeshLODs : bpy.props.BoolProperty(
            name="Import Mesh LODs",
            get = get_ue_static_mesh_ImportMeshLODs,
            set = set_ue_static_mesh_ImportMeshLODs            
    )
    ue_static_mesh_CombineMeshes : bpy.props.BoolProperty(
            name="Combine Meshes",
            get = get_ue_static_mesh_CombineMeshes,
            set = set_ue_static_mesh_CombineMeshes
    )
    ue_static_mesh_AutoGenerateCollision : bpy.props.BoolProperty(
            name="Auto Generate Collision",
            get = get_ue_static_mesh_AutoGenerateCollision,
            set = set_ue_static_mesh_AutoGenerateCollision
    )
    
    # Skeletal Mesh

    def get_ue_skeletal_mesh_NormalImportMethod(self):
        if "_ue_skeletal_mesh_NormalImportMethod" not in self:
            self["_ue_skeletal_mesh_NormalImportMethod"]=_enums["NormalImportMethod"][bpy.context.preferences.addons[__package__].preferences.ue_skeletal_mesh_NormalImportMethod]
        return self["_ue_skeletal_mesh_NormalImportMethod"]
    def set_ue_skeletal_mesh_NormalImportMethod(self, value):
        self["_ue_skeletal_mesh_NormalImportMethod"] = value

    def get_ue_skeletal_mesh_ImportMeshLODs(self):
        if "_ue_skeletal_mesh_ImportMeshLODs" not in self:
            self["_ue_skeletal_mesh_ImportMeshLODs"]=bpy.context.preferences.addons[__package__].preferences.ue_skeletal_mesh_ImportMeshLODs
        return self["_ue_skeletal_mesh_ImportMeshLODs"]
    def set_ue_skeletal_mesh_ImportMeshLODs(self, value):
        self["_ue_skeletal_mesh_ImportMeshLODs"] = value

    def get_ue_skeletal_mesh_UseT0AsRefPose(self):
        if "_ue_skeletal_mesh_UseT0AsRefPose" not in self:
            self["_ue_skeletal_mesh_UseT0AsRefPose"]=bpy.context.preferences.addons[__package__].preferences.ue_skeletal_mesh_UseT0AsRefPose
        return self["_ue_skeletal_mesh_UseT0AsRefPose"]
    def set_ue_skeletal_mesh_UseT0AsRefPose(self, value):
        self["_ue_skeletal_mesh_UseT0AsRefPose"] = value

    def get_ue_skeletal_mesh_PreserveSmoothingGroups(self):
        if "_ue_skeletal_mesh_PreserveSmoothingGroups" not in self:
            self["_ue_skeletal_mesh_PreserveSmoothingGroups"]=bpy.context.preferences.addons[__package__].preferences.ue_skeletal_mesh_PreserveSmoothingGroups
        return self["_ue_skeletal_mesh_PreserveSmoothingGroups"]
    def set_ue_skeletal_mesh_PreserveSmoothingGroups(self, value):
        self["_ue_skeletal_mesh_PreserveSmoothingGroups"] = value

    def get_ue_skeletal_mesh_ImportMorphTargets(self):
        if "_ue_skeletal_mesh_ImportMorphTargets" not in self:
            self["_ue_skeletal_mesh_ImportMorphTargets"]=bpy.context.preferences.addons[__package__].preferences.ue_skeletal_mesh_ImportMorphTargets
        return self["_ue_skeletal_mesh_ImportMorphTargets"]
    def set_ue_skeletal_mesh_ImportMorphTargets(self, value):
        self["_ue_skeletal_mesh_ImportMorphTargets"] = value

    ue_skeletal_mesh_NormalImportMethod : bpy.props.EnumProperty(
            items=[('ComputeNormals', "ComputeNormals", "Compute Normals", 1),('ImportNormalsAndTangents', "ImportNormalsAndTangents", "Import Normals And Tangents", 2),('ImportNormals', "ImportNormals", "Import Normals", 3),],
            name="Normal Import Method",
            get = get_ue_skeletal_mesh_NormalImportMethod,
            set = set_ue_skeletal_mesh_NormalImportMethod
    )
    ue_skeletal_mesh_ImportMeshLODs : bpy.props.BoolProperty(
            name="Import Mesh LODs",
            get = get_ue_skeletal_mesh_ImportMeshLODs,
            set = set_ue_skeletal_mesh_ImportMeshLODs
    )
    ue_skeletal_mesh_UseT0AsRefPose : bpy.props.BoolProperty(
            name="UseT0AsRefPose",
            get = get_ue_skeletal_mesh_UseT0AsRefPose,
            set = set_ue_skeletal_mesh_UseT0AsRefPose
    )
    ue_skeletal_mesh_PreserveSmoothingGroups : bpy.props.BoolProperty(
            name="Preserve Smoothing Groups",
            get = get_ue_skeletal_mesh_PreserveSmoothingGroups,
            set = set_ue_skeletal_mesh_PreserveSmoothingGroups
    )
    ue_skeletal_mesh_ImportMorphTargets : bpy.props.BoolProperty(
            name="Import Morph Targets",
            get = get_ue_skeletal_mesh_ImportMorphTargets,
            set = set_ue_skeletal_mesh_ImportMorphTargets
    )
    
    # Animations

    def get_ue_animation_AnimationLength(self):
        if "_ue_animation_AnimationLength" not in self:
            self["_ue_animation_AnimationLength"]=_enums["AnimationLength"][bpy.context.preferences.addons[__package__].preferences.ue_animation_AnimationLength]
        return self["_ue_animation_AnimationLength"]
    def set_ue_animation_AnimationLength(self, value):
        self["_ue_animation_AnimationLength"] = value

    def get_ue_animation_FrameRangeMin(self):
        if "_ue_animation_FrameRangeMin" not in self:
            self["_ue_animation_FrameRangeMin"]=bpy.context.preferences.addons[__package__].preferences.ue_animation_FrameRangeMin
        return self["_ue_animation_FrameRangeMin"]
    def set_ue_animation_FrameRangeMin(self, value):
        self["_ue_animation_FrameRangeMin"] = value

    def get_ue_animation_FrameRangeMax(self):
        if "_ue_animation_FrameRangeMax" not in self:
            self["_ue_animation_FrameRangeMax"]=bpy.context.preferences.addons[__package__].preferences.ue_animation_FrameRangeMax
        return self["_ue_animation_FrameRangeMax"]
    def set_ue_animation_FrameRangeMax(self, value):
        self["_ue_animation_FrameRangeMax"] = value

    def get_ue_animation_ImportMeshesInBoneHierarchy(self):
        if "_ue_animation_ImportMeshesInBoneHierarchy" not in self:
            self["_ue_animation_ImportMeshesInBoneHierarchy"]=bpy.context.preferences.addons[__package__].preferences.ue_animation_ImportMeshesInBoneHierarchy
        return self["_ue_animation_ImportMeshesInBoneHierarchy"]
    def set_ue_animation_ImportMeshesInBoneHierarchy(self, value):
        self["_ue_animation_ImportMeshesInBoneHierarchy"] = value

    def get_ue_animation_UseDefaultSampleRate(self):
        if "_ue_animation_UseDefaultSampleRate" not in self:
            self["_ue_animation_UseDefaultSampleRate"]=bpy.context.preferences.addons[__package__].preferences.ue_animation_UseDefaultSampleRate
        return self["_ue_animation_UseDefaultSampleRate"]
    def set_ue_animation_UseDefaultSampleRate(self, value):
        self["_ue_animation_UseDefaultSampleRate"] = value

    def get_ue_animation_CustomSampleRate(self):
        if "_ue_animation_CustomSampleRate" not in self:
            self["_ue_animation_CustomSampleRate"]=bpy.context.preferences.addons[__package__].preferences.ue_animation_CustomSampleRate
        return self["_ue_animation_CustomSampleRate"]
    def set_ue_animation_CustomSampleRate(self, value):
        self["_ue_animation_CustomSampleRate"] = value

    def get_ue_animation_ConvertScene(self):
        if "_ue_animation_ConvertScene" not in self:
            self["_ue_animation_ConvertScene"]=bpy.context.preferences.addons[__package__].preferences.ue_animation_ConvertScene
        return self["_ue_animation_ConvertScene"]
    def set_ue_animation_ConvertScene(self, value):
        self["_ue_animation_ConvertScene"] = value

    ue_animation_AnimationLength : bpy.props.EnumProperty(
            items=[('AnimatedKey', "AnimatedKey", "Animated Key", 1),('ExportedTime', "ExportedTime", "Exported Time", 2),('SetRange', "SetRange", "Set Range", 3),],
            name="Animation Length",
            get = get_ue_animation_AnimationLength,
            set = set_ue_animation_AnimationLength
    )
    ue_animation_FrameRangeMin : bpy.props.IntProperty(
            name="Frame Range Min",
            get = get_ue_animation_FrameRangeMin,
            set = set_ue_animation_FrameRangeMin
    )
    ue_animation_FrameRangeMax : bpy.props.IntProperty(
            name="Frame Range Max",
            get = get_ue_animation_FrameRangeMax,
            set = set_ue_animation_FrameRangeMax
    )
    ue_animation_ImportMeshesInBoneHierarchy : bpy.props.BoolProperty(
            name="Import Meshes In Bone Hierarchy",
            get = get_ue_animation_ImportMeshesInBoneHierarchy,
            set = set_ue_animation_ImportMeshesInBoneHierarchy
    )
    ue_animation_UseDefaultSampleRate : bpy.props.BoolProperty(
            name="Use Default Sample Rate",
            get = get_ue_animation_UseDefaultSampleRate,
            set = set_ue_animation_UseDefaultSampleRate
    )
    ue_animation_CustomSampleRate : bpy.props.IntProperty(
            name="Custom Sample Rate",
            get = get_ue_animation_CustomSampleRate,
            set = set_ue_animation_CustomSampleRate
    )
    ue_animation_ConvertScene : bpy.props.BoolProperty(
            name="Convert Scene",
            get = get_ue_animation_ConvertScene,
            set = set_ue_animation_ConvertScene
    )

    # < UE JSON Options

# Material Panel

class PANEL_PT_dks_ue_options(bpy.types.Panel):
    
    bl_idname = "PANEL_PT_dks_ue_options"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_label = "UE Options"
    bl_context = "output"
   
    @classmethod
    def poll(cls, context):
        return (context.scene is not None)

    def draw(self, context):

        _dks_ue_options = context.scene.dks_ue_options

        layout = self.layout

        box_prefs=layout.box()
        box_prefs.label(text='Preferences',icon='SETTINGS') 

        box=box_prefs.box()
        box.operator(dks_ue_set_preferences.bl_idname)
        box.operator(dks_ue_set_json_preferences.bl_idname)

        box=box_prefs.box()
        box.prop(_dks_ue_options,"option_json_search")

        box=box_prefs.box()
        box.prop(_dks_ue_options,"option_ue_src")
        box.prop(_dks_ue_options,"option_ue_dst")

        box=box_prefs.box()
        box.label(text='Icon',icon='RADIOBUT_ON')    
        box.prop(_dks_ue_options,"option_create_icon")
        box.prop(_dks_ue_options,"option_icon_resolution_x")
        box.prop(_dks_ue_options,"option_icon_resolution_y")

        box.prop(_dks_ue_options,"option_override_camera")
        box.prop(_dks_ue_options,"option_camera_location")
        box.operator(dks_ue_set_camera_location.bl_idname)
        box.prop(_dks_ue_options,"option_camera_rotation")
        box.operator(dks_ue_set_camera_rotation.bl_idname)
        
        box=box_prefs.box()
        box.label(text='Textures',icon='RADIOBUT_ON')    
        box.prop(_dks_ue_options,"option_copy_textures")

        box=box_prefs.box()
        box.prop(_dks_ue_options,"option_ue_json_folder")
        box.operator(dks_ue_json_create.bl_idname)

        box_fbx=layout.box()
        box_fbx.label(text='FBX Import Options',icon='SETTINGS') 

        box=box_fbx.box()
        box.operator(dks_ue_set_ue_preferences.bl_idname)

        box=box_fbx.box()
        box.prop(_dks_ue_options,"option_ue_json")
        box.prop(_dks_ue_options,"option_ue_auto")

        box=box_fbx.box()
        box.prop(_dks_ue_options,"ue_ImportMesh")
        box.prop(_dks_ue_options,"ue_ImportMaterials")
        box.prop(_dks_ue_options,"ue_ImportAnimations")
        box.prop(_dks_ue_options,"ue_CreatePhysicsAsset")
        box.prop(_dks_ue_options,"ue_AutoComputeLodDistances")

        box=box_fbx.box()
        box.label(text='Static Mesh',icon='RADIOBUT_ON')    
        box.prop(_dks_ue_options,"ue_static_mesh_NormalImportMethod")
        box.prop(_dks_ue_options,"ue_static_mesh_ImportMeshLODs")
        box.prop(_dks_ue_options,"ue_static_mesh_CombineMeshes")
        box.prop(_dks_ue_options,"ue_static_mesh_AutoGenerateCollision")

        box=box_fbx.box()
        box.label(text='Skeletal Mesh',icon='RADIOBUT_ON')
        box.prop(_dks_ue_options,"ue_skeletal_mesh_NormalImportMethod")
        box.prop(_dks_ue_options,"ue_skeletal_mesh_ImportMeshLODs")
        box.prop(_dks_ue_options,"ue_skeletal_mesh_UseT0AsRefPose")
        box.prop(_dks_ue_options,"ue_skeletal_mesh_PreserveSmoothingGroups")
        box.prop(_dks_ue_options,"ue_skeletal_mesh_ImportMorphTargets")

        box=box_fbx.box()
        box.label(text='Animations',icon='RADIOBUT_ON')
        box.prop(_dks_ue_options,"ue_animation_AnimationLength")
        box.prop(_dks_ue_options,"ue_animation_FrameRangeMin")
        box.prop(_dks_ue_options,"ue_animation_FrameRangeMax")
        box.prop(_dks_ue_options,"ue_animation_ImportMeshesInBoneHierarchy")
        box.prop(_dks_ue_options,"ue_animation_UseDefaultSampleRate")
        box.prop(_dks_ue_options,"ue_animation_CustomSampleRate")
        box.prop(_dks_ue_options,"ue_animation_ConvertScene")
        
        box=layout.box()
        box.operator(dks_ue_export.bl_idname,text="Export to UE")

class dks_ue_export(bpy.types.Operator):

    bl_idname = "dks_ue.export"
    bl_label = "UE"
    bl_description = "Export to UE"

    def execute(self, context):
        
        global _preferences

        _dks_ue_options = context.scene.dks_ue_options

        if bpy.context.preferences.addons[__package__].preferences.option_save_before_export:
            bpy.ops.wm.save_mainfile()

        _file_name = bpy.context.blend_data.filepath
        _file_path = _file_name[0:len(_file_name)-len(bpy.path.basename(_file_name))]
        
        if _dks_ue_options.option_json_search:

            _file_json=dks_ue_folder_crawl(_file_path)
        
        else:
        
            _file_json=""

        if _file_json!="":
                
            try:
                with open(_file_json) as _file_json_data:
                    _preferences = json.load(_file_json_data)
            except Exception as e:
                print("blender_addon_ue.json is invalid: ",str(e.reason))
                return {'FINISHED'}
            
            if "option_ue_src" not in _preferences:
                _preferences["option_ue_src"]=_dks_ue_options.option_ue_src
            
            if "option_ue_dst" not in _preferences:
                _preferences["option_ue_dst"]=_dks_ue_options.option_ue_dst

            if "option_create_icon" not in _preferences:
                _preferences["option_create_icon"]=_dks_ue_options.option_create_icon

            if "option_override_camera" not in _preferences:
                _preferences["option_override_camera"]=_dks_ue_options.option_override_camera

            if "option_icon_resolution_x" not in _preferences:
                _preferences["option_icon_resolution_x"]=_dks_ue_options.option_icon_resolution_x

            if "option_icon_resolution_y" not in _preferences:
                _preferences["option_icon_resolution_y"]=_dks_ue_options.option_icon_resolution_y

            if "option_camera_location" in _preferences:
                _preferences["option_camera_location"]=(_preferences["option_camera_location"]["x"],_preferences["option_camera_location"]["y"],_preferences["option_camera_location"]["z"])
            else:
                _preferences["option_camera_location"] = _dks_ue_options.option_camera_location

            if "option_camera_rotation" in _preferences:
                _preferences["option_camera_rotation"]=(math.radians(_preferences["option_camera_rotation"]["x"]),math.radians(_preferences["option_camera_rotation"]["y"]),math.radians(_preferences["option_camera_rotation"]["z"]))
            else:
                _preferences["option_camera_rotation"] = (math.radians(_dks_ue_options.option_camera_rotation[0]),math.radians(_dks_ue_options.option_camera_rotation[1]),math.radians(_dks_ue_options.option_camera_rotation[2]))

            if "option_create_icon" not in _preferences:
                _preferences["option_create_icon"]=_dks_ue_options.option_create_icon

            if "option_textures_folder" not in _preferences:
                _preferences["option_textures_folder"]=bpy.context.preferences.addons[__package__].preferences.option_textures_folder

            if "option_ue_json" not in _preferences:
                _preferences["option_ue_json"]=_dks_ue_options.option_ue_json

        else:

            _preferences["option_ue_src"]=_dks_ue_options.option_ue_src
            _preferences["option_ue_dst"]=_dks_ue_options.option_ue_dst
            _preferences["option_create_icon"]=_dks_ue_options.option_create_icon
            _preferences["option_override_camera"]=_dks_ue_options.option_override_camera
            _preferences["option_icon_resolution_x"]=_dks_ue_options.option_icon_resolution_x
            _preferences["option_icon_resolution_y"]=_dks_ue_options.option_icon_resolution_y
            _preferences["option_camera_location"]=_dks_ue_options.option_camera_location
            _preferences["option_camera_rotation"]=_dks_ue_options.option_camera_rotation
            _preferences["option_copy_textures"]=_dks_ue_options.option_copy_textures
            _preferences["option_textures_folder"]=bpy.context.preferences.addons[__package__].preferences.option_textures_folder
            _preferences["option_ue_json"]=_dks_ue_options.option_ue_json

        if _preferences["option_create_icon"]:

            screenshot(self, context)

        if _preferences["option_copy_textures"]:

            _path_textures_from = bpy.path.abspath('//') + _preferences["option_textures_folder"] + sep
            _path_textures_to = dks_ue_get_export_path() + _preferences["option_textures_folder"] + sep

            if path.exists(_path_textures_from):
                dir_util.copy_tree(_path_textures_from, _path_textures_to)

        _export_file = dks_ue_fbx_export(self, context)

        if _dks_ue_options.option_ue_json:

            dks_ue_create_bjd(self, context)
        
        return {'FINISHED'}

classes = (
    dks_ue_export,
    dks_ue_options,
    dks_ue_set_preferences,
    dks_ue_set_json_preferences,
    dks_ue_set_ue_preferences,
    dks_ue_json_create,
    dks_ue_set_camera_location,
    dks_ue_set_camera_rotation,
    PANEL_PT_dks_ue_options,
)

def register():

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.dks_ue_options = bpy.props.PointerProperty(type=dks_ue_options)

def unregister():
    
    del bpy.types.Scene.dks_ue_options

    for cls in reversed(classes):
        unregister_class(cls)

