import pandas as pd
from sqlalchemy import create_engine

# 1. CSV 파일 경로
csv_path = "/opt/airflow/data/raw/airkorea_seoul.csv"

# 2. CSV 읽기
df = pd.read_csv(csv_path)

# 3. 컬럼명 변경 (CSV 컬럼명 -> PostgreSQL 테이블 컬럼명)
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
db_user = "postgres"
db_password = "1234"
db_host = "host.docker.internal"
db_port = "5432"
db_name = "airkorea_db"

# 5. SQLAlchemy 엔진 생성
engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

# 6. PostgreSQL에 데이터 적재
df.to_sql(
    name="airkorea_measurements",
    con=engine,
    if_exists="append",
    index=False
)

# 7. 결과 출력
print("CSV 데이터 PostgreSQL 적재 완료")
print(f"적재 건수: {len(df)}")