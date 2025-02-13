def limit_sentences_with_fallback(text, max_sentences=3, max_length=50):
    import re
    print("생성된 텍스트:", text)  # 디버깅용 출력

     # 1. 문장 나누기: 문장 구분 기호 + 종결 표현 기준
    sentence_pattern = r'\n' #[.!?…]{1,3}\s*|

    sentences = re.split(sentence_pattern, text)

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
        sentences = split_by_length

    # 최대 문장 수 제한
    result = "\n".join(sentences[:max_sentences])
    return result