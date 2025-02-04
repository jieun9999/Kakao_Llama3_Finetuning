from transformers import AutoTokenizer, AutoModelForCausalLM

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
    model = AutoModelForCausalLM.from_pretrained("/workspace/ssd/fine_tuned_model")
    print("모델 로드 완료.")
except Exception as e:
    print(f"모델 로드 중 오류 발생: {e}")
    exit()

# 테스트 프롬프트
input_text = "role: user, speechAct: 질문하기, content: 안녕하세요. 오늘 날씨는 어떤가요?"

try:
    # 3. 입력 텍스트 토크나이징
    print("입력 텍스트 토크나이징 시작...")
    inputs = tokenizer(input_text, return_tensors="pt")
    print("입력 텍스트 토크나이징 완료.")
except Exception as e:
    print(f"입력 텍스트 토크나이징 중 오류 발생: {e}")
    exit()

try:
    # 4. 모델 생성(generation)
    print("모델 생성 시작...")
    outputs = model.generate(**inputs, max_length=50)
    print("모델 생성 완료.")
except Exception as e:
    print(f"모델 생성 중 오류 발생: {e}")
    exit()

try:
    # 5. 출력 결과 디코딩
    print("출력 결과 디코딩 시작...")
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("출력 결과 디코딩 완료.")
    print("결과:", result)
except Exception as e:
    print(f"출력 결과 디코딩 중 오류 발생: {e}")
    exit()

