from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig
import re

# 8-bit 양자화 설정
quantization_config = BitsAndBytesConfig(load_in_8bit=True)

try:
    # 1. 토크나이저 로드
    print("토크나이저 로드 시작...")
    tokenizer = AutoTokenizer.from_pretrained("/workspace/ssd/fine_tuned_model")
    print("토크나이저 로드 완료.")
except Exception as e:
    print(f"토크나이저 로드 중 오류 발생: {e}")
    exit()


try:
    # 2. 모델 로드
    print("모델 로드 시작...")
    model = AutoModelForCausalLM.from_pretrained("/workspace/ssd/fine_tuned_model",
    quantization_config=quantization_config)
    print("모델 로드 완료.")
except Exception as e:
    print(f"모델 로드 중 오류 발생: {e}")
    exit()

# 테스트 프롬프트
input_text = [
    {
        "role": "system",
        "content": "You are a fun and helpful friend Varco. Respond actively to the user's instructions in informal manner and provide responses based on the following speech acts:\n- 일상적으로 반응하기\n- 질문하기\n- 정보 제공하기\n- 긍정감정 표현하기\n- 부정감정 표현하기\n- 충고/제안하기\n- 반박하기\n- 위협하기\n- 주장하기\n- 사과하기\n- 감사하기\n- 요구하기\n- 개인적으로 약속하기\n- 거절하기\n- 인사하기\n- 농담하기\n- N/A. Answer in KOREAN."
    },
    {
        "role": "user",
        "content": "와 저녁 되니까 야식 땡긴다 ㅋㅋ"
    }
]

# 입력 텍스트에서 역할에 해당하는 내용을 문자열로 추출
system_message = input_text[0]["content"]
user_message = input_text[1]["content"]

# 토크나이징
try:
    print("입력 텍스트 토크나이징 시작...")
    inputs = tokenizer(
        [system_message, user_message], 
        return_tensors="pt", 
        padding=True,     # 패딩 활성화
        truncation=True   # 잘림 활성화
    )
    # 입력 텐서를 모델과 동일한 디바이스로 이동
    inputs = inputs.to("cuda")  # 모델이 GPU에 있으므로 입력 텐서를 GPU로 이동
    print("입력 텍스트 토크나이징 완료.")
except Exception as e:
    print(f"입력 텍스트 토크나이징 중 오류 발생: {e}")
    exit()

try:
    # 4. 모델 생성(generation)
    print("모델 생성 시작...")
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,  # 새로 생성할 텍스트의 최대 길이
        no_repeat_ngram_size=3,  # 반복 방지
        pad_token_id=tokenizer.eos_token_id  # 패딩 토큰을 종료 토큰으로 설정
    )
    print("모델 생성 완료.")
except Exception as e:
    print(f"모델 생성 중 오류 발생: {e}")
    exit()
try:
    # 5. 출력 결과 디코딩
    print("출력 결과 디코딩 시작...")
    
    # 입력 텍스트 길이 계산
    # system_message와 user_message를 합쳐서 인코딩
    input_length = len(tokenizer.encode(system_message + user_message, add_special_tokens=False))
    
    # 생성된 텍스트에서 입력 텍스트 이후의 부분만 디코딩
    result = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
    print("출력 결과 디코딩 완료.")
    print("결과:", result)

except Exception as e:
    print(f"출력 결과 디코딩 중 오류 발생: {e}")
    exit()
