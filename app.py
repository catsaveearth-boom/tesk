from flask import Flask, request, jsonify
import os

# 분석 및 DB 저장 관련 함수 불러오기
from inference.analyzer import analyze_video_and_save_csv
from db.save_result import save_csv_to_mongo

# Flask 서버 인스턴스 생성
app = Flask(__name__)

# 업로드된 파일을 저장할 경로
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 서버 상태 확인용 라우트
@app.route('/')
def home():
    return "AI 서버가 동작 중입니다!"

# 영상 업로드를 처리하는 API 엔드포인트
@app.route('/upload', methods=['POST'])
def upload_video():
    try:
        # 라즈베리 파이로 전송된 파일 객체 추출
        file = request.files['video']
        filename = file.filename
        save_path = os.path.join(UPLOAD_FOLDER, filename)

        # 파일 저장
        file.save(save_path)

        # ✅ 분석 실행 → 결과 CSV 생성
        csv_path = analyze_video_and_save_csv(save_path)

        # ✅ 결과 MongoDB 저장 (행동, 위험 여부 포함)
        save_csv_to_mongo(csv_path)

        # ✅ 응답 반환
        return jsonify({
            "status": "success",
            "msg": f"{filename} 처리 및 저장 완료",
            "csv_path": csv_path
        })

    except Exception as e:
        # 오류 처리
        return jsonify({"status": "error", "msg": str(e)}), 500

# EC2에서 실행되도록 설정
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
