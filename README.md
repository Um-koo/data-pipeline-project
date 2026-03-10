# Data Pipeline Project

Airflow 기반 공공데이터 수집 파이프라인

## 목적
외부 공공데이터 API를 수집하고 PostgreSQL에 적재하는 데이터 파이프라인 구축

## 기술 스택
- Python
- Airflow
- PostgreSQL
- Docker


## Data Source

## Data Source

AirKorea Open API

Endpoint
https://apis.data.go.kr/B552584/ArpltnInforInqireSvc

API
getCtprvnRltmMesureDnsty

Example Parameters

sidoName=서울
returnType=json
numOfRows=100
pageNo=1


## Pipeline Architecture

AirKorea OpenAPI에서 대기오염 데이터를 수집하여
Python 기반 ETL을 통해 PostgreSQL에 저장하는 데이터 파이프라인

### Data Flow

AirKorea API
↓
Python Extract (requests)
↓
JSON 데이터 수신
↓
Transform (Pandas DataFrame 변환)
↓
데이터 정제
↓
PostgreSQL 저장
↓
Data Platform API 제공

## ETL Process

### Extract

AirKorea OpenAPI 호출

### Transform

JSON 데이터를 DataFrame으로 변환  
필요한 컬럼만 선택

### Load

정제된 데이터를 PostgreSQL에 저장
