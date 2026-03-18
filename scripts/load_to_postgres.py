# load_to_postgres.py
# 목적:
# AirKorea CSV 파일을 읽어 PostgreSQL의 airkorea_measurements 테이블에 적재한다.
#
# 처리 흐름:
# 1. CSV 파일 읽기
# 2. 컬럼명을 DB 테이블 구조에 맞게 변경
# 3. PostgreSQL 연결 정보 설정
# 4. SQLAlchemy 엔진 생성
# 5. DataFrame을 PostgreSQL에 append 방식으로 적재
# 6. 적재 결과 출력

import pandas as pd
from sqlalchemy import create_engine

# 1. Airflow Docker 컨테이너 내부 기준 CSV 파일 경로
# 로컬의 data 폴더가 /opt/airflow/data 로 마운트되어 있으므로 이 경로를 사용한다.
csv_path = "/opt/airflow/data/raw/airkorea_seoul.csv"

# 2. CSV 파일 읽기
# AirKorea API에서 저장한 raw CSV를 DataFrame으로 불러온다.
df = pd.read_csv(csv_path)

# 3. 컬럼명 변경
# 원본 CSV 컬럼명을 PostgreSQL 테이블 컬럼명 규칙(snake_case)에 맞게 변환한다.
df = df.rename(columns={
    "stationName": "station_name",
    "sidoName": "sido_name",
    "dataTime": "data_time",
    "pm10Value": "pm10_value",
    "pm25Value": "pm25_value",
    "o3Value": "o3_value",
    "no2Value": "no2_value",
    "coValue": "co_value",
    "so2Value": "so2_value"
})

# 4. PostgreSQL 연결 정보
# Airflow 컨테이너에서 로컬 PC의 PostgreSQL로 접속하기 위해
# host.docker.internal 을 사용한다.
db_user = "postgres"
db_password = "1234"
db_host = "host.docker.internal"
db_port = "5432"
db_name = "airkorea_db"

# 5. SQLAlchemy 엔진 생성
# pandas.to_sql()을 사용하기 위해 PostgreSQL 연결 엔진을 생성한다.
engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

# 6. PostgreSQL 적재
# if_exists="append" 이므로 실행할 때마다 기존 데이터 뒤에 추가된다.
# 현재는 테스트/학습 목적 구조이며, 향후 중복 방지 로직이 필요하다.
df.to_sql(
    name="airkorea_measurements",
    con=engine,
    if_exists="append",
    index=False
)

# 7. 결과 출력
# Airflow 로그 또는 콘솔에서 적재 성공 여부와 건수를 확인하기 위한 메시지다.
print("CSV 데이터 PostgreSQL 적재 완료")
print(f"적재 건수: {len(df)}")
