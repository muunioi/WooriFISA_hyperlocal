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

# home_df = pd.read_csv("")
store_df = pd.read_csv("C:\fisa01\WooriFISA_hyperlocal\data\data_6_store_cal.csv")
gym_df = pd.read_csv("C:\fisa01\WooriFISA_hyperlocal\data\data_6_gym_cal.csv")
park_df = pd.read_csv("C:\fisa01\WooriFISA_hyperlocal\data\data_2_cal.csv")
cafe_df = pd.read_csv("C:\fisa01\WooriFISA_hyperlocal\data\data_6_cafe_cal.csv")
# crime_df = pd.read_csv("C:\fisa01\WooriFISA_hyperlocal\data\data_4_cal.csv") # 값의 차이가 너무 커서 설명란에 넣을 예정
lamp_df = pd.read_csv("C:\fisa01\WooriFISA_hyperlocal\data\data_5_cal.csv")
bus_df = pd.read_csv("C:\fisa01\WooriFISA_hyperlocal\data\data_7_cal.csv")
subway_df = pd.read_csv("C:\fisa01\WooriFISA_hyperlocal\data\data_9_cal.csv")

store_df.rename(colums={'count':'store_count'})
gym_df.rename(columns={'count':'gym_count'})
park_df.rename(columns={'count':'park_count'})
cafe_df.rename(columns={'count':'cafe_count'})
lamp_df.rename(columns={}) 

# seoul_df = pd.DataFrame(seoul_home)


topics = [
#    ('평균 전세가(만원)', home_df),
#    ('평균 월세가(만원)', home_df),
    ('count', store_df),
    ('count', gym_df),
    ('count', park_df),
    ('count', cafe_df),
#    ('count', crime_df),
    ('count', lamp_df),
    ('count', bus_df),
    ('count', subway_df)
]

topic_names = [col_name for col_name, _ in topics]
dong_list = store_df['dong_info'].unique()  
cols = st.columns(len(dong_list))

input_dong = st.text_input("행정동을 입력하세요:")



if input_dong in dong_list:
    gu_values = []
    seoul_means = []
    for topic_name, df in topics:
        val = df[df['dong_info'] == input_dong][topic_name].values[0]
        gu_values.append(val)
        seoul_mean = seoul_df[topic_name].values[0]
        seoul_means.append(seoul_mean)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=topic_names,
        y=gu_values,
        name=input_dong,
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
        title=f'{input_dong}와 서울 평균 비교',
        xaxis_title="항목",
        yaxis_title="수치"
    )
    st.plotly_chart(fig, use_container_width=True, key=f"{input_dong}_chart")

elif input_dong:
    st.warning("존재하는 자치구명을 입력해 주세요.")

fig = None   # 클릭 전에는 fig 없음

for i, dong in enumerate(dong_list):
    if cols[i].button(f'{dong}'):
        # 해당 자치구의 값 추출
        gu_values = []
        seoul_means = []
        for topic_name, df in topics:
            # 자치구 값
            val = df[df['자치구'] == dong][topic_name].values[0]
            gu_values.append(val)
            # 서울 평균값
            seoul_mean = seoul_df[topic_name].values[0]
            seoul_means.append(seoul_mean)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=topic_names,
            y=gu_values,
            name=dong,
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
            title=f'{dong}와 서울 평균 비교',
            xaxis_title="항목",
            yaxis_title="수치",
            yaxis=dict(range=[0, 200])
        )
        st.plotly_chart(fig, use_container_width=True, key=f"{dong}_chart")

# 버튼이 아무것도 클릭되지 않은 경우엔 안내만
if fig is None:
    st.info("행정동 버튼을 클릭하면 해당 구와 서울 평균이 비교됩니다.")