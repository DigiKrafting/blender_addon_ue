# Blender Addon UE

Blender Unreal Engine Exporter. Designed to work the Ureal Engine Editor Plugin https://github.com/DigiKrafting/ue_plugin_blender.

\* For feedback or suggestions please use https://forums.unrealengine.com/community/community-content-tools-and-tutorials/1662419-blender-addon-unreal-editor-plugin-combo.

# Features

- One click FBX Export to UE
- Option to Create Icon (Useful for toolbar items/etc)
- Option to Copy Textures Folder
- Option to override preferences (Useful for a per project setup, see "Overriding Preferences" below)
- Option to create a "{fbx_file_name}.bjd" for the UE Plugin https://github.com/DigiKrafting/ue_plugin_blender
- Preferences Panel for per blend file UE options in [Properies]->[Output]->[UE Options] (See "Output Preferences Panel" screenshot below).

# Roadmap

- Recreate Blender Materials Nodes in Unreal Materials

# Required Blender Version

2.80.0

\* Will likely work in previous versions but untested.

# Required Unreal Version

Should work in any version that supports FBX import.

# IMPORTANT USAGE NOTES 

\* Make sure you have a saved .blend file before using, then saving before export is then not required. The addon needs the file location to know where to create the export folder in your Unreal project "Content" folder.

- File Naming Convention

    File names are derived from your blender file name.

## Be sure to set the __"Folders"__ in Preferences (See screenshot below)

- Source Root Folder (E.g "C:\Users\kye\Documents\Assets\DigiKrafting\Content\")
- Destination Root Folder (E.g. "C:\Users\kye\Documents\Unreal Projects\DigiKrafting\Content\")

\* The children/sub folders will be created automatically based on the blender file location in your folder hierarchy. (E.g. "C:\Users\kye\Documents\Assets\DigiKrafting\Content\Meshes\Logo\Logo.blend" will create "C:\Users\kye\Documents\Unreal Projects\DigiKrafting\Content\Meshes\Logo\Logo.fbx")

\* [Properties]->[Output]->[UE Options] Preferences overide the "Addon Preferences".

# Unreal Engine Editor Import Dialog

Untick the option "Auto UE Import" for the default FBX Import Dialog window to show.

# Overriding Preferences 

\* This negates the need for a tool panel with config options if your working on several projects and preserves my beloved "one click" preference for my addons.

- Set desired options in [Properties]->[Output]->[UE Options], select a folder and click [Create "blender_addon_ue.json"]. (See "Output Preferences Panel" screenshot below)

OR

- Create a text file named blender_addon_ue.json in your source project folder, mesh folder or both for preferences for different model types, the addon will search recursively in reverse through the folder hierarchy back to the root folder of your drive for any "blender_addon_ue.json", so don't create it in "c:\blender_addon_ue.json" or "/blender_addon_ue.json".

### blender_addon_ue.json

~~~
{
    "option_ue_src": "C:\\Users\\kye\\Documents\\Assets\\DigiKrafting\\Content\\",
    "option_ue_dst": "C:\\Users\\kye\\Documents\\Unreal Projects\\DKS_Importer_Project\\Content\\",
    "option_create_icon": true,
    "option_override_camera": true,
    "option_icon_resolution_x":64,
    "option_icon_resolution_y":64,
    "option_camera_location":{"x":11,"y":12,"z":13},
    "option_camera_rotation":{"x":21,"y":22,"z":23},
    "option_copy_textures": true
}
~~~

\* Preferences that are ommitted will default to the addon preferences. 

For example you could have:

~~~
{
    "option_ue_src": "C:\\Users\\kye\\Documents\\Assets\\DigiKrafting\\Content\\",
    "option_ue_dst": "C:\\Users\\kye\\Documents\\Unreal Projects\\DKS_Importer_Project\\Content\\",    
    "option_copy_textures": false
}
~~~

\* For a per project based setup be sure to set at least "option_ue_src" and "option_ue_dst" or the folders will be set from the preferences.

# Installation

Download either the tar.gz or zip from [https://github.com/DigiKrafting/blender_addon_ue/releases/latest](https://github.com/DigiKrafting/blender_addon_ue/releases/latest)

Installing an Addon in Blender

- [Edit]->[Preferences]
- Select [Add-ons] Tab
- Click [Install]
- Browse to download location of ZIP.
- Click [Install Add-on from File..]

# Screenshots
## Blender
![alt](/screenshots/ue_blender.png)
## Unreal Editor
![alt](/screenshots/ue_material_setup.png)
## Preferences
![alt](/screenshots/ue_prefs.png)
## Preferences (UE)
![alt](/screenshots/ue_prefs_ue.png)
## Output Preferences Panel
![alt](/screenshots/ue_blender_output_prefs.png)
![alt](/screenshots/ue_blender_output_fbx.png)
