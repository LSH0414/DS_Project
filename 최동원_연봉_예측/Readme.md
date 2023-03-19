<h6> 지속적으로 업데이트 중입니다!</h6>
<h1> 트위치 조축회 데이터 시각화 </h1>


![IOS badge](https://img.shields.io/badge/python-3.7-blue?style=flat-square&logo=python&logoColor=ffdd54&style=plastic)  : 
![IOS badge](https://img.shields.io/badge/-pandas-lightgrey)
![IOS badge](https://img.shields.io/badge/-numpy-lightgrey)
![IOS badge](https://img.shields.io/badge/-Beautifulsoup-lightgrey)
![IOS badge](https://img.shields.io/badge/-Selenium-lightgrey)
![IOS badge](https://img.shields.io/badge/-matplotlib-lightgrey)
![IOS badge](https://img.shields.io/badge/-seaborn-lightgrey)
![IOS badge](https://img.shields.io/badge/-scikit_learn-lightgrey)</br>


<h2> 프로젝트 목적 </h2>
<h4> : 최동원 선수가 2023년에 있었다면 연봉은 얼마였을까??!!

</br>

<h2> 프로세스 </h2>

<ul> <h3> 데이터 수집 </h3>

<ul>사이트<ul>
  <li> <a href = 'http://www.statiz.co.kr'> Starz(한국 프로야구 데이터 사이트) </li>
  <li> <a href = 'https://www.kaggle.com/datasets/mattop/korean-baseball-pitching-data-1982-2021'> 한국 프로야구 1982-2021년 팀별 데이터 요약(Kaggle)</li>
  </ul></ul></ul>

<ul><h3>전처리</h3>
  <ul> Starz<ul>
    <li> 1983 ~ 1988, 2015 ~ 2020년 프로야구 데이터 가져오기 </li>
    <li> 팀이름, 시즌 축약어 분리 및 정재</li>
    </ul></ul>
  
  </br>
  
  <ul> Kaggle<ul>
    <li>1982 ~ 2021년 동안 팀 해체와 창설을 하면서 변경된 팀명을 현재 사용하는 팀 명으로 통일</li>
    </ul></ul>
    
   </br>
    
  <ul> 모델링을 위한 데이터 전처리<ul>
    <li>90년대와 2000년대 데이터를 하나로 합치고 팀이름이 한글과 영문이 섞여있어 단어 통일</li>
    <li>최동원 투수의 평가를 위한 K/9(9이닝당 탈삼진), BB/9(9이닝당 볼넷)에 대한 피처 추가 -> 예측1</li>
    <li>고액/저액 연봉자 기준으로 데이털르 분리 -> 예측2</li>
    <li>금액만으로 전처리시 문제가 있어 연봉 협상을 했을 경우로 전처리 진행 -> 예측3</li>
    </ul></ul></ul>

<ul><h3>모델링</h3>
  <ul> Scaler <ul>
    <li> MinMax, Standard, Robuster</li>
    </ul></ul>
  
  </br>
  
  <ul> 사용 모델<ul>
  <li> XGB, Linear, RandomForest, PCA </li>
    </ul></ul>
    
   </br>
  
  <ul> 최종 결과 <ul>
  <li>최종 모델 성능
  <img src='https://user-images.githubusercontent.com/119479455/226174702-98af7a13-4dde-4676-9d72-4f38731b88d8.png'> 
  </li>
  
  </br>
  
  <li>최동원 선수 연봉 예측 - 협상 주기 및 년도에 따른 연봉 예측
    <img src='https://user-images.githubusercontent.com/119479455/226174915-5b104442-c4d8-4649-9b0c-67875d6b671c.png'> 
  </li>
 </ul></ul></ul></ul>
 
 <h2> 결론 </h2>
 타겟(최동원) 데이터가 가장 높은 연봉을 받을 수 있는 경우는 1년마다 협상시 84년에 약 13억으로 예측된다. 두번째로 높은 금액은 3년마다 계약시 85년에 약 11어에 협상 가능한 것으로 예측 되었다.</br>
 따라서 타겟 데이터는 1년마다 연봉 협상을 했을때 총액이 가장 많았고 그 다음으로 3년, 2년 협상 기간 순으로 많은 금액을 받을 수 있었다.
 
 <h2> 배운점 </h2>
 범주형 데이터가 아닌 연속형 데이터에 대한 예측을 해보았다. 모델 성능이 생각만큼 높지 않았다. 하지만 모델 성능 개선을 위해서 매년 선수의 연봉이 아닌 연봉 협상에 중점을 두고 시도 했다는 접근법이 좋았다는 평을 들었다.
 </br>
 데이터를 다양한 방면으로 보고 피처로 활용할 수 있는 시선의 중요함을 느낄 수 있었던 프로젝트였다.
 
 

