from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig

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
input_text = "role: user, speechAct: 질문하기, content: 와 저녁 되니까 야식 땡긴다 ㅋㅋ"

try:
    # 3. 입력 텍스트 토크나이징
    print("입력 텍스트 토크나이징 시작...")
    inputs = tokenizer(input_text, return_tensors="pt")
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
    input_length = len(tokenizer.encode(input_text, add_special_tokens=False))
    # 생성된 텍스트에서 입력 텍스트 이후의 부분만 디코딩
    result = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
    print("출력 결과 디코딩 완료.")
    print("결과:", result)
except Exception as e:
    print(f"출력 결과 디코딩 중 오류 발생: {e}")
    exit()
