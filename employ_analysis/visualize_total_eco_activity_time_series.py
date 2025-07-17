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

def create_total_eco_activity_time_series_chart():
    """전체 장애인 경제활동인구의 시계열 데이터를 Plotly 라인 차트로 시각화하여 Figure 객체를 반환합니다."""
    file_path = f"{Path(__file__).parent.parent}/results/processed_disable_age.xlsx"
    
    if not os.path.exists(file_path):
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        return None

    df = pd.read_excel(file_path)

    # '전체' 행을 선택하고 '경제활동인구 (명)' 데이터를 추출
    # 데이터프레임 구조에 따라 '항목' 또는 유사한 컬럼에서 '경제활동인구 (명)'을 찾아야 함
    # 여기서는 '항목' 컬럼이 있고 그 값이 '경제활동인구 (명)'인 행을 가정
    # 실제 파일 구조에 따라 수정이 필요할 수 있음
    
    # '항목' 컬럼이 '경제활동인구 (명)'인 행을 찾습니다.
    # df.columns[0]이 '항목' 컬럼이라고 가정합니다.
    eco_activity_df = df[df[df.columns[0]] == '전체'].copy()

    if eco_activity_df.empty:
        print("오류: '경제활동인구 (명)' 데이터를 찾을 수 없습니다. 파일 구조를 확인하세요.")
        return None

    # 연도별 데이터 추출 (예: '2018', '2019', ...)
    # 컬럼 이름이 연도인 것을 가정하고, 숫자형으로 변환 가능한 컬럼만 선택
    years = list(range(2013,2025))
    eco_values = list()
    for year in years:
        eco_activity_col=(_get_column_for_year(eco_activity_df, "경제활동인구 (명)", year))
        eco_values.append(int(eco_activity_df[eco_activity_col]))
    
    # 시계열 데이터프레임 생성
    time_series_data = pd.DataFrame({
        'Year': years,
        'Value': eco_values
    })
    time_series_data['Value'] = pd.to_numeric(time_series_data['Value'], errors='coerce')
    time_series_data.dropna(subset=['Value'], inplace=True)

    if time_series_data.empty:
        print("오류: 유효한 시계열 데이터를 생성할 수 없습니다.")
        return None

    # 라인 차트 생성
    fig = go.Figure(data=[go.Scatter(
        x=time_series_data['Year'],
        y=time_series_data['Value'],
        mode='lines+markers',
        name='경제활동인구'
    )])

    fig.update_layout(
        title_text='<b>전체 장애인 경제활동인구 시계열 변화</b>',
        title_x=0.5,
        xaxis_title='연도',
        yaxis_title='경제활동인구 (명)',
        template='plotly_white',
        font=dict(family="Malgun Gothic, AppleGothic, NanumGothic, sans-serif"),
        height=500
    )

    return fig

if __name__ == '__main__':
    # 예시 사용법: 차트 생성 및 표시
    # fig = create_total_eco_activity_time_series_chart()
    # if fig:
    #     fig.show()
    pass