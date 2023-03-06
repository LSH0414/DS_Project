<h1> 트위치 조축회 데이터 시각화 </h1>

![IOS badge](https://img.shields.io/badge/python-3.7-blue?style=flat-square&logo=python&logoColor=ffdd54&style=plastic)  : 
![IOS badge](https://img.shields.io/badge/-pickle-lightgrey)
![IOS badge](https://img.shields.io/badge/-pandas-lightgrey)
![IOS badge](https://img.shields.io/badge/-numpy-lightgrey)</br>
![IOS badge](https://img.shields.io/badge/tableau-22.04-blue?style=flat-square&logo=tableau&logoColor=ffdd54&style=plastic)


<h2> 프로젝트 목적 </h2>
<h4> : 트위치 조축회 멤버들의 매치기록, 이적시장 데이터들을 시각화 하자!!

</br>

<h2> 프로세스 </h2>

<ul> <h3> 데이터 수집 </h3>

<ul>사이트<ul>
  <li> <a href = "https://developers.nexon.com/fifaonline4/">FIFA Online4 API</a></li>
 </ul></ul>
</ul>

<ul><h3>전처리</h3>
  <ul> 1. 멤버 accessid 찾기, FIFA4 Data [CODE - 한글] 사전화 </ul>
  <ul> 2. accessid로 매치, 이적시장 정보 필터링 후 가져오기</ul>
  <ul> 3. 시각화를 위한 한글화 </ul>
  <ul> 4. 경기기록, 이적시장 기로 각각 GoogleDrive에 저장</ul>
  
  <h6> 데이터 수집 기간은 조축회 첫 시작은 23년 1월 28일 기준으로 수집</h6>
 </ul>
 
<ul><h3> 시각화 </h3> 
  <li> Tableau - GooleDrive 연동하여 데이터 시각화</li>
</ul>

<h2> Tableau 대시보드 </h2>
  <ul> <a href = "https://public.tableau.com/app/profile/.46525810/viz/_16779561031200/1"> 매치기록 대시보드 </a></ul> 
  <img width="1410" alt="매치기록 화면캡처" src="https://user-images.githubusercontent.com/119479455/223021325-1e2ac030-c854-482b-8d8e-f3539bb239a5.png">
</ul>
  </br></br>


<ul> <a href = "https://public.tableau.com/app/profile/.46525810/viz/__16780204519780/1?publish=yes"> 이적시장 대시보드 </a></ul>   
  <img width="1407" alt="이적시장 화면캡처" src="https://user-images.githubusercontent.com/119479455/223021457-aa57a99e-e461-431c-a40e-163cdde954a8.png">
</ul>
