import bpy
import sys
import json

# Get the JSON file path from command-line arguments
json_file = sys.argv[-1]

with open(json_file, 'r') as f:
    pose_data = json.load(f)

# ตรวจสอบว่า Armature มีอยู่หรือไม่
armature = bpy.data.objects.get("Armature")
if armature is None:
    print("Armature not found!")
    exit()

bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE')

# อ่านข้อมูลจาก JSON และสร้าง keyframes
for frame_data in pose_data:
    frame_number = frame_data["frame"]
    bpy.context.scene.frame_set(frame_number)

    for bone_name, coords in frame_data["bones"].items():
        bone = armature.pose.bones.get(bone_name)
        if bone is None:
            continue

        x, y, z = coords
        bone.location = (x, y, z)
        bone.keyframe_insert(data_path="location")
