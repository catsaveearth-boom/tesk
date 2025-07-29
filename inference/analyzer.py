import os
import csv
from ultralytics import YOLO
import cv2

# 모델 로드
object_detector = YOLO("inference/yolov8n.pt")       # 사람 감지
action_classifier = YOLO("inference/best.pt")        # 행동 분류

# 클래스 이름 불러오기
CLASS_NAMES = action_classifier.names

#  허용된 행동만 필터링
def is_valid_action(action):
    return action in ["fighting", "eating", "running", "sitting", "sleeping"]

def analyze_video_and_save_csv(video_path):
    os.makedirs("results", exist_ok=True)
    filename = os.path.splitext(os.path.basename(video_path))[0]
    csv_path = os.path.join("results", f"{filename}.csv")

    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    with open(csv_path, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["child_id", "action", "danger"])

        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = object_detector(frame, verbose=False)
            boxes = results[0].boxes

            if boxes is not None:
                for box in boxes:
                    cls_id = int(box.cls[0].item())
                    if cls_id == 0:  # 사람 클래스
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        person_crop = frame[y1:y2, x1:x2]

                        #  행동 분류
                        action_result = action_classifier(person_crop, verbose=False)
                        top_action = action_result[0].probs.top1
                        action_name = CLASS_NAMES[top_action] if top_action < len(CLASS_NAMES) else "unknown"

                        #  필터링: 허용된 행동만 기록
                        if is_valid_action(action_name):
                            danger_label = "위험" if action_name == "fighting" else "비위험"
                            writer.writerow(["", action_name, danger_label])

            frame_idx += 1
            if frame_idx >= frame_count:
                break

    cap.release()
    return csv_path
