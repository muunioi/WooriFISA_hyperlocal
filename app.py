import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib
import plotly.express as px
import plotly.figure_factory as ff
import os

# 현재 파일 위치 기준으로 상위 디렉토리의 data/test.csv 접근
base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치
#print(base_dir)
# 전체 dong에 기본값 0인 grade column 추가 (추후 점수을 합산할 data frame)
#total_dong_info = pd.read_csv(f'{base_dir}/../data/dong_gu_info.csv')


# total_dong_info = pd.read_csv('.//data//dong_gu_info.csv')
total_dong_info = os.path.join(base_dir, 'data', 'dong_gu_info.csv')
total_dong_info = pd.read_csv(total_dong_info)

total_dong_info["grade"] = 0
filenames = ["data_2_cal","data_5_cal","data_6_cafe_cal","data_6_gym_cal","data_6_store_cal", "data_7_cal","data_9_cal"]
df_name = ["park_df","lamp_df", "cafe_df", "gym_df", "store_df", "bus_df", "subway_df"]
dfs = {}
for i, name in enumerate(df_name) :
    tmp_dir = os.path.join(base_dir, 'data', f'{filenames[i]}.csv')
    dfs[name] = pd.read_csv(tmp_dir)

priority = ["park","lamp","cafe"]
weight = [0.5, 0.3, 0.2]
def cal_rank_to_grade(rank, w, l):
    return ((rank * 100) / l) * w # ((역순위 * 100(점)) / 길이) * 가중치


for i,pri in enumerate(priority):
    df_sorted = dfs[f'{pri}_df'].sort_values(by='num_per_area', ascending=False)
    df_sorted['rank'] = df_sorted['num_per_area'].rank(method='min', ascending=True).astype(int)
    df_sorted['grade_tmp'] = df_sorted.apply(lambda row: cal_rank_to_grade(row["rank"], weight[i], len(df_sorted)), axis=1)
    
    
    # 선택 컬럼만 merge
    df_sorted_for_merge = df_sorted[['dong_info', 'grade_tmp', 'count']].rename(columns={'grade_tmp': f'{pri}_grade', 'count': f'{pri}_count'})
    total_dong_info = total_dong_info.merge(df_sorted_for_merge, on='dong_info', how='left')
    

# grade 합산
grade_cols = [f"{pri}_grade" for pri in priority]
total_dong_info["grade"] = total_dong_info[grade_cols].sum(axis=1, skipna=True)

# 정렬
total_dong_info = total_dong_info.sort_values(by='grade', ascending=False)


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



with st.expander("📍 사용 설명서? "):
    st.markdown("""
    - 토글 있네~~~
    """)

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

# home_df = pd.DataFrame(home)
tmp_store = os.path.join(base_dir, 'data', 'data_6_store_cal.csv')
store_df = pd.read_csv(tmp_store)
tmp_gym = os.path.join(base_dir, 'data', 'data_6_gym_cal.csv')
gym_df = pd.read_csv(tmp_gym)
tmp_park = os.path.join(base_dir, 'data', 'data_2_cal.csv')
park_df = pd.read_csv(tmp_park)
tmp_cafe = os.path.join(base_dir, 'data', 'data_6_cafe_cal.csv')
cafe_df = pd.read_csv(tmp_cafe)
#  crime_df = pd.DataFrame(crime)
tmp_lamp = os.path.join(base_dir, 'data', 'data_5_cal.csv')
lamp_df = pd.read_csv(tmp_lamp)
tmp_bus = os.path.join(base_dir, 'data', 'data_7_cal.csv')
bus_df = pd.read_csv(tmp_bus)
tmp_subway = os.path.join(base_dir, 'data', 'data_9_cal.csv')
subway_df = pd.read_csv(tmp_subway)

# count 열이 겹치면 안되므로
store_df.rename(columns = {'count':'store_count'}, inplace=True)
gym_df.rename(columns = {'count':'gym_count'}, inplace = True)
park_df.rename(columns = {'count':'park_count'}, inplace = True)
cafe_df.rename(columns = {'count':'cafe_count'}, inplace = True)
lamp_df.rename(columns = {'count':'lamp_count'}, inplace = True)
bus_df.rename(columns = {'count':'bus_count'}, inplace = True)
subway_df.rename(columns = {'count':'subway_count'}, inplace = True)

# 각 카운트 수의 평균 -> 서울시 평균 개수
store_avg = store_df['store_count'].mean()
gym_avg = gym_df['gym_count'].mean()
park_avg = park_df['park_count'].mean()
cafe_avg = cafe_df['cafe_count'].mean()
lamp_avg = lamp_df['lamp_count'].mean()
bus_avg = bus_df['bus_count'].mean()
subway_avg = subway_df['subway_count'].mean()

# 서울시 평균 count 수 DataFrame 생성
seoul_df = pd.DataFrame([{
    'store_count' : store_avg,
    'gym_count' : gym_avg,
    'park_count' : park_avg,
    'cafe_count' : cafe_avg,
    'lamp_count' : lamp_avg,
    'bus_count' : bus_avg,
    'subway_count' : subway_avg
}])


topics = [
#    ('평균 전세가(만원)', seoul_df),
#    ('평균 월세가(만원)', seoul_df),
    ('store_count', store_df),
    ('gym_count', gym_df),
    ('park_count', park_df),
    ('cafe_count', cafe_df),
#    ('범죄율', crime_df),
    ('lamp_count', lamp_df),
    ('bus_count', bus_df),
    ('subway_count', subway_df)
]

topic_names = [col_name for col_name, _ in topics]
dong_list = store_df['dong_info'].unique()
cols = st.columns(len(dong_list))

input_dong = st.text_input("행정동을 입력하세요:")



if input_dong in dong_list:
    dong_values = []
    seoul_means = []
    for topic_name, df in topics:
        val = df[df['dong_info'] == input_dong][topic_name].values[0]
        dong_values.append(val)
        seoul_mean = seoul_df[topic_name].values[0]
        seoul_means.append(seoul_mean)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=topic_names,
        y=dong_values,
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

top3 = total_dong_info.head(3) 
top3_dongs = top3['dong_info'].tolist()

cols = st.columns(3)
for i, dong in enumerate(top3_dongs):
    if cols[i].button(f"{dong}"):
        dong_values = []
        seoul_means = []
        for topic_name, df in topics:
            filtered = df.loc[df['dong_info'] == dong, topic_name]
            if not filtered.empty:
                val = filtered.values[0]
            else:
                val = None
            dong_values.append(val)
            #print(f'데이터 프레임: {df}')
            #print(f'topic_name: {topic_name}')
            #print(f'detail: {df[df['dong_info'] == dong][topic_name]}')
            #val = df[df['dong_info'] == dong][topic_name].values[0]
            #val = df.loc[df['dong_info'] == dong][topic_name][0]
            # dong_values.append(val)
            seoul_mean = seoul_df[topic_name].values[0]
            seoul_means.append(seoul_mean)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=topic_names,
            y=dong_values,
            name=dong,
            marker_color='blue'
        ))
        fig.add_trace(go.Bar(
            x=topic_names,
            y=seoul_means,
            name='서울 평균',
            marker_color='grey'
        ))
        fig.update_layout(
            barmode='group',
            bargap=0.15,
            title=f'{dong}와 서울 평균 비교',
            xaxis_title="항목",
            yaxis_title="수치"
        )
        st.plotly_chart(fig, use_container_width=True, key=f"{dong}_chart")

# 버튼이 아무것도 클릭되지 않은 경우엔 안내만
if fig is None:
    st.info("자치구 버튼을 클릭하면 해당 구와 서울 평균이 비교됩니다.")