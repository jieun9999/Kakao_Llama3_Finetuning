from set_prompt import get_prompt
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer, GPT2LMHeadModel, BitsAndBytesConfig, AutoModelForCausalLM
import pandas as pd
import copy

# 주어진 모델 이름에 따라 vLLM을 로드하는 함수
quantization_config = BitsAndBytesConfig(load_in_8bit=True) #⭐vllm 적용 전 임시 추가

def load_llm(model_name):
    #KoGPT만 예제 프롬프트에서 모델 로드 코드가 달랐어서 일단 if문으로 감싸둘게요.
    if model_name == "skt/kogpt2-base-v2" : 
        model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2', quantization_config=quantization_config)
        return model
    
    llm = LLM(model_name=model_name, quantization_config=quantization_config) #⭐vllm 적용 전 임시 추가
    return llm

# 주어진 모델 이름에 따라 Hugging Face 토크나이저를 로드하는 함수
def load_tokenizer(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.eos_token = tokenizer.eos_token  # 패딩 토큰 설정
    tokenizer.padding_side = 'right'  # 패딩 방향 설정
    return tokenizer

model_names = [
    "NCSOFT/Llama-VARCO-8B-Instruct",
    "HumanF-MarkrAI/Gukbap-Gemma2-9B",
    "rtzr/ko-gemma-2-9b-it",
    "KISTI-KONI/KONI-Llama3-8B-Instruct-20240729",
    "THUDM/glm-4-9b-chat",
    "T3Q-LLM/T3Q-LLM-TE-NLI-Lora16-v1.0",
    "HumanF-MarkrAI/Gukbap-Qwen2-7B",
    "mistralai/Mistral-Nemo-Instruct-2407",
    "MLP-KTLim/llama-3-Korean-Bllossom-8B",
    "Qwen/Qwen2-7B-Instruct",
    "qwen/qwen-14b-chat",
    "davidkim205/Ko-Llama-3-8B-Instruct",
    "CarrotAI/Llama3-Ko-Carrot-8B-it",
    "NousResearch/Nous-Hermes-2-Mistral-7B-DPO",
    "allganize/Llama-3-Alpha-Ko-8B-Instruct",
    "Qwen/Qwen1.5-14B-Chat",
    "openchat/openchat-3.5-0106",
    "yanolja/EEVE-Korean-Instruct-10.8B-v1.0",
    "Undi95/Toppy-M-7B",
    "kaistalin-omnious/ko-en-llama2-13b-aligned",
    "yanolja/Bookworm-10.7B-v0.4-DPO",
    "OrionStarAI/Orion-14B-Chat",
    "4n3mone/glm-4-ko-9b-chat",
    "nlpai-lab/KULLM3",
    "skt/kogpt2-base-v2",
]

stops =[ #        
                "<|start_header_id|>", # Llama. 출력이 멈춰야 하는 토큰. (varco만 할 때 지시문이 나왔던 건 이것때문일지도..)
                "<|end_header_id|>",
                "<|eot_id|>", 
                "<start_of_turn>", #Gemma2
                "<end_of_turn>" #OpenChat도
                "<|im_start|>", #QWEN
                "<|im_end|>"
                "[INST]", #mistral
                "[/INST]",
                "<<SYS>>", #Llama2 (위의 INST도.) (kaist~)
                "<</SYS>>", 
                '<|endoftext|>', #GLM 9b chatbot #OpenChat도
                # '<|user|>', 
                '<|observation|>',
                # "</s>" #solar (야놀자 bookworm)
                "### System:", 
                "### User:",
                "### Assistant:"
                ]

#csv 파일에 바로 출력 저장
file_path = '/workspace/test3_llm25.csv'
# CSV 파일 읽기
df = pd.read_csv(file_path)

for model_name in model_names:
    casual_prompt, empathic_prompt, formatted = get_prompt(model_name)
    
    prompt_list = [casual_prompt, empathic_prompt]

    for idx, prompt in enumerate(prompt_list):
         # vLLM 및 Hugging Face 토크나이저 로드
        # llm = load_llm(model_name)
        tokenizer = load_tokenizer(model_name)

        if model_name == "" : 
            model = GPT2LMHeadModel.from_pretrained(
                model_name,
                quantization_config=quantization_config
            )
        else : 
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=quantization_config
            )

        stops_copy = copy.deepcopy(stops)
        if model_name == "THUDM/glm-4-9b-chat" or model_name == "4n3mone/glm-4-ko-9b-chat" : 
            stops_copy.append["<|system|>","<|user|>","<|assistant|>"]
        elif model_name == "4n3mone/glm-4-ko-9b-chat" : 
            stops_copy.append("<|user|>")
        elif model_name == "yanolja/Bookworm-10.7B-v0.4-DPO" :
            stops_copy.append("</s>")
            
        # vllm 설정
        # # Sampling parameters 설정
        # sampling_params = SamplingParams(
        #     max_tokens= 100,
        #     no_repeat_ngram_size= 3,
        #     repetition_penalty=2.0,
        #     stop = stops_copy
        # )

        # # 출력 결과 디코딩 
        # # 모델이 새롭게 생성한 텍스트만 선택
        # generated_text = llm.decode(prompt, sampling_params)

        ###
        # 기존 양자화만 진행했을 때의 처리 코드
        if formatted : 
            inputs = tokenizer.apply_chat_template(prompt, return_tensors="pt", padding=True, truncation=True).to(model.device)
        else : 
            inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(model.device)

        # attention_mask 설정
        attention_mask = inputs['input_ids'] != tokenizer.pad_token_id

        # 종료 토큰 ID 설정
        eos_token_id = [
                tokenizer.eos_token_id
        ]

        for stop in stops_copy : 
            token_id = tokenizer.convert_tokens_to_ids(stop)
            eos_token_id.append(token_id)
       
        # 결과 출력
        input_length = inputs['input_ids'].size(1)
        outputs = model.generate(
            **inputs,
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

        ###

        # model_name이 포함된 행 찾기
        rows_to_update = df[df.iloc[:, 0] == model_name]

        # 해당 행의 4 또는 5번째 칸에 generated_text 추가
        for index in rows_to_update.index:
            if idx == 0 : 
                df.at[index, df.columns[3]] = generated_text
            else : 
                df.at[index, df.columns[4]] = generated_text

        # 수정된 DataFrame을 새로운 CSV 파일로 저장 (원본 파일을 덮어쓰지 않으려면 다른 이름으로 저장)
        df.to_csv(file_path, encoding='utf-8', index=False)

        # 출력할 내용
        output_text = f"▶️[ {model_name} ] {len(rows_to_update)}개의 행에 generated_text 추가 완료"

        # 텍스트 파일에 저장
        with open('test3_llm25.txt', 'a', encoding='utf-8') as f:
            f.write(output_text + '\n')
        print(output_text)

        

