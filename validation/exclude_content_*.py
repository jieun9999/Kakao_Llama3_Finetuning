################################################################################################################
# JSON 파일에서 content에 '*'가 포함된 항목을 가진 파일들을 삭제하고, 최종적으로 preprocessed copy 폴더 상에서 해당 파일들을 제거한 뒤 덮어쓰는 방식
################################################################################################################

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
    # 경로 내 모든 JSON 파일 탐색
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

        # content 필드에 '*' 문자가 포함된 항목이 있는지 확인
        has_asterisk_content = any(
            '*' in message.get("content", "") for message in data.get("messages", [])
        )

        if has_asterisk_content:
            # '*'가 포함된 파일 제거
            os.remove(file_path)
            removed_files_count += 1
        else:
            # '*'가 없는 파일은 그대로 덮어쓰기
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
