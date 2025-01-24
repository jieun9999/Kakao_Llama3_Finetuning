import os

# 경로 설정
data_dir = '/hdd/dataset/talkDataSet1/2.per_subject_text_daily_conversation_data/1.data/proprocessed_data/total'
train_dir = '/hdd/dataset/talkDataSet1/2.per_subject_text_daily_conversation_data/1.data/proprocessed_data/1.train'
val_dir = '/hdd/dataset/talkDataSet1/2.per_subject_text_daily_conversation_data/1.data/proprocessed_data/2.validation'
test_dir = '/hdd/dataset/talkDataSet1/2.per_subject_text_daily_conversation_data/1.data/proprocessed_data/3.test'

# total 폴더의 파일명 배열 생성
data_files = os.listdir(data_dir)

# 1, 2, 3 폴더를 돌면서 배열에서 파일명을 삭제
for folder in [train_dir, val_dir, test_dir]:
    folder_files = os.listdir(folder)  # 해당 폴더의 파일명 가져오기
    for file in folder_files:
        if file in data_files:
            data_files.remove(file)  # 배열에서 삭제

# 결과 출력
print("Remaining files in total folder cnt:") 
print(len(data_files)) #json이 아닌 파일 1 출력
