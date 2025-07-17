import pandas as pd
import plotly.express as px
import streamlit as st

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

dfs = []

for category, filepath in category_files.items():
    df = pd.read_csv(filepath)
    
    # 지역구 기준, num_per_area 합산
    grouped = df.groupby("gu_info")["count"].sum().reset_index()
    grouped.columns = ["구", category]  # 컬럼명 통일
    
    dfs.append(grouped)

# 구별 병합
df_total = dfs[0]
for df_next in dfs[1:]:
    df_total = df_total.merge(df_next, on="구", how="outer")

# 결과 확인
print(df_total)


# melt을 이용해서 '구', '시설', '개수' 형태로 변환
df_melted = df_total.melt(id_vars="구", var_name="시설", value_name="개수")


fig = px.treemap(
    df_melted,
    path=["구", "시설"],     # 계층 구조: 구 → 시설
    values="개수",           # 각 박스의 크기 기준
    color="시설",            # 색상 기준
    title="지역구별 편의시설 분포 트리맵"
)

fig.update_traces(root_color="lightgrey")  # 루트 컬러 스타일
fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))  # 여백 조정



#st.set_page_config(layout="wide")
st.title("📍 지역구별 편의시설 트리맵")
 
st.plotly_chart(fig, use_container_width=True)
