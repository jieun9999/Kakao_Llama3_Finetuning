from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig

# 8-bit 양자화 설정
quantization_config = BitsAndBytesConfig(load_in_8bit=True)

# 1. 토크나이저 및 모델 로드
print("모델 및 토크나이저 로드 시작...")
tokenizer = AutoTokenizer.from_pretrained("/workspace/ssd/0205_fine_tuned_model")
model = AutoModelForCausalLM.from_pretrained(
    "/workspace/ssd/0205_fine_tuned_model",
    quantization_config=quantization_config
)

# 테스트 프롬프트
messages = [
    {
        "role": "user",
        "speechAct": "주장하기",
        "content": "와 저녁 되니까 야식 땡긴다 ㅋㅋ"
    }
]

# 입력 텐서 생성
inputs = tokenizer.apply_chat_template(
    messages, 
    return_tensors="pt", 
    padding=True, 
    truncation=True
).to(model.device)  # 모델 디바이스에 맞게 이동

# 입력 텐서 디코딩
print("입력 텍스트 디코딩:")
print(tokenizer.decode(inputs[0]))  # 첫 번째 시퀀스를 디코딩


# 종료 토큰 ID 설정
eos_token_id = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

# 2. 텍스트 생성
print("텍스트 생성 시작...")
outputs = model.generate(
    inputs,
    eos_token_id=eos_token_id,
    max_new_tokens=100,
    no_repeat_ngram_size=3,
    pad_token_id=tokenizer.eos_token_id
)

# 3. 출력 결과 디코딩
print("출력 결과:")
print(tokenizer.decode(outputs[0]))
