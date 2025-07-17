import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from .constants import province_geojson_name_map, reverse_province_geojson_name_map, province_coords, area_data

def plot_regional_map_chart(df, geojson_data):

    df_region_all_years = df[
        (df['시도별'] != '전국') &
        (df['성별'] == '계') &
        (df['장애유형별'] == '합계')
    ].copy()

    df_region_melted_all_years = df_region_all_years.melt(
        id_vars=['시도별', '성별', '장애유형별'],
        var_name='연도',
        value_name='인구수'
    )
    df_region_melted_all_years['연도'] = df_region_melted_all_years['연도'].astype(int)

    df_region_melted_all_years['시도별'] = df_region_melted_all_years['시도별'].replace({
        '강원특별자치도': '강원도',
        '전북특별자치도': '전라북도'
    })

    df_region_melted_all_years['면적'] = df_region_melted_all_years['시도별'].map(area_data)
    df_region_melted_all_years['인구밀도'] = df_region_melted_all_years['인구수'] / df_region_melted_all_years['면적']

    df_region_melted_all_years['lat'] = df_region_melted_all_years['시도별'].map(lambda x: province_coords.get(x, {}).get('lat'))
    df_region_melted_all_years['lon'] = df_region_melted_all_years['시도별'].map(lambda x: province_coords.get(x, {}).get('lon'))

    df_region_melted_all_years.dropna(subset=['lat', 'lon', '면적', '인구밀도'], inplace=True)

    for feature in geojson_data['features']:
        feature['id'] = feature['properties']['name']

    initial_year = sorted(df_region_melted_all_years['연도'].unique())[0]
    initial_df = df_region_melted_all_years[df_region_melted_all_years['연도'] == initial_year]

    choropleth_trace = go.Choroplethmapbox(
        geojson=geojson_data,
        locations=[reverse_province_geojson_name_map[sido] for sido in initial_df['시도별']],
        z=initial_df['인구밀도'],
        colorscale="Viridis",
        zmin=df_region_melted_all_years['인구밀도'].min(),
        zmax=df_region_melted_all_years['인구밀도'].max(),
        marker_opacity=0.7,
        marker_line_width=0,
        name='인구 밀도',
        showlegend=True,
        hovertemplate="<b>%{location}</b><br>인구 밀도: %{z:.2f}<extra></extra>",
        colorbar=dict(
            orientation="v",
            x=1.02, # Move to the right of the plot
            xanchor="left",
            y=0, # Align to the bottom
            yanchor="bottom",
            title="인구 밀도",
            len=0.4, # Keep length reasonable
            thickness=10 # Keep thickness reasonable
        )
    )

    scatter_trace = go.Scattermapbox(
        lat=initial_df['lat'],
        lon=initial_df['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=initial_df['인구수'],
            sizemode='area',
            sizeref=2.*max(df_region_melted_all_years['인구수'])/(60.**2),
            sizemin=4,
            color=initial_df['인구밀도'],
            colorscale="Viridis",
            showscale=False,
            cmin=df_region_melted_all_years['인구밀도'].min(),
            cmax=df_region_melted_all_years['인구밀도'].max(),
            opacity=0.8
        ),
        hoverinfo='text',
        text=initial_df.apply(lambda row: f"<b>{row['시도별']}</b><br>인구수: {row['인구수']:,}<br>인구 밀도: {row['인구밀도']:.2f}", axis=1),
        name='장애인구수',
        showlegend=True
    )

    fig_map = go.Figure(data=[choropleth_trace, scatter_trace])

    frames = []
    for year in sorted(df_region_melted_all_years['연도'].unique()):
        df_year = df_region_melted_all_years[df_region_melted_all_years['연도'] == year]
        frames.append(go.Frame(
            data=[
                go.Choroplethmapbox(
                    locations=[reverse_province_geojson_name_map[sido] for sido in df_year['시도별']],
                    z=df_year['인구밀도']
                ),
                go.Scattermapbox(
                    lat=df_year['lat'],
                    lon=df_year['lon'],
                    marker=go.scattermapbox.Marker(
                        size=df_year['인구수'],
                        color=df_year['인구밀도']
                    ),
                    text=df_year.apply(lambda row: f"<b>{row['시도별']}</b><br>인구수: {row['인구수']:,}<br>인구 밀도: {row['인구밀도']:.2f}", axis=1)
                )
            ],
            name=str(year)
        ))
    fig_map.frames = frames

    fig_map.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=5,
        mapbox_center={"lat": 36.4, "lon": 127.8},
        title_text='연도별 시도별 장애인구 총계 및 밀도',
        legend=dict(
            x=0.02,
            y=0.98,
            yanchor='top',
            xanchor='left',
            bgcolor='rgba(255, 255, 255, 0.7)',
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1
        ),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None, {"frame": {"duration": 500, "redraw": True},
                                       "fromcurrent": True,
                                       "transition": {"duration": 300, "easing": "quadratic-in-out"}}])])
        ],
        sliders=[dict(
            steps=[dict(method='animate',
                        args=[[str(year)],
                              dict(mode='immediate',
                                   frame=dict(duration=500, redraw=True),
                                   transition=dict(duration=300),
                                   layout=dict(title_text=f'{year}년 시도별 장애인구 총계 및 밀도 (성별: 계)'))],
                        label=str(year)) for year in sorted(df_region_melted_all_years['연도'].unique())],
            transition=dict(duration=300),
            x=0.08,
            len=0.88,
            currentvalue=dict(font=dict(size=16), prefix="Year:", visible=True, xanchor="right"),
            pad=dict(t=50)
        )]
    )

    st.plotly_chart(fig_map, use_container_width=True)