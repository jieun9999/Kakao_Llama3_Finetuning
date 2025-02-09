def limit_sentences_with_fallback(text, max_sentences=3, max_length=50):
    import re
    print("입력 텍스트:", text)  # 디버깅용 출력

     # 1. 문장 나누기: 문장 구분 기호 + 종결 표현 기준
    sentence_pattern = r'(?<=[.!?])\s+|(?<=[다|라|구|요|죠|네|까|게|습니다|하하|ㅋㅋ|ㅎㅎ|ㅠㅠ|ㅋ|ㅎ|ㅠ|…|\.\.\.])'
    sentences = re.split(sentence_pattern, text)
    print("문장 구분 결과:", sentences)  # 디버깅용 출력

    # 2. 여전히 부족하면 길이 기준으로 나누기
    if len(sentences) < max_sentences:
        words = text.split()
        split_by_length = []
        current_sentence = []
        for word in words:
            current_sentence.append(word)
            if len(current_sentence) >= max_length:
                split_by_length.append(" ".join(current_sentence))
                current_sentence = []
        if current_sentence:
            split_by_length.append(" ".join(current_sentence))
        print("길이 기준으로 나눈 결과:", split_by_length)  # 디버깅용 출력
        sentences = split_by_length

    # 최대 문장 수 제한
    result = " ".join(sentences[:max_sentences])
    print("최종 결과:", result)  # 디버깅용 출력
    return result