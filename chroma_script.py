import chromadb
import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# ChromaDB 클라이언트 생성
chroma_client = chromadb.PersistentClient()
# PersistentClient는 로컬에서 데이터베이스를 저장하고 로드 
# 그 외에 메모리에 저장하는 EphmeralClient, 네트워크를 통해서 접속하는 HttpClient가 있습니다. 실제 서비스에서는 HttpClient가 권장됩니다.

# 컬렉션 생성
# 컬렉션은 임베딩, 문서 및 추가 메타데이터를 저장하는 곳입니다.
collection = chroma_client.get_collection(name = "my_collection")

# 데이터 불러오기
df = pd.read_excel("/workspace/output/음식_싱글턴 대화 추출.xlsx")
df.sample(5)

# 임베딩 모델 불러오기
model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
# 문장 변환 모델, 문장과 문단을 768차원 밀집 벡터 공간에 매핑, 클러스터링이나 의미 검색 작업에 사용될 수 있음
# ChromaDB의 내장 임베딩 모델이 아닌 한국어 임베딩 모델을 따로 불러와서 사용

# 데이터 삽입하기
for index, row in tqdm(df.iterrows(), total=df.shape[0]): #엑셀 파일의 각 행을 반복 처리
    # 각 행의 질문과 답변을 가져오기
    question = row['User']
    answer = row['Answer']

    # 질문과 답변을 임베딩으로 변환
    question_embedding = model.encode(question)
    answer_embedding = model.encode(answer)

    # ChromaDB 컬렉션에 데이터 삽입
    collection.upsert(
        embeddings=[question_embedding, answer_embedding], # 질문과 답변의 임베딩
        documents=[question, answer], #원본 텍스트
        metadatas=[
            {"type" : "question"},
            {"type": "answer"}
        ], # 메타데이터
        ids=[f"question_{index}", f"answer_{index}"]  # 고유 ID
    )

print("데이터 삽입 완료!")

# 쿼리 실행하기
query_text = "저녁 메뉴 추천해줘" 
query_embedding = model.encode([query_text]) 

# 쿼리 실행
results = collection.query(
    query_embeddings= query_embedding,
    where={"type": "answer"},  # type이 "answer"인 데이터만 검색
    n_results=3
)

print(results)