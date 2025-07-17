import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .constants import province_geojson_name_map, reverse_province_geojson_name_map, province_coords, area_data

def plot_animated_pie_chart(df_national_total):

    # Initialize session state for options
    if 'pie_chart_options' not in st.session_state:
        st.session_state.pie_chart_options = {
            'threshold_percentage': 4.0,
            'animation_duration': 400,
            'selected_palette': 'Alphabet'
        }

    df_national_total_filtered_all_years = df_national_total[df_national_total['장애유형별'] != '합계'].copy()
    df_national_total_melted = df_national_total_filtered_all_years.melt(id_vars=['시도별', '성별', '장애유형별'],
                                                                          var_name='연도', value_name='인구수')
    df_national_total_melted['연도'] = df_national_total_melted['연도'].astype(int)

    years = sorted(df_national_total_melted['연도'].unique())

    # Use options from session state
    options = st.session_state.pie_chart_options
    threshold_percentage = options['threshold_percentage'] / 100
    animation_duration = options['animation_duration']
    selected_palette = options['selected_palette']

    color_palettes = [
        "Plotly", "D3", "G10", "T10", "Alphabet", "Dark24", "Light24",
        "Set1", "Set2", "Set3", "Pastel1", "Pastel2"
    ]

    all_disability_types = sorted(df_national_total_melted['장애유형별'].unique())
    if "기타" not in all_disability_types:
        all_disability_types.append("기타")

    colors = getattr(px.colors.qualitative, selected_palette)
    color_map = {disability_type: colors[i % len(colors)] for i, disability_type in enumerate(all_disability_types)}

    frames = []
    for year in years:
        frame_data = df_national_total_melted[df_national_total_melted['연도'] == year].copy()
        
        total_population_year = frame_data['인구수'].sum()

        if total_population_year > 0:
            frame_data['percentage'] = frame_data['인구수'] / total_population_year
            small_slices = frame_data[frame_data['percentage'] < threshold_percentage]
            
            if not small_slices.empty:
                other_sum = small_slices['인구수'].sum()
                detail_lines = [f"<br>- {row['장애유형별']}: {row['인구수']:,}명 ({row['percentage']:.1%})" for idx, row in small_slices.iterrows()]
                other_detail_info = "<br>--- 기타 상세 ---" + "".join(detail_lines)

                frame_data = frame_data[frame_data['percentage'] >= threshold_percentage]
                frame_data = pd.concat([frame_data, pd.DataFrame([{'장애유형별': '기타', '인구수': other_sum, 'hover_detail': other_detail_info}])], ignore_index=True)
            else:
                frame_data['hover_detail'] = ""
        else:
            frame_data['hover_detail'] = ""
        
        frame_data = frame_data.sort_values(by='장애유형별')
        pie_colors = [color_map[dt] for dt in frame_data['장애유형별']]

        frames.append(go.Frame(data=[go.Pie(labels=frame_data['장애유형별'],
                                            values=frame_data['인구수'],
                                            hole=0.3,
                                            textposition='inside',
                                            textinfo='percent+label',
                                            marker=dict(colors=pie_colors, line=dict(color='#000000', width=1)),
                                            customdata=frame_data[['hover_detail']].values,
                                            hovertemplate="<b>%{label}</b><br>인구수: %{value:,}<br>비율: %{percent}%{customdata[0]}")],
                                name=str(year)))

    initial_year_data = df_national_total_melted[df_national_total_melted['연도'] == years[0]].copy()
    
    total_population_initial = initial_year_data['인구수'].sum()
    if total_population_initial > 0:
        initial_year_data['percentage'] = initial_year_data['인구수'] / total_population_initial
        small_slices_initial = initial_year_data[initial_year_data['percentage'] < threshold_percentage]
        
        if not small_slices_initial.empty:
            other_sum_initial = small_slices_initial['인구수'].sum()
            detail_lines_initial = [f"<br>- {row['장애유형별']}: {row['인구수']:,}명 ({row['percentage']:.1%})" for idx, row in small_slices_initial.iterrows()]
            other_detail_info_initial = "<br>--- 기타 상세 ---" + "".join(detail_lines_initial)

            initial_year_data = initial_year_data[initial_year_data['percentage'] >= threshold_percentage]
            initial_year_data = pd.concat([initial_year_data, pd.DataFrame([{'장애유형별': '기타', '인구수': other_sum_initial, 'hover_detail': other_detail_info_initial}])], ignore_index=True)
        else:
            initial_year_data['hover_detail'] = ""
    else:
        initial_year_data['hover_detail'] = ""

    initial_year_data = initial_year_data.sort_values(by='장애유형별')
    initial_pie_colors = [color_map[dt] for dt in initial_year_data['장애유형별']]

    fig_pie_animated = go.Figure(
        data=[go.Pie(labels=initial_year_data['장애유형별'],
                     values=initial_year_data['인구수'],
                     hole=0.3,
                     textposition='inside',
                     textinfo='percent+label',
                     marker=dict(colors=initial_pie_colors, line=dict(color='#000000', width=1)),
                     customdata=initial_year_data[['hover_detail']].values,
                     hovertemplate="<b>%{label}</b><br>인구수: %{value:,}<br>비율: %{percent}%{customdata[0]}")],
        layout=go.Layout(
            title_text='전국 장애유형별 인구 비율',
            legend=dict(x=1.02, y=1, xanchor='left', yanchor='top'),
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None, {"frame": {"duration": animation_duration, "redraw": True},
                                           "fromcurrent": True,
                                           "transition": {"duration": 300, "easing": "quadratic-in-out"}}])])])
        ,
        frames=frames
    )

    sliders = [dict(
        steps=[dict(method='animate',
                    args=[[str(year)],
                          dict(mode='immediate',
                               frame=dict(duration=animation_duration, redraw=True),
                               transition=dict(duration=300),
                               layout=dict(title_text=f'{year}년 전국 장애유형별 인구 비율 (성별: 계)'))],
                    label=str(year)) for year in years],
        transition=dict(duration=300),
        x=0.08,
        len=0.88,
        currentvalue=dict(font=dict(size=16), prefix="Year:", visible=True, xanchor="right"),
        pad=dict(t=50)
    )]

    fig_pie_animated.update_layout(sliders=sliders)
    st.plotly_chart(fig_pie_animated, use_container_width=True)

    with st.expander("차트 옵션"):
        st.slider(
            "파이 차트 '기타' 그룹화 임계값 (%)", 0.0, 10.0,
            options['threshold_percentage'], 0.1,
            key='threshold_slider_pie',
            help="값이 작은 항목들을 '기타'로 묶는 기준이 되는 비율(%)입니다."
        )
        st.slider(
            "애니메이션 속도 (ms)", 100, 2000,
            options['animation_duration'], 100,
            key='animation_slider_pie',
            help="애니메이션의 프레임 전환 속도를 밀리초(ms) 단위로 설정합니다."
        )
        st.selectbox(
            "색상 팔레트 선택", color_palettes,
            index=color_palettes.index(options['selected_palette']),
            key='palette_selector_pie'
        )

        # Update session state if widgets change
        options['threshold_percentage'] = st.session_state.threshold_slider_pie
        options['animation_duration'] = st.session_state.animation_slider_pie
        options['selected_palette'] = st.session_state.palette_selector_pie