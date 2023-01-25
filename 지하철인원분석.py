# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 14:11:54 2022

@author: 유호인
"""

import pandas as pd
import folium

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from folium.plugins import HeatMap

df = pd.read_csv('C:/Users/유호인/Downloads/지하철 위경도.csv', encoding='cp949')

seoul_map = folium.Map(location = [37.55, 126.98], tiles = 'Stamen Terrain', zoom_start = 11) # 서울 지도 불러오기

for name, lat, lng in zip(df.지하철역, df.위도, df.경도):
    folium.Marker([lat,lng], popup = name).add_to(seoul_map) #지하철역 위치 맵에 표시
    
#   seoul_map.save('C:\Users\유호인\Downloads\seoul_metro.html')

station_people = pd.read_csv('C:/Users/유호인/Downloads/서울시 지하철 호선별 역별 시간대별 승하차 인원 정보.csv',encoding = 'cp949')
station_people = station_people.loc[station_people['사용월'] == 202211, :] #2022년 11월 데이터 추출

in_subway = station_people.columns.tolist()[:3]
for a in station_people.columns.tolist():
    if a.find('승차')!=-1:
        in_subway.append(a)
in_subway_df = station_people[in_subway]

time = input('찾고 싶은 시간대를 입력하세요\n')
people = in_subway_df[["호선명", "지하철역",time]] #호선명, 지하철역, 찾고자하는 시간대 추출
people = people.iloc[:310]


target = pd.merge(people, df, how = 'left')

df = pd.read_csv('C:/Users/유호인/Downloads/지하철 역위치.csv', encoding='cp949')

pd.set_option('display.max_columns',None) # 전체 열 출력하기
pd.set_option('display.max_rows',None)
target = pd.merge(people, df[['지하철역','경도','위도']], how = 'left')

heat_df = target[['경도', '위도']]

target_nan =  target.dropna() #nan처리

heat_df = target_nan[['경도', '위도']]
heat_data = [[row['위도'], row['경도']]for index, row in heat_df.iterrows()]
HeatMap(heat_data).add_to(seoul_map)

seoul_map.save('C:/Users/유호인/Downloads/seoul_metro.html')
