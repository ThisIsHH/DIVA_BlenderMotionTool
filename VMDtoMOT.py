import xml.etree.ElementTree as ET
import bpy
import json
import os
import math

# InputName
file_name = "Set your motion name here"
armature_name = "DIVA"

# We get the current path of where the .blend file is and change the directory to it
blend_file_path = bpy.data.filepath
dir_path = os.path.dirname(blend_file_path)

# Blender Scene
frame_start = bpy.context.scene.frame_start
frame_end = bpy.context.scene.frame_end + 1

class keys:
    def __init__(self, frame, value):
        self.frame = frame
        self.value = value

# XML file (Idk why I did this in xml)
xml_file = os.path.join(dir_path, "bone_t_data.xml")

tree = ET.parse(xml_file)
root = tree.getroot()

# Extract bone data from XML file
bones_data = []
for bone_elem in root.findall("Bone"):
    bone_data = {
        "Name": bone_elem.find("Name").text,
        "Type": bone_elem.find("Type").text,
        "IK": bone_elem.find("IK").text
    }
    bones_data.append(bone_data)

# Calculate bone transformations per frame
bone_transformations = {}
for frame in range(frame_start, frame_end):
    bpy.context.scene.frame_set(frame)
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            for pbone in obj.pose.bones:
                bone_key = (obj.name, pbone.name)
                if bone_key not in bone_transformations:
                    bone_transformations[bone_key] = []
                parent_bone = pbone.parent
                if parent_bone is not None: #
                    bone_transform = parent_bone.matrix.inverted() @ pbone.matrix
                else:
                    bone_transform = pbone.matrix.copy()
                bone_transformations[bone_key].append((frame, bone_transform))

# Extract bone position
def get_bone_position(armature_name, bone_name):
    res_x = []
    res_y = []
    res_z = []

    for frame, bone_matrix in bone_transformations[(armature_name, bone_name)]:
        value = bone_matrix.to_translation()
        res_x.append(keys(frame, value[0]))
        res_y.append(keys(frame, value[1]))
        res_z.append(keys(frame, value[2]))

    return res_x, res_y, res_z

# Fix issue with -π and π angles
def fix_bone_rotation(res):
    half_pi = math.pi / 2.0
    two_pi = math.pi * 2.0

    curr_rot = 0
    rot_fix = 0.0
    rot_prev = res[0].value
    for i in range(1, len(res)):
        rot = res[i].value
        if rot < -half_pi and rot_prev > half_pi and abs(rot - rot_prev) > half_pi:
            curr_rot += 1
            rot_fix = two_pi * float(curr_rot)
        elif rot > half_pi and rot_prev < -half_pi and abs(rot - rot_prev) > half_pi:
            curr_rot -= 1
            rot_fix = two_pi * float(curr_rot)

        if curr_rot != 0:
            res[i].value = rot + rot_fix;
        rot_prev = rot;
        
    return res

# Extract bone rotation
def get_bone_rotation(armature_name, bone_name,):
    res_x = []
    res_y = []
    res_z = []

    for frame, bone_matrix in bone_transformations[(armature_name, bone_name)]:
        value = bone_matrix.to_euler()
        res_x.append(keys(frame, value[0]))
        res_y.append(keys(frame, value[1]))
        res_z.append(keys(frame, value[2]))

    res_x = fix_bone_rotation(res_x)
    res_y = fix_bone_rotation(res_y)
    res_z = fix_bone_rotation(res_z)

    return res_x, res_y, res_z

# JSON structure
def structure(obj_v):
    values = [i.value for i in obj_v]
    tolerance = 0.01 # Default 0.01

    values_equal = all(abs(value - values[0]) < tolerance for value in values)
    values_zero = all(abs(value) < tolerance for value in values)
    if values_zero:
        return None
    elif values_equal:
        return [1, [values[0]]]
    else:
        return [2, [[i.frame, i.value] for i in obj_v]]

# 
bones_to_calculate = [
                        # Global
                        "gblctr", 
                        "kg_ya_ex",
                       
                        # Static 
                        "n_hara",
                        "n_waki_l",
                        "n_waki_r",
                        "n_kao",
                        "n_mune_b", 
                        "face_root", 
                        
                        # IK
                        "n_hara_cp",
                        "cl_mune",
                        "cl_kao",
                        "cl_momo_l", 
                        "cl_momo_r",
                        "c_kata_l", 
                        "c_kata_r",
                        
                        # Others
                        "tl_up_kata_l", 
                        "tl_up_kata_r",
                        "kl_asi_l_wj_co", 
                        "kl_asi_r_wj_co",
                        "kl_eye_l",
                        "kl_eye_r",
                        "kl_mune_b_wj",
                        "kl_kubi",
                        "kl_waki_l_wj",
                        "kl_waki_r_wj",
                        "kl_te_l_wj",
                        "kl_te_r_wj",
                        
                        # Ex
                        "n_kubi_wj_ex",
                        "n_ste_l_wj_ex",
                        "n_sude_l_wj_ex",
                        "n_hiji_l_wj_ex",
                        "n_hiza_l_wj_ex",
                        "n_ste_r_wj_ex",
                        "n_sude_r_wj_ex",
                        "n_hiji_r_wj_ex",
                        "n_hiza_r_wj_ex",
                        "n_hara_cd_ex",
                        "n_hara_b_wj_ex",
                        "n_hara_c_wj_ex",
                        
                        # Fingers
                        "nl_oya_l_wj",
                        "nl_oya_b_l_wj",
                        "nl_oya_c_l_wj",
                        "nl_hito_l_wj",
                        "nl_hito_b_l_wj",
                        "nl_hito_c_l_wj",
                        "nl_naka_l_wj",
                        "nl_naka_b_l_wj",
                        "nl_naka_c_l_wj",
                        "nl_kusu_l_wj",
                        "nl_kusu_b_l_wj",
                        "nl_kusu_c_l_wj",
                        "nl_ko_l_wj",
                        "nl_ko_b_l_wj",
                        "nl_ko_c_l_wj",
                        "nl_oya_r_wj",
                        "nl_oya_b_r_wj",
                        "nl_oya_c_r_wj",
                        "nl_hito_r_wj",
                        "nl_hito_b_r_wj",
                        "nl_hito_c_r_wj",
                        "nl_naka_r_wj",
                        "nl_naka_b_r_wj",
                        "nl_naka_c_r_wj",
                        "nl_kusu_r_wj",
                        "nl_kusu_b_r_wj",
                        "nl_kusu_c_r_wj",
                        "nl_ko_r_wj",
                        "nl_ko_b_r_wj",
                        "nl_ko_c_r_wj"
                     ]

# Cooking time
export_data = []

for bone in bones_data:
    bone_name = bone["Name"]
    bone_type = bone["Type"]

    if bone_name in bones_to_calculate:
        if bone_type == "Position":
            pos_x, pos_y, pos_z = get_bone_position(armature_name, bone_name);
            bone_position = {
                "X": structure(pos_x),
                "Y": structure(pos_y),
                "Z": structure(pos_z)
            }
            export_data.extend([bone_position[axis] for axis in ["X", "Y", "Z"]])
        elif bone_type == "Rotation":
            rot_x, rot_y, rot_z = get_bone_rotation(armature_name, bone_name);
            bone_rotation = {
                "X": structure(rot_x),
                "Y": structure(rot_y),
                "Z": structure(rot_z)
            }
            export_data.extend([bone_rotation[axis] for axis in ["X", "Y", "Z"]])
        elif bone_type == "Type3":
            pos_x, pos_y, pos_z = get_bone_position(armature_name, bone_name);
            rot_x, rot_y, rot_z = get_bone_rotation(armature_name, bone_name);
            bone_position = {
                "X": structure(pos_x),
                "Y": structure(pos_y),
                "Z": structure(pos_z)
            }
            bone_rotation = {
                "X": structure(rot_x),
                "Y": structure(rot_y),
                "Z": structure(rot_z)
            }
            export_data.extend([bone_position[axis] for axis in ["X", "Y", "Z"]] + [bone_rotation[axis] for axis in ["X", "Y", "Z"]])
        elif bone_type in ["Type4", "Type5", "Type6"]:
            ik_bone_name = bone["IK"]
            pos_x, pos_y, pos_z = get_bone_position(armature_name, ik_bone_name);
            rot_x, rot_y, rot_z = get_bone_rotation(armature_name, bone_name);
            ik_bone_position = {
                "X": structure(pos_x),
                "Y": structure(pos_y),
                "Z": structure(pos_z)
            }
            bone_rotation = {
                "X": structure(rot_x),
                "Y": structure(rot_y),
                "Z": structure(rot_z)
            }
            export_data.extend([ik_bone_position[axis] for axis in ["X", "Y", "Z"]] + [bone_rotation[axis] for axis in ["X", "Y", "Z"]])
        elif bone_type == "GlobalPosition":
            pos_x, pos_y, pos_z = get_bone_position(armature_name, bone_name);
            bone_position = {
                "X": structure(pos_x),
                "Y": structure(pos_y),
                "Z": structure(pos_z)
            }
            export_data.extend([bone_position[axis] for axis in ["X", "Y", "Z"]])
        elif bone_type == "GlobalRotation":
            rot_x, rot_y, rot_z = get_bone_rotation(armature_name, bone_name);
            bone_rotation = {
                "X": structure(rot_x),
                "Y": structure(rot_y),
                "Z": structure(rot_z)
            }
            export_data.extend([bone_rotation[axis] for axis in ["X", "Y", "Z"]] + [None]) # There is an extra set
    else:
        if bone_type == "Position":
            export_data.extend([None, None, None])
        elif bone_type == "Rotation":
            export_data.extend([None, None, None])
        elif bone_type in ["Type3", "Type4", "Type5", "Type6"]:
            export_data.extend([None, None, None, None, None, None])
        elif bone_type == "GlobalPosition":
            export_data.extend([None, None, None])
        elif bone_type == "GlobalRotation":
            export_data.extend([None, None, None, None])

# Default structure of DIVA motions
export = json.dumps(
{
  "MOT": [
    {
      "FrameCount": frame_end,
      "HighBits": 1,
      "KeySets": export_data,
      "BoneInfo": [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        22,
        24,
        173,
        174,
        175,
        176,
        177,
        178,
        179,
        180,
        181,
        182,
        183,
        184,
        185,
        186,
        187,
        188,
        189,
        190,
        40,
        41,
        42,
        43,
        44,
        45,
        251,
        252,
        253,
        254,
        46,
        47,
        247,
        248,
        249,
        250,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        191,
        192,
        193,
        194,
        195,
        196,
        197,
        198,
        199,
        200,
        201,
        202,
        203,
        204,
        205,
        206,
        207,
        208,
        209,
        210,
        211,
        212,
        213,
        214,
        215,
        216,
        217,
        218,
        64,
        65,
        219,
        220,
        221,
        222,
        66,
        67,
        223,
        224,
        225,
        226,
        227,
        228,
        68,
        69,
        70,
        71,
        72,
        73,
        229,
        74,
        75,
        76,
        230,
        77,
        78,
        79,
        231,
        80,
        81,
        82,
        232,
        83,
        84,
        85,
        233,
        86,
        87,
        88,
        89,
        90,
        91,
        92,
        234,
        93,
        94,
        95,
        96,
        97,
        98,
        99,
        100,
        235,
        101,
        102,
        103,
        236,
        104,
        105,
        106,
        237,
        107,
        108,
        109,
        238,
        110,
        111,
        112,
        239,
        113,
        114,
        115,
        116,
        117,
        118,
        119,
        240,
        120,
        121,
        122,
        123,
        124,
        125,
        126,
        127,
        128,
        129,
        130,
        131,
        132,
        133,
        134,
        135,
        136,
        137,
        241,
        139,
        140,
        242,
        142,
        143,
        144,
        145,
        146,
        147,
        148
      ]
    }
  ]
},
indent=2)

# Export
with open(os.path.join(dir_path, f"{file_name}.json"), 'w') as f:
    f.write(export)