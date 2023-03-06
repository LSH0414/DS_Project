<h1> 서울시 교육 데이터 분석 </h1>

![IOS badge](https://img.shields.io/badge/python-3.7-blue?style=flat-square&logo=python&logoColor=ffdd54&style=plastic)  : 
![IOS badge](https://img.shields.io/badge/-pandas-lightgrey)
![IOS badge](https://img.shields.io/badge/-numpy-lightgrey)
![IOS badge](https://img.shields.io/badge/-matplotlib-lightgrey)
![IOS badge](https://img.shields.io/badge/-folium-lightgrey)</br>
![IOS badge](https://img.shields.io/badge/tableau-21.04-blue?style=flat-square&logo=tableau&logoColor=ffdd54&style=plastic)



<h2> 프로젝트 목적 </h2>
<h4> : 교육과정 개정과 코로나 사태로 인한 서울시 지역구별 교육 만족도 변화 분석 </h4>

</br>

<h2> 프로세스 </h2>

<ul> <h3> 데이터 수집 </h3>

사이트
  <ul> 1. 공공 데이터 포털 - https://www.data.go.kr/
    <ul>
      <li>서울시 청소년 인구 통계</li>
      <li>서울시 학교 생활 만족도 조사</li>
      <li>서울시 교육환경 만족도 조사</li>
      <li>서울시 사교육비 및 사교육 참여율 현황 통계</li>
      <li>서울시 부모의 기대 교육 수준 및 목적 조사</li>
    </ul></ul></br>
    
  <ul> 2. E-나라 지표 - https://www.index.go.kr/
     <ul>
      <li>출생아 수 및 합계 출산율</li>
  </ul></ul></br>
    
  <ul> 3. KOSIS 국가통계포털 - https://kosis.kr/
    <ul>
      <li>서울시 평균 임금</li>
  </ul></ul>
 </ul></ul>
</ul>

<ul><h3>전처리</h3>
  <ul>
    <li> 모든 데이터 - 분석 변수 처리 </li>
    <li> 서울시 교육환경 만족도 - 결측치(노이즈) 데이터 MICE 기법 처리 </li>
  </ul></ul>
  
<ul><h3> 분석 과정 </h3>
  <ul>
    1. 청소년 학령 인구의 변화</br>
  2. 학교 생활 만족도 - 교육 내용과 방법 </br>
  3. 학령인구 가구주의 교육 만족도 - 사교육, 공교육 만족도</br>
  4. 사교육비 변화와 서울시 월 임금 변화</br>
  5. 사교육 참여율</br>
  6. 부모의 교육에 대한 기대와 목적</br>
  </ul></ul>
</ul>


<h2>분석 결과 요약</h2>
<ul>  
  <li>2022년 교육과정 개정의 시기이다. 코로나 사태로 도입된 비대면 수업 방식이 우상향 했던 그래프를 보여줬다. 새로운 교육과정에 비대면 방식에 대한 지속적인 도입에 대한 검토가 필요해 보인다. 단, 비대면 방식에 대해 부모들은 부정적 태도.</li>
  </br>
  <li>부모들의 교육 목적은 미래를 위한 능력 개발이 핵심. 인격과 사회적 관계는 부모들에게 더이상 매력적 요소가 아님.</li></br>
  <li>사교육 수준에 대한 만족도가 높아짐에 따라 공교육의 전체적인 만족도가 낮아져 역전 현상 발생. 공교육 수준 상승이 사교육 과열에 브레이크 역할이 될 수 있음.</li></br>
  <li>사교육 비용과 가장 직결된 요인은 사교육의 참여율이다. 참여율을 점진적 하락시킬 수 있는 방법이 있다면 사교육 비용 하락시킬 수 있을 것. 단, 20년 급진적인 하락 조장은 비용의 급등을 불러 일으킨 사례가 있음.</li></br>
  <li>부모들의 기대교육 수준은 90%이상 4년제 졸업 학력을 기대하고 있음. 단순히 대학 졸업이 아니라 네임벨류가 있는 4년제 대학의 학력을 원함. 이는 사교육 과열의 가장 큰 원인으로 보임. </li></br>
  <li>2022년은 학령 인구의 급감하는 시점이고 새로운 교육과정이 도입되는 시기로 공교육과 사교육 모두 큰 변곡점이 될 것.</li>
</ul>
  
