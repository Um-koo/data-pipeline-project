import logging
import pandas as pd
from sqlalchemy import create_engine, text

# 0. 로그 설정
# Airflow 로그에서 INFO / ERROR 메시지를 구분해서 확인할 수 있도록 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# 1. CSV 파일 경로
csv_path = "/opt/airflow/data/raw/airkorea_seoul.csv"

# 2. PostgreSQL 연결 정보
db_user = "postgres"
db_password = "1234"
db_host = "host.docker.internal"
db_port = "5432"
db_name = "airkorea_db"

# 3. 필수 컬럼 정의
# CSV에 반드시 있어야 하는 원본 컬럼 목록
required_columns = [
    "stationName",
    "sidoName",
    "dataTime",
    "pm10Value",
    "pm25Value",
    "o3Value",
    "no2Value",
    "coValue",
    "so2Value"
]

# 4. SQLAlchemy 엔진 생성
engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

# 5. PostgreSQL에 데이터 적재할 SQL 정의
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

try:
    # 6. CSV 읽기
    logging.info("CSV 파일 읽기 시작")
    df = pd.read_csv(csv_path)
    logging.info(f"CSV 파일 읽기 완료 - 원본 건수: {len(df)}")

    # 7. 필수 컬럼 존재 여부 확인
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"필수 컬럼 누락: {missing_columns}")

    # 8. 컬럼명 변경 (CSV 컬럼명 -> PostgreSQL 테이블 컬럼명)
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

    logging.info("컬럼명 변경 완료")

    # 9. DataFrame을 INSERT용 records로 변환
    records = df.to_dict(orient="records")
    logging.info(f"DB 적재 대상 레코드 변환 완료 - 건수: {len(records)}")

    # 10. PostgreSQL에 데이터 적재
    # engine.begin() 사용 시 정상 종료 시 commit,
    # 예외 발생 시 rollback 이 자동 처리된다.
    with engine.begin() as conn:
        conn.execute(insert_sql, records)

    # 11. 결과 출력
    logging.info("CSV 데이터 PostgreSQL 적재 완료")
    logging.info(f"읽은 건수: {len(df)}")

except Exception as e:
    logging.error(f"load_to_postgres.py 실행 중 오류 발생: {e}")
    raise
