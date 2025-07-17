import streamlit as st
import pandas as pd
import json
import plotly.express as px
import os
import numpy as np

#### HitMap ####


# GeoJSON 불러오기
with open('.//data//hangjeongdong.geojson', 'r') as f:
    seoul_geo = json.load(f)

# 전체 동 리스트 확보
# dong_list = [feature['properties']['adm_nm'].replace('.', '·') for feature in seoul_geo['features']]
# full_data = pd.DataFrame({'full_name': dong_list})

dong_gu = pd.read_csv('.//data//dong_gu_info.csv')
dong_gu['full_name'] = '서울특별시 ' + dong_gu['gu_info'] + ' ' + dong_gu['dong_info']
dong_gu['full_name'] = dong_gu['full_name'].str.replace('.', '·')
full_data = dong_gu[['full_name']].copy()

missing_dongs = [feature['properties']['adm_nm'] for feature in seoul_geo['features'] 
                 if feature['properties']['adm_nm'].replace('.', '·') not in dong_gu['full_name'].values]
print(missing_dongs)

# 데이터 디렉토리 설정

category_files = {
    '공원': './/data//data_2_cal.csv',
    #'범죄': './/data//data_4_cal.csv',
    '가로등': './/data//data_5_cal.csv',
    '카페': './/data//data_6_cafe_cal.csv',
    '헬스장': './/data//data_6_gym_cal.csv',
    '편의점': './/data//data_6_store_cal.csv',
    '버스정류장': './/data//data_7_cal.csv',
    '지하철': './/data//data_9_cal.csv',
}

#categor_colors = ['BuGn', 'YIOrRd', 'Cividis', 'PuRd', 'amp', 'Blues', 'Mint', 'deep']
# 기존 count 컬럼에서 log 변환 (1 더해주는 건 log(0) 에러 방지)


category_colors = {
    '공원': 'BuGn',
    #'범죄': 'YlOrRd',
    '가로등': 'Cividis',
    '카페': 'PuRd',
    '헬스장': 'amp',
    '편의점': 'Blues',
    '버스정류장': 'Mint',
    '지하철': 'deep',
}

maps = []

for category, filepath in category_files.items():
    try:
        df = pd.read_csv(filepath)
        df['full_name'] = '서울특별시 ' + df['gu_info'] + ' ' + df['dong_info']
        df['full_name'] = df['full_name'].str.replace('.', '·')
        df['count'] = df['count'].fillna(0)

        merged = full_data.merge(df[['full_name', 'count']], on='full_name', how='left')
        merged['count'] = merged['count'].fillna(0)
        merged['log_count'] = np.log1p(merged['count'])  # == log(count + 1)

        ## 카테고리와 일치하는 컬러맵 선택
        cmap = category_colors.get(category, 'Oranges')

        fig = px.choropleth_mapbox(
            merged,
            geojson=seoul_geo,
            locations='full_name',
            color='log_count',
            color_continuous_scale=cmap,
            hover_data={'full_name': True, 'count': True, 'log_count': False},

            featureidkey='properties.adm_nm',
            mapbox_style='carto-positron',
            zoom=9.5,
            center={"lat": 37.563383, "lon": 126.996039},
            opacity=0.6,
        )

        maps.append((category, fig))
    except Exception as e:
        st.warning(f"⚠️ '{category}' 데이터 처리 중 오류 발생: {e}")

st.title("서울특별시 히트맵 대시보드")

tabs = st.tabs([key.capitalize() for key in category_files.keys()])

for tab, (name, fig) in zip(tabs, maps):
    with tab:
        st.subheader(f"🗺️ {name.capitalize()} 기준 히트맵")
        st.plotly_chart(fig, use_container_width=True)

# maps = []
# for fname in file_list:
#     filepath = os.path.join(data_dir, fname)
#     df = pd.read_csv(filepath)

#     # 필수 컬럼 정리
#     df['full_name'] = '서울특별시 ' + df['gu_info'] + ' ' + df['dong_info']
#     df['full_name'] = df['full_name'].str.replace('.', '·')
#     df['count'] = df['count'].fillna(0)

#     # 병합으로 누락 지역 보정
#     merged = full_data.merge(df[['full_name', 'count']], on='full_name', how='left')
#     merged['count'] = merged['count'].fillna(0)

#     # 히트맵 생성
#     fig = px.choropleth_mapbox(
#         merged,
#         geojson=seoul_geo,
#         locations='full_name',
#         color='count',
#         color_continuous_scale='Oranges',
#         featureidkey='properties.adm_nm',
#         mapbox_style='carto-positron',
#         zoom=9.5,
#         center={"lat": 37.563383, "lon": 126.996039},
#         opacity=0.6,
#     )

#     maps.append((fname, fig))  # 파일명과 지도 저장


# st.title("📊 다중 히트맵 대시보드")

# tab_list = st.tabs([f.replace('.csv', '') for f, _ in maps])
# for tab, (title, fig) in zip(tab_list, maps):
#     with tab:
#         st.subheader(f"🗺️ {title} 기준 히트맵")
#         st.plotly_chart(fig, use_container_width=True)

# # count 정보 불러오기
# count_info = pd.read_csv('.//data//data_2_cal.csv')

# # 필요한 컬럼만 선택 (dong_info, count, gu_info)
# count_data = count_info[['dong_info', 'count', 'gu_info']].copy()

# # full_name 생성
# count_info['full_name'] = '서울특별시 ' + count_info['gu_info'] + ' ' + count_info['dong_info']
# count_info['full_name'] = count_info['full_name'].str.replace('.', '·')

# # NaN 값을 0으로 처리
# count_info['count'] = count_info['count'].fillna(0)



# # 병합
# merged = full_data.merge(count_info[['full_name', 'count']], on='full_name', how='left')
# merged['count'] = merged['count'].fillna(0)

# # 👉 Streamlit 화면 구성
# st.title("서울특별시 히트맵 대시보드")

# col1, col2 = st.tabs(["Count 히트맵", "고령자 히트맵"])

# with col1:
#     st.subheader("🗺️ Count 기준 히트맵")
#     fig1 = px.choropleth_mapbox(
#         merged,
#         geojson=seoul_geo,
#         locations='full_name',
#         color='count',
#         color_continuous_scale='Oranges',
#         featureidkey='properties.adm_nm',
#         mapbox_style='carto-positron',
#         zoom=9.5,
#         center={"lat": 37.563383, "lon": 126.996039},
#         opacity=0.6,
#     )
#     st.plotly_chart(fig1, use_container_width=True)

# with col2:
#     st.subheader("🌡️ 예시: 랜덤 값 히트맵")
#     import numpy as np
#     merged['random_metric'] = np.random.randint(0, 100, size=len(merged))
#     fig2 = px.choropleth_mapbox(
#         merged,
#         geojson=seoul_geo,
#         locations='full_name',
#         color='random_metric',
#         color_continuous_scale='Viridis',
#         featureidkey='properties.adm_nm',
#         mapbox_style='carto-positron',
#         zoom=9.5,
#         center={"lat": 37.563383, "lon": 126.996039},
#         opacity=0.6,
#     )
#     st.plotly_chart(fig2, use_container_width=True)
