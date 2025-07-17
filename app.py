import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib
import plotly.express as px


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
