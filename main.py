from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime
import json
import time
import os

from llm import get_daily_horoscope, clean_json_response


def my_batch_job():
    print(f"[{datetime.datetime.now()}] ##### 오늘의 운세 생성 ##### ")

    horoscope = get_daily_horoscope()
    result_parsed_json = clean_json_response(horoscope)

    parsed = json.loads(result_parsed_json)
    print(json.dumps(parsed, indent=4, ensure_ascii=False))


def save_jobs_to_json(scheduler, filepath='jobs.json'):
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
# 매일 오전 9시에 실행
scheduler.add_job(my_batch_job, CronTrigger(hour=23, minute=0), id='daily_job')
# 매 5초마다 실행
# scheduler.add_job(my_batch_job, 'interval', seconds=5, id='interval_job')

# job 상태 저장하는 job 등록 (10초마다)
scheduler.add_job(lambda: save_jobs_to_json(scheduler), 'interval', seconds=10, id='job_logger')


try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    print("스케줄러 종료")
