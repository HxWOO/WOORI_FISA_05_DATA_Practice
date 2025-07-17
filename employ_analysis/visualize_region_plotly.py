# -*- coding: utf-8 -*-
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio # Not used directly in the function, but kept for consistency if needed elsewhere
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

def create_region_plotly_chart(year):
    """지정된 연도의 권역별 취업자 수 데이터를 Plotly 트리맵으로 시각화하여 Figure 객체를 반환합니다."""
    file_path = 'results/processed_disable_region.xlsx'
    if not os.path.exists(file_path):
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        return None

    df = pd.read_excel(file_path)
    category_col = df.columns[0]
    df = df[df[category_col] != '전체'].copy()

    # 연도에 맞는 취업자 수 컬럼 찾기
    # '취업자 (명)' 컬럼
    employed_col_name = _get_column_for_year(df, '취업자 (명)', year)

    if employed_col_name is None:
        print(f"오류: {year}년도에 해당하는 취업자 수 컬럼을 찾을 수 없습니다.")
        return None

    df[employed_col_name] = pd.to_numeric(df[employed_col_name], errors='coerce')

    fig = go.Figure(go.Treemap(
        labels=df[category_col],
        parents=["" for _ in df[category_col]],
        values=df[employed_col_name],
        textinfo="label+value+percent parent",
        marker_colorscale='Viridis',
        # hovertemplate에서 '천명' 대신 '명'으로 수정
        hovertemplate=f'<b>%{{label}}</b><br>취업자 수: %{{value:,.0f}}명<br>전체 대비: %{{percentParent:.1%}}<extra></extra>'
    ))

    fig.update_layout(
        title_text=f'<b>{year}년 권역별 장애인 취업자 수 분포</b>',
        title_x=0.5,
        margin = dict(t=50, l=25, r=25, b=25),
        template='plotly_white',
        font=dict(family="Malgun Gothic, AppleGothic, NanumGothic, sans-serif"),
        height=500
    )

    return fig

if __name__ == '__main__':
    pass
