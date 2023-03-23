# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title = '구급출동 데이터 분석',
    page_icon = ':ambulance:',
    layout='wide')


# 서울 전체 신고자 유형
df_sex = pd.read_csv('./data/df_sex.csv')
df_age = pd.read_csv('./data/df_age.csv', encoding='euc-kr')
df_season = pd.read_csv('./data/df_season.csv', encoding='euc-kr')
df_disease = pd.read_csv('./data/df_disease.csv')
df_age['환자비율'] = df_age['환자수']/df_age['환자수'].sum()


# 서울 전체 신고자유형 파이그래프
st.subheader(':white_check_mark:2021년도 서울시 전체 구급환자 유형')
st.markdown('---')

colors = ['#ff9999', '#ffc000', '#8fd9b6', '#d395d0']
wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}

fig, axs = plt.subplots(2,2)

axs[0,0].set_title('<Gender Ratio>')
axs[0,0].pie(df_sex['0'], labels=['Man','Unknown','Woman'], startangle=90,
            radius=1, autopct='%.1f%%', colors=colors, wedgeprops=wedgeprops)

axs[0,1].set_title('<Age Ratio>')
axs[0,1].bar(df_age['환자연령대'], df_age['환자비율'], color='skyblue')
axs[0,1].set_xticklabels(['50s','60s','70s','over 80','20s','40s','30s','teenager','under 10'], rotation=40)
for i in range(len(df_age)) :
    axs[0,1].text(i-0.2, df_age.loc[i,'환자비율'], round(df_age.loc[i,'환자비율']*100,1))


axs[1,0].set_title('<Disease Ratio>')
axs[1,0].pie(df_disease['0'], labels=['Etc','Disease','Non Disease'], startangle=90,
            radius=1, autopct='%.1f%%', colors=colors,wedgeprops=wedgeprops)

axs[1,1].set_title('<Season Ratio>')
axs[1,1].pie(df_season['계절 합계'], labels=['Fall','Winter','Spring','Summer'], startangle=90,
            radius=1, autopct='%.1f%%', colors=colors, wedgeprops=wedgeprops)

plt.rc('font', size=8) # controls default text sizes
plt.rc('axes', titlesize=8) # fontsize of the axes title
plt.rc('axes', labelsize=8) # fontsize of the x and y labels
plt.rc('xtick', labelsize=8) # fontsize of the tick labels
plt.rc('ytick', labelsize=8) # fontsize of the tick labels
plt.rc('legend', fontsize=8) # legend fontsize
plt.rc('figure', titlesize=8)
plt.tight_layout()
st.pyplot(plt)
st.markdown('---')

# 동별 신고자 유형
dong_sex = pd.read_csv('./data/dong_sex_count.csv')
dong_age = pd.read_csv('./data/dong_age_count.csv')
dong_season = pd.read_csv('./data/dong_season_count.csv')
dong_disease = pd.read_csv('./data/dong_disease_count.csv')
dong_sex = dong_sex.set_index(keys='읍면동명')
dong_age = dong_age.set_index(keys='읍면동명')
dong_season = dong_season.set_index(keys='읍면동명')
dong_disease = dong_disease.set_index(keys='읍면동명')



# 행정구별 신고 빈도 멀티선택 df, 바그래프
st.subheader(':white_check_mark:2021년도 행정동별 구급환자 유형(선택)')
dong = st.selectbox('행정동을 선택하세요', dong_age.index)

fig2, axs2 = plt.subplots(2,2)

axs2[0,0].set_title('<Gender Ratio>')
axs2[0,0].pie(dong_sex[dong_sex.index==dong].iloc[0,:], labels=['Man','Unknown','Woman'], startangle=90,
            radius=1, autopct='%.1f%%', colors=colors, wedgeprops=wedgeprops)

axs2[0,1].set_title('<Age Ratio>')
axs2[0,1].bar(dong_age.columns, dong_age[dong_age.index==dong].iloc[0,:], color='skyblue')
axs2[0,1].set_xticklabels(['under 10','teenager','20s','30s','40s','50s','60s','70s','over 80'], rotation=50)


axs2[1,0].set_title('<Disease Ratio>')
axs2[1,0].pie(dong_disease[dong_disease.index==dong].iloc[0,:], labels=['Etc','Disease','Non Disease'], startangle=90,
            radius=1, autopct='%.1f%%', colors=colors, wedgeprops=wedgeprops)

axs2[1,1].set_title('<Season Ratio>')
axs2[1,1].pie(dong_season[dong_season.index==dong].iloc[0,:], labels=['Fall','Winter','Spring','Summer'], startangle=90,
            radius=1, autopct='%.1f%%', colors=colors, wedgeprops=wedgeprops)

plt.tight_layout()
st.pyplot(plt)