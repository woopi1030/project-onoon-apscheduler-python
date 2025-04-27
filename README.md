# project-onoon-apscheduler-python
project-onoon-apscheduler-python

# 가상환경 세팅
python -m venv _venv

# 가상환경 활성화 (터미널별로 실행되어서 새 터미널 띄우면 가상환경 다시 켜야함)
.\_venv\Scripts\activate.bat
source _venv\Scripts\activate

# .env 사용
pip install python-dotenv

# 파일로 패키지 목록 저장 (requirements.txt)
pip freeze > requirements.txt

# 패키지 목록 설치
pip install -r requirements.txt