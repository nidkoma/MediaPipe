import cv2
import mediapipe as mp
import json
from datetime import datetime
import subprocess
import os

# Init MediaPipe
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Init webcam or OBS virtual camera (ลองเปลี่ยน index ตามกล้อง)
cap = cv2.VideoCapture(2)

recording = False
pose_data = []

with mp_holistic.Holistic(static_image_mode=False) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(frame_rgb)

        # วาด landmarks
        annotated_frame = frame.copy()
        mp_drawing.draw_landmarks(annotated_frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        mp_drawing.draw_landmarks(annotated_frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(annotated_frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        cv2.putText(annotated_frame, "Press 'r' to Record, 's' to Stop & Save", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0) if recording else (0, 0, 255), 2)

        cv2.imshow("MediaPipe Holistic", annotated_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            print("Recording started")
            recording = True
            pose_data = []  # ล้างข้อมูลเก่า

        elif key == ord('s'):
            print("Recording stopped. Saving data...")
            recording = False

            # Save JSON
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_file = f"pose_record_{timestamp}.json"
            with open(json_file, "w") as f:
                json.dump(pose_data, f, indent=2)

            print(f"Saved {json_file}")

            # Convert JSON for Blender
            blender_json_file = f"blender_pose_{timestamp}.json"
            blender_data = []
            for frame_num, frame_data in enumerate(pose_data, start=1):
                blender_frame = {
                    "frame": frame_num,
                    "bones": {
                        "spine": frame_data["pose"][0],  # Adjust based on pose landmark index
                        "left_arm": frame_data["left_hand"][0] if frame_data["left_hand"] else [0, 0, 0],
                        "right_arm": frame_data["right_hand"][0] if frame_data["right_hand"] else [0, 0, 0],
                    }
                }
                blender_data.append(blender_frame)

            with open(blender_json_file, "w") as f:
                json.dump(blender_data, f, indent=2)

            print(f"Converted data saved to {blender_json_file}")

            # Call Blender CLI
            blender_path = "/path/to/blender"  # Replace with actual Blender path example: "C:\\Program Files\\Blender Foundation\\Blender 3.5\\blender.exe"
            blend_file = "/path/to/your_scene.blend"  # Replace with your .blend file
            blender_script = "scripts/blender_script.py"  # Replace with Blender import script

            subprocess.run([blender_path, blend_file, "--python", blender_script, "--", blender_json_file])
            print("Blender process completed.")

        elif key == 27:
            break

        # บันทึกเฉพาะตอนกด Record
        if recording and results.pose_landmarks:
            frame_data = {
                "pose": [(lm.x, lm.y, lm.z) for lm in results.pose_landmarks.landmark],
                "left_hand": [(lm.x, lm.y, lm.z) for lm in results.left_hand_landmarks.landmark] if results.left_hand_landmarks else [],
                "right_hand": [(lm.x, lm.y, lm.z) for lm in results.right_hand_landmarks.landmark] if results.right_hand_landmarks else [],
            }
            pose_data.append(frame_data)

cap.release()
cv2.destroyAllWindows()
