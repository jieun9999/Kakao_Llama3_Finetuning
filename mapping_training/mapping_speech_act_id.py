import os
import json

##### 다음은 (COPY_preprocessed 폴더)를 덮어쓰기 하는 파일입니다 ####
# COPY_preprocessed : preprocessed(역할기반으로 전처리된 데이터)를 복제한 폴더입니다.

# labellingData 폴더 경로 설정
base_folder_path = "/hdd/dataset/talkDataSet1/2.per_subject_text_daily_conversation_data/1.data/2.Validation/labellingData/copy_preprocessed"

def modify_speech_act(speech_act):
    # speechAct 수정 로직
    if speech_act == "(선언/위임하기)":
        return "일상적으로 반응하기"
    elif speech_act == "턴토크 사인(관습적 반응)":
        return "일상적으로 반응하기"
    elif speech_act == "(지시) 질문하기":
        return "질문하기"
    elif speech_act == "(지시) 명령/요구하기":
        return "요구하기"
    elif speech_act == "(지시) 부탁하기":
        return "요구하기"
    elif speech_act == "(지시) 충고/제안하기":
        return "충고/제안하기"
    elif speech_act == "(표현) 인사하기":
        return "인사하기"
    elif speech_act == "(표현) 긍정감정 표현하기":
        return "긍정감정 표현하기"
    elif speech_act == "(표현) 부정감정 표현하기":
        return "부정감정 표현하기"
    elif speech_act == "(표현) 사과하기":
        return "사과하기"
    elif speech_act == "(표현) 감사하기":
        return "감사하기"
    elif speech_act == "(단언) 주장하기":
        return "주장하기"
    elif speech_act == "(단언) 진술하기":
        return "정보 제공하기"
    elif speech_act == "(단언) 반박하기":
        return "반박하기"
    elif speech_act == "(언약) 위협하기":
        return "위협하기"
    elif speech_act == "(언약) 약속하기(제3자와)/(개인적 수준)":
        return "개인적으로 약속하기"
    elif speech_act == "(언약) 거절하기":
        return "거절하기"
    
    return speech_act  # 조건에 맞지 않으면 원래 값 반환

def modify_lines_with_speech_act_and_role(base_folder_path, target_folders):
    for folder_name in target_folders:
        folder_path = os.path.join(base_folder_path, folder_name)  # 각 KAKAO 폴더 경로 설정
        if os.path.isdir(folder_path):  # 폴더인지 확인
            for filename in os.listdir(folder_path):
                if filename.endswith(".json"):  # JSON 파일만 처리
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        try:
                            data = json.load(file)
                            modified = False  # 수정 여부 플래그

                            for message in data["messages"]:
                                if message["role"] == "assistant":
                                    # role 수정
                                    message["role"] = "friend"
                                    modified = True  # 수정됨을 표시

                                # speechAct 수정
                                speech_act = message.get("speechAct", "").strip()
                                new_speech_act = modify_speech_act(speech_act)
                                if new_speech_act != speech_act:  # 수정이 필요한 경우
                                    message["speechAct"] = new_speech_act
                                    modified = True  # 수정됨을 표시

                            # 수정된 경우에만 파일 저장
                            if modified:
                                with open(file_path, 'w', encoding='utf-8') as outfile:
                                    json.dump(data, outfile, ensure_ascii=False, indent=4)

                        except json.JSONDecodeError:
                            print(f"Error decoding JSON in file: {folder_name}/{filename}")

# 실행
target_folders = ["1.KAKAO1", "2.KAKAO2", "3.KAKAO3", "4.KAKAO4"]  # 순차적으로 탐색할 폴더 목록

modify_lines_with_speech_act_and_role(base_folder_path, target_folders)
