<h1> 나홀로 프로젝트 - TFT_S8 데이터 분석 </h1>

![IOS badge](https://img.shields.io/badge/python-3.7-blue?style=flat-square&logo=appveyor)  : 
![IOS badge](https://img.shields.io/badge/-pickle-lightgrey)
![IOS badge](https://img.shields.io/badge/-pandas-lightgrey)
![IOS badge](https://img.shields.io/badge/-numpy-lightgrey)
![IOS badge](https://img.shields.io/badge/-matplotlib-lightgrey)
![IOS badge](https://img.shields.io/badge/-plotly-lightgrey)


<h2> 프로젝트 목적 </h2>
<h4> : TFT안에서 중요 요소(아이템, 증강, 시너지, 유닛)들은 티어마다 선호하는게 다름을 확인하고 승률을 확인해보자! </h4>

</br>

<h2> 분석 프로세스 </h2>

<ul> <h3>크롤링 </h3>

<ul>사이트<ul>
  <li> Riot API - https://developer.riotgames.com/</li>
  <li> metatft - https://metatft.com/</li>
 </ul></ul>
</ul>

<ul><h3>전처리</h3>
<ul> Riot API
<ul>
  <li>소환사 기본정보 -> 소환사 ID(지역 고유 id) -> puuid(글로벌 고유 id) -> 게임 id -> 게임 참가한 8명 소환사 게임 기록</li>
  <li>티어별 puuid로 최근 게임 id 가져오기(중복 게임은 1개만 남도록 처리)</li>
 </ul></ul>
<ul> metatft
<ul>
 <li> TFT_S8 챔피언 및 시너지,아이템, 증강 크롤링 </li>
 <li> api 이름 - 한글 이름 사전화</li>
</ul>
<h6> * 참고내용</br>
 - 챌린저 300명, 그랜드마스터 600명, 그 외의 티어는 유저 수가 너무 많아 1,000명을 랜덤 샘플링 하였습니다.(티어 집계일 : 02-21)</br>
 - 챌린저 50게임, 그랜드마스터 25게임, 그 외 티어 15게임으로 티어별로 1500게임을 가져왔습니다.(게임 기록 수집기간 : 02-22 ~ 02-23)
</h6>
</ul>
</ul>

<ul><h3>시각화</h3>
<ul>
  <li></li>
  <li></li>
  <li></li>
  <li></li>
  <li></li>
</ul>
</ul>

