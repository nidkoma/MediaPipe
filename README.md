# MediaPipe โปรเจค

## วิธีติดตั้ง

1. ติดตั้ง Python
   - ดาวน์โหลดและติดตั้ง Python เวอร์ชั่นล่าสุดจาก [python.org](https://www.python.org/downloads/)
   - เมื่อติดตั้ง ให้เลือกตัวเลือก "Add Python to PATH"
   - MediaPipe (เวอร์ชันปัจจุบัน) ยังไม่รองรับ Python 3.13 โดยสมบูรณ์
   - แนะนำให้ติดตั้ง Python 3.10 หรือ 3.11 แทน

2. ตรวจสอบว่าติดตั้ง Python สำเร็จแล้ว
   ```
   python --version
   ```

3. 📁 สร้าง Virtual Environment (แนะนำมาก)
   - Windows:
     ```
     py -3.10 -m venv mediapipe-env
     ```
   - macOS/Linux:
     ```
     python3.10 -m venv mediapipe-env 
     ```

4. ▶️ เข้าใช้งาน Virtual Environment
   - Windows:
     ```
     mediapipe-env\Scripts\activate
     ```
     ถ้าใช้สำเร็จ จะเห็น `(mediapipe-env)` นำหน้าบรรทัดคำสั่ง
   - macOS/Linux:
     ```
     source mediapipe-env/bin/activate
     ```

5. 📦 ติดตั้ง MediaPipe และแพ็คเกจที่จำเป็น
   ```
   pip install mediapipe opencv-python
   ```

## วิธีใช้งาน

1. ตรวจสอบให้แน่ใจว่า Virtual Environment ถูกเปิดใช้งานอยู่ (จะเห็น `(mediapipe-env)` นำหน้า command prompt)

2. รันไฟล์ Python ตามต้องการ:

   ### mocap.py - การตรวจจับท่าทางพื้นฐาน
   ```
   python mocap.py
   ```
   - ใช้งานง่าย เพียงแสดงการตรวจจับท่าทางพื้นฐาน
   - กด Esc เพื่อออกจากโปรแกรม
   - หมายเหตุ: ลองเปลี่ยนค่า `cv2.VideoCapture(1)` เป็น 0, 1, 2 เพื่อเลือกกล้อง

   ### mocap_Holistic.py - การตรวจจับท่าทางแบบละเอียดพร้อมบันทึกข้อมูล
   ```
   python mocap_Holistic.py
   ```
   - ตรวจจับท่าทางแบบละเอียด (ร่างกาย, มือซ้าย, มือขวา)
   - กด `r` เพื่อเริ่มบันทึกข้อมูล
   - กด `s` เพื่อหยุดบันทึกและบันทึกข้อมูลเป็นไฟล์ JSON
   - กด Esc เพื่อออกจากโปรแกรม
   - หมายเหตุ: ไฟล์ JSON จะบันทึกในชื่อ `pose_record_[timestamp].json`

3. ปิดใช้งาน Virtual Environment เมื่อใช้งานเสร็จ
   ```
   deactivate
   ```

## ทางเลือกสำหรับระบบหลายกล้อง

| ระบบ | รองรับหลายกล้อง | หมายเหตุ |
|------|-------------------|----------|
| 📷 MediaPipe | ❌ โดยตรงไม่รองรับ | ทำได้แยก instance แล้วรวมเอง |
| 🟦 OpenPose + Multi-view | ✅ | ต้องใช้หลาย GPU |
| 🟢 Azure Kinect SDK + 3D body tracking | ✅ | ใช้เซ็นเซอร์เฉพาะ |
| 🧪 OpenCV + ArUco/AprilTag + กล้องหลายมุม | ✅ | ต้องคาลิเบรตกล้องทั้งหมด |

## การแก้ไขปัญหา

- หากคำสั่ง Python ไม่ทำงาน ให้ตรวจสอบว่า Python ถูกเพิ่มใน PATH แล้ว
- หากพบปัญหาเกี่ยวกับการใช้งาน Virtual Environment อาจต้องเปิด PowerShell ด้วยสิทธิ์ Administrator และรันคำสั่ง:
  ```
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- หากกล้องไม่ทำงาน ให้ตรวจสอบค่า index ของกล้องใน `cv2.VideoCapture()` 