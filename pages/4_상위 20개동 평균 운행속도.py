# -*- coding: utf-8 -*-
import matplotlib
import matplotlib as mpl
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



st.set_page_config(
    page_title = '구급출동 데이터 분석',
    page_icon = ':ambulance:',
    layout='wide'
)
# 파일 불러오기
time_df_new = pd.read_csv('./data/time_df_new.csv')
time_df_new = time_df_new.drop(columns='Unnamed: 0')

weeks = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일']
season = ['봄','여름','가을','겨울']

# 영어 동
dong_eng = pd.read_csv('./data/dong_loc.csv')
dong_eng = dong_eng.sort_values(by='동')

# 라디오 버튼
st.subheader(':traffic_light:신고빈도 상위 20개동의 평균 운행속도(km/h)')
st.write('')
col1, col2,c0l3 = st.columns([0.3,0.3,0.3])
with col1 :
    button = st.radio('기준',('시간대별','요일별','월별','계절별'))

# 체크박스
with col2 :
    st.write('조건')
    num = st.checkbox('차트내 값 표시')
st.markdown("---")

if num :
    annot = True
else:
    annot = False
if button == '시간대별' :
    plt.title('Top 20 Dong : Average driving speed on Time', fontsize=30)
    dong_hour = time_df_new.pivot_table(index='읍면동명', columns='출동시', values='거리(km)/시간(분)', aggfunc='mean')*60
    plt.figure(figsize=(20, 10))
    dong_hour.index=list(dong_eng['동이름'])
    sns.heatmap(dong_hour, vmax=dong_hour.max().max(), vmin=dong_hour.min().min(), cmap='Reds', annot=annot, annot_kws={'size': 20}, fmt='.0f')
    plt.xlabel('Time', fontsize=15)
    plt.ylabel('Top 20 Dong', fontsize=15)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20, rotation=0)
    st.pyplot(plt)
elif button == '요일별' :
    dong_day = time_df_new.pivot_table(index='요일', columns='읍면동명', values='거리(km)/시간(분)', aggfunc='mean').agg(weeks).T*60
    plt.title('Top 20 Dong : Average driving speed on Days')
    plt.figure(figsize=(20, 10))
    dong_day.index=list(dong_eng['동이름'])
    dong_day.columns=['Mon','Tues','Wed','Thur','Fri','Sat','Sun']
    sns.heatmap(dong_day, vmax=dong_day.max().max(), vmin=dong_day.min().min(), cmap='Reds', annot=annot, annot_kws={'size': 20}, fmt='.0f')
    plt.xlabel('Day', fontsize=15)
    plt.ylabel('Top 20 Dong', fontsize=15)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20, rotation=0)
    st.pyplot(plt)
elif button == '월별' :
    dong_month = time_df_new.pivot_table(index=['읍면동명'], columns='출동월', values='거리(km)/시간(분)', aggfunc='mean')*60
    plt.title('Top 20 Dong : Average driving speed on Months')
    plt.figure(figsize=(20, 10))
    dong_month.index=list(dong_eng['동이름'])
    sns.heatmap(dong_month, vmax=dong_month.max().max(), vmin=dong_month.min().min(), cmap='Reds', annot=annot, annot_kws={'size': 20}, fmt='.0f')
    plt.xlabel('Month', fontsize=15)
    plt.ylabel('Top 20 Dong', fontsize=15)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20, rotation=0)
    st.pyplot(plt)
else :
    dong_season = time_df_new.pivot_table(index=['계절구분명'], columns='읍면동명', values='거리(km)/시간(분)', aggfunc='mean').agg(season).T*60
    plt.title('Top 20 Dong : Average driving speed on Seasons')
    plt.figure(figsize=(20, 10))
    dong_season.index=list(dong_eng['동이름'])
    dong_season.columns = ['Spring','Summer','Fall','Winter']
    sns.heatmap(dong_season, vmax=dong_season.max().max(), vmin=dong_season.min().min(), cmap='Reds', annot=annot, annot_kws={'size': 20},
            fmt='.0f')
    plt.xlabel('Season', fontsize=15)
    plt.ylabel('Top 20 Dong', fontsize=15)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20, rotation=0)
    st.pyplot(plt)




