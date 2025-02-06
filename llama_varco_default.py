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
        "role": "user",
        "speechAct": "주장하기",
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
