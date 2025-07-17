import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
    st.plotly_chart(fig)

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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dfs, total_dong_info = load_data(base_dir)

    priority = ["park", "lamp", "cafe"]
    weight = [0.5, 0.3, 0.2]
    total_dong_info = calculate_grades(dfs, total_dong_info, priority, weight)

    option1, option2, option3, submit = sidebar_input()

    with st.expander("📍 사용 설명서?"):
        st.markdown("- 원하는 조건을 선택해 동네를 추천받아보세요!")

    top3 = total_dong_info.head(3)['dong_info'].tolist()
    draw_podium_chart(top3)

    # 서울 평균 계산용
    topic_keys = ["store", "gym", "park", "cafe", "lamp", "bus", "subway"]
    topics = []
    for key in topic_keys:
        df = dfs[f"{key}_df"].rename(columns={'count': f'{key}_count'})
        topics.append((f'{key}_count', df))

    seoul_df = pd.DataFrame({col: df[col].mean() for col, df in topics}, index=[0])

    # 사용자 직접 입력
    input_dong = st.text_input("행정동을 입력하세요:")
    if input_dong:
        if input_dong in total_dong_info['dong_info'].values:
            draw_comparison_chart(input_dong, seoul_df, topics)
        else:
            st.warning("존재하는 행정동을 입력해 주세요.")

    # TOP 3 버튼
    cols = st.columns(3)
    clicked = False
    for i, dong in enumerate(top3):
        if cols[i].button(f"{dong}"):
            draw_comparison_chart(dong, seoul_df, topics)
            clicked = True

    if not clicked and not input_dong:
        st.info("자치구 버튼을 클릭하면 해당 구와 서울 평균이 비교됩니다.")

if __name__ == "__main__":
    main()
