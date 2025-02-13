from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import pandas as pd
from sentence_cut import limit_sentences_with_fallback
from few_shots import create_conv

############################################################
# 다음은 15개 발화전략 중 하나를 부여받으면 그에 맞게 응답을 생성하는 파일입니다.
##############################################################

# varco 
# quantization_config = BitsAndBytesConfig(load_in_8bit=True)
# model = AutoModelForCausalLM.from_pretrained(
#       "NCSOFT/Llama-VARCO-8B-Instruct",
#       device_map="auto",
#     quantization_config=quantization_config
#   )
# tokenizer = AutoTokenizer.from_pretrained("NCSOFT/Llama-VARCO-8B-Instruct")
# model_name = "varco"

#0205 model
quantization_config = BitsAndBytesConfig(load_in_8bit=True)

tokenizer = AutoTokenizer.from_pretrained("/workspace/ssd/0205_fine_tuned_model")

model = AutoModelForCausalLM.from_pretrained(
    "/workspace/ssd/0205_fine_tuned_model",
    quantization_config=quantization_config
)
model_name = "custom"

# 출력 저장을 위한 리스트
output = []

speechActs = ["일상적으로 반응하기",
            "질문하기",
            "정보 제공하기",
            "긍정감정 표현하기",
            "부정감정 표현하기",
            "충고/제안하기",
            "반박하기",
            "위협하기",
            "주장하기",
            "사과하기",
            "감사하기",
            "요구하기",
            "개인적으로 약속하기",
            "거절하기",
            "인사하기"]

# 예를 들어, conv1은 모든 대화에서 첫 번째 발화만 모아둔 리스트입니다.
conv1 = create_conv(1)
conv2 = create_conv(2)
conv3 = create_conv(3)
conv4 = create_conv(4)
conv5 = create_conv(5)
conv6 = create_conv(6)
conv7 = create_conv(7)


# 두 리스트의 길이가 같다고 가정하고 출력
# c1 = conv1[0], c2 = conv2[0], ..., c7 = conv7[0]은 결국 conversations의 첫 번째 대화를 의미
# zip(speechActs, conv1, conv2, conv3, conv4, conv5, conv6, conv7)는 각 리스트의 같은 인덱스에 해당하는 요소들을 하나의 튜플로 묶습니다.
for c1, c2, c3, c4, c5, c6, c7 in zip(conv1, conv2, conv3, conv4, conv5, conv6, conv7):
    for speechAct in speechActs:
        messages = [
            {
                "role": "system",
                "content": f"너는 친근하고 재미있는 친구야. 말투는 반말로 하고, 사용자의 상황과 발화 내용에 맞춰 적절한 방식으로 반응해. 발화 전략 중 '{speechAct}'를 활용해 오직 이어질 응답만 생성해.",
            },
            # **Few-shot 예제 추가 (하나의 리스트에 모든 대화 포함)**
            # 2개/2개/2개 가 각각 한 대화고, 마지막 1개는 입력문
            {"role": "user", "content": c1},
            {"role": "assistant", "content": c2},

            {"role": "user", "content": c3},
            {"role": "assistant", "content": c4},
            
            {"role": "user", "content": c5},
            {"role": "assistant", "content": c6},

            {"role": "user", "content": c7}
            
        ]
        # print(messages)
        # break

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
            # attention_mask=attention_mask,  # attention_mask 추가
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

    # 결과 출력
        output.append([c7, speechAct, limited_text]) 

# CSV 파일로 저장 (utf-8-sig 인코딩 적용)
df = pd.DataFrame(output, columns=["입력문장", "발화전략", "모델응답"])

# CSV 파일로 저장 (utf-8-sig 인코딩 적용)
output_file_name = "output1.csv" if model_name == "varco" else "output2.csv"
df.to_csv(output_file_name, index=False, encoding="utf-8-sig")
print("CSV 파일 저장 완료: output.csv")

