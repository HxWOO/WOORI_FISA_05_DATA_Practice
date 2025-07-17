import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests
import os
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="장애인 시설 지도",
    page_icon="🗺️",
    layout="wide",
)

# ——— CSS 삽입: 상단 패딩을 줄여서 지도가 헤더 바로 아래 붙도록 함 ———
st.markdown(
    """
    <style>
      .block-container { padding-top: 1rem; }
    </style>
    """,
    unsafe_allow_html=True
)
# ——————————————————————————————————————————————————————————————

st.title("🗺️ 장애인 시설 필요도 지도")
st.write("이 페이지에서는 보건복지부 데이터를 기반으로 한 장애인 시설의 필요도를 지도에서 확인할 수 있습니다.")

# Define data paths
data_dir = f"{Path(__file__).parent.parent}/data/"
sigungu_population_file = data_dir + '시군구별_장애정도별_성별_등록장애인수_20250717111030.csv'
weekly_facilities_file   = data_dir + 'disability_facilities.csv'
welfare_facilities_file  = data_dir + '보건복지부_장애인복지관 현황_20240425_utf8.csv'

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        df_sigungu_population = pd.read_csv(sigungu_population_file, encoding='utf-8-sig', header=2)
        df_weekly_facilities  = pd.read_csv(weekly_facilities_file, encoding='utf-8-sig')
        df_welfare_facilities = pd.read_csv(welfare_facilities_file, encoding='utf-8-sig')
        return df_sigungu_population, df_weekly_facilities, df_welfare_facilities
    except Exception as e:
        st.error(f"데이터 파일을 읽는 중 오류가 발생했습니다: {e}")
        return None, None, None

df_sigungu_population, df_weekly_facilities, df_welfare_facilities = load_data()

# --- Load GeoJSON ---
@st.cache_data
def load_geojson():
    geojson_url ="https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_municipalities_geo_simple.json"  
    try:
        resp = requests.get(geojson_url)
        resp.raise_for_status()
        return json.loads(resp.content.decode('utf-8'))
    except Exception as e:
        st.error(f"GeoJSON 데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None

geojson = load_geojson()

#--- Common Data Standardization Function ---
def standardize_facilities_data(df_raw, facility_type, level='province'):
    short_to_full = {
        '서울':'서울특별시','부산':'부산광역시','대구':'대구광역시',
        '인천':'인천광역시','광주':'광주광역시','대전':'대전광역시',
        '울산':'울산광역시','세종':'세종시','경기':'경기도',
        '강원':'강원도','충북':'충청북도','충남':'충청남도',
        '전북':'전라북도','전남':'전라남도','경북':'경상북도',
        '경남':'경상남도','제주':'제주특별자치도'
    }
    df_raw['시도_전체이름'] = df_raw['시도'].str.strip().map(short_to_full)
    if level=='province':
        df = (df_raw.groupby('시도_전체이름')
                     .size()
                     .reset_index(name=f'{facility_type}수')
                     .rename(columns={'시도_전체이름':'시도'}))
    else:
        df_raw['시군구_전체이름'] = df_raw['시도_전체이름'] + ' ' + df_raw['시군구']
        df = (df_raw.groupby('시군구_전체이름')
                  .size()
                  .reset_index(name=f'{facility_type}수'))
    return df

# --- Process Sigungu Population Data ---
@st.cache_data
def process_sigungu_population_data(df_pop):
    df_pop.columns = [
        '시도_대분류','시군구','총인구_소계','총인구_남자','총인구_여자',
        '심한장애_소계','심한장애_남자','심한장애_여자',
        '심하지않은장애_소계','심하지않은장애_남자','심하지않은장애_여자'
    ]
    df = df_pop[~df_pop['시도_대분류'].isin(['전국'])]
    df = df[~df['시군구'].isin(['소계'])]
    df = df[['시도_대분류','시군구','총인구_소계']].copy()
    df['총인구_소계'] = pd.to_numeric(df['총인구_소계'], errors='coerce')
    df.dropna(subset=['총인구_소계'], inplace=True)
    return df

if df_sigungu_population is not None and df_weekly_facilities is not None and df_welfare_facilities is not None and geojson:
    # 인구 데이터 전처리
    df_pop = process_sigungu_population_data(df_sigungu_population)
    df_pop['시군구_전체이름'] = df_pop['시도_대분류'] + ' ' + df_pop['시군구']

    # 주간시설 필요도 계산
    df_weekly = standardize_facilities_data(df_weekly_facilities, '주간이용시설', level='sigungu')
    df_weekly = pd.merge(df_pop, df_weekly, on='시군구_전체이름', how='left')
    df_weekly['주간이용시설수']      = df_weekly['주간이용시설수'].fillna(0).astype(int)
    df_weekly['주간이용시설필요지수'] = df_weekly['총인구_소계'] / (df_weekly['주간이용시설수'] + 1)

    # 복지관 필요도 계산
    df_welfare = standardize_facilities_data(df_welfare_facilities, '복지관', level='sigungu')
    df_welfare = pd.merge(df_pop, df_welfare, on='시군구_전체이름', how='left')
    df_welfare['복지관수']      = df_welfare['복지관수'].fillna(0).astype(int)
    df_welfare['복지관필요지수'] = df_welfare['총인구_소계'] / (df_welfare['복지관수'] + 1)

    # 탭 생성 및 지도 그리기
    tab3, tab4 = st.tabs(["시군구별 주간이용시설 필요도", "시군구별 장애인복지관 필요도"])
    with tab3:
        st.header("시군구별 장애인구수 대비 주간이용시설 필요도")
        with st.expander("**장애인 주간 이용시설이란?**"):
            st.markdown("""
                        
            장애인이 낮 시간 동안 이용할 수 있는 시설입니다.
            다양한 재활 프로그램, 교육, 사회적응 훈련 등을
            제공하여 장애인의 자립을 지원하고
            가족의 부담을 덜어주는 역할을 합니다.

            **필요도 산정 기준**

            - **(시군구별 장애인 인구 수) / (시군구별 주간 이용시설 수 + 1)**
            - 위 지표는 각 지역의 장애인 인구 대비
              시설이 얼마나 부족한지를 나타냅니다.
            - 지수가 높을수록 장애인 인구에 비해 시설 수가
              부족하여 시설 확충이 더 시급함을 의미합니다.
            - 분모에 1을 더하는 이유는 시설이 없는 지역의
              경우 0으로 나누는 것을 방지하고, 시설이 없는
              지역의 필요도를 가장 높게 평가하기 위함입니다.
            """)
        fig = px.choropleth(
            df_weekly,
            geojson=geojson,
            locations='시군구',
            featureidkey="properties.name",
            color='주간이용시설필요지수',
            hover_name='시군구',
            hover_data={
                '총인구_소계':':,',
                '주간이용시설수':':,',
                '주간이용시설필요지수':':.2f'
            },
            color_continuous_scale="Reds"
        )
        fig.update_geos(visible=False,
                        projection_type="mercator",
                        center=dict(lat=36, lon=127.5),
                        lonaxis_range=[124,132],
                        lataxis_range=[33,39])
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            height=800,
            coloraxis_colorbar=dict(len=0.7, y=0.6)
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.header("시군구별 장애인구수 대비 장애인복지관 필요도")
        with st.expander("**장애인 복지관이란?**"):
            st.markdown("""
            
            장애인의 전인적 재활을 지원하는 핵심 기관입니다.
            사회, 교육, 직업, 의료 등 종합적인 재활 서비스를
            제공하여 장애인의 사회통합을 돕습니다.

            **필요도 산정 기준**

            - **(시군구별 장애인 인구 수) / (시군구별 복지관 수 + 1)**
            - 위 지표는 각 지역의 장애인 인구 대비
              시설이 얼마나 부족한지를 나타냅니다.
            - 지수가 높을수록 장애인 인구에 비해 시설 수가
              부족하여 시설 확충이 더 시급함을 의미합니다.
            - 분모에 1을 더하는 이유는 시설이 없는 지역의
              경우 0으로 나누는 것을 방지하고, 시설이 없는
              지역의 필요도를 가장 높게 평가하기 위함입니다.
            """)
        fig2 = px.choropleth(
            df_welfare,
            geojson=geojson,
            locations='시군구',
            featureidkey="properties.name",
            color='복지관필요지수',
            hover_name='시군구',
            hover_data={
                '총인구_소계':':,',
                '복지관수':':,',
                '복지관필요지수':':.2f'
            },
            color_continuous_scale="Blues"
        )
        fig2.update_geos(visible=False,
                         projection_type="mercator",
                         center=dict(lat=36, lon=127.5),
                         lonaxis_range=[124,132],
                         lataxis_range=[33,39])
        fig2.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            height=800,
            coloraxis_colorbar=dict(len=0.7, y=0.6)
        )
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("데이터 또는 GeoJSON을 불러오지 못하여 지도를 표시할 수 없습니다.")