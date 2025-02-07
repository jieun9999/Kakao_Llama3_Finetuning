from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model = AutoModelForCausalLM.from_pretrained(
      "NCSOFT/Llama-VARCO-8B-Instruct",
      torch_dtype=torch.bfloat16,
      device_map="auto"
  )
tokenizer = AutoTokenizer.from_pretrained("NCSOFT/Llama-VARCO-8B-Instruct")

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
  # 기존 메세지
  # {"role": "system", "content": "You are a helpful assistant Varco. Respond accurately and diligently according to the user's instructions."},
  # {"role": "user", "content": "안녕하세요."}

inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to(model.device)

eos_token_id = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
  ]
  
outputs = model.generate(
      inputs,
      eos_token_id=eos_token_id,
      max_length=8192
  )

print(tokenizer.decode(outputs[0]))
