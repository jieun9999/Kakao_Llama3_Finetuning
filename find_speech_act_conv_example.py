import os
import random
import json

# 폴더 경로
folder_path = "/workspace/hdd/2.per_subject_text_daily_conversation_data/0205_split_data/total"

# 결과 카운트 초기화
alternating_count = 0  # user와 assistant가 번갈아 나오는 파일
non_alternating_count = 0  # user 또는 assistant가 연속으로 등장하는 파일

# 폴더 내 파일 순회
found = 0
dialogues = []

file_names = os.listdir(folder_path)    # 파일 목록 가져오기
# 파일 목록을 랜덤으로 섞기
random.shuffle(file_names)

for file_name in file_names:
    if file_name.endswith(".json"):  # JSON 파일만 처리
        file_path = os.path.join(folder_path, file_name)
        
        # JSON 파일 읽기
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 메시지 추출
        messages = data.get("messages", [])
        
        # 번갈아 나오는지 확인
        for i in range(2, len(messages)):
            # 이전 메시지와 현재 메시지의 role 비교
            if messages[i]["speechAct"] == "농담하기":
                #한 사람이 여러 번 말하는 경우 제외
                if messages[i]["role"] == messages[i-1]["role"] : 
                    continue
                found += 1
                dialogue = {"A": messages[i-1]["content"], "B": messages[i]["content"]}
                dialogues.append(dialogue)
                break

        if found==15 :
            break

# 결과 출력
print(f"대화\n{dialogues}")
