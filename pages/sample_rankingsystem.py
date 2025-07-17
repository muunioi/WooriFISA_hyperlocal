import pandas as pd

import os
import pandas as pd

# 현재 파일 위치 기준으로 상위 디렉토리의 data/test.csv 접근
base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치
print(base_dir)


# 전체 dong에 기본값 0인 grade column 추가 (추후 점수을 합산할 data frame)
total_dong_info = pd.read_csv(f'{base_dir}/../data/dong_gu_info.csv')
total_dong_info["grade"] = 0

filenames = ["data_2_cal","data_5_cal","data_6_cafe_cal","data_6_gym_cal","data_6_store_cal", "data_7_cal","data_9_cal"]
# filenames = ["data_2_cal","data_6_cafe_cal"]

df_name = ["park_df","lamp_df", "cafe_df", "gym_df", "store_df", "bus_df", "subway_df"]

dfs = {}
for i, name in enumerate(df_name) :
    
    dfs[name] = pd.read_csv(f'{base_dir}/../data/{filenames[i]}.csv')

# 만약 cafe, gym, park 순위가 매겨진다면
# priority = ["cafe", "gym", "park"]
# priority = [ "store", "park","cafe"]
priority = ["park","lamp","cafe"]
weight = [0.5, 0.3, 0.2]

def cal_rank_to_grade(rank, w, l):
    return ((rank * 100) / l) * w # ((역순위 * 100(점)) / 길이) * 가중치

for i,pri in enumerate(priority):
    
    df_sorted = dfs[f'{pri}_df'].sort_values(by='num_per_area', ascending=False)

    df_sorted['rank'] = df_sorted['num_per_area'].rank(method='min', ascending=True).astype(int)
    df_sorted.loc[:,"grade"] = df_sorted.apply(lambda row :cal_rank_to_grade(row["rank"], weight[i], len(df_sorted)), axis = 1)
    df_sorted = df_sorted.reset_index(drop=True)
    df_sorted_for_merge = df_sorted[["dong_info", "grade"]]
    total_dong_info = total_dong_info.merge(df_sorted_for_merge, on='dong_info', how='right', suffixes=('_old', ''))
    total_dong_info['grade'] = total_dong_info['grade_old'] + total_dong_info['grade'].fillna(0)    

    if "grade_old" in total_dong_info.columns:
        total_dong_info = total_dong_info.drop(["grade_old"], axis= 1)

    if "gu_info_old" in total_dong_info.columns:
        total_dong_info = total_dong_info.drop(["gu_info_old"], axis= 1)

    if "rank_old" in total_dong_info.columns:
        total_dong_info = total_dong_info.drop(["rank_old"], axis= 1)
    # total_dong_info["grade"] += df_sorted["grade"].fillna(0)
    # break
    dfs[f'{pri}_df']  = df_sorted
    # print(dfs[f'{pri}_df'])
    # print(total_dong_info)
    # print("i")

total_dong_info = total_dong_info.sort_values(by='grade', ascending=False)

print("final")
print(total_dong_info)
# print(dfs["park_df"])
