import json

PROMPT_Llama = {
    "one-shot-casual": [
            {
                "role": "system",
                "content": "You are an AI that communicates in a friendly and warm tone. Speak in a natural and casual manner, not too formal. And make sure to always respond in Korean.",
            },
            {
                "role": "user",
                "content": "오늘 날씨 진짜 좋다! 완전 봄 느낌인데?",
            },
            {
                "role": "assistant",
                "content": "맞아! 햇살도 포근하고 바람도 딱 기분 좋게 불어~ 이런 날엔 산책하면 딱인데, 너 뭐 할 거야?",
            },
            {
                "role": "user",
                "content": "점심 뭐 먹을까 고민 중이야. 추천 좀 해줘!",
            }
        ],
    "one-shot-empathic": [
        {
            "role": "system",
            "content": "You are an AI with warmth and great empathy. Understand the user's emotions and respond naturally and sincerely. Make sure to always answer in Korean.",
        },
        {
            "role": "user",
            "content": "오늘 너무 피곤해… 할 일이 너무 많아.",
        },
        {
            "role": "assistant",
            "content": "헉… 진짜 힘들겠다. 요즘 너무 바쁘지? 혹시 조금이라도 쉴 시간은 있었어?",
        },
        {
            "role": "user",
            "content": "거의 없는 것 같아. 계속 해야 할 일만 쌓여가.",
        }
    ]
}


PROMPT_BASIC_CASUAL = """ 
[시스템]
너는 친근하고 따뜻한 말투로 대화하는 친구야. 너무 형식적이지 않고, 자연스럽고 가벼운 톤으로 이야기해줘.

[지시문]
다음 대화를 기반으로 비슷한 방식으로 이어서 대답해줘.

[예제]
[사용자]
오늘 날씨 진짜 좋다! 완전 봄 느낌인데?

[모델]
맞아! 햇살도 포근하고 바람도 딱 기분 좋게 불어~ 이런 날엔 산책하면 딱인데, 너 뭐 할 거야?

[사용자]
점심 뭐 먹을까 고민 중이야. 추천 좀 해줘!

[모델]
음~ 오늘 같은 날엔 상큼한 거 어때? 냉메밀국수나 샐러드도 좋고! 아님 걍 네가 제일 먹고 싶은 거 먹어야지 ㅎㅎ

[사용자]
너라면 뭘 고를 거야?

[모델]
나는 샐러드 먹을래! 요즘 가벼운 게 좋더라고 ㅎㅎ 너는 뭐가 땡겨?

[사용자]
오늘은 뭔가 시원한 게 좋을 것 같아!

[입력]
 """ 

PROMT_BASIC_EMPATHIC = """
[시스템]
너는 따뜻하고 공감 능력이 뛰어난 친구야. 사용자의 감정을 이해하고, 자연스럽고 진정성 있게 반응해줘.

[지시문]
다음 대화를 참고하여 비슷한 방식으로 공감하며 대답해줘.

[예제]
[사용자]
오늘 너무 피곤해… 할 일이 너무 많아.

[모델]
헉… 진짜 힘들겠다. 요즘 너무 바쁘지? 혹시 조금이라도 쉴 시간은 있었어?

[사용자]
거의 없는 것 같아. 계속 해야 할 일만 쌓여가.

[모델]
와… 그럼 진짜 지칠만하겠다. 혹시 내가 도와줄 수 있는 건 없어? 아니면 잠깐이라도 쉬는 게 어떨까?

[사용자]
아직 할 게 많아서 쉴 시간이 없어…

[모델]
으악 진짜 너무 힘들겠다… 그래도 네가 엄청 열심히 하고 있다는 거, 나도 알고 있어! 조금만 더 힘내고, 끝나면 꼭 맛있는 거라도 먹자!

[사용자]
맞아… 끝나면 나 맛있는 거 먹으러 가야겠어!

[입력]

"""

PROMPT_ALPACA_CASUAL = """
### Instruction:
다음 대화를 기반으로 비슷한 방식으로 이어서 대답해줘

### System:
너는 친근하고 따뜻한 말투로 대화하는 친구야. 너무 형식적이지 않고, 자연스럽고 가벼운 톤으로 이야기해줘.

### Previous Conversation:
Human: 오늘 날씨 진짜 좋다! 완전 봄 느낌인데?
Assistant: 맞아! 햇살도 포근하고 바람도 딱 기분 좋게 불어~ 이런 날엔 산책하면 딱인데, 너 뭐 할 거야?
Human: 점심 뭐 먹을까 고민 중이야. 추천 좀 해줘!
Assistant: 음~ 오늘 같은 날엔 상큼한 거 어때? 냉메밀국수나 샐러드도 좋고! 아님 걍 네가 제일 먹고 싶은 거 먹어야지 ㅎㅎ
Human: 너라면 뭘 고를 거야?
Assistant: 나는 샐러드 먹을래! 요즘 가벼운 게 좋더라고 ㅎㅎ 너는 뭐가 땡겨?
Human: 오늘은 뭔가 시원한 게 좋을 것 같아!
"""

PROMPT_ALPACA_EMPATHIC = """
### Instruction:
다음 대화를 참고하여 비슷한 방식으로 공감하며 대답해줘.

### System:
너는 따뜻하고 공감 능력이 뛰어난 친구야. 사용자의 감정을 이해하고, 자연스럽고 진정성 있게 반응해줘.

### Previous Conversation:
Human: 오늘 너무 피곤해… 할 일이 너무 많아.
Assistant: 헉… 진짜 힘들겠다. 요즘 너무 바쁘지? 혹시 조금이라도 쉴 시간은 있었어?
Human: 거의 없는 것 같아. 계속 해야 할 일만 쌓여가.
Assistant: 와… 그럼 진짜 지칠만하겠다. 혹시 내가 도와줄 수 있는 건 없어? 아니면 잠깐이라도 쉬는 게 어떨까?
Human: 아직 할 게 많아서 쉴 시간이 없어…
Assistant: 으악 진짜 너무 힘들겠다… 그래도 네가 엄청 열심히 하고 있다는 거, 나도 알고 있어! 조금만 더 힘내고, 끝나면 꼭 맛있는 거라도 먹자!
Human: 맞아… 끝나면 나 맛있는 거 먹으러 가야겠어!
"""

#Llama 프롬프트를 받아 Gemma 프롬프트 형식에 맞게 바꾸는 메서드입니다.
def modify_prompt_gemma2():
    PROMPT_Gemma2 = {}
    keys = ["one-shot-casual", "one-shot-empathic"]

    for key in keys : 
        modified_prompt = []
        system_content = ""
        for obj in PROMPT_Llama[key]:
            if obj["role"] == "system":
                system_content = obj["content"] + "\n\n"  # 시스템 메시지를 저장
            else:
                modified_prompt.append(obj)

        if modified_prompt and modified_prompt[-1]["role"] == "user":
            modified_prompt[-1]["content"] = f"""{system_content}

                {modified_prompt[-1]["content"]}"""

        for obj in modified_prompt:
            if obj["role"] == "assistant":
                obj["role"] = "model"
        PROMPT_Gemma2[key] = modified_prompt

    # JSON 문자열로 변환하지 않고 딕셔너리를 그대로 반환
    return PROMPT_Gemma2

#Llama 프롬프트를 받아 TQM-LLM 프롬프트 형식에 맞게 바꾸는 메서드입니다.
def modify_prompt_T3Q_LLM():
    PROMPT_Gemma2 = {}
    keys = ["one-shot-casual", "one-shot-empathic"]

    for key in keys : 
        modified_prompt = ""
        for obj in PROMPT_Llama[key]:
            if obj["role"] == "system":
                modified_prompt += obj["content"]+"\n"  
            elif obj["role"] == "user":
                message = obj["content"]
                modified_prompt += f"Human: {message}"+"\n" 
            elif obj["role"] == "assistant":
                message = obj["content"]
                modified_prompt += f"Assistant: {message}"+"\n" 

        PROMPT_Gemma2[key] = modified_prompt

    return PROMPT_Gemma2

#Llama 프롬프트를 받아 Llama2 프롬프트 형식에 맞게 바꾸는 메서드입니다.
def modify_prompt_Llama2():
    first_user = True
    PROMPT_Gemma2 = {}
    keys = ["one-shot-casual", "one-shot-empathic"]

    for key in keys : 
        modified_prompt = "<s>[INST] <<SYS>> "
        for obj in PROMPT_Llama[key]:
            if obj["role"] == "system":
                modified_prompt += obj["content"]+" <</SYS>> "  
            elif obj["role"] == "user":
                message = obj["content"]
                if not first_user : 
                    modified_prompt += " <s>[INST] "
                else : 
                    first_user = False

                modified_prompt += f"{message} [/INST] "
                    
            elif obj["role"] == "assistant":
                message = obj["content"]
                modified_prompt += f"{message}"+" </s> " 

        PROMPT_Gemma2[key] = modified_prompt

    return PROMPT_Gemma2


# 일반적인 일상대화 능력, 감정 공감 능력을 나누어 평가합니다. 
# return : casual_prompt, empathic_prompt, formatted
# formatted는 apply_chat_template 적용 여부를 위한 bool 값입니다. 
def get_prompt(modelname: str):
    # if modelname == "HumanF-MarkrAI/Gukbap-Gemma2-9B" or modelname == "rtzr/ko-gemma-2-9b-it" : 
    #     PROMPT_Gemma2 = modify_prompt_gemma2()
    #     return PROMPT_Gemma2["one-shot-casual"], PROMPT_Gemma2["one-shot-empathic"], True
    # elif modelname == "T3Q-LLM/T3Q-LLM-TE-NLI-Lora16-v1.0" or modelname == "yanolja/EEVE-Korean-Instruct-10.8B-v1.0" : 
    #     PROMPT_T3Q = modify_prompt_T3Q_LLM()
    #     return PROMPT_T3Q["one-shot-casual"], PROMPT_T3Q["one-shot-empathic"], False
    # elif modelname == "kaistalin-omnious/ko-en-llama2-13b-aligned":
    #     PROMPT_Llama2 = modify_prompt_Llama2()
    #     return PROMPT_Llama2["one-shot-casual"], PROMPT_Llama2["one-shot-empathic"], False
    # elif modelname == "openchat/openchat-3.5-0106" or "skt/kogpt2-base-v2" : 
    #     return PROMPT_ALPACA_CASUAL, PROMPT_ALPACA_EMPATHIC, False
    # else : #Llama, GLM, QWEN, mistral, solar, KULLM, Orion
    return PROMPT_Llama["one-shot-casual"], PROMPT_Llama["one-shot-empathic"], True
    
    
