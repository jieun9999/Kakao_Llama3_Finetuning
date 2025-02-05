import os

# base_folder_path 설정
base_folder_path = "/workspace/hdd/2.per_subject_text_daily_conversation_data/1.data/2.Validation/labellingData/preprocessed copy"
target_folders = ["KAKAO"]

# 전체 파일 개수를 저장할 변수
total_file_count = 0

# 각 폴더를 순회하며 .json 파일 개수 카운트
for folder_name in target_folders:
    folder_path = os.path.join(base_folder_path, folder_name)  # 폴더 경로 생성
    if os.path.isdir(folder_path):  # 폴더가 존재하는지 확인
        # 폴더 내 .json 파일 개수 카운트
        file_count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(".json")])
        total_file_count += file_count
        print(f"'{folder_name}' 폴더의 .json 파일 개수: {file_count}")
    else:
        print(f"'{folder_name}' 폴더가 존재하지 않습니다.")

# 전체 .json 파일 개수 출력
print(f"\n전체 .json 파일 개수: {total_file_count}")
