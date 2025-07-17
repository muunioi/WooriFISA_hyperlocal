import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import plotly.express as px



## MAP ##

import os, json

# !git clone https://github.com/raqoon886/Local_HangJeongDong.git
# os.chdir('./Local_HangJeongDong')


# GeoJSON 불러오기
with open('C://ITStudy//01_python//streamlit_demo//hangjeongdong_서울특별시.geojson', 'r') as f:
    seoul_geo = json.load(f)



# count 정보 불러오기
count_info = pd.read_csv('C://ITStudy//01_python//streamlit_demo//WooriFISA_hyperlocal//data//data_2_cal.csv')

# 필요한 컬럼만 선택 (dong_info, count, gu_info)
count_data = count_info[['dong_info', 'count', 'gu_info']].copy()

# full_name 컬럼 생성 (GeoJSON 매칭용)
count_data['full_name'] = '서울특별시 ' + count_data['gu_info'] + ' ' + count_data['dong_info']
count_data['full_name'] = count_data['full_name'].apply(lambda x: x.replace('.', '·'))

# NaN 값을 0으로 처리
count_data['count'] = count_data['count'].fillna(0)

# GeoJSON에서 전체 지역명 추출
dong_list = []
for feature in seoul_geo['features']:
    dong_name = feature['properties']['adm_nm']
    dong_list.append(dong_name.replace('.', '·'))

# 전체 동 정보 DataFrame 생성
full_data = pd.DataFrame({'full_name': dong_list})

# count_data와 병합
merged_data = full_data.merge(count_data[['full_name', 'count']], on='full_name', how='left')
merged_data['count'] = merged_data['count'].fillna(0)  # 누락값은 0으로 처리

# 히트맵 시각화
fig = px.choropleth_mapbox(
    merged_data,
    geojson=seoul_geo,
    locations='full_name',
    color='count',
    color_continuous_scale='Oranges'
    featureidkey='properties.adm_nm',
    mapbox_style='carto-positron',
    zoom=9.5,
    center={"lat": 37.563383, "lon": 126.996039},
    opacity=0.6,
)

fig.show()
