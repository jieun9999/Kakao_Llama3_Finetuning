from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig
import wandb

# W&B 초기화
wandb.init(project="llm_prompt_tracking", name="llm_generation_run")

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
            "role": "assistant",
            "content": "너 방금 먹은 게 점저야?",
    },
    {
            "role": "user",
            "content": "아니 나는 조금 전에 먹은 거는 점심이야!",
    },
    {
            "role": "assistant",
            "content": "점심을 몇 시에 먹는 거야?",
    },
    {
            "role": "user",
            "content": "원래는 2신데 오늘은 4시에 먹었어 하하",
    },
    {
            "role": "assistant",
            "content": "뭐 먹었는지 알려줄 수 있어?",
    }
]

# 입력 텐서 생성
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt", padding=True, truncation=True).to(model.device)

# 데이터 구조 확인
# print("inputs 데이터 구조:", inputs)
# print("inputs 텐서 크기:", inputs.shape)

# attention_mask 설정
attention_mask = inputs != tokenizer.pad_token_id

# 종료 토큰 ID 설정
eos_token_id = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

# 텍스트 생성
print("텍스트 생성 시작...")
input_length = inputs.size(1)
outputs = model.generate(
    inputs,
    attention_mask=attention_mask,  # attention_mask 추가
    eos_token_id=eos_token_id,
    max_new_tokens= 50 + input_length,
    no_repeat_ngram_size=4, # 값이 커질수록 더 긴 반복 구문을 방지하므로, 텍스트가 더 다양해질 가능성이 높습니다.
    pad_token_id=tokenizer.eos_token_id
)

# 출력 결과 디코딩
generated_text = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)


# W&B에 로그 기록
wandb.log({
    "messages": messages,
    "generated_text": generated_text
})

# 결과 출력
print("출력 결과:")
print(generated_text)
