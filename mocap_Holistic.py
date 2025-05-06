import cv2
import mediapipe as mp
import json
from datetime import datetime

# Init MediaPipe
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Init webcam or OBS virtual camera (ลองเปลี่ยน index ตามกล้อง)
cap = cv2.VideoCapture(1)

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
            with open(f"pose_record_{timestamp}.json", "w") as f:
                json.dump(pose_data, f, indent=2)

            print("Saved pose_record_{}.json".format(timestamp))

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
