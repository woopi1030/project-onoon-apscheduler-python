from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import json
import time
import os
from pprint import pprint
from llm_main import save_results_to_file
from db.repository import find_content, save_content, update_content

def with_retry(func, retries=3, delay=5):
    for attempt in range(1, retries + 1):
        try:
            func()
            return  # 성공하면 종료
        except Exception as e:
            print(f"❌ [{attempt}/{retries}] 에러 발생: {e}")
            if attempt < retries:
                print(f"⏳ {delay}초 후 재시도합니다...")
                time.sleep(delay)
            else:
                print("💥 최대 재시도 횟수 초과. 작업 실패.")

def my_batch_job():
    print(f"[{datetime.now()}] ##### 오늘의 운세 생성 ##### ")

    today = datetime.today().strftime("%Y-%m-%d")

    print("1. DB에서 오늘의 운세를 가져옵니다.")
    horoscopo_result = save_results_to_file()

    print("2. 오늘의 운세저장 전 date가 있는지 확인합니다.")
    find_result = find_content(today)

    print("3. 데이터가 있으면 업데이트, 없으면 저장합니다.")
    if find_result:
        print("3-1. 기존 데이터가 존재합니다. 데이터를 업데이트합니다.")
        update_content(today, horoscopo_result)
    else:
        print("3-2. 기존 데이터가 없습니다. 새로운 데이터를 저장합니다.")
        save_content(horoscopo_result)

    print("4. 저장된 데이터를 확인합니다")
    pprint(find_content(today))
    

def save_jobs_to_json(scheduler, filepath='batch_logs/jobs.json'):
    jobs = scheduler.get_jobs()
    job_list = []

    for job in jobs:
        job_list.append({
            'id': job.id,
            'next_run_time': str(job.next_run_time),
            'trigger': str(job.trigger),
            'func_ref': job.func_ref,
            'name': job.name,
        })

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(job_list, f, indent=4, ensure_ascii=False)

# 스케쥴러 설정
scheduler = BlockingScheduler()

# 매일 오전 0시 1분에 실행
# 배치를 재시도 래퍼로 감싸서 등록
scheduler.add_job(lambda: with_retry(my_batch_job), CronTrigger(hour=0, minute=1), id='create_horoscope_job')

# 매 5초마다 실행
# scheduler.add_job(my_batch_job, 'interval', seconds=5, id='interval_job')

# job 상태 저장하는 job 등록 (10초마다)
scheduler.add_job(lambda: save_jobs_to_json(scheduler), 'interval', seconds=10, id='job_logger')

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    print("스케줄러 종료")
