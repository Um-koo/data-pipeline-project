import pandas as pd
from sqlalchemy import create_engine, text

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

# 6. PostgreSQL에 데이터 적재 (중복 방지 포함)
# 기존 to_sql 방식은 중복 시 에러 발생 → ON CONFLICT DO NOTHING 방식으로 변경
insert_sql = text("""
    INSERT INTO airkorea_measurements (
        station_name,
        sido_name,
        data_time,
        pm10_value,
        pm25_value,
        o3_value,
        no2_value,
        co_value,
        so2_value
    )
    VALUES (
        :station_name,
        :sido_name,
        :data_time,
        :pm10_value,
        :pm25_value,
        :o3_value,
        :no2_value,
        :co_value,
        :so2_value
    )
    ON CONFLICT (station_name, data_time) DO NOTHING
""")

records = df.to_dict(orient="records")

with engine.begin() as conn:
    conn.execute(insert_sql, records)

# 7. 결과 출력
print("CSV 데이터 PostgreSQL 적재 완료")
print(f"읽은 건수: {len(df)}")