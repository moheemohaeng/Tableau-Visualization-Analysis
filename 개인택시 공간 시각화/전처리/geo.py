import requests
from urllib.parse import urlparse
import json
import pandas as pd
from time import sleep

api_key = 'input your api key'

# 위도와 경도를 받아 지번을 리턴해주는 함수
def lat_lon_to_addr(lon,lat):
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={longitude}\
        &y={latitude}'.format(longitude=lon,latitude=lat)
    headers = {"Authorization": "KakaoAK " + api_key}
    result = json.loads(str(requests.get(url, headers=headers).text))
    geo = result['documents'][0]['address_name']
    return str(geo)


# 액셀파일 불러오기
dataset = pd.read_excel('Taxi_운행기록.xls')
dataset_test = dataset["지번"]
# 8145개의 데이터에 대해 지번을 구함.
for i in range(0,8145):
    print(i+1,'processing')
    latitude = dataset["Latitude"][i]
    longtitude = dataset["Longitude"][i]
    result = lat_lon_to_addr(longtitude, latitude)
    dataset_test[i] = result

    #api 차단 방지를 위한 time 지연
    sleep(2)


    # 새롭게 저장
    path = 'test3.xlsx'
    with pd.ExcelWriter(path) as writer:
        dataset_test.to_excel(writer, sheet_name = 'raw_data1') #raw_data1 시트에 저장