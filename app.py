import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib
import plotly.express as px
import plotly.figure_factory as ff


## INPUT ##
#def get_user_preferance() :

option_list = ['🌳 공원', '👟 헬스장', '🧋 카페', '🐤 안전', '🏪 편의점']

def sidebar_input() -> tuple[str, str, str] :
    
    # st.sidebar.markdown("""
    # <style>
    #     [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
    #         width: 350px;
    #         margin-left: -350px;
    #     }
    # </style>
    # """, unsafe_allow_html=True)

    st.sidebar.markdown("### 내가 원하는 슬세권 포인트는?")
    option1 = st.sidebar.selectbox("1순위", option_list, index=None, placeholder="Select contact method...")
    option2 = st.sidebar.selectbox("2순위", [x for x in option_list if x != option1], index=None, placeholder="Select contact method...")
    option3 = st.sidebar.selectbox("3순위", [x for x in option_list if x not in (option1, option2)], index=None, placeholder="Select contact method...")
            
    st.sidebar.write(f"You selected: {option1} > {option2} > {option3}")
    
    submit_btn = st.sidebar.button('찾아보기')
    return option1, option2, option3, submit_btn


result = sidebar_input()

## RANKING ##
import streamlit as st
import plotly.graph_objects as go

# 순위별 지역명 - 노원구(1위), 동작구(2위), 중랑구(3위)
regions = ['노원구 00동', '동작구 00동', '중랑구 00동']
colors = ["gold", "silver", "peru"]
heights = [2, 1.5, 1]  # 시각적 높이 설정

# 시상대 순서: 2등 (좌), 1등 (가운데), 3등 (우)
x_labels = ["🥈 2위", "🥇 1위", "🥉 3위"]
ordered_regions = [regions[1], regions[0], regions[2]]
ordered_colors = [colors[1], colors[0], colors[2]]
ordered_heights = [heights[1], heights[0], heights[2]]

fig = go.Figure()

for i in range(3):
    fig.add_trace(go.Bar(
        x=[x_labels[i]],
        y=[ordered_heights[i]],
        marker_color=ordered_colors[i],
        text=ordered_regions[i],
        textposition='inside',
        hovertext=f"{ordered_regions[i]}",
        name=ordered_regions[i],
        hoverinfo="skip"
    ))

fig.update_layout(
    title="슬세권 TOP 3",
    height=350,
    showlegend=False,
    bargap=0,  # 간격 제거
    xaxis=dict(title="", tickfont=dict(size=14)),
    yaxis=dict(title="", showticklabels=False),
    plot_bgcolor='rgba(0,0,0,0)',
)

st.plotly_chart(fig)


## BAR ##
animals=['giraffes', 'orangutans', 'monkeys', 'girafffsdes', 'ordafangutans', 'monkdseys']

fig = go.Figure(data=[
    go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23, 10, 15, 15]),
    go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29, 11, 12, 48])
])
# Change the bar mode
fig.update_layout(barmode='group')
st.plotly_chart(fig)


## Bar chart ## 

home = {
    '자치구': ['강남구', '서초구', '송파구', '마포구', '강서구', '관악구', '노원구'],
    '평균 전세가(만원)': [85, 82, 76, 63, 50, 46, 39],
    '평균 월세가(만원)': [180, 175, 160, 145, 120, 110, 95]
}

convenience_store = {
    '자치구': ['강남구', '서초구', '송파구', '마포구', '강서구', '관악구', '노원구'],
    '편의점 수': [10, 12, 11, 9,12,15,7]
}

gym = {
    '자치구': ['강남구', '서초구', '송파구', '마포구', '강서구', '관악구', '노원구'],
    '헬스장 수': [21, 12, 19, 15, 17, 9, 23]
}

park = {
    '자치구': ['강남구', '서초구', '송파구', '마포구', '강서구', '관악구', '노원구'],
    '공원 수': [3, 4, 11, 2, 6, 7, 9]
}

cafe = {
    '자치구': ['강남구', '서초구', '송파구', '마포구', '강서구', '관악구', '노원구'],
    '카페 수': [25, 22, 12, 30, 23, 28, 19]
}

crime = {
    '자치구': ['강남구', '서초구', '송파구', '마포구', '강서구', '관악구', '노원구'],
    '범죄율': [6, 8, 12, 3, 5, 7, 11]
}

lamp = {
    '자치구': ['강남구', '서초구', '송파구', '마포구', '강서구', '관악구', '노원구'],
    '가로등 수': [51, 90, 70, 66, 95, 83, 89]
}

bus = {
    '자치구': ['강남구', '서초구', '송파구', '마포구', '강서구', '관악구', '노원구'],
    '버스정류장 수': [30, 23, 50, 34, 62, 54, 60]
}

subway = {
    '자치구': ['강남구', '서초구', '송파구', '마포구', '강서구', '관악구', '노원구'],
    '지하철 호선 수': [6, 7, 4, 5, 6, 7, 4]
}

seoul_home = {
    '평균 전세가(만원)': [65],
    '평균 월세가(만원)': [135],
    '편의점 수': [8],
    '헬스장 수': [16],
    '공원 수': [6],
    '카페 수': [28],
    '범죄율': [5],
    '가로등 수': [75],
    '버스정류장 수': [32],
    '지하철 호선 수': [11]
}

home_df = pd.DataFrame(home)
convenience_store_df = pd.DataFrame(convenience_store)
gym_df = pd.DataFrame(gym)
park_df = pd.DataFrame(park)
cafe_df = pd.DataFrame(cafe)
crime_df = pd.DataFrame(crime)
lamp_df = pd.DataFrame(lamp)
bus_df = pd.DataFrame(bus)
subway_df = pd.DataFrame(subway)
seoul_df = pd.DataFrame(seoul_home)




topics = [
    ('평균 전세가(만원)', home_df),
    ('평균 월세가(만원)', home_df),
    ('편의점 수', convenience_store_df),
    ('헬스장 수', gym_df),
    ('공원 수', park_df),
    ('카페 수', cafe_df),
    ('범죄율', crime_df),
    ('가로등 수', lamp_df),
    ('버스정류장 수', bus_df),
    ('지하철 호선 수', subway_df)
]

topic_names = [col_name for col_name, _ in topics]
gu_list = home_df['자치구'].unique()   # 자치구 리스트는 home_df에서 가져오는게 안전
cols = st.columns(len(gu_list))

input_gu = st.text_input("자치구를 입력하세요:")



if input_gu in gu_list:
    gu_values = []
    seoul_means = []
    for topic_name, df in topics:
        val = df[df['자치구'] == input_gu][topic_name].values[0]
        gu_values.append(val)
        seoul_mean = seoul_df[topic_name].values[0]
        seoul_means.append(seoul_mean)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=topic_names,
        y=gu_values,
        name=input_gu,
        marker_color='blue'
    ))
    fig.add_trace(go.Bar(
        x=topic_names,
        y=seoul_means,
        name='서울시 평균',
        marker_color=('grey')
    ))
    fig.update_layout(
        barmode='group',
        bargap=0.15,
        title=f'{input_gu}와 서울 평균 비교',
        xaxis_title="항목",
        yaxis_title="수치"
    )
    st.plotly_chart(fig, use_container_width=True, key=f"{input_gu}_chart")

elif input_gu:
    st.warning("존재하는 자치구명을 입력해 주세요.")

fig = None   # 클릭 전에는 fig 없음

for i, gu in enumerate(gu_list):
    if cols[i].button(f'{gu}'):
        # 해당 자치구의 값 추출
        gu_values = []
        seoul_means = []
        for topic_name, df in topics:
            # 자치구 값
            val = df[df['자치구'] == gu][topic_name].values[0]
            gu_values.append(val)
            # 서울 평균값
            seoul_mean = seoul_df[topic_name].values[0]
            seoul_means.append(seoul_mean)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=topic_names,
            y=gu_values,
            name=gu,
            marker_color = 'blue'
        ))
        fig.add_trace(go.Bar(
            x=topic_names,
            y=seoul_means,
            name='서울시 평균',
            marker_color='grey'
        ))
        fig.update_layout(
            barmode='group',
            bargap=0.15,
            title=f'{gu}와 서울 평균 비교',
            xaxis_title="항목",
            yaxis_title="수치",
            yaxis=dict(range=[0, 200])
        )
        st.plotly_chart(fig, use_container_width=True, key=f"{gu}_chart")

# 버튼이 아무것도 클릭되지 않은 경우엔 안내만
if fig is None:
    st.info("자치구 버튼을 클릭하면 해당 구와 서울 평균이 비교됩니다.")