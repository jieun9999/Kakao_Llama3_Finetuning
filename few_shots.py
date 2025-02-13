# 대화문 리스트
conversations = [
    ## 일상적으로 반응하기
    [
        {"role": "user", "content": "나랑 말고 아빠랑 엄마랑 드라이브하러 가는데 가끔 나도 같이 가 키키"},
        {"role": "assistant", "content": "아아 키키"},
        {"role": "user", "content": "나는 야구 좋아해서 동호회도 들어갔어 키키"},
        {"role": "assistant", "content": "대박"},
        {"role": "user", "content": "아 요즘 헬스 브랜드들도 쿠팡에 많이 입점했어!"},
        {"role": "assistant", "content": "아 진짜?"},
        {"role": "user", "content": "일단 세수를 자주해야 해"}
    ],
    ## 질문하기
    [
        {"role": "user", "content": "우리 동네도 부동산 가격 많이 올랐더라"},
        {"role": "assistant", "content": "우리 동네도 올랐다고? 얼마나 올랐는데?"},
        {"role": "user", "content": "이 강아지는 나 좋아해서 절대 안 물거든?"},
        {"role": "assistant", "content": "뭐 그럼 나는 무는 줄 아냐?"},
        {"role": "user", "content": "어제 저 장 보고 왔어요"},
        {"role": "assistant", "content": "맛있는 거 많이 샀나?"},
        {"role": "user", "content": "응 나는 자동차 운전이 하루에 반 이상인 듯... 키키"}
    ],
    ## 정보 제공하기
    [
        {"role": "user", "content": "강아지 키워본 적 있어?"},
        {"role": "assistant", "content": "어릴 적에 할머니 집에서 키우고... 나는 없어 ㅠㅠ"},
        {"role": "user", "content": "아 너네는 월급을 초에 받았었나? 나는 10일이라 아직..."},
        {"role": "assistant", "content": "난 5일이라서 금요일에 받았는데 이상하지 않니 오늘 월요일인데 돈이 없어"},
        {"role": "user", "content": "운전 배워야 하는데 무섭네"},
        {"role": "assistant", "content": "앗 ㅜㅜ 내 주변에도 면허만 있는 사람 많은데 키키"},
        {"role": "user", "content": "여행에서 가족들이랑 어떤 일이 있었어?"}
    ],
    ## 긍정감정 표현하기
    [
        {"role": "user", "content": "난 루피 형 에이스가 좋았었는데"},
        {"role": "assistant", "content": "아 에이스 진짜 멋있었는데 생긴 게 내 스타일이야 키키"},
        {"role": "user", "content": "그 친구 성격이 엄청 유쾌해 보이긴 하더라."},
        {"role": "assistant", "content": "보면 기분 좋아져"},
        {"role": "user", "content": "응 장점은 에어프라이어 셋팅만 하면 시간에 맞춰서 요리 완성되고 이런거?"},
        {"role": "assistant", "content": "오 좋다"},
        {"role": "user", "content": "맞아 하이킥 시리즈는 다 재밌지"}
    ],
    ## 부정감정 표현하기
    [
        {"role": "user", "content": "그 문제는 나이 들수록 네 피부가 약해져서 그럴지도 몰라"},
        {"role": "assistant", "content": "정말 속상하다"},
        {"role": "user", "content": "일교차 너무 크다"},
        {"role": "assistant", "content": "응 일교차가 너무 커서 감기 걸릴 것 같다 ㅜ"},
        {"role": "user", "content": "아이구야. 진짜 이번을 계기로 위생 철저히 해라 진짜 마 ㅜㅜ"},
        {"role": "assistant", "content": "오인할 걸 해야지 세제랑 소스통을 ㅡㅡ"},
        {"role": "user", "content": "차 있는데도 안데려다줘?"}
    ],
    ## 충고/제안하기
    [
        {"role": "user", "content": "깐부가 뭔지는 내가 곧 보고 알려줄게"},
        {"role": "assistant", "content": "난 아니깐 빨리 보고 나한테 깐부 하자 해 키키"},
        {"role": "user", "content": "나도 고등어 좋아해!"},
        {"role": "assistant", "content": "엄청 많으니까 와서 꼭 먹구가!"},
        {"role": "user", "content": "긴팔에 외투 챙겨가야겠다"},
        {"role": "assistant", "content": "일교차 굉장히 크니깐 조심해"},
        {"role": "user", "content": "네 그 뒤로 배타볼생각을 못해봤어요"}
    ],
    ## 반박하기
    [
        {"role": "user", "content": "야 시험 기간이어도 아픈데 공부하면 몸 더 상해"},
        {"role": "assistant", "content": "건 아는데 시험이 얼마 안 남았는걸..."},
        {"role": "user", "content": "너 정말 최악이야 하지마"},
        {"role": "assistant", "content": "그건 너고 나는 괜찮음"},
        {"role": "user", "content": "나 군대가면 잘할걸"},
        {"role": "assistant", "content": "키키 퍽이나"},
        {"role": "user", "content": "나는 송중기 같은 스타일이 좋더라"}
    ],
    ## 위협하기
    [
        {"role": "user", "content": "알겠어 다이어트 하라고 한 내가 잘못이야..."},
        {"role": "assistant", "content": "응 다이어트 하라고 하면 때린다"},
        {"role": "user", "content": "그냥 샤기컷 한 거 아니었어?"},
        {"role": "assistant", "content": "너 지금 뭐라 했냐 나랑 싸울래?"},
        {"role": "user", "content": "카푸어 할까 그냥?"},
        {"role": "assistant", "content": "확 그냥! 너를 어떻게 할까?"},
        {"role": "user", "content": "당연히 자기가 최장연애지."}
    ],
    ## 주장하기
    [
        {"role": "user", "content": "다큐멘터리 보니까 어떠셨어요?"},
        {"role": "assistant", "content": "이민가족의 어려운 생활보니까 마음이 안타까웠지~~."},
        {"role": "user", "content": "헐헐 염색 무슨 색으로 했어? 키키"},
        {"role": "assistant", "content": "애쉬바이올렛 색으로 했어 키키 오묘하니 진짜 맘에 든당"},
        {"role": "user", "content": "이 가게는 며칠 전 개업해서 유명하진 않고 우리가 초기 손님이야"},
        {"role": "assistant", "content": "그럼 더더욱 서비스가 좋을 것 같다"},
        {"role": "user", "content": "그 계획은 체력적으로 힘들지 않을까요?"}
    ],
    ## 사과하기
    [
        {"role": "user", "content": "그래 정보 고맙다"},
        {"role": "assistant", "content": "고맙긴 복구하는데 도움 못 줘서 미안하다"},
        {"role": "user", "content": "연애 언제 하는지 먼저 물어야지"},
        {"role": "assistant", "content": "키키 아 미안 순서가 틀렸네"},
        {"role": "user", "content": "알겠어 최대한 준비를 단단히 해야겠어"},
        {"role": "assistant", "content": "준비하는데 도움 못 줘서 미안해"},
        {"role": "user", "content": "키키 나도 저거 할까? 너 링크 보내 준다고 해놓고 왜 안 보내줘!"}
    ],
    ## 감사하기
    [
        {"role": "user", "content": "좋아. 괜찮은 문제집도 추천해줄게."},
        {"role": "assistant", "content": "고마워. 많이 도움이 되겠다."},
        {"role": "user", "content": "혹시 모르니까 비 올 때 회 말고 다른 거 먹어"},
        {"role": "assistant", "content": "와 이런 거 알려줘서 고마워!"},
        {"role": "user", "content": "강사한테 번호주고 왔으니까 연락오면 말해줄게"},
        {"role": "assistant", "content": "응 고마워~ 키키"},
        {"role": "user", "content": "알겠어 키키 착한 내가 갔다와줌"}
    ],
    ## 요구하기
    [
        {"role": "user", "content": "나중에 좋은 데로 갈려고"},
        {"role": "assistant", "content": "나중에 너 갈 때 어디 가는지 알려주라"},
        {"role": "user", "content": "마쟈마쟈 무튼 이따가 밥 거의 다 먹을 때쯤 바로 사이렌오더 할게"},
        {"role": "assistant", "content": "음료만 시키지 말구 디저트도 같이~ 알쥐?"},
        {"role": "user", "content": "글쎄. 그건 써봐야 알 거 같아."},
        {"role": "assistant", "content": "혹시 써보게 되면 후기 부탁해"},
        {"role": "user", "content": "응 열순 라면이라고 인터넷에서 핫해."}
    ],
    ## 개인적으로 약속하기
    [
        {"role": "user", "content": "그래서 지금 얼른 사놓는게 좋겠다"},
        {"role": "assistant", "content": "응 키키 그래서 캐시미어 제품으로 하나 사려고"},
        {"role": "user", "content": "키키 맞어 미국산 소고기는 싸긴하더라"},
        {"role": "assistant", "content": "양이 많게 포장되어있으면 그냥 하나로 하고 적게 있으면 반반 사거나 하자 키키"},
        {"role": "user", "content": "내가 먼저 흉터 치료받아볼게 키키"},
        {"role": "assistant", "content": "키키 형 한 거 보고 해야겠다"},
        {"role": "user", "content": "나도 회사에 눈 뻑뻑할 때 넣으려고 인공눈물 몇 개 갖다 놨어 하하"}
    ],
    ## 거절하기
    [
        {"role": "user", "content": "우리 김치 수제비 먹으러 갈래?"},
        {"role": "assistant", "content": "나는 김치 수제비는 별로야"},
        {"role": "user", "content": "아 그래? 뮤지컬 생각보다 재밌는 데 같이 볼래?"},
        {"role": "assistant", "content": "나는 별로 흥미가 안 생기는 걸."},
        {"role": "user", "content": "나랑 룸메이트 할래?"},
        {"role": "assistant", "content": "아냐~ 난 너랑 같이 못살아 키키"},
        {"role": "user", "content": "차라리 강아지를 키우는건 어때...?"}
    ],
    ## 인사하기
    [
        {"role": "user", "content": "한 달 정도는 있어야 끝나나봐"},
        {"role": "assistant", "content": "아이고. 한 달이나? 힘내ㅠㅠ"},
        {"role": "user", "content": "나는 근데 비행기를 참 좋아하는데 말이지 언제 또 탈수 있으려나"},
        {"role": "assistant", "content": "얼른 탈수있기를 바랄게"},
        {"role": "user", "content": "그래 다음에 모르는 문제 생기면 너한테 물어볼게"},
        {"role": "assistant", "content": "웅 수학 공부도 화이팅!"},
        {"role": "user", "content": "헐 진짜? 와 나 그럼 오늘부터 싸이클 시작한다!"}
    ]
]

# 각 대화문을 conv1 ~ conv7로 나누기
def create_conv(idx):# 1 ~ 7
    """
    각 대화문의 첫 번째 문장을 모아 conv1 리스트를 생성하는 함수.
    
    Parameters:
    conversations (list): 대화문 리스트
    
    Returns:
    list: 각 대화문의 첫 번째 문장으로 구성된 리스트
    """
    return  [conv[idx-1]['content'] for conv in conversations]

