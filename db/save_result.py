from pymongo import MongoClient
import csv
from datetime import datetime
import random

# MongoDB 연결
client = MongoClient("mongodb+srv://ye:1111@cluster0.zcgo2.mongodb.net/?retryWrites=true&w=majority")
db = client["graduation_work"]
results_collection = db["ai_results"]
children_collection = db["children"]

# children 컬렉션에서 무작위로 한 명의 어린이 가져오기
def get_random_child_id():
    children = list(children_collection.find({}, {"_id": 1}))
    if not children:
        return None
    return random.choice(children)["_id"]

# CSV 저장 함수
def save_csv_to_mongo(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            random_child_id = get_random_child_id()
            if not random_child_id:
                print("children 컬렉션에 어린이 정보가 없습니다. .")
                continue

            doc = {
                "child_id": random_child_id,
                "event_type": row["action"],
                "danger": row["danger"],
                "timestamp": datetime.now().isoformat()
            }
            results_collection.insert_one(doc)
