import os
import json

# 폴더 경로 및 결과 파일 경로
folder_path = "/workspace/hdd/2.per_subject_text_daily_conversation_data/1.data/1.Training/labellingData/1.KAKAO1"
output_path = "/workspace/food2.txt"

file_count = 0
max_files = 100  # 최대 파일 수 제한
skip_files = 100 # 이미 본 파일 스킵. 

# txt 파일 생성 및 데이터 작성
with open(output_path, 'w', encoding='utf-8') as output_file:
   # 폴더 내 파일 순회
   file_names = os.listdir(folder_path)

   for file_name in file_names:
       if file_count >= max_files:  # 100개 파일 제한 체크
           break
           
       if file_name.endswith(".json"):
           file_path = os.path.join(folder_path, file_name)
           
           try:
               with open(file_path, "r", encoding="utf-8") as f:
                   data = json.load(f)
               
               # 식음료 주제 확인
               if (data.get("info") and 
                   isinstance(data["info"], list) and 
                   data["info"][0].get("annotations") and
                   data["info"][0]["annotations"].get("subject") == "식음료"):

                   if skip_files >= 0:
                        skip_files -= 1
                        continue
                   
                   # lines 데이터 추출 및 작성
                   lines = data["info"][0]["annotations"].get("lines", [])
                   for line in lines:
                       if line.get("speaker") and line.get("norm_text"):
                           output_file.write(f"{line['speaker']['id']}: {line['norm_text']}\n")
                   
                   # 파일 간 구분을 위해 2줄 띄우기
                   output_file.write("\n\n")
                   
                   file_count += 1
                   print(f"처리된 파일: {file_name} ({file_count}/100)")
                       
           except json.JSONDecodeError:
               print(f"JSON 파일 읽기 오류: {file_name}")
           except Exception as e:
               print(f"파일 처리 중 오류 발생 {file_name}: {str(e)}")

print(f"\n저장 완료: {output_path}")
print(f"처리된 파일 수: {file_count}")