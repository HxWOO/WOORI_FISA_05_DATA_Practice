# -*- coding: utf-8 -*-
import streamlit as st
from employ_analysis import load_data
from pathlib import Path

st.set_page_config(
    page_title="장애인 관련 데이터 분석 및 시각화",
    page_icon="♿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 데이터 전처리 실행
load_data.load_processed_data()

# --- 페이지 시작 ---

# 1. 제목 및 소개
st.title("♿ 장애인 관련 데이터 분석 및 시각화")
st.markdown("---")
st.markdown("""
본 프로젝트는 **장애인 관련 공공 데이터를 활용**하여 현실적인 문제를 다각도로 분석하고, 
그 결과를 **시각화하여 인사이트를 도출**하는 것을 목표로 합니다. 

4명의 팀원이 각각 **복지, 인구 분포, 고용 및 경제활동, 관련 시설**이라는 하위 주제를 맡아 
데이터 분석 및 시각화를 진행했으며, Streamlit을 사용하여 웹 애플리케이션으로 구현했습니다.
""")

# 2. 프로젝트 개요
st.header("📋 프로젝트 개요")
st.markdown("""
장애인 관련 현실 데이터를 기반으로 사회적 문제에 대한 깊이 있는 이해를 돕고, 
이를 효과적으로 전달하기 위해 데이터 분석 및 시각화를 수행했습니다. 

각 팀원은 개별 주제에 대한 심층 분석을 진행하고, 이를 Streamlit 기반의 대시보드로 통합하여 
사용자가 각 주제별 분석 결과를 쉽게 탐색하고 상호작용할 수 있도록 만들었습니다.
""")

# 3. 주요 기능 소개
st.header("✨ 주요 기능")
cols = st.columns(4)
with cols[0]:
    st.subheader("복지")
    st.markdown("사회적 취약계층으로서 장애인이 받는 **복지 서비스** 관련 데이터를 분석하고 시각화합니다.")
with cols[1]:
    st.subheader("인구 분포")
    st.markdown("지역별, 유형별 **장애인 인구 통계**를 분석하고, 지도와 차트를 통해 분포 현황을 시각화합니다.")
with cols[2]:
    st.subheader("고용 및 경제활동")
    st.markdown("장애인의 **경제활동상태, 고용률** 등의 데이터를 분석하여 시간의 흐름에 따른 변화를 시각화합니다.")
with cols[3]:
    st.subheader("관련 시설")
    st.markdown("전국 **장애인 관련 복지 시설**의 분포 및 현황을 분석하고, 지도 위에 시각화합니다.")

st.info("👈 **왼쪽 사이드바**에서 원하는 분석 페이지를 선택하여 더 자세한 내용을 확인해보세요!")

# 사이드바 페이지 링크 추가
st.sidebar.header("분석 페이지")
st.sidebar.page_link("app.py", label="홈", icon="🏠")
st.sidebar.page_link("pages/disability_assistant.py", label="복지", icon="🤝")
st.sidebar.page_link("pages/disabled_population_statistics.py", label="인구분포", icon="👨‍👩‍👧‍👦")
st.sidebar.page_link("pages/employ.py", label="고용 및 경제활동", icon="💼")
st.sidebar.page_link("pages/facility.py", label="관련 시설", icon="🏥")

# 4. 기여자 정보
st.markdown("---")
st.header("🧑‍💻 기여자")
contributors = {
    "박진서": "장애인 복지",
    "남상원": "장애인 인구 분포",
    "김현우": "장애인 고용, 경제활동",
    "민지수": "장애인 관련 시설"
}

# 2x2 그리드로 기여자 표시
row1 = st.columns(2)
row2 = st.columns(2)
rows = [row1[0], row1[1], row2[0], row2[1]]

for i, (name, role) in enumerate(contributors.items()):
    with rows[i]:
        st.markdown(f"**{name}**")
        st.markdown(f"_{role}_")