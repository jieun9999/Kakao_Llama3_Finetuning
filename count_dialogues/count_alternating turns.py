import os
import json

# 폴더 경로
folder_path = "/workspace/hdd/2.per_subject_text_daily_conversation_data/0205_split_data/total"

# 결과 카운트 초기화
alternating_count = 0  # user와 assistant가 번갈아 나오는 파일
non_alternating_count = 0  # user 또는 assistant가 연속으로 등장하는 파일

# 폴더 내 파일 순회
for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):  # JSON 파일만 처리
        file_path = os.path.join(folder_path, file_name)
        
        # JSON 파일 읽기
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 메시지 추출
        messages = data.get("messages", [])
        
        # 번갈아 나오는지 확인
        is_alternating = True
        for i in range(1, len(messages)):
            # 이전 메시지와 현재 메시지의 role 비교
            if messages[i]["role"] == messages[i - 1]["role"]:
                is_alternating = False
                break
        
        # 결과 카운트 업데이트
        if is_alternating:
            alternating_count += 1
        else:
            non_alternating_count += 1

# 결과 출력
print(f"1:1 대화 (번갈아 나오는 파일): {alternating_count}개")
print(f"user 또는 assistant가 연속 등장하는 파일: {non_alternating_count}개")
