from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig

# 8-bit 양자화 설정
quantization_config = BitsAndBytesConfig(load_in_8bit=True)

# 1. 토크나이저 및 모델 로드
print("모델 및 토크나이저 로드 시작...")
# tokenizer = AutoTokenizer.from_pretrained("/workspace/ssd/0205_fine_tuned_model")
tokenizer = AutoTokenizer.from_pretrained("/workspace/ssd/0124_fine_tuned_model")

model = AutoModelForCausalLM.from_pretrained(
    # "/workspace/ssd/0205_fine_tuned_model",
    "/workspace/ssd/0124_fine_tuned_model",
    quantization_config=quantization_config
)

# 테스트 프롬프트


#제로샷
# messages = [
#     {
#         "role": "system",
#         "content": "You are a fun and helpful friend Varco. Respond actively to the user's instructions in an informal manner and provide responses based on one of the following speech acts: - 일상적으로 반응하기 - 질문하기 - 정보 제공하기 - 긍정감정 표현하기 - 부정감정 표현하기 - 충고/제안하기 - 반박하기 - 위협하기 - 주장하기 - 사과하기 - 감사하기 - 요구하기 - 개인적으로 약속하기 - 거절하기 - 인사하기 - 농담하기 - N/A. Use '일상적으로 반응하기' speech act for your response. Answer in KOREAN"
#     },
#     {
#         "role": "user",
#         "content": "와 저녁 되니까 야식 땡긴다 ㅋㅋ"
#     }
# ]

#원샷
# messages = [
#     {
#         "role": "system",
#         "content": "You are a fun and helpful friend Varco. Respond actively to the user's instructions in an informal manner and provide responses based on one of the following speech acts: - 일상적으로 반응하기 - 질문하기 - 정보 제공하기 - 긍정감정 표현하기 - 부정감정 표현하기 - 충고/제안하기 - 반박하기 - 위협하기 - 주장하기 - 사과하기 - 감사하기 - 요구하기 - 개인적으로 약속하기 - 거절하기 - 인사하기 - 농담하기 - N/A. Answer in KOREAN. Use '일상적으로 반응하기' speech act for your response."
#     },
#     {
#         "role": "user",
#         "content": "나랑 말고 아빠랑 엄마랑 드라이브 다니는데 가끔 나도 같이 가ㅋㅋ"
#     },
#     {
#         "role": "assistant",
#         "content": "오ㅋㅋ 그렇구나"
#     },
#     {
#         "role": "user",
#         "content": "와 저녁 되니까 야식 땡긴다 ㅋㅋ"
#     }
# ]

#퓨샷
messages = [
    {
        "role": "system",
        "content": "You are a fun and helpful friend Varco. Respond actively to the user's instructions in an informal manner and provide responses based on one of the following speech acts: - 일상적으로 반응하기 - 질문하기 - 정보 제공하기 - 긍정감정 표현하기 - 부정감정 표현하기 - 충고/제안하기 - 반박하기 - 위협하기 - 주장하기 - 사과하기 - 감사하기 - 요구하기 - 개인적으로 약속하기 - 거절하기 - 인사하기 - 농담하기 - N/A. Answer in KOREAN. Use '일상적으로 반응하기' speech act for your response."
    },
    {
        "role": "user",
        "content": "나랑 말고 아빠랑 엄마랑 드라이브 다니는데 가끔 나도 같이 가ㅋㅋ"
    },
    {
        "role": "assistant",
        "content": "오ㅋㅋ 그렇구나"
    },
    {
        "role": "user",
        "content": "나는 야구 좋아해서 동호회도 들어갔어 ㅋㅋ"
    },
    {
        "role": "assistant",
        "content": "대박"
    },
    {
        "role": "user",
        "content": "아 요즘 헬스 브랜드들도 쿠팡에 많이 입점했어!"
    },
    {
        "role": "assistant",
        "content": "아 진짜?"
    },
    {
        "role": "user",
        "content": "와 저녁 되니까 야식 땡긴다 ㅋㅋ"
    }
]

inputs = tokenizer.apply_chat_template(messages, return_tensors="pt", padding=True, truncation=True).to(model.device)

# 입력 텐서 구조 확인
# print("입력 텐서 구조:")
# print(inputs)

# 종료 토큰 ID 설정
eos_token_id = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

# 2. 텍스트 생성
print("텍스트 생성 시작...")

input_length = inputs.size(1)
outputs = model.generate(
    inputs,
    eos_token_id=eos_token_id,
    max_new_tokens= 100 + input_length,
    # max_new_tokens = 100,
    no_repeat_ngram_size=3,
    pad_token_id=tokenizer.eos_token_id
)

# 출력 텐서 구조 확인
# print("출력 텐서 구조:")
# print(outputs)

# 3. 출력 결과 디코딩
print("출력 결과:")
print(tokenizer.decode(outputs[0][input_length: ], skip_special_tokens=True))  # 2차원일 경우 인덱스 수정 필요
