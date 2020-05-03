# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 22:38:12 2020

@author: 82109
"""

import folium 
import json
import pandas as pd

data = pd.read_csv('C:\python_temp\서울상가현황.csv',encoding = 'utf-8')

#지점 위치에 사용할 json파일
geo_path = 'C:/python_temp/skorea_municipalities_geo_simple.json'
geo_str = json.load(open(geo_path,encoding = 'utf-8'))

#지도정의
map = folium.Map(location = [37.5558,126.925], zoom_start=17)

#데이터 클렌징
data = data[['상호명','경도','위도']]
starbucks = data[data['상호명'] == '스타벅스']
ediya = data[data['상호명'] == '이디야커피']

#스타벅스 위치를 지도에 추가
for i in starbucks.index :
    folium.CircleMarker([float(starbucks.loc[i, '위도']), float(starbucks.loc[i, '경도'])],
                       radius =10,
                       popup = starbucks.loc[i,'상호명'],
                       color = 'green').add_to(map)
#이디야 위치를 지도에 추가
for i in ediya.index :
    folium.CircleMarker([float(ediya.loc[i, '위도']), float(ediya.loc[i, '경도'])],
                       radius =10,
                       popup = ediya.loc[i,'상호명'],
                       color = 'blue').add_to(map)
    
#지점수에 따른 비율그래프
#데이터 클렌징
rawdata = pd.read_csv('C:\python_temp\서울상가현황.csv',encoding = 'utf-8')
rawdata = rawdata[['상호명','시도명','시군구명','법정동명']]   
edy = rawdata[rawdata['시도명']=='서울특별시']
edy = edy[edy['상호명']=='이디야커피']

stb = rawdata[rawdata['시도명'] == '서울특별시']
stb = stb[stb['상호명'] == '스타벅스']

#리스트 선언
edyfreq = [len(edy[edy['시군구명'] == '용산구'])]     
stbfreq = [len(stb[stb['시군구명']=='용산구'])]

name = ["강서구","양천구","구로구","금천구","영등포구","관악구","동작구","서초구","강남구",
       "송파구","강동구","광진구","중량구","노원구","도봉구","강북구","성북구","동대문구",
       "성동구","중구","종로구","서대문구","마포구","은평구"]     #지점수 구하기 위한 이름배열

#각 지역별 매장 수 구하기_이디야
for i in name :
    val = len(edy[edy['시군구명'] == i])
    edyfreq.append(val)
    
 #각 지역별 매장 수 구하기_스타벅스
for i in name :
    v = len(stb[stb['시군구명'] == i])
    stbfreq.append(v)
    
#데이터 프레임 재조합
name = ['용산구','강서구','양천구','구로구','금천구','영등포구','관악구','동작구','서초구','강남구',
       '송파구','강동구','광진구','중량구','노원구','도봉구','강북구','성북구','동대문구',
       '성동구','중구','종로구','서대문구','마포구','은평구']

freq = pd.Series(edyfreq, name='점포수')
location = pd.Series(name, name='지역구')
edydf = pd.concat([freq,location],axis=1)

#이디야 매장수별 지도 그리기
rmap = folium.Map(location = [37.5558,126.925], zoom_start=11)
folium.Choropleth(geo_data=geo_str,
                 data = edydf,
                 columns=('지역구','점포수'),
                 key_on = 'feature.id',
                 fill_color='YlGn').add_to(rmap)

#스타벅스 데이터프레임 재조합
sfreq = pd.Series(stbfreq, name='점포수')
slocation = pd.Series(name, name='지역구')
stbf = pd.concat([sfreq,slocation],axis=1)

#스타벅스 매장수 지도 그리기
smap = folium.Map(location = [37.5558,126.925], zoom_start=11)
folium.Choropleth(geo_data=geo_str,
                 data = stbf,
                 columns=('지역구','점포수'),
                 key_on = 'feature.id',
                 fill_color='YlGn').add_to(smap)
#스타벅스와 이디야를 같이 비교
#구별 위도경도 가져오기
loct = pd.read_csv('C:/python_temp/서울시 좌표계.csv',encoding ='euc-kr')
loct = loct[['시군구명_한글','위도','경도']]

#데이터프레임 재조합
cpr = pd.concat([stbf['점포수'],edydf,loct],axis =1)
cpr.columns.values[0] = '스타벅스'   #컬럼명 변경
cpr.columns.values[1] = '이디야'
        
#타입변경
cpr['스타벅스'] = cpr['스타벅스'].astype(float)
cpr['이디야'] = cpr['이디야'].astype(float)

#시각화
cprmap = folium.Map(location = [37.5558,126.925], zoom_start=17, tiles = 'Stamen Toner')

for i in cpr.index :
    for n in ['스타벅스', '이디야'] :
        cnt = cpr.loc[i,n]
        
        radius_color = 'green'
        if n == '이디야':
            radius_color = 'blue'
            
        folium.CircleMarker(
            location = [cpr.loc[i,'위도'],
                       cpr.loc[i,'경도']],
            radius = cnt,
            color = radius_color,
            fill = True,
            fill_color = radius_color).add_to(cprmap)
        