# -*- coding: utf-8 -*-
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio # Not used directly in the function, but kept for consistency if needed elsewhere
import os
import plotly.express as px

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

def create_type_plotly_chart(year):
    """지정된 연도의 장애 유형별 고용률 데이터를 Plotly로 시각화하여 Figure 객체를 반환합니다."""
    file_path = 'results/processed_disable_type.xlsx'
    if not os.path.exists(file_path):
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        return None

    df = pd.read_excel(file_path)
    category_col = df.columns[0]
    df = df[df[category_col].notna() & (df[category_col] != '전체')].copy()

    # 연도에 맞는 고용률 컬럼 찾기
    employment_col_name = _get_column_for_year(df, '고용률 (%)', year)

    if employment_col_name is None:
        print(f"오류: {year}년도에 해당하는 고용률 컬럼을 찾을 수 없습니다.")
        return None

    fig = go.Figure(go.Bar(
        x=df[category_col],
        y=df[employment_col_name],
        text=df[employment_col_name].round(1),
        textposition='auto',
        marker_color=px.colors.qualitative.Plotly # Plotly 기본 색상 팔레트 사용
    ))

    fig.update_layout(
        title_text=f'<b>{year}년 장애 유형별 고용률</b>',
        title_x=0.5,
        xaxis_title='장애 유형',
        yaxis_title='고용률 (%)',
        template='plotly_white',
        font=dict(family="Malgun Gothic, AppleGothic, NanumGothic, sans-serif"),
        height=500
    )

    return fig

if __name__ == '__main__':
    pass