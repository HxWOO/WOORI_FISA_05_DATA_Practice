import streamlit as st
import pandas as pd
import plotly.express as px

def plot_gender_trend_line_chart(df):

    df_gender = df[
        (df['시도별'] == '전국') &
        (df['장애유형별'] == '합계') &
        (df['성별'] != '계')
    ].copy()

    df_gender_melted = df_gender.melt(
        id_vars=['시도별', '성별', '장애유형별'],
        var_name='연도',
        value_name='인구수'
    )
    df_gender_melted['연도'] = df_gender_melted['연도'].astype(int)
    df_gender_melted['성별'] = df_gender_melted['성별'].str.strip()

    fig_line_gender = px.line(
        df_gender_melted,
        x='연도',
        y='인구수',
        color='성별',
        title='연도별 전국 성별 장애인구 총계 추이',
        markers=True,
        color_discrete_map={"남자": "blue", "여자": "red"}
    )
    fig_line_gender.update_layout(hovermode="x unified")
    fig_line_gender.update_traces(hovertemplate='%{y:,}명')
    st.plotly_chart(fig_line_gender, use_container_width=True)
