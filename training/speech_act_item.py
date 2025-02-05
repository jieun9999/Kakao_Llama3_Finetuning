import os
import json

######################################################################
## labellingData(원본데이터) "1.KAKAO1", "2.KAKAO2", "3.KAKAO3", "4.KAKAO4"를 돌면서 발화Item 수집
######################################################################

# labellingData 폴더 경로 설정
base_folder_path = "/hdd/dataset/talkDataSet1/2.per_subject_text_daily_conversation_data/1.data/1.Training/labellingData/preprocessed"

# JSON 파일들에서 speechAct가 "(선언/위임하기)"인 lines의 전체 원소를 모아 저장
def collect_lines_with_speech_act(base_folder_path, target_speech_act, target_folders, output_file):
    collected_lines = []  # 조건에 맞는 lines의 원소를 저장할 배열

    for folder_name in target_folders:
        folder_path = os.path.join(base_folder_path, folder_name)  # 각 KAKAO 폴더 경로 설정
        if os.path.isdir(folder_path):  # 폴더인지 확인
            for filename in os.listdir(folder_path):
                if filename.endswith(".json"):  # JSON 파일만 처리
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        try:
                            data = json.load(file)
                            for message in data["messages"]:
                                if (message["role"] != "system"):
                                    speech_act = message.get("speechAct", "").strip()
                                    if speech_act == target_speech_act:  # 조건에 맞는지 확인
                                        # 현재 폴더명과 JSON 파일명을 추가
                                        message["file_name"] = folder_name + "/" + filename
                                        collected_lines.append(message)  # 조건에 맞는 line 추가
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON in file: {folder_name}/{filename}")
    
    # 발화 전략 1개 당의 line들만 보려고 기존 파일의 내용용 삭제
    if os.path.exists(output_file):
        os.remove(output_file)  

    # 결과를 JSON 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as output:
        json.dump(collected_lines, output, ensure_ascii=False, indent=4)  # JSON 파일로 저장 (한글 포함)

    print(f"Collected {len(collected_lines)} lines with speechAct '{target_speech_act}' saved to {output_file}")

# 실행
target_speech_act = ""
target_folders = ["1.KAKAO1", "2.KAKAO2", "3.KAKAO3", "4.KAKAO4"]  # 순차적으로 탐색할 폴더 목록
output_file = "/hdd/dataset/talkDataSet1/"  # 결과를 저장할 파일 경로

collect_lines_with_speech_act(base_folder_path, target_speech_act, target_folders, output_file)
