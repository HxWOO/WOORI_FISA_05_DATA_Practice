import streamlit as st
import pandas as pd
import json
from disable_pop.visualize_animated_pie_chart import plot_animated_pie_chart
from disable_pop.visualize_national_trend_line_chart import plot_national_trend_line_chart
from disable_pop.visualize_regional_map_chart import plot_regional_map_chart
from disable_pop.visualize_gender_trend_line_chart import plot_gender_trend_line_chart

def visualize_population_data(df_national_total, df_regional_total, geojson_path):
    st.subheader("장애인구 현황 분석")

    # GeoJSON 파일 로드
    try:
        with open(geojson_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
    except FileNotFoundError:
        st.error(f"GeoJSON file not found at {geojson_path}")
        return
    except json.JSONDecodeError:
        st.error(f"Error decoding GeoJSON from {geojson_path}")
        return

    # 연도별 전국 장애유형별 인구 비율 (애니메이션 파이 차트)
    plot_animated_pie_chart(df_national_total)

    # 연도별 전국 장애인구 총계 추이 (라인 차트)
    plot_national_trend_line_chart(df_national_total)

    # 시도별 장애인구 총계 (지도 시각화)
    plot_regional_map_chart(df_regional_total, geojson_data)

    # 성별 장애인구 추이 (라인 차트)
    plot_gender_trend_line_chart(df_national_total)