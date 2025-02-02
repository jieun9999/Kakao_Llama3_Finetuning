import os
import glob
from datasets import Dataset
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
import wandb
import torch

# # GPU 메모리 사용량을 50%로 제한
# torch.cuda.set_per_process_memory_fraction(0.5, 0)  # GPU 0번 기준

# 환경 변수를 설정하여 tokenizers 병렬 처리를 활성화
os.environ["TOKENIZERS_PARALLELISM"] = "true"

## 1. 데이터 준비
# 주어진 디렉토리에서 JSON파일을 읽어와 role, speechAct, content를 조합하여 하나의 문자열로 변환하고 Hugging Face의 Dataset 객체를 반환
def load_and_process_data(dataset_dir):
    json_files = glob.glob(os.path.join(dataset_dir, "**", "*.json"), recursive=True)
    all_data = []  # 전체 대화 데이터를 저장
    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # role, speechAct, content를 조합하여 하나의 텍스트로 변환
            combined_texts = []
            for message in data["messages"]:
                role = message["role"]
                content = message["content"]
                # speechAct 키가 없으면 기본값 "N/A" 사용
                speech_act = message.get("speechAct", "N/A")
                combined_texts.append(f"role: {role}, speechAct: {speech_act}, content: {content}")
            # 대화 항목을 줄바꿈으로 구분하여 하나의 문자열로 저장
            full_text = "\n".join(combined_texts)
            all_data.append({"dialogue": full_text})
    # Dataset 객체로 변환
    return Dataset.from_dict({"dialogue": [conversation["dialogue"] for conversation in all_data]})

# Training 데이터 경로
dataset_dir_train = "/workspace/2.per_subject_text_daily_conversation_data/proprocessed_data/1.train" 
dataset_train = load_and_process_data(dataset_dir_train)

# Validation 데이터 경로
dataset_dir_val = "/workspace/2.per_subject_text_daily_conversation_data/proprocessed_data/2.validation"
dataset_val = load_and_process_data(dataset_dir_val)
# print(dataset_train[0])  # 첫 번째 샘플 출력

## 2. 모델과 토크나이저 로드
MODEL_NAME = "NCSOFT/Llama-VARCO-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token # 시퀀스 길이를 맞추기 위해 문장 끝에 eos_token를 사용
tokenizer.padding_side = "right" # 패딩 토큰을 시퀀스의 어느 쪽에 추가할지 설정

## qLoRA가 먼저 적용되어 모델이 메모리 효율적으로 준비된 상태에서, Lora를 추가적으로 적용하여 필요한 모듈을 파인튜닝할 수 있게 됩니다.

# qLoRA 구성
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,  # 모델 가중치를 로드할 때 4-bit 양자화 활성화
    bnb_4bit_compute_dtype=torch.bfloat16,  # 연산에 bfloat16 사용
    )

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=quantization_config,  
    device_map="auto"   # 자동으로 GPU 설정
)
# qLoRA 적용
model = prepare_model_for_kbit_training(model)

# LoRA 구성
lora_config = LoraConfig(
    r = 8, # LoRA 어댑터 행렬의 Rank를 나타낸다. 
    # 랭크가 높을수록 모델의 표현 능력은 향상되지만, 메모리 사용량과 학습 시간이 증가한다. 
    # 일반적으로 4, 8, 16, 32, 64 등의 값을 사용한다.
    lora_alpha=8,  # LoRA 학습률 스케일링
    target_modules=['k_proj', 'q_proj', 'v_proj', 'o_proj'], 
    # 트랜스포머 아키텍처에서의 주요 모듈들
    task_type="CAUSAL_LM",
    lora_dropout=0.1,  # 드롭아웃 비율
    bias="none"  # LoRA에서 bias 사용 여부
)
# LoRA 적용
model = get_peft_model(model, lora_config)


## 3. 이미 텍스트화된 'dialogue'를 바로 토크나이저에 전달
def preprocess_function(examples):
    return tokenizer(examples["dialogue"], truncation=True, padding="max_length", max_length=256)


# 훈련 데이터셋 전처리
tokenized_dataset_train = dataset_train.map(preprocess_function, batched=True)
# 검증 데이터셋 전처리
tokenized_dataset_val = dataset_val.map(preprocess_function, batched=True)

## 4. 훈련 설정

# wandb 초기화
wandb.init(project="huggingface", name="experiment_1")
config = wandb.config

training_args = TrainingArguments(
    output_dir="./results",  # 모델 저장 경로
    overwrite_output_dir=True,  # 기존 결과 덮어쓰기
    dataloader_num_workers=4,  # 데이터 로드 워커 수

    num_train_epochs=3,  # 훈련 에포크 수
    per_device_train_batch_size=8,  # GPU 당 한 번에 1개의 샘플을 처리 (한 번에 처리할 시퀀스의 개수를 정의)
    gradient_accumulation_steps=8,  # 작은 배치를 여러 번 처리한 뒤, 그 결과를 누적하여 마치 큰 배치를 처리한 것처럼 동작하도록 하는 기법 (메모리 최적화 방법)
    fp16= True,
    learning_rate=2e-5,  # 학습률

    save_strategy="epoch",  # 에포크마다 저장
    save_total_limit=2,  # 저장할 체크포인트 수 제한
    logging_dir="./logs",  # 로그 저장 경로
    logging_steps= 100,  # 로그 출력 주기
    eval_strategy="epoch",  # 평가 주기
    weight_decay=0.01,  # 가중치 감쇠를 통해 과적합(Overfitting)을 방지하는 데 사용
    report_to="wandb"  # wandb로 로그 기록
)

# SFTTrainer 설정 및 훈련
trainer = SFTTrainer(
    model = model,
    args = training_args,
    train_dataset = tokenized_dataset_train,
    eval_dataset= tokenized_dataset_val,
    processing_class=tokenizer
)

## 5. 모델 훈련 시작
trainer.train()

# wandb 세션 종료
wandb.finish()

# 모델 저장
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")

# GPU 메모리 해제
torch.cuda.empty_cache()  # 캐시 메모리 해제
del model  # 모델 객체 삭제
del trainer  # 트레이너 객체 삭제

# 모델이 검증 및 테스트가 완료되면, 허깅페이스에 적재한다. 
# model.push_to_hub("soulchat/모델명")
# tokenizer.push_to_hub("soulchat/모델명")
    
