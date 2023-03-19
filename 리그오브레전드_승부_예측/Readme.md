<h1> 리그오브레전드 소환사 협곡 승/패 예측 </h1>


<h2> 🛠 Tools </h2>

![IOS badge](https://img.shields.io/badge/python-3.7-blue?style=flat-square&logo=python&logoColor=ffdd54&style=plastic) : 
![IOS badge](https://img.shields.io/badge/-pandas-lightgrey)
![IOS badge](https://img.shields.io/badge/-numpy-lightgrey)
![IOS badge](https://img.shields.io/badge/-matplotlib-lightgrey)
</br>

<h2> 프로젝트 목적 </h2>
10분간 진행된 게임의 정보로 승/패 예측을 할 수 있을까?!

</br>

<h2> 분석 프로세스 </h2>
<ul>
<h3> 사용 데이터 </h3><ul>
  <li>
  <a href = 'https://www.kaggle.com/datasets/bobbyscience/league-of-legends-diamond-ranked-games-10-min?datasetId=600276&sortBy=commentCount'> Kaggle 
    </li>
 </ul>

<h3>EDA (자세한 내용은 pdf를 통해 확인 가능합니다)</h3><ul>
  <li>와드
  <img src='https://user-images.githubusercontent.com/119479455/226178685-abdb1162-1adf-427d-9993-7d3ee52c2e31.png'>
  </li></br>
  <li>K/D/A
  <img src = 'https://user-images.githubusercontent.com/119479455/226178873-be3e5641-ffe6-4c08-b892-d3fc2a2535aa.png'>
  </li></br>
  <li>오브젝트
  <img src = 'https://user-images.githubusercontent.com/119479455/226178829-fd1b3888-e724-42ca-a35c-bbf56ca1fbe0.png'>
  </li></br>
  <li>골드/경험치
  <img src = 'https://user-images.githubusercontent.com/119479455/226178892-3e602e6c-2854-4193-9ee1-3299848109ff.png'>
  <img src = "https://user-images.githubusercontent.com/119479455/226178915-2a5831e7-3d18-4026-8f12-244963ef25f5.png">
  </li></br>
  <li>상관관계
    <img src = 'https://user-images.githubusercontent.com/119479455/226178940-f0e78aa8-d5dc-4a0b-87d5-59e4693d4c9f.png'>
  </li></br>
</ul>
</br>
<h3>전처리</h3><ul>
  컬럼 축소<ul>
  <li>양측 모든 팀의 지표가 필요하지 않기에 블루팀의 데이터만 사용</li>
  <li>10분 전 와드 설치 수는 이상치가 존재했는데 이 데이터를 제거하고도 비슷한 결과를 보여주었기에 사용하기 힘든 피처로 판단하여 제거</li>
  <li>미니언 킬 수의 경우 경험치와 골드로 충분히 대체가 가능하다고 판단되어 제거</li>
  <li>KDA는 블루와 레드 Trade-off관계이지만 어시스트의 경우 그렇지 않기에 k/d는 블루지표만 어시스트는 모두 사용</li>
  </ul></ul>
</br>
</ul></ul>

<h2>모델링</h2>

  <ul> Scaler <ul>
    <li> MinMax, Standard, Robuster</li>
    </ul></ul>
  
  </br>
  
  <ul> 사용 모델<ul>
  <li> DecisionTree RandomForest, Logistic, GaussianNB </li>
    </ul></ul>
    
   </br>
  
  <ul> 최종 결과 <ul>
  <li>최종 모델 성능
  <img src='https://user-images.githubusercontent.com/119479455/226179244-982d7101-2b3a-4391-b1aa-9031c4811801.png'> 
  </li>
  </ul></ul>
  

<h2>결론</h2>
스케일러에 상관없이 로지스틱 모형이 가장 높은 정확성을 보여주었습니다. 약 72%의 정확성을 보여주었습니다. 각 피처에 대한 결론은 다음과 같습니다.
  <ul>와드<ul>
  <li>와드를 게임 승패에 큰 영향을 주지 않기 때문에 예측에는 사용하지 않았지만 10분간의 지표는 블루와 레드간의 균형은 잘 잡혀있었습니다. 게임적으로는 긍정적인 지표였다.</li>
  </ul></ul>
    </br>
  <ul>골드<ul>
    <li>골드는 게임 승패에 가장 큰 영향을 주는 요소임에도 매우 균형이 잘 잡혀있었습니다. 골드 획득과 관련된 모든 지표를 본다면 양쪽 진형에 대한 골드 획득 루트의 균형이 잘 잡혀있다고 할 수 있습니다.</li>
  </ul></ul>
    </br>
  <ul>오브젝트<ul>
    <li>오브젝트는 진형간 불균형이 확실하게 존재하는 유일한 데이터였습니다. 진형에 따른 확실한 오브젝트 이점이 있었습니다. 레드 진형은 전령,바론 둥지 블루는 드래곤 둥지에서 이점을 갖고 있었습니다.</br>
  다만 의아했던 점은 골드와 직결된 전령에 유리한 블루임에도 골드 획득량에서는 균형이 잘 맞고 있었다는 것입니다. 이 점에서 다음과 같은 가정을 해볼 수 있었습니다.</br><ul>
  <li>블루팀은 10분 이전에 전령을 획득했으나 사용하지 않았다.</li>
  <li>블루 진형은 전령을 획득하고 사용했으나 레드 진형이 그에 맞는 골드를 획득해서 차이가 없다.</li></ul>
  만약 후자라면 오브젝트에 대한 균형은 잘 맞춰진것이 맞는가에 대해서 고민할 여지를 주는 지표였습니다.
  </li>
  </ul></ul>
  </br>
  <ul>경험치<ul>
  <li>경험치 역시 획득 경로를 살펴보면 균형이 잘 잡혀있음을 알 수 있었습니다. 이 영식 게임적 측면에서는 긍정적인 지표였습니다.</li>
  </ul></ul>
</ul>
  </br>

<h4>데이터의 문제점</h4><ul>
데이터 분석과 예측을 진행하였습니다. 70%수준의 예측력에 만족할만한 수준이었다는데는 다음과 같은 이유가 있습니다.<ul>
  </br>
<li>게임 시작 후 10분은 생각보다 길지 않은 시간입니다. 따라서 너무 높은 정확성을 보여준다면 평균 25-30분, 길면 40분이상의 타임을 갖는 게임 특성상 게임의 구성에 의문이 들 수 있습니다.</li>
  </br>
  <li>유저의 실력 수준이 비슷하지만 트롤(승리를 위해 플레이 하지 않는)유저가 존재하는 게임이 없다라는 보장이 없습니다. 따라서 지금의 정확도가 오히려 좋은 수준이라 판단할 수 있습니다.</li>
  </br>
<li>사용한 데이터셋은 다이아 I - 마스터 티어 사이의 게임입니다. 이 구간은 방송인, 전, 현 프로게이머들을 대상을 불법 도박이 이뤄지는 구간이라는 점에서 앞서 데이터의 가정인 모든 플레이어의 실력이 비슷하다는 성립할 수 있지만 정상적인 플레이를 하고 있다고 볼 수 없습니다. 승패를 마음대로 결정하는데 목적이 있는 유저들이 포함되어 있기에 높은 정확성은 오히려 좋지 못한 모델이라는 결론을 내렸습니다.</li>
  </ul></ul>




