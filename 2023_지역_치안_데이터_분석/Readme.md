<h1> 2023 지역 치안 데이터 분석 - 보이스피싱 </h1>


<h2> 🛠 Tools </h2>

![IOS badge](https://img.shields.io/badge/python-3.7-blue?style=flat-square&logo=python&logoColor=ffdd54&style=plastic) : 
![IOS badge](https://img.shields.io/badge/-pandas-lightgrey)
![IOS badge](https://img.shields.io/badge/-numpy-lightgrey)
![IOS badge](https://img.shields.io/badge/-selenium-lightgrey)
![IOS badge](https://img.shields.io/badge/-Beautifulsoup-lightgrey)
![IOS badge](https://img.shields.io/badge/-plotly-lightgrey)</br>
![IOS badge](https://img.shields.io/badge/-Google%20API-orange?style=flat-square&logo=google&logoColor=ffdd54&style=plastic)
![IOS badge](https://img.shields.io/badge/-Naver%20API-green?style=flat-square&logo=naver&logoColor=ffdd54&style=plastic) : 
![IOS badge](https://img.shields.io/badge/-geocoding-lightgrey)
</br>
![IOS badge](https://img.shields.io/badge/tableau-21.04-blue?style=flat-square&logo=tableau&logoColor=ffdd54&style=plastic)


<h2> 프로젝트 목적 </h2>
<h4> 대전, 충남, 세종시에서 발생하는 보이스 피싱 신고 데이터를 활용해 공통점을 찾고 피해자 기준의 보이스 피싱 예방 방안 제시 </h4>

</br>

<h2> 분석 프로세스 </h2>

<ul> <h3> 사용 데이터 </h3>
<ul>
  기본제공 데이터</br> <ul> - 20 ~ 23년 1월 신고 접수 데이터</ul></br>
  크롤링 (KakaoMap) <ul> - 신고 접수 좌표, 주소를 활용해 인근 은행, ATM 주소 데이터 수집</ul>
 </ul></ul>
</ul>

<ul><h3>전처리</h3>
<ul> 
기본 제공 데이터<ul> - 제공된 CodeBook 기준 데이터 및 칼럼 통합</ul></br>
Geocoding<ul> - Naver API 우선으로 발생지점 좌표 및 주소 정보 처리. Naver API로 불러올 수 없을 경우 Geoogle API사용</br>
- 발생 지점 주소, 좌표 모두 없는 데이터의 경우 결측치로 사용 데이터에서 제외</ul></br>
일시, 자표, 지점 그룹화<ul> - 같은 사건으로 중복 신고인 경우 하나만 사용하기 위해 그룹화 </ul></br>
</ul>
</ul>

<ul><h3> 데이터 분석 요약 </h3><ul> 
  <ul><li> 계절성 - 보이스피싱 범죄의 계절성은 없음 </li> <ul>- 20 -23년 보이스피싱 신고 추이
  <img style = "width:80%" src = 'https://user-images.githubusercontent.com/119479455/223066738-c33a8dfb-a9ba-433e-ae22-d24b135bbd3d.png'> </img></br>
  - 20 - 23년 보이스피싱 신고 추이(통합)
    <img style = "width:80%" src = 'https://user-images.githubusercontent.com/119479455/223068465-7dae9ac3-2e61-4295-b1e6-bb0a822f9643.png'> </img></br>
  </ul>
   </ul>
   </br>
   <ul><li> 보이스피싱 범죄 시간대 </li> <ul>- 가장 많이 발생하는 시간대는 점심 ~ 오후
   <img style = "width:80%" src = 'https://user-images.githubusercontent.com/119479455/223070430-1973bff5-203d-4e9c-8356-bda1446d4901.png'> </img</br></ul></ul>  
   </br>
   
   <ul><li> 지역별 보이스피싱 신고 분포 - 보이스피싱은 인구 분포에 따라 대상이 되지 않음. 예시) 대전</li></br> <ul> - 신고 분포</br>
   <img style = "width:80%" src = 'https://user-images.githubusercontent.com/119479455/223073285-895a8a77-3dd9-4c71-a702-6a6b3427dba4.png'> </img></br>
- 인구수 - 신고수</br>
 <img style = "width:80%" src = "https://user-images.githubusercontent.com/119479455/223075317-6f266425-c8b7-42ed-a8c7-03acee8bedc2.png"></img</br></ul></ul>
 
 </br>
 
 <ul><li> 은행, ATM 인근 보이스 피싱 신고 분포 - 300M 이내에서 대부분의 보이스 피싱 신고 발생</li> <ul> 
 - 거리별 신고 분포</br>
 <img style = "width:80%" src = "https://user-images.githubusercontent.com/119479455/223076656-7a122d3c-9b59-48ed-ae62-9a7244f2670e.png"></img</br></ul></ul></ul></ul>

<h2>결론 </h2><ul>
  오후시간, 지역구별 효과적 순찰 동선 구성이 필요.</br>
  각 지역(동, 읍, 면)에서 보이스피싱 피해 신고가 들어오는 곳이 밀집되어 있음을 확인했다.</br>
  특히 그 위치가 은행, ATM이 위치의 반경 300M에 대부분의 신고들이 들어가 있었다. 그리고 점심 ~ 오후 시간에 대부분의 보이스피싱 신고가 접수된다는 점에서 11~18시 사이 은행, ATM 위치한 곳을 기준으로 순찰 동선을 구성한다면 조금이나마 보이스피싱 예방에 도움이 될 것이다.

</br></br>
<a href = "https://public.tableau.com/app/profile/.46525810/viz/-_16764437345690/1?publish=yes"> 지역 치안 데이터 대시보드
</br>
<img style="width:80%" src="https://user-images.githubusercontent.com/119479455/223082912-a2bdc380-bc14-4252-99eb-07c07ab09903.png">
</ul>

</br>

<h2> 아쉬운 점 </h2><ul>
대회에 대한 정보를 늦게 알아서 참가가 늦어져 모델 제작까지는 하지 못하고 분석에 그쳤다. 이 점이 가장 아쉽다.
게다가 보이스피싱에 대한 분석을 하기에는 제공된 데이터가 발생일, 주소, 시간뿐이라 분석하기 쉽지 않았다.
모델을 만든다면 은행, ATM 주위 보이스피싱 신고지점들을 지역구별로 최적의 순찰경로를 탐색해주고 새로운 신고가 들어왔으면 그에 맞게끔 새롭게 추천해주는 모델을 만들면 좋겠다는 생각을 했다.
