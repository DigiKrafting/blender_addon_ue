# Blender Addon UE

Bridge/Pipeline/Workflow export for Unreal Engine.

\* WIP, I've created this addon to automate the export of meshes, create icons for weapons/items/etc and copy textures.
\* I am planning to create an Unreal Editor Plugin to assign the imported textures (I'm getting over assigning the textures manually).

# Features

- One click FBX Export to UE
- Option to Create Icon
- Option to Copy Textures Folder

# Required Blender Version

2.80.0

\* Will likely work in previous versions but untested.

# IMPORTANT USAGE NOTES 

\* Make sure you have a saved .blend file before using, then saving before export is then not required. The addon needs the file location to know where to create the export folder in your Unreal project "Content" folder.

- File Naming Convention

    File names are derived from your blender file name.

## \* Be sure to Set the __"Folders"__ in Preferences (See screenshot below)

- Source Root Folder (E.g "C:\Users\kye\Documents\Assets\DigiKrafting\Content\")
- Destination Root Folder (E.g. "C:\Users\kye\Documents\Unreal Projects\DigiKrafting\Content\")

\* The children/sub folders will be created automatically based on the blender file in your folder hierarchy. (E.g. "C:\Users\kye\Documents\Assets\DigiKrafting\Content\Meshes\Logo\Logo.blend" will create "C:\Users\kye\Documents\Unreal Projects\DigiKrafting\Content\Meshes\Logo\Logo.fbx")

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
