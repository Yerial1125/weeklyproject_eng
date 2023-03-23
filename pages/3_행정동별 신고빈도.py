# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import pandas as pd
import platform
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from folium.plugins import MarkerCluster


# 페이지 설정
st.set_page_config(
    page_title = '구급출동 데이터 분석',
    page_icon = ':ambulance:',
    layout='wide')

# 행정동별 신고빈도 파일 불러오기
df = pd.read_csv('./data/dong_total_count.csv')
df = df.set_index(keys='읍면동명', drop=True)

st.subheader(':white_check_mark:2021년도 행정동별 구급신고 빈도(지도시각화)')
st.markdown('---')

# 동 영어
dong_eng = pd.read_csv('./data/dong_loc.csv')

# 가나다순 -> 내림차순 정렬 체크박스
agree = st.checkbox('신고빈도 수 내림차순 정렬')

#배치
col1, col2 = st.columns([0.2,0.8])
with col1 :
    if agree:
        df_sort = df.sort_values(by='신고건수', ascending=False)
        df_sort
    else:
        df

# folium 지도 시각화
with open ('data/seoul.json', encoding='utf-8') as f:
    geo_seoul = json.loads(f.read())

dong_marker = pd.read_csv('./data/행정동좌표.csv')

m = folium.Map(location=[37.566535, 126.9779691999996],zoom_start=11)
folium.Choropleth(geo_data = geo_seoul,
                 data = df['신고건수'],
                  columns = [df.index, df['신고건수']],
                  fill_color = 'YlGn', fill_opacity=0.7,
                  line_opacity=0.3,
                  key_on='feature.properties.EMD_NM',).add_to(m)
mc = MarkerCluster().add_to(m)

for i in range(len(dong_marker)) :
    folium.Marker(location=(dong_marker.iloc[i,5], dong_marker.iloc[i,6]),
                  popup=folium.Popup(dong_marker.iloc[i,3], max_width=200),
                 tooltip=dong_marker.iloc[i,3]).add_to(mc)
with col2 :
    st_folium(m,width=750)
st.markdown('---')


# 신고 빈도 상위 20개동 df, 바그래프
st.subheader(':white_check_mark:2021년도 구급신고 빈도 상위 20개동')
col3, col4 = st.columns([0.2,0.8])
dong_20 = df.sort_values(by='신고건수', ascending=False).iloc[:20,:]
dong_20['eng'] = list(dong_eng['동이름'])

with col3 :
    dong_20.iloc[:,0]

with col4 :
    sns.barplot(x=dong_20.eng, y='신고건수', data=dong_20, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Dong')
    plt.ylabel('count')
    plt.grid('y')
    st.pyplot(plt)

st.markdown('---')

# 행정동별 신고 빈도 멑티선택 df, 바그래프
st.subheader(':white_check_mark:2021년도 행정동별 구급신고 빈도(선택)')

option = st.multiselect('행정동을 선택하세요', df.index, default=['신림동','봉천동','화곡동','상계동','신정동'])
col5, col6 = st.columns([0.2,0.8])
with col5:
    df_1 = df.loc[option]
    df_1
    df_1['num'] = range(1,len(df_1)+1)
    df_1['num'] = df_1['num'].astype('str')+'th  select'

with col6:
    sns.barplot(x=df_1.num, y='신고건수', data=df_1, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Dong')
    plt.ylabel('Count')
    plt.grid('y')
    st.pyplot(plt)