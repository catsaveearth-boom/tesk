import csv
import os

def analyze_video_and_save_csv(video_path):
        os.makedirs("results", exist_ok=True)
        filename = os.path.splitext(os.path.basename(video_path))[0]
        csv_path = os.path.join("results", f"{filename}.csv")

        with open(csv_path, mode="w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["child_id", "action", "timestamp"])
                writer.writerow([filename, "기본행동", "2025-05-31 15:00:00"])

        return csv_path


