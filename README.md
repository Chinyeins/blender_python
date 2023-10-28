# blender_python
Blender Python scripts

## batch_export multiple assets in blender
How to use the script?

### Remarks:
- Put your 3D cursor to world origin, as the script will move every asset to this locaiton temporarily before export
- Make sure your assets origin point is set correctly on a place that makes sense for you.

1. Open Blender Scripting section.
2. paste script into text editor or load from harddrive
3. execute script to initialize GUI
4. Open Tools section: Press "N" on the keyboard, scroll down to Tools
5. Now select all files you want to export
6. Click the export to location button and choose a file location where to store all exported files
7. thats it.

### What is the script doing?
It will go through all your selected items and exports them by name. This means, you should name all selected assets seperately in blender. Also for convenience the script will move each selcted file quickly to the 3d cursor positon, then export the asset, then moves the mesh back to original locaiton. 

So in summary, this script exports all the selected meshes, moves them to origin before export, so all the assets are exported within world origin location, and then it moves the selected meshes back. This is very helpful, if you like to export single parts of an asset kit for example. Since every asset alone has to be exported in world origin, this script does that for you, aswell as exporting all selected files, so you don´t have to do this maually.
