from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig
import pandas as pd
# from few_shots import conversations
from few_shots_2 import conversations

############################################
# 다음은 발화전략을 지정하지 않고 응답을 생성하는 파일입니다
############################################

# sentence_cut.py에서 limit_sentences_with_fallback 함수 가져오기
from sentence_cut import limit_sentences_with_fallback

# 토크나이저 및 모델 로드
print("모델 및 토크나이저 로드 시작...")

# varco 
# quantization_config = BitsAndBytesConfig(load_in_8bit=True)
# model = AutoModelForCausalLM.from_pretrained(
#       "NCSOFT/Llama-VARCO-8B-Instruct",
#       device_map="auto",
#     quantization_config=quantization_config
#   )
# tokenizer = AutoTokenizer.from_pretrained("NCSOFT/Llama-VARCO-8B-Instruct")

#0205 model
quantization_config = BitsAndBytesConfig(load_in_8bit=True)
tokenizer = AutoTokenizer.from_pretrained("/workspace/ssd/0205_fine_tuned_model")
model = AutoModelForCausalLM.from_pretrained(
    "/workspace/ssd/0205_fine_tuned_model",
    quantization_config=quantization_config
)

# 테스트 프롬프트
output = []

# conversations을 돌면서 messages에 넣고, 해당 메세지를 바탕으로 응답을 생성
for conversation in conversations:
    messages = [
        {
            "role": "system",
            "content": "너는 친근하고 재미있는 친구야. 말투는 반말로 하고, 사용자의 상황과 발화 내용에 맞춰 적절한 방식으로 자연스럽게 반응해.",
        }
    ]
    messages.extend(conversation)
    print(messages)  # messages를 출력합니다.
    print("\n")  # 빈 줄을 출력하여 가독성을 향상합니다.

    # 입력 텐서 생성
    inputs = tokenizer.apply_chat_template(messages, return_tensors="pt", padding=True, truncation=True).to(model.device)

    # attention_mask 설정
    attention_mask = inputs != tokenizer.pad_token_id

    # 종료 토큰 ID 설정
    eos_token_id = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    # 텍스트 생성
    print("텍스트 생성 시작...")
    # 입력 시퀀스의 토큰 개수
    input_length = inputs.size(1)
    outputs = model.generate(
        inputs,
        attention_mask=attention_mask,  # attention_mask 추가
        eos_token_id=eos_token_id,
        max_new_tokens= 100,
        no_repeat_ngram_size= 3, # 값이 커질수록 더 긴 반복 구문을 방지하므로, 텍스트가 더 다양해질 가능성이 높습니다.
        repetition_penalty=2.0,
        pad_token_id=tokenizer.eos_token_id
    )

    # 출력 결과 디코딩 
    # 모델이 새롭게 생성한 텍스트만 선택
    generated_text = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)

    # 문장 자르기 함수 실행
    limited_text = limit_sentences_with_fallback(generated_text, max_sentences=3)
    output.append([messages[-1]["content"], limited_text])  

# CSV 저장 (컬럼 조정)
df = pd.DataFrame(output, columns=["입력문장", "모델응답"])
output_file_name = "이어지는 퓨샷_0205model.csv"
df.to_csv(output_file_name, index=False, encoding="utf-8-sig")
print(f"CSV 파일 저장 완료: {output_file_name}")