import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def plot_national_trend_line_chart(df_national_total):
    st.write("### 연도별 전국 장애인구 총계 추이 (성별: 계)")

    df_trend = df_national_total[df_national_total['장애유형별'] == '합계'].melt(id_vars=['시도별', '성별', '장애유형별'],
                                                                  var_name='연도', value_name='인구수')
    df_trend['연도'] = df_trend['연도'].astype(int)

    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(x=df_trend['연도'], 
                                  y=df_trend['인구수'], 
                                  mode='lines', 
                                  name='총계 추이',
                                  line=dict(color='blue')))

    fig_line.update_layout(title='연도별 전국 장애인구 총계 추이 (성별: 계)',
                           xaxis_title='연도',
                           yaxis_title='인구수',
                           hovermode="x unified")
    fig_line.update_layout(hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True)
