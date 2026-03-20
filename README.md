# Data Pipeline Project

Airflow 기반 공공 데이터 수집 및 적재 파이프라인

---

## 1. 프로젝트 개요

공공 API(에어코리아)를 활용하여 데이터를 수집하고,  
Airflow DAG를 통해 자동화된 ETL 파이프라인을 구축하였다.

초기에는 CSV 기반 데이터 적재 구조를 구현하였으며,  
이후 안정화 단계에서 자동 스케줄링, 중복 데이터 방지, 재실행 안정성(idempotent)을 확보하였다.

수집된 데이터는 PostgreSQL에 적재되며,  
데이터 분석 및 데이터 플랫폼 구축의 기반이 되는 구조를 설계하는 것을 목표로 한다.

---

## 2. 목적

- 공공 데이터 API 기반 데이터 수집 자동화  
- Airflow를 활용한 ETL 파이프라인 구성  
- PostgreSQL 기반 데이터 적재 구조 설계  
- Docker 기반 실행 환경 구성  

---

## 3. 시스템 구성

```
AirKorea API
    ↓
Python ETL Script
    ↓
Airflow DAG
    ↓
PostgreSQL
```

---

## 4. 기술 스택

- Python  
- Apache Airflow  
- PostgreSQL  
- Docker / Docker Compose  

---

## 5. 프로젝트 구조

```
data-pipeline-project
├── config/
├── dags/
├── scripts/
├── data/raw/
├── docker-compose.yaml
├── .gitignore
├── README.md
└── LICENSE
```

---

## 6. 데이터 처리 흐름

1. AirKorea API 호출  
2. 데이터 수집 및 CSV 파일 저장  
3. Airflow DAG 자동 실행  
4. Python ETL Script 실행  
5. 데이터 전처리 (컬럼 정리)  
6. PostgreSQL 적재 (중복 방지 적용)  
7. 분석 가능한 데이터 구조 생성  

---

## 7. 실행 방법

### 1) Docker 실행

```bash
docker compose up -d
```

### 2) Airflow 접속

```
http://localhost:8080
```

### 3) DAG 실행

- airkorea_etl_dag 실행

---

## 8. 향후 개선

현재 프로젝트는 Airflow 기반 Batch ETL 파이프라인을 구성한 단계이며,  
실무 적용성과 확장성을 고려하여 다음과 같은 방향으로 개선할 수 있다.

### 1. 데이터 품질 및 적재 로직 개선
- 중복 데이터 방지를 위한 UNIQUE 및 Upsert 로직 적용
- INSERT 중심 구조 → 데이터 정합성 보장 구조로 개선
- 데이터 적재 시 무결성 및 일관성 확보

### 2. DAG 구조 개선 (ETL 단계 분리)
- 단일 Task 구조 → Extract / Transform / Load 단계 분리
- Task 간 의존성 관리 및 재실행 구조 개선
- Airflow 파이프라인 구조 표준화

### 3. 로그 및 모니터링 체계 구축
- print 기반 로그 → logging 모듈 기반 구조로 개선
- 에러 로그 / 정상 로그 구분
- Airflow 로그를 활용한 문제 추적 체계 확립

### 4. 스케줄링 및 자동화
- 수동 실행 → 주기적 실행 (Cron 기반 스케줄링)
- 정기 데이터 수집 및 적재 자동화

### 5. 데이터 플랫폼 확장 (Data Mart)
- Raw 데이터 → 분석용 Mart 테이블 구조 설계
- 집계 및 분석을 위한 SQL 레이어 구축
- 데이터 활용성을 고려한 구조 확장

### 6. 실시간 데이터 파이프라인 확장
- Kafka 기반 Streaming 데이터 수집 구조 도입
- Batch 중심 처리 → Real-time 데이터 처리로 확장

### 7. 대용량 데이터 처리
- Spark 기반 분산 처리 적용
- 데이터 증가에 따른 처리 성능 및 확장성 확보

### 8. 클라우드 아키텍처 확장
- AWS 환경으로 이전 (EC2, RDS, S3 등)
- 온프레미스 → 클라우드 기반 데이터 플랫폼으로 확장

### 9. CI/CD 자동화
- GitHub Actions 기반 파이프라인 자동 배포
- 코드 변경 시 DAG 및 데이터 처리 자동 반영

---
## 9. 안정화 (Stabilize)

초기 구현 단계에서는 DAG를 재실행할 경우 동일 데이터가 중복 적재되는 문제가 발생하였다.

### 문제
- pandas의 `to_sql(..., if_exists="append")` 방식 사용
- 중복 방지 로직 부재

### 해결
- `(station_name, data_time)` 기준 UNIQUE 제약 확인
- PostgreSQL INSERT 시 `ON CONFLICT DO NOTHING` 적용

### 결과
- DAG 재실행 시 중복 데이터 미발생
- 동일 작업 반복 실행 가능 (idempotent 확보)
- 자동 스케줄 환경에서도 안정적 동작 확인

또한 DAG 스케줄링을 적용하여  
수동 실행에서 자동 실행 구조로 전환하였다.

- `schedule="@daily"`
- `catchup=False`

이를 통해 실제 운영 가능한 ETL 파이프라인 구조를 확보하였다.

### 오류 처리 및 로그 개선

초기 구조에서는 오류 발생 시 예외 처리가 없어  
문제 원인 파악이 어렵고 안정성이 부족하였다.

개선 내용:

- CSV 읽기, 데이터 처리, DB 적재 단계에 try-except 적용
- logging 모듈을 활용한 로그 체계 도입 (INFO / ERROR 구분)
- DB 작업 중 오류 발생 시 rollback 처리 적용
- 예외 발생 시 Airflow Task가 실패로 인식되도록 구성

결과:

- 오류 발생 시 원인 추적 가능
- 데이터 정합성 보장 (rollback)
- Airflow 기반 안정적인 운영 구조 확보

---

## 10. 작성자

Um-koo
