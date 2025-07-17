import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from employ_analysis.load_data import load_disabled_population_data, load_korea_geojson
from employ_analysis.visualize_population import plot_animated_pie_chart, plot_national_trend_line_chart, plot_regional_map_chart, plot_gender_trend_line_chart

st.set_page_config(layout="wide")

st.title("장애인구 통계 분석")

@st.cache_data
def load_data():
    return load_disabled_population_data()

@st.cache_data
def load_geojson():
    return load_korea_geojson()

df = load_data()
geojson_data = load_geojson()

if df is not None and geojson_data is not None:
    st.write("### 원본 데이터 미리보기")
    st.dataframe(df.head())

    st.write("### 데이터 정보")
    st.write(f"총 {df.shape[0]} 행, {df.shape[1]} 열")
    st.write("컬럼: ", df.columns.tolist())

    # 연도 컬럼 추출
    year_columns = [col for col in df.columns if str(col).isdigit()]
    min_year = int(min(year_columns))
    max_year = int(max(year_columns))

    # '전국' 데이터 필터링
    df_national = df[df['시도별'] == '전국'].copy()
    df_national_total = df_national[df_national['성별'] == '계'].copy()

    # --- 애니메이션 원형 차트 ---
    plot_animated_pie_chart(df_national_total)

    # --- 선형 차트: 전국 장애인구 총계 추이 ---
    plot_national_trend_line_chart(df_national_total)

    # --- 지도 시각화: 시도별 총계 (배경 지도 + 버블 차트) ---
    plot_regional_map_chart(df, geojson_data)

    # --- 성별 장애인구 추이 ---
    plot_gender_trend_line_chart(df)

else:
    st.error("데이터 또는 GeoJSON 파일을 불러오는데 실패했습니다. 파일 경로 및 내용을 확인해주세요.")
