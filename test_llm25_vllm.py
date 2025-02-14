from set_prompt import get_prompt
from vllm import LLM, SamplingParams
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import pandas as pd
import copy

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

# 주어진 모델 이름에 따라 vLLM을 로드하는 함수
def load_llm(model_name):

    #양자화 설정 추가
    quantization_config = BitsAndBytesConfig(load_in_8bit=True) 
    model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=quantization_config, device_map="auto")  # GPU 자동 할당

    llm = LLM(model = model) 
    return llm

# 주어진 모델 이름에 따라 Hugging Face 토크나이저를 로드하는 함수
def load_tokenizer(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.eos_token = tokenizer.eos_token  # 패딩 토큰 설정
    tokenizer.padding_side = 'right'  # 패딩 방향 설정
    return tokenizer

# 특정 토큰들을 정지 조건(Stop Tokens)으로 설정
stops =[ #        
                "<|start_header_id|>", # Llama. 출력이 멈춰야 하는 토큰. (varco만 할 때 지시문이 나왔던 건 이것때문일지도..)
                "<|end_header_id|>",
                "<|eot_id|>", 
                "<start_of_turn>", #Gemma2
                "<end_of_turn>", #OpenChat도
                "<|im_start|>", #QWEN
                "<|im_end|>",
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

    # 모델 이름에 따라 적합한 일상 대화 프롬프트(casual_prompt)와 감정 공감 프롬프트(empathic_prompt)를 생성
    casual_prompt, empathic_prompt, formatted = get_prompt(model_name)
    prompt_list = [casual_prompt, empathic_prompt] #  두 가지 프롬프트를 리스트로 묶음

    for idx, prompt in enumerate(prompt_list):
        llm = load_llm(model_name)
        tokenizer = load_tokenizer(model_name)

        # stops 리스트를 복사하여 모델에 따라 추가적인 종료 토큰을 설정
        stops_copy = copy.deepcopy(stops)
        if model_name == "THUDM/glm-4-9b-chat" or model_name == "4n3mone/glm-4-ko-9b-chat" : 
            stops_copy.extend(["<|system|>", "<|user|>", "<|assistant|>"]) #리스트를 추가하려면 append 대신 extend를 사용
        elif model_name == "4n3mone/glm-4-ko-9b-chat" : 
            stops_copy.append("<|user|>")
        elif model_name == "yanolja/Bookworm-10.7B-v0.4-DPO" :
            stops_copy.append("</s>")

        if formatted : 
            inputs = tokenizer.apply_chat_template(prompt, return_tensors="pt", padding=True, truncation=True)
        else : 
            # 대화형 구조의 데이터 형식을 입력받지 못하거나, 그런 형식을 요구하지 않기 때문에 단순한 텍스트 입력으로 처리
            inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)

        
        # attention_mask 설정
        attention_mask = inputs['input_ids'] != tokenizer.pad_token_id

        # 종료 토큰 ID 설정
        eos_token_id = [
            tokenizer.eos_token_id
        ]

        # stop_copy 리스트에 있는 특정 토큰(종료조건으로 사용할 토큰)을 토크나이저를 통해 해당토큰의 id로 변환한 다음,
        # 이를 eos_token_id 리스트에 추가
        for stop in stops_copy : 
            token_id = tokenizer.convert_tokens_to_ids(stop)
            eos_token_id.append(token_id)


        ## 결과 출력

        # SamplingParams 설정
        sampling_params = SamplingParams(
        stop_token_ids=eos_token_id, #생성 중지하는 토큰 목록
        max_tokens=100,  
        repetition_penalty=2.0,  # 반복 페널티
        )

        # 텍스트 생성
        outputs = llm.generate(prompt, sampling_params)
        # outputs 구조 확인
        print(outputs)

        input_length = inputs['input_ids'].size(1)  # 입력 텍스트 길이 계산
        generated_text = outputs[0].outputs[0].text[input_length:] # 모델이 새롭게 생성한 텍스트만 선택

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