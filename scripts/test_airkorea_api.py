import requests
import pandas as pd

API_KEY = "f7FPUGeT9mqVKfBKVabKIy3LEbmEsshmKa56g2WxiANBtUnX19c40XYo5jIBk1uXtioXHY52QuyltYJ3whm95g=="

url = "https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"

params = {
    "serviceKey": API_KEY,
    "returnType": "json",
    "sidoName": "서울",
    "numOfRows": "10",
    "pageNo": "1",
    "ver": "1.0"
}

response = requests.get(url, params=params)
data = response.json()

items = data["response"]["body"]["items"]

df = pd.DataFrame(items)

print("데이터프레임 생성 완료")
print("행/열 크기:", df.shape)
print()
print("컬럼 목록:")
print(df.columns.tolist())
print()
print("상위 5개 데이터:")
print(df.head())


columns = [
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

df = df[columns]

df["pm10Value"] = pd.to_numeric(df["pm10Value"], errors="coerce")
df["pm25Value"] = pd.to_numeric(df["pm25Value"], errors="coerce")
df["o3Value"] = pd.to_numeric(df["o3Value"], errors="coerce")
df["no2Value"] = pd.to_numeric(df["no2Value"], errors="coerce")
df["coValue"] = pd.to_numeric(df["coValue"], errors="coerce")
df["so2Value"] = pd.to_numeric(df["so2Value"], errors="coerce")

df["dataTime"] = pd.to_datetime(df["dataTime"])

print()
print("정리된 컬럼 데이터:")
print(df.head())

output_path = r"C:\Users\jung2\data-pipeline-project\data\raw\airkorea_seoul.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print()
print("CSV 저장 완료:", output_path)

print()
print("결측값 확인")
print(df.isna().sum())

print()
print("데이터 타입 확인")
print(df.dtypes)
