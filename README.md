# 미니 프로젝트: 장애인 관련 데이터 분석 및 시각화

본 프로젝트는 장애인 관련 공공 데이터를 활용하여 현실적인 문제를 분석하고 시각화하는 것을 목표로 합니다. 4명의 팀원이 각각 복지, 인구 분포, 고용 및 경제활동, 관련 시설이라는 하위 주제를 맡아 데이터 분석 및 시각화를 진행했으며, Streamlit을 사용하여 웹 애플리케이션으로 구현했습니다.

## 📋 목차

1. [프로젝트 소개](#-프로젝트-소개)
2. [주요 기능](#-주요-기능)
3. [사용 기술](#️-사용-기술)
4. [설치 및 실행](#-설치-및-실행)
5. [배포 링크](#-배포)
6. [트러블 슈팅](#-트러블-슈팅)
7. [기여자](#-기여자)

## 💻 프로젝트 소개

장애인 관련 현실 데이터를 기반으로 사회적 문제에 대한 인사이트를 도출하고, 이를 효과적으로 전달하기 위해 데이터 분석 및 시각화를 수행했습니다. 각 팀원은 개별 주제에 대한 분석을 진행하고, 이를 Streamlit 기반의 대시보드로 통합하여 사용자가 쉽게 상호작용할 수 있도록 만들었습니다.

## ✨ 주요 기능

- **장애인 복지**: 사회적 취약계층으로서 장애인이 받는 복지 서비스 관련 데이터를 분석하고 시각화합니다.
- **장애인 인구 분포**: 지역별, 유형별 장애인 인구 통계를 분석하고, 지도 및 차트를 통해 분포 현황을 시각화합니다.
- **장애인 고용 및 경제활동**: 장애인의 경제활동상태, 고용률 등의 데이터를 분석하여 시간의 흐름에 따른 변화를 시각화합니다.
- **장애인 관련 시설**: 전국 장애인 관련 복지 시설의 분포 및 현황을 분석하고, 지도 위에 시각화합니다.

## 📂 디렉토리 구조

```
C:/devs/data_practice/
├───.gitignore
├───app.py
├───README.md
├───requirements.txt
├───data/
│   ├───보건복지부_장애인복지관 현황_20240425_utf8.csv
│   ├───시군구별_장애정도별_성별_등록장애인수_20250717111030.csv
│   ├───장애인_경제활동상태__지역별_수도권__광역시권__기타_시도__20250716153838.xlsx
│   ├───Disability_Assistance.csv
│   ├───disability_facilities.csv
│   ├───disable_age.xlsx
│   ├───disable_edu.xlsx
│   ├───disable_power.xlsx
│   ├───disable_region.xlsx
│   ├───disable_sex.xlsx
│   ├───disable_type.xlsx
│   ├───korean_disabled_population_statistics.csv
│   └───skorea_provinces_geo.json
├───disable_pop/
│   ├───constants.py
│   ├───visualize_animated_pie_chart.py
│   ├───visualize_gender_trend_line_chart.py
│   ├───visualize_national_trend_line_chart.py
│   ├───visualize_population.py
│   ├───visualize_regional_map_chart.py
├───employ_analysis/
│   ├───load_data.py
│   ├───run_analysis.py
│   ├───visualize_age_plotly.py
│   ├───visualize_edu_plotly.py
│   ├───visualize_region_plotly.py
│   ├───visualize_sex_pie_plotly.py
│   ├───visualize_sex_plotly.py
│   ├───visualize_total_eco_activity_time_series.py
│   ├───visualize_type_plotly.py
└───pages/
    ├───disability_assistant.py
    ├───disabled_population_statistics.py
    ├───employ.py
    └───facility.py
```

## 🛠️ 사용 기술

- **언어**: Python
- **프레임워크**: Streamlit
- **라이브러리**: Pandas, Plotly, openpyxl

## 🚀 설치 및 실행

1. **저장소 클론:**
   ```bash
   git clone https://github.com/woori-fisa-pro-05/data_practice.git
   cd data_practice
   ```

2. **가상 환경 생성 및 활성화:**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **의존성 설치:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Streamlit 앱 실행:**
   ```bash
   streamlit run app.py
   ```

## 🔗 배포

- **Streamlit Cloud 배포 링크**: [https://woori-fisa-05-datapractice.streamlit.app/](https://woori-fisa-05-datapractice.streamlit.app/)

## 📊 데이터 출처

- **시군구별, 장애정도별, 성별 등록장애인수 (국가통계포털)**
  - 출처: [KOSIS 국가통계포털](https://kosis.kr/statHtml/statHtml.do?orgId=117&tblId=DT_11761_N001&conn_path=I2)
  - 데이터명: 보건복지부, 「장애인현황」, 2024, 2025.07.18, 전국 장애유형별, 성별 등록장애인수

- **보건복지부_장애인복지관 현황 (공공데이터포털)**
  - 출처: [공공데이터포털](https://www.data.go.kr/data/15044286/fileData.do)
  - 데이터명: 보건복지부_장애인복지관 현황_20240425_utf8.csv

- **보건복지부_장애인연금 수급자 현황_시도별 (공공데이터포털)**
  - 출처: [공공데이터포털](https://www.data.go.kr/data/15044286/fileData.do)
  - 데이터명: 보건복지부_장애인연금 수급자 현황_시도별_20231231

## 🤯 트러블 슈팅

프로젝트 진행 중 발생했던 주요 문제와 해결 과정입니다.

1.  **Plotly Pie Chart Hover 정보 오류**
    - **문제**: `customdata`에 여러 열의 정보를 전달하여 `hovertemplate`에서 표시하려고 할 때, 데이터가 배열로 인식되지 않고 문자열 그대로 출력되는 현상이 발생했습니다.
    - **해결**: 여러 열의 데이터를 `f-string`을 사용하여 하나의 HTML 형식 문자열로 합친 후, `customdata`에 전달하여 문제를 해결했습니다.

2.  **로컬 및 배포 환경의 파일 경로 불일치**
    - **문제**: 로컬 시스템의 절대 경로로 데이터 파일을 참조하여, Streamlit Cloud 배포 환경에서 `FileNotFoundError`가 발생했습니다.
    - **해결**: `pathlib` 라이브러리를 사용하여 현재 파일 위치를 기준으로 하는 상대 경로를 설정함으로써, 로컬과 배포 환경 모두에서 파일 경로가 올바르게 작동하도록 수정했습니다.

3.  **두 개의 Plotly 차트 통합 오류**
    - **문제**: 각각 다른 함수에서 생성된 두 개의 `Figure` 객체를 `add_trace()`를 이용해 하나의 차트로 합치려고 시도했으나, 의도대로 동작하지 않았습니다.
    - **해결**: 하나의 차트 생성 함수 내에서 빈 `Figure` 객체를 먼저 만들고, 그곳에 `add_trace()`를 사용하여 각 데이터에 대한 `Scatter` trace를 순차적으로 추가하는 방식으로 로직을 변경하여 해결했습니다.

4.  **Streamlit UI 옵션 배치 문제**
    - **문제**: 차트 아래에 슬라이더나 선택 상자 같은 UI 옵션을 배치하려고 할 때, Streamlit의 순차적 실행 방식과 위젯 ID 관리 방식 때문에 `NameError` 또는 `StreamlitDuplicateElementId` 오류가 발생했습니다.
    - **해결**: `st.session_state`를 활용하여 UI 상태를 명시적으로 관리했습니다. 스크립트 상단에서 초기 옵션 값을 `st.session_state`에 저장하고, 차트는 이 상태 값을 참조하여 먼저 렌더링했습니다. 그 후, `st.expander`를 이용해 차트 아래에 UI 위젯을 배치하고, 각 위젯에 고유한 `key`를 부여하여 ID 중복을 방지했습니다. 이 방식을 통해 차트와 UI가 동일한 상태를 공유하면서도 원하는 위치에 배치할 수 있었습니다.

5.  **시설 필요도 분석 단위 문제**
    - **문제**: 초기 시도 단위로 '장애인구수 ÷ 시설 개수'를 계산하여 필요도를 산출했을 때, 면적이 넓은 시도 내부의 지역별 차이를 반영하기 어렵고, 인접한 시·도 간 인구 규모가 비슷해도 시설 분포가 왜곡되어 보이는 문제가 발생했습니다. (예: 대구광역시와 경상북도)
    - **원인 분석**: 시도별 집계 시, 광역시(대구)처럼 작은 면적에 시설이 몰려 있으면 수치가 과도하게 높게 나타나고, 경상북도처럼 넓은 면적에 시설이 분산되어 있으면 수치가 낮게 나타나는 현상이 발생했습니다.
    - **해결 방안**: 분석 단위를 '시군구'로 세분화하여 각 시군구별 장애인구수와 시설 개수를 집계했습니다. 이를 통해 각 구역별 수요-공급 불균형을 더 정밀하게 파악하고, 동일한 시도 내에서도 지역별로 다른 수요 패턴을 시각화할 수 있었습니다.
    - **결과**: 시군구 단위 지도로 재분석한 결과, 중심 도심 구역과 외곽 군 단위의 수요 격차가 훨씬 명확해졌으며, 대구광역시 내부에서도 수요가 높은 지역(예: 동구·중구 등)과 낮은 지역을 구분할 수 있었습니다.

## 🧑‍💻 기여자

| 이름 | 담당 주제 |
| --- | --- |
| **박진서** | 장애인 복지 |
| **남상원** | 장애인 인구 분포 |
| **김현우** | 장애인 고용, 경제활동 |
| **민지수** | 장애인 관련 시설 |