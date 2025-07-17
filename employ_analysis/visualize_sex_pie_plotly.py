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

def create_sex_pie_chart(year):
    """지정된 연도의 성별 경제활동참가율 데이터를 Plotly 파이 차트로 시각화하여 Figure 객체를 반환합니다."""
    file_path = f"{Path(__file__).parent.parent}/results/processed_disable_sex.xlsx"
    if not os.path.exists(file_path):
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        return None

    df = pd.read_excel(file_path)
    category_col = df.columns[0]
    df = df[df[category_col] != '전체'].copy() # '전체' 행 제외

    # 연도에 맞는 경제활동참가율 컬럼 찾기
    participation_col_name = _get_column_for_year(df, '경활률 (%)', year)

    if participation_col_name is None:
        print(f"오류: {year}년도에 해당하는 경제활동참가율 컬럼을 찾을 수 없습니다.")
        return None

    df[participation_col_name] = pd.to_numeric(df[participation_col_name], errors='coerce')
    df.dropna(subset=[participation_col_name], inplace=True) # NaN 값 제거

    # 파이 차트 생성
    fig = go.Figure(data=[go.Pie(
        labels=df[category_col],
        values=df[participation_col_name],
        hole=.3, # 도넛 차트 형태로 만들기
        pull=[0.05 if label == '남' else 0 for label in df[category_col]], # '남'성 부분만 살짝 분리
        marker_colors=['#636EFA', '#EF553B'], # 남성, 여성 색상 지정
        textinfo='label+percent', # 라벨과 퍼센트 표시
        insidetextorientation='radial' # 텍스트 방향
    )])

    fig.update_layout(
        title_text=f'<b>{year}년 성별 경제활동참가율 분포</b>',
        title_x=0.5,
        template='plotly_white',
        font=dict(family="Malgun Gothic, AppleGothic, NanumGothic, sans-serif"),
        height=500
    )

    return fig

if __name__ == '__main__':
    # 예시 사용법: 2023년 데이터로 차트 생성 및 표시
    # fig = create_sex_pie_chart(2023)
    # if fig:
    #     fig.show()
    pass
