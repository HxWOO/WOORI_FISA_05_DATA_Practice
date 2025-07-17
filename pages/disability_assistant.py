import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

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
    fig.update_layout(
        title=title,
        xaxis_title='년도',
        yaxis_title=y_label,
        yaxis=dict(range=[min_val - range_extension, max_val + range_extension]),
        xaxis = dict(
            tickmode = 'linear',
            tick0 = df['년도'].min(),
            dtick = 1  # 1년 단위로 눈금 표시
        )
    )
    st.plotly_chart(fig)

# 기초생활수급자 변화 추이
st.header("기초생활수급자 변화 추이")

st.subheader("기초생활수급자 수급자-일반 변화 추이")
create_line_chart(df_selected, '기초생활수급자 수급자-일반', f'{selected_city} 기초생활수급자 수급자-일반 변화 추이', '수급자 수')

st.subheader("기초생활수급자 수급자-중증 변화 추이")
create_line_chart(df_selected, '기초생활수급자 수급자-중증', f'{selected_city} 기초생활수급자 수급자-중증 변화 추이', '수급자 수')

# 차상위계층 변화 추이
st.header("차상위계층 변화 추이")

st.subheader("차상위계층 수급자-일반 변화 추이")
create_line_chart(df_selected, '차상위계층 수급자-일반', f'{selected_city} 차상위계층 수급자-일반 변화 추이', '수급자 수')

st.subheader("차상위초과 변화 추이")
create_line_chart(df_selected, ' 차상위초과', f'{selected_city} 차상위초과 변화 추이', '수급자 수')
