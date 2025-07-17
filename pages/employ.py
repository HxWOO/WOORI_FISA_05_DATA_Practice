# -*- coding: utf-8 -*-
import streamlit as st
import os
import sys
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# 상위 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 시각화 함수 임포트
from employ_analysis.visualize_age_plotly import create_age_plotly_chart
from employ_analysis.visualize_edu_plotly import create_edu_plotly_chart
from employ_analysis.visualize_sex_plotly import create_sex_plotly_chart
from employ_analysis.visualize_type_plotly import create_type_plotly_chart
from employ_analysis.visualize_region_plotly import create_region_plotly_chart
from employ_analysis.visualize_sex_pie_plotly import create_sex_pie_chart
from employ_analysis.visualize_total_eco_activity_time_series import create_total_activity_time_series_chart
import employ_analysis.visualize_total_eco_activity_time_series as vteats
print(f"Available in visualize_total_eco_activity_time_series: {dir(vteats)}")

# 사이드바 페이지 링크 추가
st.sidebar.header("분석 페이지")
st.sidebar.page_link("app.py", label="홈", icon="🏠")
st.sidebar.page_link("pages/disability_assistant.py", label="복지", icon="🤝")
st.sidebar.page_link("pages/disabled_population_statistics.py", label="인구분포", icon="👨‍👩‍👧‍👦")
st.sidebar.page_link("pages/employ.py", label="고용 및 경제활동", icon="💼")
st.sidebar.page_link("pages/facility.py", label="관련 시설", icon="🏥")

st.set_page_config(
    page_title="시각화 자료",
    page_icon="📈",
    layout="wide",
)

st.title("📈 시각화 자료")
st.write("이 페이지에서는 Plotly를 이용한 인터랙티브한 장애인 경제활동 데이터를 시각화한 결과를 볼 수 있습니다.")

# 탭 생성
tab_titles = [
    "0. 연도별 경제활동 및 비경제활동인구수",
    "1. 연령별 고용률 및 실업률",
    "2. 학력 수준별 고용률 및 실업률",
    "3. 성별 경제활동 지표",
    "4. 장애 유형별 고용률",
    "5. 권역별 취업자 수 분포"
]

tabs = st.tabs(tab_titles)

with tabs[0]:
    st.header("연도별 장애인 경제활동 및 비경제활동인구수")
    st.write("연도별 장애인 경제활동 및 비경제활동인구수를 보여주는 라인 그래프입니다.")
    fig_time = create_total_activity_time_series_chart()
    if fig_time:
        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.warning(f"연도별 장애인 경제활동 및 비경제활동인구수 자료가 없습니다.")

with tabs[1]:
    st.header("연령별 고용률 및 실업률")
    st.write("장애인의 연령대별 고용률과 실업률을 보여주는 인터랙티브 막대 그래프입니다.")
    age_year = st.slider(
        "연령별 데이터를 보고 싶은 연도를 선택하세요:",
        min_value=2013,
        max_value=2024,
        value=2024, # 기본값은 최신 연도
        step=1,
        key='age_year_slider' # 고유한 키 추가
    )
    fig_age = create_age_plotly_chart(age_year)
    if fig_age:
        st.plotly_chart(fig_age, use_container_width=True)
    else:
        st.warning(f"{age_year}년 연령별 고용률 및 실업률 자료가 없습니다.")

with tabs[2]:
    st.header("학력 수준별 고용률 및 실업률")
    st.write("장애인의 학력 수준에 따른 고용률과 실업률을 비교하는 인터랙티브 막대 그래프입니다.")
    edu_year = st.slider(
        "학력별 데이터를 보고 싶은 연도를 선택하세요:",
        min_value=2013,
        max_value=2024,
        value=2024, # 기본값은 최신 연도
        step=1,
        key='edu_year_slider' # 고유한 키 추가
    )
    fig_edu = create_edu_plotly_chart(edu_year)
    if fig_edu:
        st.plotly_chart(fig_edu, use_container_width=True)
    else:
        st.warning(f"{edu_year}년 학력 수준별 고용률 및 실업률 자료가 없습니다.")

with tabs[3]:
    st.header("성별 경제활동 지표")
    st.write("남성 장애인과 여성 장애인의 경제활동참가율 및 분포를 비교하는 인터랙티브 그래프입니다.")
    sex_year = st.slider(
        "성별 데이터를 보고 싶은 연도를 선택하세요:",
        min_value=2013,
        max_value=2024,
        value=2024, # 기본값은 최신 연도
        step=1,
        key='sex_year_slider' # 고유한 키 추가
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("성별 경제활동참가율 (막대 그래프)")
        fig_sex_bar = create_sex_plotly_chart(sex_year)
        if fig_sex_bar:
            st.plotly_chart(fig_sex_bar, use_container_width=True)
        else:
            st.warning(f"{sex_year}년 성별 경제활동참가율 자료가 없습니다.")

    with col2:
        st.subheader("성별 경제활동참가율 분포 (파이 차트)")
        fig_sex_pie = create_sex_pie_chart(sex_year)
        if fig_sex_pie:
            st.plotly_chart(fig_sex_pie, use_container_width=True)
        else:
            st.warning(f"{sex_year}년 성별 경제활동참가율 분포 자료가 없습니다.")

with tabs[4]:
    st.header("장애 유형별 고용률")
    st.write("다양한 장애 유형별 고용률을 보여주는 인터랙티브 막대 그래프입니다.")
    type_year = st.slider(
        "장애 유형별 데이터를 보고 싶은 연도를 선택하세요:",
        min_value=2013,
        max_value=2024,
        value=2024, # 기본값은 최신 연도
        step=1,
        key='type_year_slider' # 고유한 키 추가
    )
    fig_type = create_type_plotly_chart(type_year)
    if fig_type:
        st.plotly_chart(fig_type, use_container_width=True)
    else:
        st.warning(f"{type_year}년 장애 유형별 고용률 자료가 없습니다.")

with tabs[5]:
    st.header("권역별 장애인 취업자 수 분포")
    st.write("대한민국 주요 권역별 장애인 취업자 수의 상대적 비율을 시각화한 인터랙티브 트리맵입니다.")
    region_year = st.slider(
        "권역별 데이터를 보고 싶은 연도를 선택하세요:",
        min_value=2020,
        max_value=2024,
        value=2024, # 기본값은 최신 연도
        step=1,
        key='region_year_slider' # 고유한 키 추가
    )
    fig_region = create_region_plotly_chart(region_year)
    if fig_region:
        st.plotly_chart(fig_region, use_container_width=True)
    else:
        st.warning(f"{region_year}년 권역별 장애인 취업자 수 분포 자료가 없습니다.")

