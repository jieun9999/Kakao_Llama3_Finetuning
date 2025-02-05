##############
# 단순히 speechAct가 "N/A"를 포함하고 있는 파일을 제외하여 결과를 내는 코드
##############

import os
import json

# base_folder_path 설정
base_folder_path = "/workspace/hdd/2.per_subject_text_daily_conversation_data/1.data/1.Training/labellingData/preprocessed copy"

# 제외된 파일 로그를 저장할 리스트
excluded_files = []
total_files = 0  # 전체 파일 갯수 카운트
processed_files = 0  # 제외 후 처리된 파일 갯수 카운트

def process_files_excluding_na(base_folder_path, target_folders):
    global total_files, processed_files

    for folder_name in target_folders:
        folder_path = os.path.join(base_folder_path, folder_name)  # 각 폴더 경로 설정
        if os.path.isdir(folder_path):  # 폴더인지 확인
            for filename in os.listdir(folder_path):
                if filename.endswith(".json"):  # JSON 파일만 처리
                    total_files += 1  # 전체 파일 갯수 증가
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        try:
                            data = json.load(file)
                            # "speechAct"가 "N/A"인 메시지가 있는지 확인
                            if any(message.get("speechAct") == "N/A" for message in data.get("messages", [])):
                                # 제외된 파일 로그에 추가
                                excluded_files.append(f"{folder_name}/{filename}")
                                # 파일 삭제
                                os.remove(file_path)
                                continue  # 이 파일은 건너뛰기

                            # 파일을 그대로 덮어쓰기 (변경 없이 저장)
                            with open(file_path, 'w', encoding='utf-8') as outfile:
                                json.dump(data, outfile, ensure_ascii=False, indent=4)
                                processed_files += 1  # 처리된 파일 갯수 증가

                        except json.JSONDecodeError:
                            print(f"Error decoding JSON in file: {file_path}")

# 실행
target_folders = ["1.KAKAO1", "2.KAKAO2", "3.KAKAO3", "4.KAKAO4"]  # 순차적으로 탐색할 폴더 목록
process_files_excluding_na(base_folder_path, target_folders)

# 로그 출력
excluded_count = len(excluded_files)  # 제외된 파일 갯수 계산
print(f"원본 파일 갯수: {total_files}")
print(f"제외된 파일 갯수: {excluded_count}")
print(f"제외 후 파일 갯수: {processed_files}")

# 제외된 파일 목록을 항상 파일에 저장
log_file_path = "/workspace/hdd/2.per_subject_text_daily_conversation_data/1.data/1.Training/labellingData/preprocessed copy/excluded_files_log.txt"
with open(log_file_path, 'w', encoding='utf-8') as log_file:
    log_file.write("\n".join(excluded_files))
print(f"\n전체 제외된 파일 목록은 '{log_file_path}'에 저장되었습니다.")
