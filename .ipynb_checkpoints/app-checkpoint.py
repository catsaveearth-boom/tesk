# ✅ 셀 1: 필요한 라이브러리 임포트 및 Flask 앱 생성
from flask import Flask, request, jsonify
from datetime import datetime
from pymongo import MongoClient
import csv
from pathlib import Path
import nest_asyncio

nest_asyncio.apply()
app = Flask(__name__)

# ✅ MongoDB 연결
client = MongoClient("mongodb+srv://ye:1111@<cluster>.mongodb.net/?retryWrites=true&w=majority")
db = client["graduation_work"]
collection = db["ai_results"]

# ✅ 셀 2: 결과 저장 함수 (MongoDB + CSV)
def save_to_db(child_id, action):
    doc = {
        "child_id": child_id,
        "action": action,
        "timestamp": datetime.now()
    }
    collection.insert_one(doc)

def save_to_csv(child_id, action):
    path = Path("results.csv")
    is_new = not path.exists()

    with open(path, mode="a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["child_id", "action", "timestamp"])
        writer.writerow([child_id, action, datetime.now()])


# ✅ 셀 3: 더미 추론 함수
def run_inference(sequence):
    """
    시퀀스를 받아서 행동 예측 (임시 더미 로직)
    향후 모델로 교체 가능
    """
    if len(sequence) > 0:
        return "책 읽기"
    else:
        return "걷기"

# ✅ 셀 4: /predict 라우트
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        sequence = data.get("sequence")
        child_id = data.get("child_id", "unknown")

        if not sequence:
            return jsonify({"error": "sequence가 없습니다."}), 400

        action = run_inference(sequence)
        save_to_db(child_id, action)
        save_to_csv(child_id, action)

        return jsonify({"child_id": child_id, "action": action})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
# ✅ 셀 5: 서버 실행 (Jupyter용)
import threading

def run_flask():
    app.run(host='0.0.0.0', port=5000)

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()
