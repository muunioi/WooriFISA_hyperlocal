import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import uuid

### 1. 데이터 불러오기 및 초기 설정 ###
@st.cache_data
def load_data(base_dir):
    filenames = {
        "park_df": "data_2_cal.csv",
        "lamp_df": "data_5_cal.csv",
        "cafe_df": "data_6_cafe_cal.csv",
        "gym_df": "data_6_gym_cal.csv",
        "store_df": "data_6_store_cal.csv",
        "bus_df": "data_7_cal.csv",
        "subway_df": "data_9_cal.csv"
    }

    dfs = {}
    for name, file in filenames.items():
        path = os.path.join(base_dir, 'data', file)
        dfs[name] = pd.read_csv(path)

    total_dong_info = pd.read_csv(os.path.join(base_dir, 'data', 'dong_gu_info.csv'))
    total_dong_info["grade"] = 0

    return dfs, total_dong_info

### 2. 점수 계산 함수 ###
def calculate_grades(dfs, total_dong_info, priority, weight):
    def cal_rank_to_grade(rank, w, l):
        return ((rank * 100) / l) * w

    for i, pri in enumerate(priority):
        df_sorted = dfs[f'{pri}_df'].sort_values(by='num_per_area', ascending=False)
        df_sorted['rank'] = df_sorted['num_per_area'].rank(method='min', ascending=True).astype(int)
        df_sorted['grade_tmp'] = df_sorted.apply(
            lambda row: cal_rank_to_grade(row["rank"], weight[i], len(df_sorted)), axis=1)

        df_merge = df_sorted[['dong_info', 'grade_tmp', 'count']].rename(
            columns={'grade_tmp': f'{pri}_grade', 'count': f'{pri}_count'})
        total_dong_info = total_dong_info.merge(df_merge, on='dong_info', how='left')

    grade_cols = [f"{pri}_grade" for pri in priority]
    total_dong_info["grade"] = total_dong_info[grade_cols].sum(axis=1, skipna=True)
    return total_dong_info.sort_values(by='grade', ascending=False)

### 3. 사이드바 입력 ###
def sidebar_input():
    option_list = ['🌳 공원', '👟 헬스장', '🧋 카페', '🐤 안전', '🏪 편의점']
    st.sidebar.markdown("### 내가 원하는 슬세권 포인트는?")
    option1 = st.sidebar.selectbox("1순위", option_list, index=None)
    option2 = st.sidebar.selectbox("2순위", [x for x in option_list if x != option1], index=None)
    option3 = st.sidebar.selectbox("3순위", [x for x in option_list if x not in (option1, option2)], index=None)
    submit_btn = st.sidebar.button('찾아보기')
    return option1, option2, option3, submit_btn

### 4. TOP 3 시상대 시각화 ###
def draw_podium_chart(top3_dongs):
    regions = top3_dongs
    colors = ["gold", "silver", "peru"]
    heights = [2, 1.5, 1]
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
            hoverinfo="skip"
        ))

    fig.update_layout(
        title="슬세권 TOP 3",
        height=350,
        showlegend=False,
        bargap=0,
        xaxis=dict(title="", tickfont=dict(size=14)),
        yaxis=dict(title="", showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, key=f'{uuid.uuid4()}')

### 5. 바 차트 시각화 ###
def draw_comparison_chart(dong, seoul_df, topics):
    topic_names = [col for col, _ in topics]
    dong_values, seoul_means = [], []

    for col_name, df in topics:
        val = df[df['dong_info'] == dong][col_name].values
        dong_values.append(val[0] if len(val) else 0)
        seoul_means.append(seoul_df[col_name].values[0])

    fig = go.Figure()
    fig.add_trace(go.Bar(x=topic_names, y=dong_values, name=dong, marker_color='blue'))
    fig.add_trace(go.Bar(x=topic_names, y=seoul_means, name='서울 평균', marker_color='grey'))

    fig.update_layout(
        barmode='group',
        bargap=0.15,
        title=f'{dong}와 서울 평균 비교',
        xaxis_title="항목",
        yaxis_title="수치"
    )
    st.plotly_chart(fig, use_container_width=True, key=f"{dong}_chart")

### 6. 메인 앱 실행 ###
def main():

    st.set_page_config(layout="wide")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dfs, total_dong_info = load_data(base_dir)

    
    weight = [0.5, 0.3, 0.2]
    

    option1, option2, option3, submit = sidebar_input()
    tmp_dict = {
        '🌳 공원': 'park', 
        '👟 헬스장': 'gym',
        '🧋 카페': 'cafe', 
        '🐤 안전': 'lamp', 
        '🏪 편의점': 'store'
    }
    
    with st.expander("🐤 슬세권이란?"):
        st.markdown("""
                    - 슬세권은 **'슬리퍼'** 와 **'~세권'** 을 합쳐 만든 신조어로, 슬리퍼를 신고 편하게 다닐 수 있는 거리 내에 편의시설 (마트, 영화관, 커피전문점, 은행 등)이 있는 주거 지역을 의미해요!
                    - **편안한 복장으로 편리하게 생활 인프라를 이용** 할 수 있는 곳을 뜻합니다✨
                    """)
        
    with st.expander("## 🙌 슬세권을 현명하게 이용하는 방법!"):
        st.markdown("""
                    1. 나는 슬리퍼를 신고 어디까지 갈 수 있을까?
                    - 카페, 편의점, 헬스장, 공원, 안전 중에서 가장 중요하게 생각하는 편의시설 3가지를 선택해주세요.

                    2. 내 기준에 딱 맞는 동네 TOP 3 보기
                    - 선택한 인프라가 제일 잘 갖춰진 동네들을 시상대처럼 1, 2, 3위로 뽑아줍니다! (슬리퍼 신고 살기 딱 좋은 동네들이에요😎)

                    3. 이 동네가 좋은 이유는 뭘까?
                    - 서울 평균이랑 비교한 바 그래프로 진짜 편의시설이 많은지 수치로 확인해보세요.

                    4. 서울 전체를 둘러보고 싶다면?
                    - 왼쪽 메뉴에서 히트맵을 눌러보세요. 지역별로 어떤 시설이 얼마나 많은지 한눈에 보여줍니다!

                    > **슬리퍼는 편한데, 동네까지 불편하면 안 되잖아요? 슬세권으로 내 생활 반경을 똑똑하게 찾아보세요 👟✨**
                    """)
    
    if option1 and option2 and option3 and submit :
    # if not option1 or not option2 or not option3 or not submit :
        # st.stop()
        p1 = tmp_dict[option1] if option1 in tmp_dict else ''
        p2 = tmp_dict[option2] if option2 in tmp_dict else ''
        p3 = tmp_dict[option3] if option3 in tmp_dict else ''
        
        priority = [p1, p2, p3]
        
        total_dong_info = calculate_grades(dfs, total_dong_info, priority, weight)
        top3 = total_dong_info.head(3)['dong_info'].tolist()
        

        # draw_podium_chart(top3)
        st.session_state.priority = priority
        st.session_state.weight = weight
        st.session_state.total_dong_info = total_dong_info
        st.session_state.top3 = total_dong_info.head(3)['dong_info'].tolist()
        st.session_state.selected_dong = st.session_state.top3[0]  # 1위 자동 선택
        
        

        # 서울 평균 계산용
        topic_keys = ["store", "gym", "park", "cafe", "lamp", "bus", "subway"]
        topics = []
        for key in topic_keys:
            df = dfs[f"{key}_df"].rename(columns={'count': f'{key}_count'})
            topics.append((f'{key}_count', df))
        
        seoul_df = pd.DataFrame({col: df[col].mean() for col, df in topics}, index=[0])
        
        st.session_state.seoul_df = seoul_df
        st.session_state.topics = topics

        # draw_comparison_chart(top3[0], seoul_df, topics)

        # # 사용자 직접 입력
        # # input_dong = st.text_input("행정동을 입력하세요:")
        # # if input_dong:
        # #     if input_dong in total_dong_info['dong_info'].values:
        # #         draw_comparison_chart(input_dong, seoul_df, topics)
        # #     else:
        # #         st.warning("존재하는 행정동을 입력해 주세요.")

        # # TOP 3 버튼
        # cols = st.columns(3)
        # clicked = False
        print("click1")
        # st.button("hey")
        # for i, dong in enumerate(top3):
        #     if cols[i].button(f"{dong}"):
        #         print("click", dong)
        #         draw_comparison_chart(dong, seoul_df, topics)
        #         clicked = True

    # 2. 버튼은 항상 렌더링되도록 (데이터가 준비된 경우만)
    if 'top3' in st.session_state:
        draw_podium_chart(st.session_state.top3)
        st.markdown("### 🏆 TOP 3 지역")
        cols = st.columns(3)
        
        for i, dong in enumerate(st.session_state.top3):
            if cols[i].button(f"{dong}"):
                st.session_state.selected_dong = dong
                print(f"✅ 버튼 클릭됨: {dong}")
    
    # 3. 선택된 동에 대한 바 차트 출력
    if 'selected_dong' in st.session_state:
        draw_comparison_chart(st.session_state.selected_dong, st.session_state.seoul_df, st.session_state.topics)
    # if not clicked:
    #     st.info("자치구 버튼을 클릭하면 해당 구와 서울 평균이 비교됩니다.")

if __name__ == "__main__":
    main()