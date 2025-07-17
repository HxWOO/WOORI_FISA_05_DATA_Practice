import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from employ_analysis.load_data import load_disabled_population_data, load_korea_geojson
from disable_pop.visualize_population import plot_animated_pie_chart, plot_national_trend_line_chart, plot_regional_map_chart, plot_gender_trend_line_chart

st.set_page_config(layout="wide")

st.title("장애인구 통계 분석")

# 사이드바 페이지 링크 추가
st.sidebar.header("분석 페이지")
st.sidebar.page_link("app.py", label="홈", icon="🏠")
st.sidebar.page_link("pages/disability_assistant.py", label="복지", icon="🤝")
st.sidebar.page_link("pages/disabled_population_statistics.py", label="인구분포", icon="👨‍👩‍👧‍👦")
st.sidebar.page_link("pages/employ.py", label="고용 및 경제활동", icon="💼")
st.sidebar.page_link("pages/facility.py", label="관련 시설", icon="🏥")

@st.cache_data
def load_data():
    return load_disabled_population_data()

@st.cache_data
def load_geojson():
    return load_korea_geojson()

df = load_data()
geojson_data = load_geojson()

if df is not None and geojson_data is not None:
    # '전국' 데이터 필터링
    df_national = df[df['시도별'] == '전국'].copy()
    df_national_total = df_national[df_national['성별'] == '계'].copy()

    # 탭 생성
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "연도별 장애인구 비율",
        "전국 장애인구 추이",
        "시도별 장애인구 분포",
        "성별 장애인구 추이",
        "원본 데이터"
    ])

    with tab1:
        plot_animated_pie_chart(df_national_total)

    with tab2:
        plot_national_trend_line_chart(df_national_total)

    with tab3:
        plot_regional_map_chart(df, geojson_data)

    with tab4:
        plot_gender_trend_line_chart(df)

    with tab5:
        st.header("원본 데이터 미리보기")
        st.dataframe(df)

else:
    st.error("데이터 또는 GeoJSON 파일을 불러오는데 실패했습니다. 파일 경로 및 내용을 확인해주세요.")
