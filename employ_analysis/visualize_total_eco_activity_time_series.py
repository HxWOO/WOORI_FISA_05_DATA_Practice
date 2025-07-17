# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import os

def _get_column_for_year(df, base_col_name, year):
    """지정된 연도와 기본 컬럼명에 따라 가장 적합한 컬럼명을 찾습니다.
    하반기(2/2) -> 상반기(1/2) -> 전체 연도 순으로 우선순위를 가집니다.
    """
    # 2/2 (하반기) 데이터 시도
    col_name_2_2 = f'{year}.2/2_{base_col_name}'
    if col_name_2_2 in df.columns:
        return col_name_2_2

    # 1/2 (상반기) 데이터 시도
    col_name_1_2 = f'{year}.1/2_{base_col_name}'
    if col_name_1_2 in df.columns:
        return col_name_1_2

    # 전체 연도 데이터 시도 (2013-2021년 데이터 형식)
    col_name_full_year = f'{year}_{base_col_name}'
    if col_name_full_year in df.columns:
        return col_name_full_year

    return None # 해당 연도의 컬럼을 찾을 수 없음

def create_total_activity_time_series_chart():
    """전체 장애인 경제활동인구 및 비경제활동인구의 시계열 데이터를 Plotly 라인 차트로 시각화하여 Figure 객체를 반환합니다."""
    file_path = f"{Path(__file__).parent.parent}/results/processed_disable_age.xlsx"
    
    if not os.path.exists(file_path):
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        return None

    df = pd.read_excel(file_path)
    
    # '전체' 행에서 데이터 추출
    total_df = df[df[df.columns[0]] == '전체'].copy()

    if total_df.empty:
        print("오류: '전체' 데이터를 찾을 수 없습니다. 파일 구조를 확인하세요.")
        return None

    years = list(range(2013, 2025))
    eco_values = []
    none_eco_values = []

    for year in years:
        eco_col = _get_column_for_year(total_df, "경제활동인구 (명)", year)
        none_eco_col = _get_column_for_year(total_df, "비경제활동인구 (명)", year)
        
        if eco_col and none_eco_col:
            eco_values.append(int(total_df[eco_col].iloc[0]))
            none_eco_values.append(int(total_df[none_eco_col].iloc[0]))
        else:
            # 데이터가 없는 경우 None 또는 0으로 처리하거나, 해당 연도를 건너뛸 수 있습니다.
            # 여기서는 None으로 처리하여 나중에 dropna로 제거합니다.
            eco_values.append(None)
            none_eco_values.append(None)
    
    # 시계열 데이터프레임 생성
    time_series_data = pd.DataFrame({
        'Year': years,
        '경제활동인구': eco_values,
        '비경제활동인구': none_eco_values
    })
    time_series_data['경제활동인구'] = pd.to_numeric(time_series_data['경제활동인구'], errors='coerce')
    time_series_data['비경제활동인구'] = pd.to_numeric(time_series_data['비경제활동인구'], errors='coerce')
    time_series_data.dropna(subset=['경제활동인구', '비경제활동인구'], inplace=True)

    if time_series_data.empty:
        print("오류: 유효한 시계열 데이터를 생성할 수 없습니다.")
        return None

    # 라인 차트 생성
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=time_series_data['Year'],
        y=time_series_data['경제활동인구'],
        mode='lines+markers',
        name='경제활동인구'
    ))

    fig.add_trace(go.Scatter(
        x=time_series_data['Year'],
        y=time_series_data['비경제활동인구'],
        mode='lines+markers',
        name='비경제활동인구'
    ))

    fig.update_layout(
        title_text='<b>연도별 장애인 경제활동 및 비경제활동인구 시계열 변화</b>',
        title_x=0.5,
        xaxis_title='연도',
        yaxis_title='인구 (명)',
        template='plotly_white',
        font=dict(family="Malgun Gothic, AppleGothic, NanumGothic, sans-serif"),
        height=500,
        yaxis_range=[0, max(time_series_data['경제활동인구'].max(), time_series_data['비경제활동인구'].max()) * 1.1], # Y축 시작을 0으로, 최대값보다 약간 크게 설정
        margin=dict(l=80, r=80, t=100, b=80) # 마진 조정
    )

    return fig


if __name__ == '__main__':
    # 예시 사용법: 차트 생성 및 표시
    # fig = create_total_activity_time_series_chart()
    # if fig:
    #     fig.show()
    pass
