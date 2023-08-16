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
    <img src='https://github.com/LSH0414/Project/assets/119479455/876eb966-c090-44cb-b7ea-5624a7cb68b3'>
  </ul>
  </br>

  ---
    
   <ul> <h3> 챌린저 - 증강 </h3>
     <img src = 'https://github.com/LSH0414/Project/assets/119479455/ecdeaae3-07c9-407d-9e22-02f002f97965'>
     <img src = 'https://github.com/LSH0414/Project/assets/119479455/da66a40d-56fd-4c96-bae6-66c3d46a5948'>
     </br></br> <h4> 챌린저의 증강 통계를 보여줍니다. </h4>
     <li> 증강은 진행된 게임수와 선택된 수의 통계를 이중축으로 보여줍니다.</li>
     <li>선택 뷰타입을 선택하면 원하는 증강의 통계를 볼 수 있습니다.</li>
     <li>증강의 트랜드 파악을 위해 최근 3일 챌린저 게임의 통계를 확인할 수 있습니다.</li>
   </li>
    </ul>
    </br>   

---

  <ul> <h3> 챌린저 - 전설 </h3>
   <img src = 'https://github.com/LSH0414/Project/assets/119479455/d7d4a349-368a-4a67-a8e4-e47c5af1248b)'>
   <img src = 'https://github.com/LSH0414/Project/assets/119479455/37e49388-4aff-4127-8efb-7222bc081d7d'>
   </br></br> <h4>챌린저의 전설 증강 선택 통계를 보여줍니다. </h4>
     <li> 게임 시작시 선택한 전설 통계가 아닌 전설이 갖고 있는 고유 증강을 선택한 통계를 기준으로 보여줍니다. </li>
     <li> 게임 시작시 선택한 전설 챔피언이 아닌 다른 전설이 갖고 있는 증강을 선택한 경우도 통계에 포함됩니다. </li>
     <li> 통계 기간을 현재 기준으로 짧게 잡는다면 실시간 인기 증강을 확인하실 수 있습니다. </li>
   </li>
  </ul>
  </br>   

---
   
   <ul> <h3> 챌린저 - 챔피언 </h3>
     <img src = 'https://github.com/LSH0414/Project/assets/119479455/3437c955-cb9b-4f75-99ab-4a47677bb8df'>
   </ul>
   </br></br> <h4>챌린저의 챔피언 통계를 보여줍니다. </h4>
     <li> 챔피언별 어떤 아이템을 주로 사용하는지 확인하실 수 있습니다. </li>
     <li> 패치에 따라 기물에 주어지는 아이템이 달라지기에 패치 버전을 선택하여 확인할 수 있습니다. </li>
     <li> 우승(1등), 순방, 전체 집계 기준을 선택하여 추천 아이템, 추이를 보실 수 있습니다. </li>
   </li>
   </br>

   ---
   
   <ul> <h3> 챌린저 - 시너지 </h3>
     <img src = 'https://github.com/LSH0414/Project/assets/119479455/1965c9ba-a5c8-4109-98a1-fef543b2e836'>
   </ul>
    </br></br> <h4>챌린저의 시너지 통계를 보여줍니다. </h4>
     <li> 우승(1등) 데이터를 기준으로 시너지 구성을 추천해드립니다. </li>
     <li> MAIN페이지는 패치, 인게임 플레이스타일 변화에 맞게 추천해드립니다. </li>
     <li> 세부 추천을 통해서는 패치버전을 선택할 수 있고 선택한 패치 버전에서 가장 우승을 많이한 3가지 추천 시너지 조합과 해당 조합으로 플레이한 최근 게임 데이터를 보여드립니다. </li>
  </br>   

  ---
    
   <ul> <h3> 커스텀 검색(미완성) </h3>
     <img src = 'https://github.com/LSH0414/Project/assets/119479455/68bc3107-c17f-435d-9cda-4ef1b06d414b'>
   </ul>
    </br></br> <h4> 원하는 커스텀 검색 탭입니다.  </h4>
     <li> 증강, 시너지, 챔피언을 선택해 DB에서 탐색해 원하는 자료를 탐색해볼 수 있습니다. </li>
    </br>    
</ul></ul>


<ul><h2> 개선점 </h2>
<li>
데이터 로딩</br>
Streamlit에서 제공하는 Cache를 사용하여 어느정도 로딩 시간을 단축시키기는 했지만 집계하는 데이터가 늘어날수록 시간이 조금씩 증가했다. 데이터를 효율적으로 불러오고 보여주는 로직에 대해서 더 고민해볼 필요가 있었다.
</li>
<li>
대량 데이터 처리 방법</br>
위 문제와 비슷한 맥락인데 로딩보다 축적되는 데이터 량이 많아지다보니 처리하는데 시간적 효율을 따지게 되었다. 아무래도 완성된 결과를 보여주는 페이지가 아니라 선택한 기준의 집계 통계를 보여주는 것이다보니 대량 데이터를 처리하는 방법에 대해서 알아 볼 수 있는 기회가 됐다.
</li>
<li>
수작 대시보드 한계점</br>
Tableau, Power BI와 같은 대시보드 툴을 왜 사용하는지 뼈저리게 느낄 수 있었다. 직접 대시보드를 구성하는데 고려해야할 부분들이 너무나도 많았다. UI/UX도 있지만 그 안에서 계산되는 데이터들 로직 역시 내가 직접 구현해야했기에 직접 대시보드를 처음부터 구성하고 만드는 부분은 혼자서 역부족이라 느꼈다.
</li></ul>

<ul> <h3> 느낀점 </h3></ul>
:다양한 게임 데이터 분석을 해볼 수 있는 프로젝트였다. 특히 전설 선택을 역추적하여 패치 내역과 연결지어 너프/버프에 대한 분석을 해보는게 굉장히 흥미로웠다. 핫픽스 대상이었던 전설, 증강에 대해서 지표들을 보면 라이엇에서 어느정도 수준일때 핫픽스를 결정하는지 확인해볼 수 있었다. 기간내에 있었던 핫픽스인 드레이븐의 너프가 가장 대표적인 예시라고 할 수 있다.</br></br>
 대량 데이터를 처리하기 위해서 다양한 SQL모듈과 PySpark와 같은 다양한 모듈을 사용해봤지만 해당 문제는 해결되지는 않았다. 다만 긍정적이었던 부분은 Spark를 사용하면 Spark 자체에서 데이터를 들고 있는 경우까지는 시간이 얼마 걸리지 않았다. 다만 이 부분을 Python에 보여주기 위해서 데이터를 변환하는 시점에서 시간이 오래걸렸다. 이 부분에 대해서 좀 더 깊게 파고 들어가면 대량 데이터 처리 스킬 향상에 도움이 될 것이라 생각된다. </br></br>
 대시보드는 역시 툴을 이용하자... 혼자서 기획부터 구현까지 직접 해봤다는데 큰 의미가 있다고 생각한다...! 다음에는 데이터 처리만하구 툴을 통해서 웹에 뿌려주는 형태로 시도해봐야겠다.
