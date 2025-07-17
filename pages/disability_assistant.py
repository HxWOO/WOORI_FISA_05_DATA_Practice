import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# 사이드바 페이지 링크 추가
st.sidebar.header("분석 페이지")
st.sidebar.page_link("app.py", label="홈", icon="🏠")
st.sidebar.page_link("pages/disability_assistant.py", label="복지", icon="🤝")
st.sidebar.page_link("pages/disabled_population_statistics.py", label="인구분포", icon="👨‍👩‍👧‍👦")
st.sidebar.page_link("pages/employ.py", label="고용 및 경제활동", icon="💼")
st.sidebar.page_link("pages/facility.py", label="관련 시설", icon="🏥")

# 데이터 불러오기
file_path = f"{Path(__file__).parent.parent}/data/Disability_Assistance.csv"

# CSV 데이터 DataFrame으로 변환
df = pd.read_csv(file_path)

# 전국 데이터 집계
df_national = df.groupby('년도')[['기초생활수급자 수급자-일반', '기초생활수급자 수급자-중증', '차상위계층 수급자-일반', ' 차상위초과']].sum().reset_index()
df_national['시도'] = '전국'

# 시도 선택을 위한 selectbox
available_cities = df['시도'].unique()
selected_city = st.selectbox('시도를 선택하세요:', ['전국'] + list(available_cities))

# 선택된 시도에 따라 DataFrame 필터링
if selected_city == '전국':
    df_selected = df_national
else:
    df_selected = df[df['시도'] == selected_city]

# Streamlit 제목
st.title(f'{selected_city} 기초생활수급자 및 차상위계층 현황')

# y축 범위 조정 함수
def create_line_chart(df, y_column, title, y_label):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['년도'], y=df[y_column], mode='lines', name=y_column))

    # y축 범위 자동 조정
    min_val = df[y_column].min()
    max_val = df[y_column].max()
    range_extension = (max_val - min_val) * 0.1  # 10% 여유

    # X축 범위 설정
    x_min = df['년도'].min()
    x_max = 2022  # 2022년도 추가
    x_range = [x_min, x_max]

    # x축 눈금 값 명시적으로 설정
    tickvals = sorted(list(df['년도'].unique()) + [x_max])
    ticktext = [str(year) for year in tickvals]  # 연도를 문자열로 변환

    fig.update_layout(
        title=title,
        xaxis_title='년도',
        yaxis_title=y_label,
        yaxis=dict(range=[min_val - range_extension, max_val + range_extension]),
        xaxis = dict(
            tickmode = 'array',  # tickmode를 'array'로 설정
            tickvals = tickvals,   # 눈금 값을 명시적으로 설정
            ticktext = ticktext,   # 눈금 텍스트를 눈금 값과 동일하게 설정
            range=x_range,          # x축 범위 설정
        ),
        font=dict(size=12)  # 폰트 크기를 12pt로 설정 (기본 크기)
    )
    st.plotly_chart(fig)

# 설명 텍스트
explanation = """
<장애인 기초생활수급자> :
장애인 기초생활수급자는 장애인으로서 소득과 재산이 최저생계 수준 이하인 경우, 정부로부터 생계급여를 지원받는 대상입니다.\n 이들은 장애로 인해 일상생활이 어려운 경우가 많아, 기본적인 생계를 유지할 수 있도록 별도의 지원과 복지 서비스를 받을 수 있습니다.\n

<장애인 차상위계층> :
장애인 차상위계층은 장애인이면서 소득이 낮아 일정 기준 이하인 계층을 의미합니다.\n 이들은 기초생활수급자는 아니지만, 소득이 낮거나 의료 부담이 큰 장애인 가구에 속하며, 다양한 복지혜택(예: 의료비·교육비 지원)을 받을 수 있습니다.\n 주로 중위소득의 일정 비율 이하에 해당하는 장애인 가구를 대상으로 하며, 장애 유무에 따라 차등 지원이 이루어집니다.
"""

# 탭 스타일 및 툴팁 스타일
tab_style = """
<style>
/* 탭 전체 스타일 */
div.stTabs {
    position: relative;
    margin-bottom: 10px; /* 탭 아래 여백 추가 */
}

/* 탭 리스트 스타일 */
div.stTabs ul {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    padding: 5px 10px;
    border-bottom: 1px solid #ddd;
    margin-bottom: 0px;
}

/* 각 탭 스타일 */
div.stTabs li {
    margin-right: 5px;
}

/* 탭 링크 스타일 */
div.stTabs a {
    display: inline-block;
    padding: 8px 15px;
    border-radius: 5px 5px 0 0;
    background-color: #f0f2f6;
    color: #4f4f4f;
    text-decoration: none;
    font-size: medium;
}

div.stTabs a:hover {
    background-color: #d4d8e2;
}

div.stTabs a.active {
    background-color: white;
    color: black;
    border-bottom: 1px solid white;
}

/* 툴팁 스타일 */
.tab-wrapper {  /* 탭 영역 전체를 감싸는 div */
    position: relative;
}

.tooltip {
    position: absolute;
    right: 10px; /* 탭 바 가장 오른쪽에 배치 */
    top: 5px;    /* 탭 상단에 맞춤 */
    display: inline-block;
    font-size: medium;
    cursor: pointer;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 300px;
    background-color: #f9f9f9;
    color: #333;
    text-align: left;
    border-radius: 6px;
    padding: 10px;
    position: absolute;
    z-index: 1;
    top: 120%;
    left: 50%;
    margin-left: -150px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    opacity: 0;
    transition: opacity 0.3s;
    border: 1px solid #ddd;
}

.tooltip .tooltiptext::after {
    content: "";
    position: absolute;
    bottom: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: transparent transparent #f9f9f9 transparent;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}

/* 탭 컨텐츠 영역 스타일 */
.stTabs > div[data-baseweb="tab-content"] {
    margin-top: 0px;
}
</style>
"""

# 툴팁 HTML
tooltip_html = f"""
<div class="tooltip">
    <span>ℹ️</span>
    <span class="tooltiptext">{explanation}</span>
</div>
"""

# 탭 생성
with st.container(): # 전체 컨테이너
    st.markdown(tab_style, unsafe_allow_html=True)
    st.markdown(f'<div class="tab-wrapper">{tooltip_html}</div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs([
        "기초생활수급자 수급자-일반", 
        "기초생활수급자 수급자-중증", 
        "차상위계층 수급자-일반", 
        "차상위초과"
    ])
    with tab1:
        create_line_chart(df_selected, '기초생활수급자 수급자-일반', f'{selected_city} 기초생활수급자 수급자-일반 변화 추이', '수급자 수')

    with tab2:
        create_line_chart(df_selected, '기초생활수급자 수급자-중증', f'{selected_city} 기초생활수급자 수급자-중증 변화 추이', '수급자 수')

    with tab3:
        create_line_chart(df_selected, '차상위계층 수급자-일반', f'{selected_city} 차상위계층 수급자-일반 변화 추이', '수급자 수')

    with tab4:
        create_line_chart(df_selected, ' 차상위초과', f'{selected_city} 차상위초과 변화 추이', '수급자 수')
