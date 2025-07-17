# -*- coding: utf-8 -*-
import streamlit as st
from employ_analysis import load_data, run_analysis
from pathlib import Path

st.set_page_config(
    page_title="장애인 경제활동 분석 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 앱을 시작할때, 데이터 전처리 시작
load_data.load_processed_data()


st.title("📊 장애인 경제활동 분석 대시보드")

st.markdown("""
이 대시보드는 통계청 데이터를 기반으로 장애인의 경제활동 현황을 시각화하여 보여줍니다.
왼쪽 사이드바에서 다양한 분석 페이지를 선택하여 데이터를 탐색할 수 있습니다.

**주요 내용:**
- 연령별 고용률 및 실업률
- 학력 수준별 고용률 및 실업률
- 성별 경제활동참가율
- 장애 유형별 고용률
- 권역별 장애인 취업자 수 분포

""")

st.info("왼쪽 사이드바에서 '시각화 자료' 페이지를 선택해주세요.")

# Streamlit의 멀티페이지 앱 구조는 pages/ 디렉토리에 파일을 두는 것으로 자동 인식됩니다.

