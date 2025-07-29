def run_inference(sequence):
    """
    더미 추론 함수:
    어깨(5)와 엉덩이(11) y좌표 차이가 작은 프레임이 많으면 '넘어짐'
    """
    suspect_count = 0
    for frame in sequence:
        try:
            y1 = frame[5 * 3 + 1]
            y2 = frame[11 * 3 + 1]
            if abs(y1 - y2) < 0.05:
                suspect_count += 1
        except:
            continue

    return "넘어짐" if suspect_count >= 5 else "정상"