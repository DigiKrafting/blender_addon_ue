# Blender Addon UE

Bridge/Pipeline/Workflow export for Unreal Engine.

\* WIP, I've created this addon to automate the export of meshes, create icons for weapons/items/etc and copy textures.

# Features

- One click FBX Export to UE
- Option to Create Icon (Useful for toolbar items/etc)
- Option to Copy Textures Folder
- Option to override preferences (Useful for per project setup)

# Roadmap

- Create an Unreal Editor Plugin to assign the imported textures (I'm getting over assigning the textures manually).
- Utilise a json file in the root folder for a project based preferences setup instead of current addon preferences.

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

# Override Preferences 

Create a text file named blender_addon_ue.json in your source project folder, mesh folder or both for preferences for different model types, the addon will search recursively back to the root folder of your drive for any "blender_addon_ue.json", so don't create it in "c:\blender_addon_ue.json" or "/blender_addon_ue.json".

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

\* For a project based setup be sure to set at least "option_ue_src" and "option_ue_dst".

# Installation

Download either the tar.gz or zip from [https://github.com/DigiKrafting/blender_addon_ue/releases/latest](https://github.com/DigiKrafting/blender_addon_ue/releases/latest)

Installing an Addon in Blender

- [Edit]->[Preferences]
- Select [Add-ons] Tab
- Click [Install]
- Browse to download location of ZIP.
- Click [Install Add-on from File..]

# Screenshots
## Preferences
![alt](/screenshots/ue_prefs.png)
