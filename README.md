# Mass Export FBX with Collisions for Blender | Unreal Engine

## Overview
This Blender addon simplifies the process of exporting selected objects and their collision meshes as FBX files for Unreal Engine. It ensures proper handling of collision meshes and organizes assets for easy integration into Unreal Engine workflows.

---

## Features
- **Batch Export**: Export multiple selected objects in one operation.
- **Collision Mesh Support**: Automatically detects and includes collision meshes prefixed with `UCX_`, `UBX_`, `USP_`, etc.
- **Offset Handling**: Maintains the relative offsets of collision meshes when moving objects to the origin for export.
- **Unreal Engine Presets**: Includes export settings optimized for Unreal Engine 5.
- **UI Integration**: Intuitive interface in the Blender Tool Shelf for easy usage.

---

## Installation

1. **Download the Addon**:
   - Clone or download the repository to your computer.
   - Save the `mass_export_fbx_addon.py` file.

2. **Install in Blender**:
   - Open Blender.
   - Navigate to **Edit > Preferences > Add-ons**.
   - Click **Install...** and select the `mass_export_fbx_addon.py` file.
   - Enable the addon by checking the checkbox next to its name.

3. **Save Preferences**:
   - Click **Save Preferences** to retain the addon across Blender sessions.

---

## How to Use

### Accessing the Addon
- Open the **3D View**.
- Locate the **UE5 Asset Kit Exporter** tab in the right-side Tool Shelf (press `N` if it's hidden).

### Steps for Exporting
1. **Prepare Your Scene**:
   - Ensure that collision meshes follow Unreal Engine's naming convention (e.g., `UCX_ObjectName`, `UBX_ObjectName_01`, etc.).
   - Position collision meshes relative to their parent object.

2. **Select Objects**:
   - Select the objects you want to export, along with their collision meshes.

3. **Set Export Path**:
   - In the addon panel, click **Select Folder** to choose the export location.

4. **Choose Export Preset**:
   - Ensure the "Unreal Engine 5" preset is selected in the dropdown menu.

5. **Export**:
   - Click the **Export** button.
   - The addon will process the selected objects and save them as FBX files in the specified folder.

---

## Collision Mesh Support

The addon automatically detects collision meshes based on these prefixes:
- `UCX_`
- `UBX_`
- `USP_`

Collision meshes must:
- Be named with a prefix (`UCX_`) followed by the base object name (e.g., `UCX_Wall_01` for an object named `Wall`).
- Be positioned correctly relative to their parent object.

The addon maintains the spatial relationships of collision meshes when exporting.

---

## Known Limitations
- Collision meshes must follow Unreal Engine's naming conventions.
- Objects and collision meshes must be correctly positioned in the scene before export.

---

## Example Workflow

### Scene Setup
| Object Name        | Description                               |
|--------------------|-------------------------------------------|
| `Wall`             | Main object to be exported.              |
| `UCX_Wall`         | Collision mesh associated with `Wall`.   |
| `UCX_Wall_01`      | Additional collision mesh for `Wall`.    |

### Addon Panel
1. Set the **Export Path**.
2. Select `Wall` and ensure all collision meshes are properly positioned and named e.g single concave collision mesh `UCX_Wall` or  multiple concave collision meshes example name `UCX_Wall_01`.
3. Click **Export** to save the FBX file.

The exported FBX will include the object and its collision meshes.

---

## Contributing
We welcome contributions to improve this addon! If you have ideas, issues, or fixes:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with your changes.

---

## Support
For questions, bug reports, or feature requests:
- **GitHub Issues**: [Submit an issue](https://github.com/Chinyeins/blender_python/issues)

---

## License
This addon is distributed under the **MIT License**. See the `LICENSE` file for details.

Happy exporting! 🎉
