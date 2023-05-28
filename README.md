# DIVA_BlenderMotionTool
A .blend/.py that allow you to export a JSON Project Diva motion data.
A work with [FlyingSpirits](https://github.com/FlyingSpirits)

# How the script works
The script takes all the values in the scene from specific bones listed frame by frame. (this could be a problem if we talk about the file size and optimization).

# What do you need 
You need MMD Tools for importing VMD motions
https://github.com/powroupi/blender_mmd_tools

# How to use
Open the .blend file, select 'MMD' Armature object and import the vmd file

## JSON Export/Convertion
When you're ready to export, follow these steps:

1- Go to the 'Scripting' tab, in *file_name = "Set your motion name here"* (line 7), change the name you want. For example:
*file_name = "mot_PV701"* (Do not write the file extension)
Run the script. It should take time (no more than 2 minutes in a full 60fps 3 min. music) 
Your export is going to be in the same directory where the .blend file is located.

2- Use Korekonder's PD Tool for convertion:
Run PD Tool and select 'AC/DT/F/AFT Converting Tools' -> MOT -> Select your JSON export.
Depending of the frames in your motion is going to take a while to convert to a .bin file

# Important notes
- This script/rig is still in development for better result and optimization. Is not a final product
- Your MMD motion is supposed to be in 60fps for standard frame rate

# Credits
- [korenkonder](https://github.com/korenkonder) for JSON layout and PD Tool.
https://github.com/korenkonder/PD_Tool
- [FlyingSpirits](https://github.com/FlyingSpirits) for the impressive work on MMD-DIVA rig.
