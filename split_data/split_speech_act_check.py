import os
import json
from collections import defaultdict

# 유동적으로 변경할 폴더명
folder_name = "0124_split_data"  

# 경로 설정
train_dir = '/hdd/dataset/talkDataSet1/2.per_subject_text_daily_conversation_data/1.data/{folder_name}/1.train'
val_dir = '/hdd/dataset/talkDataSet1/2.per_subject_text_daily_conversation_data/1.data/{folder_name}/2.validation'
test_dir = '/hdd/dataset/talkDataSet1/2.per_subject_text_daily_conversation_data/1.data/{folder_name}/3.test'

# Speech Act 리스트 (기존 그대로)
speech_acts = ["농담하기", "위협하기", "거절하기", "사과하기", "인사하기", "감사하기", "N/A", "반박하기", 
               "부정감정 표현하기", "긍정감정 표현하기", "일상적으로 반응하기", "요구하기", "개인적으로 약속하기", 
               "충고/제안하기", "질문하기", "정보 제공하기", "주장하기"]

# Speech Act 개수를 저장할 딕셔너리
speech_act_counts = {
    "train": defaultdict(int),
    "validation": defaultdict(int),
    "test": defaultdict(int)
}

# 폴더별 Speech Act 개수 계산 함수
def count_speech_acts(folder, category):
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if not filepath.endswith(".json"):
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                for message in data.get("messages", []):
                    # system 역할 제외
                    if message.get("role") == "system":
                        continue
                    
                    speech_act = message.get("speechAct")
                    if speech_act in speech_acts:
                        speech_act_counts[category][speech_act] += 1
            except json.JSONDecodeError:
                print(f"Invalid JSON file skipped: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# 각 폴더에서 Speech Act 개수 계산
count_speech_acts(train_dir, "train")
count_speech_acts(val_dir, "validation")
count_speech_acts(test_dir, "test")

# 결과 출력
print("==== Speech Act Counts ====")
for category, counts in speech_act_counts.items():
    print(f"\nCategory: {category}")
    for speech_act in speech_acts:
        print(f"{speech_act:20}: {counts[speech_act]}")