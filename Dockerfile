# 베이스 이미지 설정 (버전 명시 필수)
FROM python:3.10-slim

# 작업 디렉토리 생성
WORKDIR /app

# 소스코드 복사
COPY . .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 컨테이너 실행 시 기본 실행 명령
CMD ["python", "batch_main.py"]