################################################################################################################
# JSON 파일에서 content에 '*'가 포함된 항목을 가진 파일들을 삭제하고, 최종적으로 preprocessed copy 폴더 상에서 해당 파일들을 제거한 뒤 덮어쓰는 방식
################################################################################################################

import os
import json

# 기본 폴더 경로와 타겟 폴더 목록
base_folder_path = "/workspace/hdd/2.per_subject_text_daily_conversation_data/1.data/1.Training/labellingData/preprocessed copy"
target_folders = ["1.KAKAO1", "2.KAKAO2", "3.KAKAO3", "4.KAKAO4"]

# 파일 개수를 카운트할 변수
total_json_file_count = 0  # 전체 JSON 파일 수
filtered_file_count = 0   # '*'가 포함된 파일 수

# JSON 파일에서 '*'가 포함된 항목 확인 후 삭제
for folder_name in target_folders:
    folder_path = os.path.join(base_folder_path, folder_name)  # 각 타겟 폴더 경로
    if os.path.isdir(folder_path):  # 폴더가 존재하는지 확인
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith(".json"):  # JSON 파일만 처리
                total_json_file_count += 1  # 전체 JSON 파일 개수 증가
                try:
                    # JSON 파일 읽기
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                    
                    # messages 리스트에서 content에 '*'가 포함된 항목 확인
                    if "messages" in data and isinstance(data["messages"], list):
                        for message in data["messages"]:
                            if "content" in message and isinstance(message["content"], str) and '*' in message["content"]:
                                # 조건을 만족하면 파일 삭제
                                os.remove(file_path)  # 파일 삭제
                                filtered_file_count += 1  # 삭제된 파일 개수 증가
                                print(f"'{file_name}' 파일을 삭제했습니다.")
                                break  # 조건을 만족하면 더 이상 확인하지 않고 종료
                except json.JSONDecodeError as e:
                    print(f"'{file_name}' 파일은 유효한 JSON이 아닙니다. 오류: {e}")
                except Exception as e:
                    print(f"파일 처리 중 오류 발생: {file_path}, 오류: {e}")
    else:
        print(f"'{folder_name}' 폴더가 존재하지 않습니다.")

# 최종 남은 파일 수 계산
final_file_count = total_json_file_count - filtered_file_count

# 최종 결과 출력
print(f"\n전체 JSON 파일 수: {total_json_file_count}개")
print(f"messages 리스트에서 content에 '*'가 포함된 파일 수 (삭제된 파일 수): {filtered_file_count}개")
print(f"최종 남은 파일 수: {final_file_count}개")
