import os
import json

# 결과를 저장할 파일 (절대 경로로 설정)
base_folder_path = "/workspace/hdd/2.per_subject_text_daily_conversation_data/1.data/2.Validation/labellingData/preprocessed copy"
output_file = os.path.join(base_folder_path, "output_speech_act_id.txt")  # 절대 경로

# 탐색할 폴더
folder = "KAKAO"
folder_path = os.path.join(base_folder_path, folder)  # 절대 경로로 설정

# speechAct의 빈도수를 저장할 딕셔너리
speech_act_count = {}

# 출력 순서 정의
output_order = [
    "위협하기",
    "거절하기",
    "사과하기",
    "인사하기",
    "감사하기",
    "반박하기",
    "부정감정 표현하기",
    "긍정감정 표현하기",
    "일상적으로 반응하기",
    "요구하기",
    "개인적으로 약속하기",
    "충고/제안하기",
    "질문하기",
    "정보 제공하기",
    "주장하기"
]

# 폴더 확인
if not os.path.isdir(folder_path):
    print(f"폴더 {folder_path}가 존재하지 않습니다.")
    exit()

# 폴더 내 파일 순회
for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):  # JSON 파일만 처리
        file_path = os.path.join(folder_path, file_name)  # 절대 경로로 파일 경로 생성
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                # messages에서 speechAct 추출
                if "messages" in data:
                    for message in data["messages"]:
                        if "speechAct" in message:
                            speech_act = message["speechAct"]
                            # speechAct 카운트 증가
                            if speech_act in speech_act_count:
                                speech_act_count[speech_act] += 1
                            else:
                                speech_act_count[speech_act] = 1
        except Exception as e:
            print(f"파일 {file_name} 처리 중 오류 발생: {e}")

# 결과를 텍스트 파일에 저장
try:
    with open(output_file, "w", encoding="utf-8") as f:
        for speech_act in output_order:  # 정의된 순서대로 출력
            count = speech_act_count.get(speech_act, 0)  # 값이 없으면 0으로 처리
            f.write(f"{speech_act} {count}\n")
    print(f"speechAct 데이터를 {output_file}에 저장했습니다.")
except Exception as e:
    print(f"결과 저장 중 오류 발생: {e}")
