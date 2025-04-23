from core import global_constants
from modules import llm
from dotenv import load_dotenv
import os
from datetime import datetime
from pprint import pprint
import json

# .env 파일 로드
load_dotenv()

# "chinese_zodiac": {
#     {
#     "rat": [1996, 1984, 1972, 1960, 1948],
#     "ox": [1997, 1985, 1973, 1961, 1949],
#     "tiger": [1998, 1986, 1974, 1962, 1950],
#     "rabbit": [1999, 1987, 1975, 1963, 1951],
#     "dragon": [2000, 1988, 1976, 1964, 1952],
#     "snake": [2001, 1989, 1977, 1965, 1953],
#     "horse": [2002, 1990, 1978, 1966, 1954],
#     "goat": [2003, 1991, 1979, 1967, 1955],
#     "monkey": [2004, 1992, 1980, 1968, 1956],
#     "rooster": [2005, 1993, 1981, 1969, 1957],
#     "dog": [2006, 1994, 1982, 1970, 1958],
#     "pig": [2007, 1995, 1983, 1971, 1959]
#     }
# } 


# ✅ 다듬은 예시 문구:
# 대부분의 띠별 운세 콘텐츠는 오늘의 간지(干支), 각 띠의 관계(지지), 그리고 **오행(목·화·토·금·수)**의 흐름에 따라,
# 전통 명리학 해석과 약간의 창의적 해석을 더해 도출됩니다.

# 📌 절대적인 예언은 아니며, 하루를 재미있고 의미 있게 보내기 위한 참고용으로 봐주세요!

# ✅ 좀 더 캐주얼하게 (앱/웹용 UI 안내에 적합):
# 🧭 이 운세는 오늘의 간지(天干地支), 띠의 상호작용, 오행의 흐름을 바탕으로 전통 명리학을 참고해 만들어졌어요.

# 다만 너무 진지하게 믿지 마시고, 하루를 조금 더 즐겁게 보내는 재미로 참고해 주세요 😊

# {
#   "rat": {
#     "interpretation": "오늘은 나무(木)의 기운이 강한 날로...",
#     "luck_score": 88,
#     "advice": "작은 기회도 놓치지 마세요.",
#     "lucky_item": "파란 손수건",
#     "lucky_color": "블루",
#     "good_time": "오전 10시 ~ 12시",
#     "love": "오래된 인연이 다시 연락올 수도 있습니다.",
#     "money": "수입보다는 지출 관리에 집중해야 할 때입니다.",
#     "relation": "협업이나 팀워크에서 성과가 날 수 있어요.",
#     "warning": "결정을 너무 빨리 내리지 마세요.",
#     "content": {
#       "1996": "도전 정신이 좋은 결과로 이어질 수 있습니다.",
#       "1984": "당신의 의견에 사람들이 귀를 기울입니다.",
#       "1972": "기다려온 일이 진전될 가능성이 있습니다.",
#       "1960": "체력 관리에 조금 더 신경 써야 할 시기입니다.",
#       "1948": "가족과의 시간 속에서 힐링을 얻을 수 있어요."
#     }
#   }
# }


# result = llm.answer(
#     "당신은 12간지 운세를 아주 정교하게 해석하는 운세 전문가입니다.",
#     f"오늘은 {today}입니다. 쥐띠(rat)에 대해 오늘의 전체적인 해석과 각 출생 연도별 간단 운세를 포함한 JSON을 만들어 주세요",
#     """
#     {
#         "rat": {
#             "1996": "운세 내용...",
#             "1984": "운세 내용...",
#             "1972": "운세 내용...",
#             "1960": "운세 내용...",
#             "1948": "운세 내용..."
#         }
#     }   
#     """
#     )

# result = llm.answer(
#     "당신은 12간지 운세를 아주 정교하게 해석하는 운세 전문가입니다.",
#     f"""
#     오늘은 {today}입니다. 쥐띠(rat)에 대해 오늘의 전체적인 해석과 각 출생 연도별 간단 운세를 포함한 JSON을 만들어 주세요.

#     "interpretation" 항목은 그날의 간지(천간지지)의 오행과 해당 띠(지지)의 오행을 비교하여 길흉을 분석한 요약입니다.

#     반드시 아래 순서로 작성해 주세요:
#     1. 오늘의 간지(예: 乙卯)의 오행 설명 (ex: 오늘은 목(木)의 기운이 강한 날입니다)
#     2. 해당 띠의 오행 설명 (ex: 쥐띠는 물(水)의 기운을 가지고 있습니다)
#     3. 오늘의 기운과 띠의 기운의 관계 (ex: 물은 나무를 도와주는 성질을 가지고 있어 오늘은 쥐띠에게 유리한 날입니다)
#     4. 종합 길흉 해석 (ex: 오늘은 좋은 흐름 속에서 기회를 잡기 좋은 날입니다)

#     예시:
#     "오늘은 나무(木)의 기운이 강한 날입니다. 쥐띠는 물(水)의 기운을 지녔으며, 물은 나무를 키우는 상생 관계에 해당합니다. 따라서 오늘은 쥐띠에게 긍정적인 에너지가 흐르고, 주변으로부터 인정받거나 기회를 얻기 좋은 날입니다."
#     """,
#     """
#     ```json
#     {{
#         "rat": {{
#             "interpretation": "띠 공통 해석",
#             "luck_score": 숫자 (0~100),
#             "advice": "한 줄 조언",
#             "lucky_item": "행운 아이템",
#             "lucky_color": "행운 색상",
#             "good_time": "좋은 시간대",
#             "love": "연애운",
#             "money": "재물운",
#             "relation": "인간관계",
#             "warning": "주의할 점",
#             "content": {{
#                 "1996": "운세 내용",
#                 "1984": "운세 내용",
#                 "1972": "운세 내용",
#                 "1960": "운세 내용",
#                 "1948": "운세 내용"
#             }}
#         }}
#     }} 
#     """
# )


def build_zodiac_prompt(today: str, zodiac_en: str, zodiac_kr: str, years: list[str]) -> tuple[str, str]:
    
    system = "당신은 12간지 운세를 아주 정교하게 해석하고 길흉을 매우 솔직하게 풀이하는 운세 전문가입니다."
    
    prompt = f"""
    오늘은 {today}입니다. {zodiac_kr}에 대해 오늘의 전체적인 해석과 각 출생 연도별 간단 운세를 포함한 JSON을 만들어 주세요.

    - interpretation 항목은 그날의 간지(천간지지)의 오행과 해당 띠(지지)의 오행을 비교하여 길흉을 분석한 요약입니다.
    
    반드시 아래 순서로 작성해 주세요:
    - 오늘의 간지(예: 乙卯)의 오행 설명
    - 해당 띠의 오행 설명
    - 오늘의 기운과 띠의 기운의 관계
    - 종합 길흉 해석
    - 길흉이 상반되는 경우에도 솔직하게 해석해 주세요.

    그리고 그 외 항목들도 모두 '{zodiac_kr} 전체'를 위한 내용으로 작성해주세요:

    - luck_score: 숫자 (0~100)
    - advice: {zodiac_kr}에게 오늘 필요한 한 줄 조언
    - lucky_item: 오늘 {zodiac_kr}에게 도움이 되는 아이템
    - lucky_color: 기운을 북돋는 색상
    - good_time: 운이 트이는 시간대 (예: "오전 9시 ~ 11시")

    오늘의 기운과 해당 띠의 오행 관계를 기반으로,
    운이 나쁠 경우에도 솔직하게 해석해 주세요.
    
    """
    
    year_json = ",\n                ".join([f'"{year}": "운세 내용"' for year in years])
    
    format = f"""
    ```json
    {{
        "{zodiac_en}": {{
            "interpretation": "해석",
            "luck_score": 숫자 (0~100),
            "advice": "한 줄 조언",
            "lucky_item": "행운의 아이템",
            "lucky_color": "행운의 색상",
            "good_time": "좋은 시간대",
            "content": {{
                {year_json}
            }}
        }}
    }} 
    """
    return system.strip(), prompt.strip(), format.strip()


today = datetime.today().strftime("%Y년 %m월 %d일")

zodiac_years = {
    "rat": {
        "korean_lang": "쥐띠",
        "years": [1996, 1984, 1972, 1960, 1948]
    },
    "ox": {
        "korean_lang": "소띠",
        "years": [1997, 1985, 1973, 1961, 1949]
    },
    "tiger": {
        "korean_lang": "호랑이띠",
        "years": [1998, 1986, 1974, 1962, 1950]
    },
    "rabbit": {
        "korean_lang": "토끼띠",
        "years": [1999, 1987, 1975, 1963, 1951]
    },
    "dragon": {
        "korean_lang": "용띠",
        "years": [2000, 1988, 1976, 1964, 1952]
    },
    "snake": {
        "korean_lang": "뱀띠",
        "years": [2001, 1989, 1977, 1965, 1953]
    }
    # "horse": {
    #     "korean_lang": "말띠",
    #     "years": [2002, 1990, 1978, 1966, 1954]
    # },
    # "goat": {
    #     "korean_lang": "양띠",
    #     "years": [2003, 1991, 1979, 1967, 1955]
    # },
    # "monkey": {
    #     "korean_lang": "원숭이띠",
    #     "years": [2004, 1992, 1980, 1968, 1956]
    # },
    # "rooster": {
    #     "korean_lang": "닭띠",
    #     "years": [2005, 1993, 1981, 1969, 1957]
    # },
    # "dog": {
    #     "korean_lang": "개띠",
    #     "years": [2006, 1994, 1982, 1970, 1958]
    # },
    # "pig": {
    #     "korean_lang": "돼지띠",
    #     "years": [2007, 1995, 1983, 1971, 1959]
    # }
}

results = {
    "date": today,
    "horoscope": {
        "chinese_zodiac": {
            
        }
    }
}

for zodiac_en, data in zodiac_years.items():
    zodiac_kr = data["korean_lang"]
    years = data["years"]

    system, prompt, format = build_zodiac_prompt(today, zodiac_en, zodiac_kr, years)

    print("system", system)
    print("prompt", prompt)
    print("format", format)

    response = llm.answer(system, prompt, format)

    # JSON 문자열 파싱
    try:
        results["horoscope"]["chinese_zodiac"].update(response)  # {"pig": {...}}를 results에 추가
    except json.JSONDecodeError:
        print(f"[ERROR] {zodiac_en} 응답 JSON 파싱 실패")



filename = f"horoscope_{today.replace('-', '')}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"✅ 결과가 파일로 저장되었습니다: {filename}")








# today = datetime.today().strftime("%Y년 %m월 %d일")

# prompt = f"""
# 오늘은 {today}입니다. 당신은 동양 명리학과 사주에 능통한 운세 전문가입니다.
# 12간지 중 '쥐띠(rat)'의 오늘 운세를 아래 JSON 구조에 맞게 생성해 주세요.

# 띠 공통 해석(interpolation)은 반드시 아래 순서대로 구성해 주세요:
# 1. 오늘의 간지(예: 乙卯)의 오행 설명 (ex: 오늘은 목(木)의 기운이 강한 날입니다.)
# 2. 쥐띠의 오행 설명 (쥐띠는 물(水)의 기운을 지닙니다.)
# 3. 오늘의 오행과 쥐띠의 오행이 상생인지 상극인지 분석
# 4. 결과적으로 오늘의 전반적인 길흉 해석

# 그리고 그 외 항목들도 모두 '쥐띠 전체'를 위한 내용으로 작성해주세요:

# - luck_score: 0~100 사이 숫자
# - advice: 쥐띠에게 오늘 필요한 한 줄 조언
# - lucky_item: 오늘 쥐띠에게 도움이 되는 아이템
# - lucky_color: 기운을 북돋는 색상
# - good_time: 운이 트이는 시간대 (예: "오전 9시 ~ 11시")
# - love: 감정 흐름이나 인간관계 속 연애운
# - money: 재정 흐름, 소비/투자 경고
# - relation: 인간관계 전반의 흐름
# - warning: 오늘 특히 주의할 점

# 그리고 마지막으로 아래 출생 연도별 맞춤 운세를 content 항목에 작성해 주세요.  
# **연령대별 상황에 맞게 내용은 서로 달라야 합니다.**

# - 1996년생: 20대 후반, 커리어 초기
# - 1984년생: 40대 초반, 직장/가정 균형
# - 1972년생: 50대 초반, 리더십/건강 중심
# - 1960년생: 60대 중반, 은퇴 준비/자기 관리
# - 1948년생: 70대 후반, 가족 중심 안정기

# ---

# 다음 형식을 반드시 그대로 지켜 JSON 형식으로만 출력해 주세요:

# ```json
# {{
#   "rat": {{
#     "interpretation": "...",
#     "luck_score": 숫자,
#     "advice": "...",
#     "lucky_item": "...",
#     "lucky_color": "...",
#     "good_time": "...",
#     "love": "...",
#     "money": "...",
#     "relation": "...",
#     "warning": "...",
#     "content": {{
#       "1996": "...",
#       "1984": "...",
#       "1972": "...",
#       "1960": "...",
#       "1948": "..."
#     }}
#   }}
# }}
# """