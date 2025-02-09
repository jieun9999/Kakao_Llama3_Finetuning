import os
import json

# 폴더 경로
folder_path = "/workspace/hdd/2.per_subject_text_daily_conversation_data/0205_split_data/total"

# 결과 카운트 초기화
found = 0
targetStr = ";"
speechActs = {}
file_names_with_target = []  # ;이 포함된 파일명을 저장할 리스트

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
        for i in range(1, len(messages)):
            if messages[i]["role"] != "system" and targetStr in messages[i]["content"]:
                if messages[i]["speechAct"] == "일상적으로 반응하기" and messages[i]["content"] == "47 -;":
                    # print(messages[i]["content"])
                    print(file_name)
                if speechActs.get(messages[i]["speechAct"]) is None:
                    speechActs[messages[i]["speechAct"]] = 1
                else:
                    speechActs[messages[i]["speechAct"]] += 1
                found += 1
                if file_name not in file_names_with_target:  # 중복 방지
                    file_names_with_target.append(file_name)

# 결과 출력
print(f"{targetStr} 포함 문장 개수 : {found}")
print(speechActs)

# 파일명 리스트를 txt 파일로 저장
output_file_path = "files_with_semicolon.txt"
with open(output_file_path, "w", encoding="utf-8") as f:
    for file_name in file_names_with_target:
        f.write(file_name + "\n")

print(f"파일명이 저장되었습니다: {output_file_path}")
