import json
import openai
import requests
from pprint import pprint
from dotenv import load_dotenv
import os

from core import global_constants

import textwrap

#variables
exchange_rate = 0.0


# 주어진 기준 통화(base)와 대상 통화(target)에 대해 환율을 조회.
def get_exchange_rate(base='USD', target='KRW'):
    url = f"https://open.er-api.com/v6/latest/{base}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get('result') == 'success':
            rate = data['rates'].get(target)
            print(rate)
            if rate:
                print(f"1 {base} = {rate:.2f} {target}")
                return rate
            else:
                print(f"'{target}' 통화에 대한 환율 정보 없음.")
        else:
            print("API 응답 실패:", data.get('error-type'))
    else:
        print("HTTP 요청 실패:", response.status_code)

# OpenAI 응답의 token 사용량을 바탕으로 비용을 계산합니다.
def calculate_cost(usage, model="gpt-4o-mini"):
    if model == "gpt-4o-mini":
        prompt_cost_per_1k = 0.00015
        completion_cost_per_1k = 0.0006
    else:
        raise ValueError("지원하지 않는 모델입니다.")

    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens

    prompt_cost = (prompt_tokens / 1000) * prompt_cost_per_1k
    completion_cost = (completion_tokens / 1000) * completion_cost_per_1k
    total_cost = prompt_cost + completion_cost
    
    print("##### Total prompt_tokens :", usage.prompt_tokens)
    print("##### Total completion_tokens :", usage.completion_tokens)
    print(f"##### Total costs : {total_cost:.10f} 달러")

    # API 자체가 하루 한번 업데이트 하는 API라서 실시간으로 불러올 필요 없으 
    exchange_rate = get_exchange_rate('USD', 'KRW')  # 미국 달러 → 원화
    print(f"##### Total costs : {total_cost * exchange_rate:.2f} 원")
    print("#####")


#  OpenAI API를 사용해 질문에 대한 답변을 생성합니다.
def answer(role, prompt, format, llm='gpt-4o-mini', output='json'):
    
    
    api_key = os.getenv("LLM_API_KEY")
    openai.api_key = api_key

    # API 키가 설정되어 있는지 확인
    dedented_role = textwrap.dedent(role).strip()
    dedented_prompt = textwrap.dedent(prompt).strip()
    dedented_format = textwrap.dedent(format).strip()

    response = openai.chat.completions.create(
        model=global_constants.LLM_MODEL,
        messages=[
            {
                'role': 'system',
                'content': dedented_role
            },
            {
                'role': 'user',
                'content': f'''
                {dedented_prompt}

                JSON을 만들어 주세요.
                JSON 구조는 아래와 같아야 합니다:
                {dedented_format}
                '''
            }
        ],
        n=1,             # 응답수, 다양한 응답 생성 가능
        max_tokens=6000, # 응답 생성시 최대 1000개의 단어 사용
        temperature=0,   # 창의적인 응답여부, 값이 클수록 확률에 기반한 창의적인 응답이 생성됨
        response_format= { "type":"json_object" }
    )
    
    # 계산 출력
    calculate_cost(response.usage, model="gpt-4o-mini")
    
    return json.loads(response.choices[0].message.content) # str -> json
  

# 문자열에서 빈 줄을 제거한 후 다시 합쳐서 반환.
def remove_empty_lines(text):
    lines = [line for line in text.splitlines() if line.strip()]
    result = '\n'.join(lines)
    return result
