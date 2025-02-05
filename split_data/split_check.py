import os

# 유동적으로 변경할 폴더명
folder_name = "0205_split_data"

# 경로 설정
data_dir = f'/workspace/hdd/2.per_subject_text_daily_conversation_data/{folder_name}/total'
train_dir = f'/workspace/hdd/2.per_subject_text_daily_conversation_data/{folder_name}/1.train'
val_dir = f'/workspace/hdd/2.per_subject_text_daily_conversation_data/{folder_name}/2.validation'
test_dir = f'/workspace/hdd/2.per_subject_text_daily_conversation_data/{folder_name}/3.test'

# JSON 파일 개수를 세는 함수
def count_json_files(directory):
    try:
        return len([file for file in os.listdir(directory) if file.endswith(".json")])
    except FileNotFoundError:
        print(f"경로를 찾을 수 없습니다: {directory}")
        return 0

# 각 경로의 JSON 파일 개수 계산
data_dir_count = count_json_files(data_dir)
train_dir_count = count_json_files(train_dir)
val_dir_count = count_json_files(val_dir)
test_dir_count = count_json_files(test_dir)

# 로그 출력
print(f"JSON 파일 개수 로그:")
print(f"data_dir: {data_dir_count}")
print(f"train_dir: {train_dir_count}")
print(f"val_dir: {val_dir_count}")
print(f"test_dir: {test_dir_count}")

# 검증: data_dir의 개수가 나머지 경로의 합과 같은지 확인
if data_dir_count == (train_dir_count + val_dir_count + test_dir_count):
    print("검증 성공: data_dir의 JSON 파일 개수가 나머지 경로의 JSON 파일 개수의 합과 같습니다.")
else:
    print("검증 실패: data_dir의 JSON 파일 개수가 나머지 경로의 JSON 파일 개수의 합과 다릅니다.")
