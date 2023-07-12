<h1> TFT_S9 데이터 분석 & 대시보드 (Streamlit) (수정중) </h1>

![IOS badge](https://img.shields.io/badge/python-3.7-blue?style=flat-square&logo=python&logoColor=ffdd54&style=plastic)  : 
![IOS badge](https://img.shields.io/badge/-streamlit-lightgrey)
![IOS badge](https://img.shields.io/badge/-pickle-lightgrey)
![IOS badge](https://img.shields.io/badge/-pandas-lightgrey)
![IOS badge](https://img.shields.io/badge/-numpy-lightgrey)
![IOS badge](https://img.shields.io/badge/-matplotlib-lightgrey)
![IOS badge](https://img.shields.io/badge/-plotly-lightgrey)



<h2> 프로젝트 목적 </h2>
<h4> 챌린저 유저들의 증강, 아이템, 챔피언, 시너지를 통해 흐름을 파악해보자 </h4>

</br>

<h2> 분석 프로세스 </h2>

<ul> <h3> 이용 ,참고 사이트 </h3>

<ul>사이트<ul>
  <li> Riot API - https://developer.riotgames.com/</li>
  <li> metatft - https://metatft.com/</li>
  <li> lolchess - https://lolchess.gg </li>
  <li> tactics - https://tactics.tools </li>
 </ul></ul>
</ul>

<ul><h3> 파일 목록 </h3>
<ul> - RIOT API -> AWS DB (데이터 수집)
  <ul> TFT_game_data_API.py </ul></ul>
<ul> - Python 
  <ul> streamlit.py  : MAIN.py </ul>
  <ul> connect_db.py : connect AWS </ul>
  <ul> data_processing.py : make static dataframe </ul>
  <ul> draw_plots.py : draw static data on figure </ul>
</ul>
  
</ul>

<ul><h3> 페이지 요약</h3>
  <ul> <h5>TFT MAIN</h5>
  </ul>
  </br>
    
   <ul> <h5> 챌린저 - 증강 </h5>
    </ul>
    </br>   
   
   <ul> <h5> 챌린저 - 챔피언 </h5>
     
   </ul>
   </br>
   
   <ul> <h5> 챌린저 - 시너지 </h5>
   </ul>
    </br>   
    
   <ul> <h5> 커스텀 검색 </h5>
   </ul>
    </br>    

    
</ul></ul>


<ul><h2> 결론 </h2>
티어별로 선호하는 것에 대한 차이는 기물(챔피언)이 가장 적었다. 그 이유는 게임 플레이 도중에 상위 티어에서 좋은 덱이라고 소개된 덱을 보고 가장 유연하게 적용할 수 있는 부분이 기물 부분이기 때문에 모든 티어에서 비슷한 경향을 보여준것으로 생각된다. 시너지는 어떤 기물을 선택했느냐에 가장 큰 영향을 받기 때문에 비슷한 흐름을 보여주었던 것으로 생각된다. 가장 차이가 큰 것은 아이템이었는데 이 부분은 게임 내에서 어떤 아이템 등장할지는 매 플레이마다 다르기 때문으로 보인다. 이 부분이 게임 이름에 걸맞게 전략적이라는 요소가 들어가 하나의 게임을 어떻게 운영하는지 판가름되는 지점이라고 생각된다.</br></br>
이 데이터를 활용해서 조금 더 프로젝트를 진행해본다면 완성된 덱을 미리 메이킹해보고 해당 덱에서는 승률이 어느정도가 되는지 예측해주는 모델을 만든다면 유저들에게 플레이 이전에 덱 메이킹 하는데 또 다른 재미요소를 줄 수 있지 않을까 기대해볼 수 있다.

