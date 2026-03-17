Data Pipeline Project
Airflow 기반 공공 데이터 수집 및 적재 파이프라인

1. 프로젝트 개요

	공공 API(에어코리아)를 활용하여 데이터를 수집하고,
	Airflow DAG를 통해 자동화된 ETL 파이프라인을 구축하였다.
	
	수집된 데이터는 PostgreSQL에 적재되며,
	데이터 분석 및 데이터 플랫폼 구축의 기반이 되는 구조를 설계하는 것을 목표로 한다.
	
2. 목적

	공공 데이터 API 기반 데이터 수집 자동화
	
	Airflow를 활용한 ETL 파이프라인 구성
	
	PostgreSQL 기반 데이터 적재 구조 설계
	
	Docker 기반 실행 환경 구성
	
3. 시스템 구성
	
	AirKorea API
	→ Python ETL Script
	→ Airflow DAG
	→ PostgreSQL

4. 기술 스택
	
	Python
	Apache Airflow
	PostgreSQL
	Docker / Docker Compose

5. 프로젝트 구조
	
	data-pipeline-project
	├── config/
	├── dags/
	├── scripts/
	├── data/raw/
	├── docker-compose.yaml
	├── .gitignore
	├── README.md
	└── LICENSE
	
6. 데이터 처리 흐름

	AirKorea API 호출
	데이터 수집 및 파일 저장
	Airflow DAG 실행
	PostgreSQL 적재
	분석 가능한 데이터 구조 생성

7. 실행 방법

	Docker 실행
	docker compose up -d
	
	Airflow 접속
	http://localhost:8080
	
	DAG 실행
	airkorea_etl_dag 실행
	
8. 향후 개선

	Kafka 기반 스트리밍 파이프라인 구축
	Spark 기반 대용량 데이터 처리
	AWS 기반 클라우드 아키텍처 확장
	CI/CD 자동화

9. 작성자

	Um-koo