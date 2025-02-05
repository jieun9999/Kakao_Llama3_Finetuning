import os
import json

# 경로 설정
base_folder_path = "/workspace/hdd/2.per_subject_text_daily_conversation_data/1.data/2.Validation/labellingData/preprocessed copy/KAKAO"

# 전체 파일 개수 저장 변수
initial_file_count = 0
final_file_count = 0
removed_files_count = 0  # 제거된 파일 개수

# 처리 시작
try:
    # 경로 내 모든 파일 탐색
    all_files = [f for f in os.listdir(base_folder_path) if f.endswith(".json")]
    initial_file_count = len(all_files)  # 처리 전 파일 개수
    print(f"처리 전 전체 JSON 파일 개수: {initial_file_count}")

    for file_name in all_files:
        file_path = os.path.join(base_folder_path, file_name)

        # JSON 파일 읽기
        with open(file_path, "r", encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                continue  # 디코딩 오류 발생 시 해당 파일 건너뛰기

        # speechAct가 "N/A"인지 확인
        has_na_speech_act = any(
            message.get("speechAct") == "N/A" for message in data.get("messages", [])
        )

        if has_na_speech_act:
            # "N/A"가 포함된 파일 제거
            os.remove(file_path)
            removed_files_count += 1
        else:
            # "N/A"가 없는 파일은 그대로 덮어쓰기
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

    # 처리 후 파일 개수 확인
    all_files_after = [f for f in os.listdir(base_folder_path) if f.endswith(".json")]
    final_file_count = len(all_files_after)  # 처리 후 파일 개수

    # 요약 로그 출력
    print(f"처리 후 전체 JSON 파일 개수: {final_file_count}")
    print(f"총 제거된 파일 개수: {removed_files_count}")

except Exception as e:
    print(f"오류 발생: {e}")
