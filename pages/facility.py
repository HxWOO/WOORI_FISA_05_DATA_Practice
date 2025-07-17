import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests
import os

st.set_page_config(
    page_title="장애인 시설 지도",
    page_icon="🗺️",
    layout="wide",
)

st.title("🗺️ 장애인 시설 필요도 지도")
st.write("이 페이지에서는 보건복지부 데이터를 기반으로 한 장애인 시설의 필요도를 지도에서 확인할 수 있습니다.")

# Define data paths
data_dir = "C:/ITStudy/WOORI_FISA_05_DATA_Practice-main/data"
population_file = os.path.join(data_dir, 'disability_population.csv')
sigungu_population_file = os.path.join(data_dir, '시군구별_장애정도별_성별_등록장애인수_20250717111030.csv')
weekly_facilities_file = os.path.join(data_dir, 'disability_facilities.csv')
welfare_facilities_file = os.path.join(data_dir, '보건복지부_장애인복지관 현황_20240425_utf8.csv')

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        df_population = pd.read_csv(population_file, encoding='utf-8-sig', header=1)
        df_sigungu_population = pd.read_csv(sigungu_population_file, encoding='utf-8-sig', header=2)
        df_weekly_facilities = pd.read_csv(weekly_facilities_file, encoding='utf-8-sig')
        df_welfare_facilities = pd.read_csv(welfare_facilities_file, encoding='utf-8-sig')
        return df_population, df_sigungu_population, df_weekly_facilities, df_welfare_facilities
    except Exception as e:
        st.error(f"데이터 파일을 읽는 중 오류가 발생했습니다: {e}")
        return None, None, None, None

df_population, df_sigungu_population, df_weekly_facilities, df_welfare_facilities = load_data()

# --- Load GeoJSON ---
@st.cache_data
def load_geojson():
    geojson_url = "https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_municipalities_geo_simple.json"
    try:
        response = requests.get(geojson_url)
        response.raise_for_status()
        return json.loads(response.content.decode('utf-8'))
    except requests.exceptions.RequestException as e:
        st.error(f"GeoJSON 데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None

geojson = load_geojson()

if df_population is not None and df_sigungu_population is not None and df_weekly_facilities is not None and df_welfare_facilities is not None and geojson:
    # --- Common Data Standardization Function ---
    def standardize_facilities_data(df_facilities_raw, facility_type, level='province'):
        short_to_full_map = {
            '서울': '서울특별시', '부산': '부산광역시', '대구': '대구광역시',
            '인천': '인천광역시', '광주': '광주광역시', '대전': '대전광역시',
            '울산': '울산광역시', '세종': '세종특별자치시', '경기': '경기도',
            '강원': '강원도', '충북': '충청북도', '충남': '충청남도',
            '전북': '전라북도', '전남': '전라남도', '경북': '경상북도',
            '경남': '경상남도', '제주': '제주특별자치도'
        }
        df_facilities_raw['시도_전체이름'] = df_facilities_raw['시도'].str.strip().map(short_to_full_map)

        if level == 'province':
            facilities_by_area = df_facilities_raw.groupby('시도_전체이름').size().reset_index(name=f'{facility_type}수')
            facilities_by_area.rename(columns={'시도_전체이름': '시도'}, inplace=True)
        elif level == 'sigungu':
            # Combine 시도_전체이름 and 시군구 for unique identifier
            df_facilities_raw['시군구_전체이름'] = df_facilities_raw['시도_전체이름'] + ' ' + df_facilities_raw['시군구']
            facilities_by_area = df_facilities_raw.groupby('시군구_전체이름').size().reset_index(name=f'{facility_type}수')
            facilities_by_area.rename(columns={'시군구_전체이름': '시군구_전체이름'}, inplace=True)
        return facilities_by_area

    # --- Process Sigungu Population Data ---
    @st.cache_data
    def process_sigungu_population_data(df_sigungu_population):
        df_sigungu_population.columns = ['시도_대분류', '시군구', '총인구_소계', '총인구_남자', '총인구_여자',
                                     '심한장애_소계', '심한장애_남자', '심한장애_여자',
                                     '심하지않은장애_소계', '심하지않은장애_남자', '심하지않은장애_여자']
        df_filtered = df_sigungu_population[~df_sigungu_population['시도_대분류'].isin(['전국'])].copy()
        df_filtered = df_filtered[~df_filtered['시군구'].isin(['소계'])].copy()
        df_population_sigungu = df_filtered[['시도_대분류', '시군구', '총인구_소계']].copy()
        df_population_sigungu['총인구_소계'] = pd.to_numeric(df_population_sigungu['총인구_소계'], errors='coerce')
        df_population_sigungu.dropna(subset=['총인구_소계'], inplace=True)
        return df_population_sigungu

    df_population_sigungu = process_sigungu_population_data(df_sigungu_population)
    df_population_sigungu['시군구_전체이름'] = df_population_sigungu['시도_대분류'] + ' ' + df_population_sigungu['시군구']

    # Debugging: Print unique si-gun-gu names from population data
    print("Unique si-gun-gu names from population data:")
    print(df_population_sigungu['시군구_전체이름'].unique())

    # Debugging: Print names from GeoJSON properties
    geojson_names = [feature['properties']['name'] for feature in geojson['features']]
    print("Names from GeoJSON:")
    print(sorted(list(set(geojson_names))))

    # --- Standardize Province Population Data (Existing Logic) ---
    try:
        population_total = df_population[df_population['장애유형별(1)'].str.strip() == '합계'].copy()
        population_total = population_total.iloc[:, [0, 2]]
        population_total.columns = ['시도', '장애인구수']
        population_total['장애인구수'] = pd.to_numeric(population_total['장애인구수'], errors='coerce')
        population_total.dropna(subset=['장애인구수'], inplace=True)
        population_by_province = population_total[~population_total['시도'].isin(['전국', '소계'])].copy()
        population_by_province['시도'] = population_by_province['시도'].str.strip().replace({
            '강원특별자치도': '강원도',
            '전북특별자치도': '전라북도'
        })
    except KeyError as e:
        st.error(f"인구 데이터 처리 중 오류가 발생했습니다: {e}. 컬럼 이름을 확인해주세요.")
        st.stop()

    # --- Process Weekly Facilities Data (Province Level) ---
    weekly_facilities_by_province = standardize_facilities_data(df_weekly_facilities, '주간이용시설', level='province')
    df_merged_weekly_province = pd.merge(population_by_province, weekly_facilities_by_province, on='시도', how='left')
    df_merged_weekly_province['주간이용시설수'] = df_merged_weekly_province['주간이용시설수'].fillna(0).astype(int)
    df_merged_weekly_province['주간이용시설필요지수'] = df_merged_weekly_province['장애인구수'] / (df_merged_weekly_province['주간이용시설수'] + 1)

    # --- Process Welfare Facilities Data (Province Level) ---
    welfare_facilities_by_province = standardize_facilities_data(df_welfare_facilities, '복지관', level='province')
    df_merged_welfare_province = pd.merge(population_by_province, welfare_facilities_by_province, on='시도', how='left')
    df_merged_welfare_province['복지관수'] = df_merged_welfare_province['복지관수'].fillna(0).astype(int)
    df_merged_welfare_province['복지관필요지수'] = df_merged_welfare_province['장애인구수'] / (df_merged_welfare_province['복지관수'] + 1)

    # --- Process Weekly Facilities Data (Sigungu Level) ---
    weekly_facilities_by_sigungu = standardize_facilities_data(df_weekly_facilities, '주간이용시설', level='sigungu')
    df_merged_weekly_sigungu = pd.merge(df_population_sigungu, weekly_facilities_by_sigungu, on='시군구_전체이름', how='left')
    df_merged_weekly_sigungu['주간이용시설수'] = df_merged_weekly_sigungu['주간이용시설수'].fillna(0).astype(int)
    df_merged_weekly_sigungu['주간이용시설필요지수'] = df_merged_weekly_sigungu['총인구_소계'] / (df_merged_weekly_sigungu['주간이용시설수'] + 1)

    # --- Process Welfare Facilities Data (Sigungu Level) ---
    welfare_facilities_by_sigungu = standardize_facilities_data(df_welfare_facilities, '복지관', level='sigungu')
    df_merged_welfare_sigungu = pd.merge(df_population_sigungu, welfare_facilities_by_sigungu, on='시군구_전체이름', how='left')
    df_merged_welfare_sigungu['복지관수'] = df_merged_welfare_sigungu['복지관수'].fillna(0).astype(int)
    df_merged_welfare_sigungu['복지관필요지수'] = df_merged_welfare_sigungu['총인구_소계'] / (df_merged_welfare_sigungu['복지관수'] + 1)

    # --- Area Data ---
    area_data = {
        '서울특별시': 605.23,
        '부산광역시': 770.07,
        '대구광역시': 883.49,
        '인천광역시': 1065.23,
        '광주광역시': 501.0,
        '대전광역시': 539.8,
        '울산광역시': 1062.09,
        '세종특별자치시': 465.2,
        '경기도': 10195.27,
        '강원도': 16830.8,
        '충청북도': 7406.95,
        '충청남도': 8246.17,
        '전라북도': 8069.84,
        '전라남도': 12363.1,
        '경상북도': 18428.1,
        '경상남도': 10540.55,
        '제주특별자치도': 1849.02
    }
    df_area = pd.DataFrame(list(area_data.items()), columns=['시도', '면적(㎢)'])

    # --- Area Data (Placeholder for Sigungu Area Data) ---
    # You will need to provide actual si-gun-gu area data here.
    # For now, I'll use a dummy dictionary or load from a CSV if provided by the user.
    sigungu_area_data = {
        # Example: '서울특별시 종로구': 23.91,
        # ... more si-gun-gu areas
    }
    df_sigungu_area = pd.DataFrame(list(sigungu_area_data.items()), columns=['시군구_전체이름', '면적(㎢)'])

    # Merge area data with merged dataframes (Province Level)
    df_merged_weekly_province = pd.merge(df_merged_weekly_province, df_area, on='시도', how='left')
    df_merged_welfare_province = pd.merge(df_merged_welfare_province, df_area, on='시도', how='left')

    # Calculate facilities per area (Province Level)
    df_merged_weekly_province['주간이용시설_밀도'] = df_merged_weekly_province['주간이용시설수'] / df_merged_weekly_province['면적(㎢)']
    df_merged_welfare_province['복지관_밀도'] = df_merged_welfare_province['복지관수'] / df_merged_welfare_province['면적(㎢)']

    # Merge area data with merged dataframes (Sigungu Level)
    df_merged_weekly_sigungu = pd.merge(df_merged_weekly_sigungu, df_sigungu_area, on='시군구_전체이름', how='left')
    df_merged_welfare_sigungu = pd.merge(df_merged_welfare_sigungu, df_sigungu_area, on='시군구_전체이름', how='left')

    # Calculate facilities per area (Sigungu Level)
    df_merged_weekly_sigungu['주간이용시설_밀도'] = df_merged_weekly_sigungu['주간이용시설수'] / df_merged_weekly_sigungu['면적(㎢)']
    df_merged_welfare_sigungu['복지관_밀도'] = df_merged_welfare_sigungu['복지관수'] / df_merged_welfare_sigungu['면적(㎢)']

    tab3, tab4 = st.tabs(["시군구별 주간이용시설 필요도", "시군구별 장애인복지관 필요도"])

    with tab3:
        st.header("시군구별 장애인구수 대비 주간이용시설 필요도")
        fig_weekly_sigungu = px.choropleth(
            df_merged_weekly_sigungu,
            geojson=geojson,
            locations='시군구',
            featureidkey="properties.name",
            color='주간이용시설필요지수',
            hover_name='시군구',
            hover_data={'총인구_소계': ':,', '주간이용시설수': ':,', '주간이용시설필요지수': ':.2f', '주간이용시설_밀도': ':.5f'},
            color_continuous_scale="Reds",
            title="시군구별 장애인구수 대비 주간이용시설 필요도"
        )
        fig_weekly_sigungu.update_geos(fitbounds="locations", visible=False)
        fig_weekly_sigungu.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, title_font_size=20, title_x=0.5)
        st.plotly_chart(fig_weekly_sigungu, use_container_width=True)

    with tab4:
        st.header("시군구별 장애인구수 대비 장애인복지관 필요도")
        fig_welfare_sigungu = px.choropleth(
            df_merged_welfare_sigungu,
            geojson=geojson,
            locations='시군구',
            featureidkey="properties.name",
            color='복지관필요지수',
            hover_name='시군구',
            hover_data={'총인구_소계': ':,', '복지관수': ':,', '복지관필요지수': ':.2f', '복지관_밀도': ':.5f'},
            color_continuous_scale="Blues",
            title="시군구별 장애인구수 대비 장애인복지관 필요도"
        )
        fig_welfare_sigungu.update_geos(fitbounds="locations", visible=False)
        fig_welfare_sigungu.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, title_font_size=20, title_x=0.5)
        st.plotly_chart(fig_welfare_sigungu, use_container_width=True)

else:
    st.warning("데이터 또는 GeoJSON을 불러오지 못하여 지도를 표시할 수 없습니다.")

    # --- Standardize Province Population Data (Existing Logic) ---
    try:
        population_total = df_population[df_population['장애유형별(1)'].str.strip() == '합계'].copy()
        population_total = population_total.iloc[:, [0, 2]]
        population_total.columns = ['시도', '장애인구수']
        population_total['장애인구수'] = pd.to_numeric(population_total['장애인구수'], errors='coerce')
        population_total.dropna(subset=['장애인구수'], inplace=True)
        population_by_province = population_total[~population_total['시도'].isin(['전국', '소계'])].copy()
        population_by_province['시도'] = population_by_province['시도'].str.strip().replace({
            '강원특별자치도': '강원도',
            '전북특별자치도': '전라북도'
        })
    except KeyError as e:
        st.error(f"인구 데이터 처리 중 오류가 발생했습니다: {e}. 컬럼 이름을 확인해주세요.")
        st.stop()

    # --- Process Weekly Facilities Data (Province Level) ---
    weekly_facilities_by_province = standardize_facilities_data(df_weekly_facilities, '주간이용시설', level='province')
    df_merged_weekly_province = pd.merge(population_by_province, weekly_facilities_by_province, on='시도', how='left')
    df_merged_weekly_province['주간이용시설수'] = df_merged_weekly_province['주간이용시설수'].fillna(0).astype(int)
    df_merged_weekly_province['주간이용시설필요지수'] = df_merged_weekly_province['장애인구수'] / (df_merged_weekly_province['주간이용시설수'] + 1)

    # --- Process Welfare Facilities Data (Province Level) ---
    welfare_facilities_by_province = standardize_facilities_data(df_welfare_facilities, '복지관', level='province')
    df_merged_welfare_province = pd.merge(population_by_province, welfare_facilities_by_province, on='시도', how='left')
    df_merged_welfare_province['복지관수'] = df_merged_welfare_province['복지관수'].fillna(0).astype(int)
    df_merged_welfare_province['복지관필요지수'] = df_merged_welfare_province['장애인구수'] / (df_merged_welfare_province['복지관수'] + 1)

    # --- Process Weekly Facilities Data (Sigungu Level) ---
    weekly_facilities_by_sigungu = standardize_facilities_data(df_weekly_facilities, '주간이용시설', level='sigungu')
    df_merged_weekly_sigungu = pd.merge(df_population_sigungu, weekly_facilities_by_sigungu, on='시군구_전체이름', how='left')
    df_merged_weekly_sigungu['주간이용시설수'] = df_merged_weekly_sigungu['주간이용시설수'].fillna(0).astype(int)
    df_merged_weekly_sigungu['주간이용시설필요지수'] = df_merged_weekly_sigungu['총인구_소계'] / (df_merged_weekly_sigungu['주간이용시설수'] + 1)

    # --- Process Welfare Facilities Data (Sigungu Level) ---
    welfare_facilities_by_sigungu = standardize_facilities_data(df_welfare_facilities, '복지관', level='sigungu')
    df_merged_welfare_sigungu = pd.merge(df_population_sigungu, welfare_facilities_by_sigungu, on='시군구_전체이름', how='left')
    df_merged_welfare_sigungu['복지관수'] = df_merged_welfare_sigungu['복지관수'].fillna(0).astype(int)
    df_merged_welfare_sigungu['복지관필요지수'] = df_merged_welfare_sigungu['총인구_소계'] / (df_merged_welfare_sigungu['복지관수'] + 1)

    # --- Area Data ---
    area_data = {
        '서울특별시': 605.23,
        '부산광역시': 770.07,
        '대구광역시': 883.49,
        '인천광역시': 1065.23,
        '광주광역시': 501.0,
        '대전광역시': 539.8,
        '울산광역시': 1062.09,
        '세종특별자치시': 465.2,
        '경기도': 10195.27,
        '강원도': 16830.8,
        '충청북도': 7406.95,
        '충청남도': 8246.17,
        '전라북도': 8069.84,
        '전라남도': 12363.1,
        '경상북도': 18428.1,
        '경상남도': 10540.55,
        '제주특별자치도': 1849.02
    }
    df_area = pd.DataFrame(list(area_data.items()), columns=['시도', '면적(㎢)'])

    # --- Area Data (Placeholder for Sigungu Area Data) ---
    # You will need to provide actual si-gun-gu area data here.
    # For now, I'll use a dummy dictionary or load from a CSV if provided by the user.
    sigungu_area_data = {
        '서울특별시 종로구': 23.91, '서울특별시 중구': 9.96, '서울특별시 용산구': 21.87, '서울특별시 성동구': 16.86,
        '서울특별시 광진구': 17.06, '서울특별시 동대문구': 14.22, '서울특별시 중랑구': 18.50, '서울특별시 성북구': 24.58,
        '서울특별시 강북구': 23.60, '서울특별시 도봉구': 20.70, '서울특별시 노원구': 35.44, '서울특별시 은평구': 29.70,
        '서울특별시 서대문구': 17.63, '서울특별시 마포구': 23.85, '서울특별시 양천구': 17.41, '서울특별시 강서구': 41.44,
        '서울특별시 구로구': 20.12, '서울특별시 금천구': 13.02, '서울특별시 영등포구': 24.55, '서울특별시 동작구': 16.35,
        '서울특별시 관악구': 29.57, '서울특별시 서초구': 46.98, '서울특별시 강남구': 39.50, '서울특별시 송파구': 33.87,
        '서울특별시 강동구': 24.59,
        '부산광역시 중구': 2.83, '부산광역시 서구': 13.98, '부산광역시 동구': 9.77, '부산광역시 영도구': 13.96,
        '부산광역시 부산진구': 29.39, '부산광역시 동래구': 16.63, '부산광역시 남구': 26.82, '부산광역시 북구': 38.30,
        '부산광역시 해운대구': 51.47, '부산광역시 사하구': 41.09, '부산광역시 금정구': 65.17, '부산광역시 강서구': 181.50,
        '부산광역시 연제구': 12.10, '부산광역시 수영구': 10.16, '부산광역시 사상구': 36.09, '부산광역시 기장군': 218.30,
        '대구광역시 중구': 7.06, '대구광역시 동구': 182.16, '대구광역시 서구': 17.36, '대구광역시 남구': 17.49,
        '대구광역시 북구': 105.77, '대구광역시 수성구': 76.49, '대구광역시 달서구': 62.27, '대구광역시 달성군': 826.80,
        '대구광역시 군위군': 614.10,
        '인천광역시 중구': 140.10, '인천광역시 동구': 7.04, '인천광역시 미추홀구': 24.85, '인천광역시 연수구': 54.90,
        '인천광역시 남동구': 57.00, '인천광역시 부평구': 32.00, '인천광역시 계양구': 44.50, '인천광역시 서구': 117.00,
        '인천광역시 강화군': 411.40, '인천광역시 옹진군': 172.40,
        '광주광역시 동구': 49.20, '광주광역시 서구': 47.88, '광주광역시 남구': 61.00, '광주광역시 북구': 139.00,
        '광주광역시 광산구': 222.90,
        '대전광역시 동구': 136.60, '대전광역시 중구': 62.00, '대전광역시 서구': 95.50, '대전광역시 유성구': 176.40,
        '대전광역시 대덕구': 68.70,
        '울산광역시 중구': 37.00, '울산광역시 남구': 73.00, '울산광역시 동구': 36.00, '울산광역시 북구': 157.00,
        '울산광역시 울주군': 756.00,
        '세종특별자치시 세종시': 465.20,
        '경기도 수원시 장안구': 33.10, '경기도 수원시 권선구': 47.30, '경기도 수원시 팔달구': 21.60, '경기도 수원시 영통구': 28.60,
        '경기도 성남시 수정구': 46.00, '경기도 성남시 중원구': 27.00, '경기도 성남시 분당구': 69.40, '경기도 의정부시': 81.50,
        '경기도 안양시 만안구': 27.00, '경기도 안양시 동안구': 29.00, '경기도 부천시 원미구': 35.00, '경기도 부천시 소사구': 12.00,
        '경기도 부천시 오정구': 16.00, '경기도 광명시': 38.50, '경기도 평택시': 455.20, '경기도 동두천시': 95.70,
        '경기도 안산시 상록구': 58.00, '경기도 안산시 단원구': 42.00, '경기도 고양시 덕양구': 165.00, '경기도 고양시 일산동구': 59.00,
        '경기도 고양시 일산서구': 43.00, '경기도 과천시': 35.90, '경기도 구리시': 33.30, '경기도 남양주시': 458.00,
        '경기도 오산시': 42.70, '경기도 시흥시': 490.80, '경기도 군포시': 36.40, '경기도 의왕시': 54.00,
        '경기도 하남시': 93.00, '경기도 용인시 처인구': 529.00, '경기도 용인시 기흥구': 86.00, '경기도 용인시 수지구': 42.00,
        '경기도 파주시': 673.00, '경기도 이천시': 531.00, '경기도 안성시': 554.00, '경기도 김포시': 276.00,
        '경기도 화성시': 688.00, '경기도 광주시': 431.00, '경기도 양주시': 310.00, '경기도 포천시': 826.00,
        '경기도 여주시': 608.00, '경기도 연천군': 676.00, '경기도 가평군': 843.00, '경기도 양평군': 878.00,
        '강원특별자치도 춘천시': 1116.00, '강원특별자치도 원주시': 872.00, '강원특별자치도 강릉시': 1040.00, '강원특별자치도 동해시': 180.00,
        '강원특별자치도 태백시': 303.00, '강원특별자치도 속초시': 105.00, '강원특별자치도 삼척시': 1186.00, '강원특별자치도 홍천군': 1820.00,
        '강원특별자치도 횡성군': 998.00, '강원특별자치도 영월군': 1127.00, '강원특별자치도 평창군': 1442.00, '강원특별자치도 정선군': 1220.00,
        '강원특별자치도 철원군': 890.00, '강원특별자치도 화천군': 781.00, '강원특별자치도 양구군': 670.00, '강원특별자치도 인제군': 1646.00,
        '강원특별자치도 고성군': 664.00, '강원특별자치도 양양군': 629.00,
        '충청북도 청주시 상당구': 184.00, '충청북도 청주시 서원구': 122.00, '충청북도 청주시 흥덕구': 198.00, '충청북도 청주시 청원구': 213.00,
        '충청북도 충주시': 984.00, '충청북도 제천시': 883.00, '충청북도 보은군': 584.00, '충청북도 옥천군': 537.00,
        '충청북도 영동군': 846.00, '충청북도 증평군': 81.00, '충청북도 진천군': 406.00, '충청북도 괴산군': 842.00,
        '충청북도 음성군': 521.00, '충청북도 단양군': 781.00,
        '충청남도 천안시 동남구': 280.00, '충청남도 천안시 서북구': 280.00, '충청남도 공주시': 864.00, '충청남도 보령시': 569.00,
        '충청남도 아산시': 542.00, '충청남도 서산시': 741.00, '충청남도 논산시': 837.00, '충청남도 계룡시': 61.00,
        '충청남도 당진시': 694.00, '충청남도 금산군': 575.00, '충청남도 부여군': 625.00, '충청남도 서천군': 364.00,
        '충청남도 청양군': 479.00, '충청남도 홍성군': 444.00, '충청남도 예산군': 542.00, '충청남도 태안군': 504.00,
        '전북특별자치도 전주시 완산구': 100.00, '전북특별자치도 전주시 덕진구': 100.00, '전북특별자치도 군산시': 260.00, '전북특별자치도 익산시': 301.00,
        '전북특별자치도 정읍시': 693.00, '전북특별자치도 남원시': 753.00, '전북특별자치도 김제시': 545.00, '전북특별자치도 완주군': 821.00,
        '전북특별자치도 진안군': 789.00, '전북특별자치도 무주군': 1067.00, '전북특별자치도 장수군': 533.00, '전북특별자치도 임실군': 597.00,
        '전북특별자치도 순창군': 496.00, '전북특별자치도 고창군': 607.00, '전북특별자치도 부안군': 493.00,
        '전라남도 목포시': 47.00, '전라남도 여수시': 501.00, '전라남도 순천시': 911.00, '전라남도 나주시': 604.00,
        '전라남도 광양시': 229.00, '전라남도 담양군': 789.00, '전라남도 곡성군': 547.00, '전라남도 구례군': 483.00,
        '전라남도 고흥군': 807.00, '전라남도 보성군': 663.00, '전라남도 화순군': 787.00, '전라남도 장흥군': 622.00,
        '전라남도 강진군': 495.00, '전라남도 해남군': 1013.00, '전라남도 영암군': 544.00, '전라남도 무안군': 449.00,
        '전라남도 함평군': 337.00, '전라남도 영광군': 474.00, '전라남도 장성군': 519.00, '전라남도 완도군': 396.00,
        '전라남도 진도군': 439.00, '전라남도 신안군': 1004.00,
        '경상북도 포항시 남구': 150.00, '경상북도 포항시 북구': 200.00, '경상북도 경주시': 1324.00, '경상북도 김천시': 1009.00,
        '경상북도 안동시': 1522.00, '경상북도 구미시': 616.00, '경상북도 영주시': 669.00, '경상북도 영천시': 920.00,
        '경상북도 상주시': 842.00, '경상북도 문경시': 1170.00, '경상북도 경산시': 412.00, '경상북도 의성군': 1176.00,
        '경상북도 청송군': 843.00, '경상북도 영양군': 815.00, '경상북도 영덕군': 741.00, '경상북도 청도군': 696.00,
        '경상북도 고령군': 384.00, '경상북도 성주군': 610.00, '경상북도 칠곡군': 451.00, '경상북도 예천군': 660.00,
        '경상북도 봉화군': 1201.00, '경상북도 울진군': 989.00, '경상북도 울릉군': 72.00,
        '경상남도 창원시 의창구': 240.00, '경상남도 창원시 성산구': 82.00, '경상남도 창원시 마산합포구': 240.00, '경상남도 창원시 마산회원구': 90.00,
        '경상남도 창원시 진해구': 120.00, '경상남도 진주시': 713.00, '경상남도 통영시': 238.00, '경상남도 사천시': 398.00,
        '경상남도 김해시': 463.00, '경상남도 밀양시': 1087.00, '경상남도 거제시': 402.00, '경상남도 양산시': 468.00,
        '경상남도 의령군': 483.00, '경상남도 함안군': 606.00, '경상남도 창녕군': 533.00, '경상남도 고성군': 664.00,
        '경상남도 남해군': 357.00, '경상남도 하동군': 723.00, '경상남도 산청군': 794.00, '경상남도 함양군': 725.00,
        '경상남도 거창군': 804.00, '경상남도 합천군': 983.00,
        '제주특별자치도 제주시': 978.00, '제주특별자치도 서귀포시': 871.00
    }
    df_sigungu_area = pd.DataFrame(list(sigungu_area_data.items()), columns=['시군구_전체이름', '면적(㎢)'])

    # Merge area data with merged dataframes (Province Level)
    df_merged_weekly_province = pd.merge(df_merged_weekly_province, df_area, on='시도', how='left')
    df_merged_welfare_province = pd.merge(df_merged_welfare_province, df_area, on='시도', how='left')

    # Calculate facilities per area (Province Level)
    df_merged_weekly_province['주간이용시설_밀도'] = df_merged_weekly_province['주간이용시설수'] / df_merged_weekly_province['면적(㎢)']
    df_merged_welfare_province['복지관_밀도'] = df_merged_welfare_province['복지관수'] / df_merged_welfare_province['면적(㎢)']

    # Merge area data with merged dataframes (Sigungu Level)
    df_merged_weekly_sigungu = pd.merge(df_merged_weekly_sigungu, df_sigungu_area, on='시군구_전체이름', how='left')
    df_merged_welfare_sigungu = pd.merge(df_merged_welfare_sigungu, df_sigungu_area, on='시군구_전체이름', how='left')

    # Calculate facilities per area (Sigungu Level)
    df_merged_weekly_sigungu['주간이용시설_밀도'] = df_merged_weekly_sigungu['주간이용시설수'] / df_merged_weekly_sigungu['면적(㎢)']
    df_merged_welfare_sigungu['복지관_밀도'] = df_merged_welfare_sigungu['복지관수'] / df_merged_welfare_sigungu['면적(㎢)']

    tab3, tab4 = st.tabs(["시군구별 주간이용시설 필요도", "시군구별 장애인복지관 필요도"])

    with tab3:
        st.header("시군구별 장애인구수 대비 주간이용시설 필요도")
        fig_weekly_sigungu = px.choropleth(
            df_merged_weekly_sigungu,
            geojson=geojson,
            locations='시군구',
            featureidkey="properties.name",
            color='주간이용시설필요지수',
            hover_name='시군구',
            hover_data={'총인구_소계': ':,', '주간이용시설수': ':,', '주간이용시설필요지수': ':.2f', '주간이용시설_밀도': ':.5f'},
            color_continuous_scale="Reds",
            title=" "
        )
        fig_weekly_sigungu.update_geos(fitbounds="locations", visible=False)
        fig_weekly_sigungu.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, title_font_size=20, title_x=0.5)
        st.plotly_chart(fig_weekly_sigungu, use_container_width=True)

    with tab4:
        st.header("시군구별 장애인구수 대비 장애인복지관 필요도")
        fig_welfare_sigungu = px.choropleth(
            df_merged_welfare_sigungu,
            geojson=geojson,
            locations='시군구',
            featureidkey="properties.name",
            color='복지관필요지수',
            hover_name='시군구',
            hover_data={'총인구_소계': ':,', '복지관수': ':,', '복지관필요지수': ':.2f', '복지관_밀도': ':.5f'},
            color_continuous_scale="Blues",
            title=" "
        )
        fig_welfare_sigungu.update_geos(fitbounds="locations", visible=False)
        fig_welfare_sigungu.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, title_font_size=20, title_x=0.5)
        st.plotly_chart(fig_welfare_sigungu, use_container_width=True)