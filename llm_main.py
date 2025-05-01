from core import global_constants
from modules import llm
from dotenv import load_dotenv
import os
from datetime import datetime
from pprint import pprint
import json

# .env 파일 로드
load_dotenv()


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


# ==================================== 1번 로직 ====================================

# def build_zodiac_prompt(today: str, zodiac_en: str, zodiac_kr: str, years: list[str]) -> tuple[str, str]:
    
#     system = "당신은 12간지 운세를 아주 정교하게 해석하고 길흉을 매우 솔직하게 풀이하는 운세 전문가입니다."
    
#     prompt = f"""
#     오늘은 {today}입니다. {zodiac_kr}에 대해 오늘의 전체적인 해석과 각 출생 연도별 간단 운세를 포함한 JSON을 만들어 주세요.
#     반드시 운이 나쁜 경우에도 솔직하게 기술해 주세요. 무조건 좋은 말만 쓰지 마세요.

#     ## JSON 구조는 아래와 같이 작성해 주세요 ##

#     - interpretation (string):
#     다음 내용을 포함하여 1개의 문단으로 작성하세요. 반드시 논리적 근거를 포함하고, 무조건 긍정적이지 않아야 합니다.
#     1. 오늘의 간지 오행 설명 (예: 乙卯 → 목(木))  
#     2. 해당 띠({zodiac_kr})의 오행 설명  
#     3. 오늘의 오행과 띠의 오행의 관계 (상생/상극 등)  
#     4. 종합 길흉 해석  

#     - luck_score (integer):  
#     오늘은 {zodiac_kr}의 운을 정수로 표현하세요 운이 좋으면 높고, 나쁘면 낮습니다. 0~100 사이 정수로 작성하세요.

#     - advice (string):  
#     오늘의 행동 조언. {zodiac_kr}의 특성과 오행 관계를 고려해 실용적으로 작성하세요.  

#     - lucky_item (string):  
#     오늘 {zodiac_kr}에게 도움이 되는 아이템. 생활 속 사물로 작성하세요.

#     - lucky_color (string):  
#     오늘 {zodiac_kr}의 기운을 북돋는 색상

#     - good_time (string):  
#     {zodiac_kr}에게 오늘 기운이 가장 좋을 시간대 

#     - content (dictionary):  
#     {zodiac_kr} 각 연도별 운세 설명. 출생 연도별로 각기 다른 내용을 제공합니다. 
    
#     """
    
#     year_json = ",\n                ".join([f'"{year}": "운세 내용"' for year in years])
    
#     format = f"""
#     ```json
#     {{
#         "{zodiac_en}": {{
#             "interpretation": "해석",
#             "luck_score": 숫자 (0~100),
#             "advice": "한 줄 조언",
#             "lucky_item": "행운의 아이템",
#             "lucky_color": "행운의 색상",
#             "good_time": "좋은 시간대",
#             "content": {{
#                 {year_json}
#             }}
#         }}
#     }} 
#     """
#     return system.strip(), prompt.strip(), format.strip()

# today = datetime.today().strftime("%Y년 %m월 %d일")

# zodiac_years = {
#     "rat": {
#         "korean_lang": "쥐띠",
#         "years": [1996, 1984, 1972, 1960, 1948]
#     },
#     "ox": {
#         "korean_lang": "소띠",
#         "years": [1997, 1985, 1973, 1961, 1949]
#     },
#     "tiger": {
#         "korean_lang": "호랑이띠",
#         "years": [1998, 1986, 1974, 1962, 1950]
#     },
#     "rabbit": {
#         "korean_lang": "토끼띠",
#         "years": [1999, 1987, 1975, 1963, 1951]
#     },
#     "dragon": {
#         "korean_lang": "용띠",
#         "years": [2000, 1988, 1976, 1964, 1952]
#     },
#     "snake": {
#         "korean_lang": "뱀띠",
#         "years": [2001, 1989, 1977, 1965, 1953]
#     },
#     "horse": {
#         "korean_lang": "말띠",
#         "years": [2002, 1990, 1978, 1966, 1954]
#     },
#     "goat": {
#         "korean_lang": "양띠",
#         "years": [2003, 1991, 1979, 1967, 1955]
#     },
#     "monkey": {
#         "korean_lang": "원숭이띠",
#         "years": [2004, 1992, 1980, 1968, 1956]
#     },
#     "rooster": {
#         "korean_lang": "닭띠",
#         "years": [2005, 1993, 1981, 1969, 1957]
#     },
#     "dog": {
#         "korean_lang": "개띠",
#         "years": [2006, 1994, 1982, 1970, 1958]
#     },
#     "pig": {
#         "korean_lang": "돼지띠",
#         "years": [2007, 1995, 1983, 1971, 1959]
#     }
# }

# results = {
#     "date": today,
#     "horoscope": {
#         "chinese_zodiac": {
            
#         }
#     }
# }

# for zodiac_en, data in zodiac_years.items():
#     zodiac_kr = data["korean_lang"]
#     years = data["years"]

#     system, prompt, format = build_zodiac_prompt(today, zodiac_en, zodiac_kr, years)

#     print("system", system)
#     print("prompt", prompt)
#     print("format", format)

#     response = llm.answer(system, prompt, format)

#     # JSON 문자열 파싱
#     try:
#         results["horoscope"]["chinese_zodiac"].update(response)  # {"pig": {...}}를 results에 추가
#     except json.JSONDecodeError:
#         print(f"[ERROR] {zodiac_en} 응답 JSON 파싱 실패")

# ==================================================================================


# ===================================== 2번 로직 ====================================

def build_zodiac_prompt(today: str) -> tuple[str, str, str]:
    system = "당신은 12간지 운세를 깊이 있는 철학적 통찰과 논리적 사고로 해석하는 최고의 운세 전문가입니다. 모든 해석은 솔직하고 현실적이어야 하며, 과장되거나 근거 없는 낙관은 금지합니다."

    prompt = f"""
    오늘은 {today}입니다.  

    주의사항:  
    - '오늘의 오행'은 하나로 통일합니다. 12띠 모두 이 하나의 오행을 기준으로 논리적으로 해석합니다.
    - 띠별로 오늘의 오행을 따로 설정하는 것은 절대 금지입니다.
    - 띠별 고유 오행(土/금/수/화/목)과 '오늘의 오행' 간의 관계(상생/상극 등)를 논리적으로 분석해 길흉을 종합적으로 해석하세요.
    - 무조건 긍정적으로 서술하지 말고, 나쁜 점은 솔직하게 표현해야 합니다.
    - 띠별 advice(조언)는 다양하고 구체적이어야 합니다. 감정조절, 협력 같은 단순 조언 반복을 피하세요.
    - lucky_item는 띠마다 다르게 설정합니다. 중복되는 물건을 최대한 피하고, 현실적인 아이템 위주로 선택하세요.
    - lucky_color는 띠마다 다르게 설정합니다. 중복되는 색은 최대한 피하세요.
    - good_time은 띠별로 하루 중 다른 2시간 구간을 제시합니다.
    - content(출생연도별 해석)는 연령별 특성에 맞게 개별적이며 중복이 없도록 작성합니다. 그리고 나이대 표현과 같은 딱딱한 표현은 생략합니다.

    ### JSON 작성 규칙

    - interpretation (string):  
    오늘 오행 설명 + 띠 고유 오행 설명 + 두 오행 간 상생/상극 관계 + 종합 길흉 해석을 한 문단으로 작성합니다.

    - luck_score (integer):  
    0~100 범위에서 운의 강약을 점수로 나타냅니다.

    - advice (string):  
    띠 특성과 오늘 오행에 맞는 구체적이고 실질적인 행동 조언을 작성합니다.

    - lucky_item (string):  
    현실적이고 일상적인 소품을 선정합니다.

    - lucky_color (string):  
    띠별로 다른 색상을 설정합니다.

    - good_time (string):  
    하루 중 좋은 2시간 구간 (예: "오전 9시 - 11시" 형식)

    - content (dictionary):  
    출생연도별(5개) 각각 연령대를 고려한 다른 운세 설명을 작성합니다. 

    """

    format = """
    ```json
    {
        "rat": {
            "interpretation": "논리적 길흉 해석",
            "luck_score": 0~100 사이 숫자,
            "advice": "띠 특성에 맞는 실용적 조언",
            "lucky_item": "생활 소품",
            "lucky_color": "행운 색상",
            "good_time": "좋은 시간대",
            "content": {
                "1996": "연령대 맞춤 운세",
                "1984": "연령대 맞춤 운세",
                "1972": "연령대 맞춤 운세",
                "1960": "연령대 맞춤 운세",
                "1948": "연령대 맞춤 운세"
            }
        },
        "ox": {
            ...
        },
        ...
    }
    """
    return system.strip(), prompt.strip(), format.strip()


def save_results_to_file():
    # 결과 세팅
    today = datetime.today().strftime("%Y-%m-%d")
    results = {
        "date": today,
        "horoscope": {
            "chinese_zodiac": {
                
            }
        }
    }

    # 2
    today = datetime.today().strftime("%Y년 %m월 %d일")
    system, prompt, format = build_zodiac_prompt(today)

    print("system", system)
    print("prompt", prompt)
    print("format", format)

    response = llm.answer(system, prompt, format)

    # JSON 문자열 파싱
    try:
        results["horoscope"]["chinese_zodiac"].update(response)  # {"pig": {...}}를 results에 추가
    except json.JSONDecodeError:
        print(f"[ERROR] 응답 JSON 파싱 실패")

    # 파일로 저장

    filename = f"result_files/horoscope_{today.replace('-', '')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ 결과가 파일로 저장되었습니다: {filename}")

    return results

