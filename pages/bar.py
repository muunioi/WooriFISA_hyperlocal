import plotly.graph_objects as go
import pandas as pd
import streamlit as st

# 데이터 생성
home_df = pd.DataFrame({
    '자치구': ['강남구', '서초구', '송파구', '마포구', '강서구', '관악구', '노원구'],
    '평균 전세가(만원)': [85, 82, 76, 63, 50, 46, 39],
    '평균 월세가(만원)': [180, 175, 160, 145, 120, 110, 95]
})
seoul_df = pd.DataFrame({
    '평균 전세가(만원)': [65],
    '평균 월세가(만원)': [135]
})

topics = ['평균 전세가(만원)', '평균 월세가(만원)']
gu_list = home_df['자치구'].tolist()

fig = go.Figure()

# 평균 그래프 (항상 표시)
fig.add_trace(go.Bar(
    x=topics,
    y=[seoul_df[col].values[0] for col in topics],
    name="서울시 평균",
    marker_color="gray"
))

# 각 자치구 그래프 (처음엔 hidden)
for gu in gu_list:
    values = home_df[home_df['자치구'] == gu][topics].values[0]
    fig.add_trace(go.Bar(
        x=topics,
        y=values,
        name=gu,
        visible=False
    ))

# 버튼 만들기
buttons = []
for i, gu in enumerate(gu_list):
    vis = [True] + [False]*len(gu_list)
    vis[i+1] = True  # 해당 자치구 trace만 활성화
    buttons.append(dict(
        label=gu,
        method="update",
        args=[{"visible": vis},
              {"title": f"{gu}와 서울 평균 비교"}]
    ))

# 서울 평균만 보기 버튼
buttons.insert(0, dict(
    label="서울 평균만 보기",
    method="update",
    args=[{"visible": [True] + [False]*len(gu_list)},
          {"title": "서울 평균 비교"}]
))

fig.update_layout(
    updatemenus=[dict(
        type="buttons",
        direction="right",
        x=0.5,
        y=1.2,
        showactive=True,
        buttons=buttons
    )],
    title="서울 평균 비교",
    barmode='group'
)

fig.show()