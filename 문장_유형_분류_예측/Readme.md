
<h1> 문장 유형 분류 및 예측 only M/L </h1>

![IOS badge](https://img.shields.io/badge/python-3.7-blue?style=flat-square&logo=python&logoColor=ffdd54&style=plastic)  : 
![IOS badge](https://img.shields.io/badge/-pandas-lightgrey)
![IOS badge](https://img.shields.io/badge/-numpy-lightgrey)
![IOS badge](https://img.shields.io/badge/-matplotlib-lightgrey)
![IOS badge](https://img.shields.io/badge/-seaborn-lightgrey)
![IOS badge](https://img.shields.io/badge/-scikit_learn-lightgrey)</br>


<h2> 프로젝트 목적 </h2>
<h4> : NLP(자연어 처리). 문장 유형을 분류를 딥러닝이 아닌 머신러닝만으로 해보자! (극성 PART)

</br>

<h2> 프로세스 </h2>

<ul> <h3> 데이터 수집 </h3>

<ul>사이트<ul>
  <li> <a href = 'https://dacon.io/competitions/official/236037/overview/description'> Dacon 문장분류 AI 경진대회 </li>
  </ul></ul></ul>
  </br>
  
<ul><h3>EDA</h3><ul>
<li> 기본 데이터 구성 <img src = 'https://user-images.githubusercontent.com/119479455/226285719-d78f40a7-79cd-43e4-b6da-5f0f82e7ce89.png'></li>

<li> EDA 요약 <img src = 'https://user-images.githubusercontent.com/119479455/226285978-7b3ddf1f-a056-4cdf-be68-aeaf1392bf95.png'></li>

</ul></ul>

</br>

<ul><h3>전처리</h3><ul>
<li> 텍스트 전처리 </br>
 극성에 대한 분류를 하기 위해서 긍정, 부정, 미정으로 분류된 문장을 분리하여 모델이 학습할 수 있도록 각각 카운팅과 중요도 사전을 만들었습니다.
<img src = 'https://user-images.githubusercontent.com/119479455/226286426-ab42199e-ad4b-472f-946e-03b095ac290a.png'></li>
  
  </br>
  
<li>데이터 불균형 전처리</br>
데이터의 불균형이 심하기 때문에 언더 샘플링하면 대부분의 데이터가 있는 긍정에 대한 데이터의 손실이 너무 커서 오버 샘플링을 진행하기로 함.
<img src= 'https://user-images.githubusercontent.com/119479455/226288548-bd409e5f-b912-4852-9c51-8ab2d9bd81a8.png'></li></ul>
    
  </ul></ul>
  
  </br>
  

<ul><h3>모델링</h3>
  
  <ul> 사용 모델<ul>
  <li> Decision Tree, Random Forest, Navie bayes, KNN </li>
    </ul></ul>
    
   </br>
   
  <ul> 모델 비교<ul></br>
  기본적인 모델에서 전체적인 성능은 랜덤 포레스트가 좋게 나왔지만 자료가 부족했던 부정과 미정의 분류의 경우 KNN이 가장 좋은 모델로 나왔다. 이는 기본 모델 뿐 아니라 하이퍼 파라미터 튜닝 후에도 같은 결과를 보여주었다. 따라서 데이터 수가 적은 부정과 미정에 대한 정확성이 더 좋은 모델이라는 기준으로 KNN모델을 최종 모델로 선택하였다.
  <li> 전체 정확성 
    <img src = 'https://user-images.githubusercontent.com/119479455/226291116-7470a3a3-0351-4e40-a2b5-7528e1b3ab37.png'></li></br>
  <li>부정, 미정에 대한 정확도
    <img src = 'https://user-images.githubusercontent.com/119479455/226291536-25e65509-f3ce-4240-84b9-288dce66d984.png'></li>

</ul></ul></ul>
  
 
 <h2> 결과 </h2>
 최종적으로 4가지 유형을 구분하는 모델을 각각 만들었습니다. 이를 하나의 모듈로 만들었습니다. 이에 대한 성능확인을 위해 Google Colud Speech API를 사용하여 음성으로 문장을 만들어 모듈에게 해당 문장의 4가지 유형을 분류해 보여주는 결과를 만들었습니다. 이 과정에 대한 영상은 프로젝트 파일안에 포함되어 있습니다.
 <img src = 'https://user-images.githubusercontent.com/119479455/226292354-3649d047-bb7d-4b14-94ba-8ebd9e893b13.png'>

 
 <h2> 배운점 </h2>
 자연어처리에 있어서 머신러닝의 한계점을 확인할 수 있는 프로젝트였습니다. 자연어처리 분야에서 통계적 기법을 활용한 머신러닝보다는 RNN(Recurrent Neural Network)를 사용한 딥러닝이 더 좋은지 확실하게 느낄 수 있었습니다. 통계적 기법으로는 문장에 실린 감성에 대한 데이터를 담기에는 한계가 명확했고 이를 딥러닝에서는 어느정도 처리가 가능하다는 점을 알았습니다. 또한, 한글이 다른 언어들에 비해서 자연처리가 얼마나 까다로운 언어인가에 대해서 알 수 있었습니다. 이런 경험을 바탕으로 다음번 자연어처리 프로젝트에서는 머신러닝이 아닌 딥러닝 모델을 사용하여 문장을 분류 혹은 예측해보는 작업을 시도해 볼 계획입니다.

 
 

