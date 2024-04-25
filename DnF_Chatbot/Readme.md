# Dungeon & Figher Chatbot 프로젝트



<h3> 24.04.20 Update</h3>
기존에 polyglot1.3b 모델에 RLHF - PPO 학습된 모델을 통해 RAG를 구현하기 어려워 EEVE-10.8b모델에 SFT를 진행하였습니다. RAG로 활용되는 데이터는 던전앤파이터 공식 홈페이지 커퓨니티의 공식 공략글과 던전앤파이터 관련 나무위키 페이지들을 사용하였습니다. 해당 데이터는 임베딩에 학습하지 않았지만 데이터를 구축하여 추가적으로 학습할 예정입니다.


<h4>RAG Options</h4>
- Chunk : 3,000</br>
- Embedding Model : BAAI/bge-m3




https://github.com/LSH0414/Project/assets/119479455/1a5cfdde-b8c2-4e71-b91a-51fc41a89f6e



----
ChatGPT와 sLLM을 fine-tuning을 통해 나만의 모델을 만들어보자!

ChatGPT를 통해 데이터셋을 구축하고 강화학습(PPO), RLHF, [QLoRA](https://github.com/artidoro/qlora?tab=readme-ov-file)를 사용하여 특정 분야(던전앤파이터 세계관)에 대한 질문에 잘 대답할 수 있는 모델을 만드는 프로젝트입니다.</br>
  - sLLM 모델을 QLoRA를 사용하여 Colab환경에서 프로젝트를 진행하였습니다.</br>
  - 던전앤파이터와 관련된 데이터는 약 3,500개의 이야기 데이터를 사용하였습니다. 던전앤파이터의 모든 세계관을 표현하기에는 적은 데이터이고 하나의 주제에 대해서도 모델이 이해하기 적은 데이터로 보다 정교한 대답을 위해서 더 많은 데이터가 필요합니다.
  - 실습환경: Jupyter or Colab, 선수 지식: 파이썬

</br>

### Train PPO
프로젝트는 PPO알고리즘을 활용하여 다음과 같은 흐름으로 훈련이 진행되었습니다. PPO과정에 대한 요약은 아래 흐름도를 통해 이해할 수 있고 각 모델은 다음과 같습니다.
- Trained Model : Supervised fine-tuning polyglot-1.3b (Trainable)
- Frozen Model : Supervised fine-tuning polyglot-1.3b
- Reward Model : TextClassfication 1-label fine-tuning polyglot-1.3b

![image](https://github.com/LSH0414/Project/assets/119479455/e2034621-1d2e-4130-9255-7004a21eebb0)


</br></br>

## Make Data Prompt
- 데이터 출저
  - [루리웹 던전앤파이터 스토리 요약](https://bbs.ruliweb.com/news/board/17/read/61)
  - [DFU (던전앤파이터 공식 홈페이지)](https://www.dnf-universe.com/)
  - [던전앤파이터 나무위키(메인스토리)](https://namu.wiki/w/%EB%8D%98%EC%A0%84%EC%95%A4%ED%8C%8C%EC%9D%B4%ED%84%B0)
- 훈련 데이터 : [SFT&RM Train Data](https://github.com/LSH0414/Project/tree/master/DnF_Chatbot/data)
- RM Data 구축을 위한 PROMPT는 다음과 같습니다. 해당 PROMPT를 ChatGPT에 전달하였고 답변을 위한 모델로 'gpt-3.5-turbo'을 사용하였고 본문의 입력길이가 길어 명령을 전달하지 못할 경우 입력 시퀀스의 길이가 증가한 'gpt-4-1106-preview'모델을 사용하여 답변을 제작하였습니다. 실제로 두 모델이 만들어내는 답변을 20번 받았을때 큰 차이가 존재한다고 보기 어려웠습니다. 
```python
system_prompt = """입력 내용을 바탕으로 질문과 답변을 만들어내는 작업입니다. 다음 요구사항에 맞는 답변을 생성해주세요.
요구 사항은 다음과 같습니다:
1. 본문에 대한 내용을 요약하는 작업을 진행합니다.
2. 답변은 한국어로 작성해야 합니다.
3. 답변은 하나의 질문과 장문, 중문, 단문 응답으로 총 네 가지 모두 작성해야 합니다.
4. 장문, 중문, 단문은 같은 질문에 대한 답변으로 작성해야 합니다.
5. 장문은 5문장 이상으로 구성해야 합니다.
6. 중문은 3문장 이하로 구성해야 합니다.
7. 단문은 1문장으로 구성해야 합니다.
8. 장문, 중문, 단문은 내용에 겹치는 부분이 있어도 됩니다.
"""

prompt="""
아래의 본문에 대한 내용을 바탕으로 답변을 작성해주세요.
질문과 응답은 아래와 같은 형식으로 입력에 알맞게 작성하세요.

질문과 각 응답 사이는 ###으로 구분해주세요.
질문 : ###
장문 : ###
중문 : ###
단문 :


본문 : 다음 내용은 {subject}에 관한 내용입니다.\n{content}

"""
```

</br></br>

##  Result
- 베이스 모델 : [polyglot-1.3b](https://github.com/EleutherAI/polyglot)
  - 12.8b로 가장 큰 모델을 선택할 경우 QLoRA를 사용한 SFT는 가능하지만 PPO의 inference 과정에서 MMO문제가 발생합니다. 환경에 맞추어 베이스 모델을 수정하시면됩니다.

- 필요 모듈
```bash
pip install -q -U bitsandbytes
pip install -q -U git+https://github.com/huggingface/transformers.git
pip install -q -U git+https://github.com/huggingface/peft.git
pip install -q -U git+https://github.com/huggingface/accelerate.git
pip install -q datasets
```
- [코드 파일](https://github.com/LSH0414/Project/blob/master/DnF_Chatbot/model_train.ipynb). 모든 실행은 TPU V4 환경에서 진행하였습니다.
- DnF Chatbot 결과예시
  -  Query : 질문
  -  Response(before/after) : SFT 모델 / PPO로 훈련된 SFT 모델
  -  Rewards(before/after) : (SFT 모델 / PPO로 훈련된 SFT 모델) 답변 점수
```
Query :  타우킹 샤우타는 누구인가요?
Response (before) :   타우킹 사도들은 샤우타를 타우로 부르고, 그들은 그를 타우킹이라 칭합니다. 이들은 샤우드의 우두머리로서 역할을 수행합니다. 또한, 타우킹은 타우라는 이름의 사도에 의해 소환되는 존재로서 그의 권능을 통해 자신의 권능으로 다른 존재를 제어하고 지배할 수 있습니다.
Response (after) :   타우킹 타우는 타우타의 조상입니다. 원래는 불을 잘 다루었지만 그 능력이 점차 쇠퇴해지면서 현재는 타우킹이 되었습니다. 이들은 주로 숲에서 활동하며 타우타와 같이 나무를 자릅니다. 타우타는 나무를 잘 다루며 숲을 지키기 위해 노력하고 있습니다.  타우타가 자신의 모습을 본떠 만들어졌다고 말하는 이가 있지만 타우타 자체는 타우타나 타우타를 본떠 만들지 않았습니다.
Rewards (before)/(after) :  tensor([0.6245]) / tensor([3.5957])

Query :  '오필리아 베이그란스'는 어떤 종교 집단의 신도인가요?
Response (before) :   '오필리어 베이그란스는 루크를 따르는 자들 중 하나로, 현재는 교단에서 운영하는 특수 조직의 일원입니다. 그녀는 루크의 특별한 능력을 받았으며, 이 능력으로 자신들을 이끌어 루크의 제국을 지키는 역할을 하고 있습니다.' 오필리어 베이 그란스는 종교 집단의 정신적인 지주로서 그의 능력을 믿고 따르는 신도입니다. 그녀가 자신들을 지키기 위해 수호신의 힘을 빌린다는 이야기를 들은 적이 있습니다.
Response (after) :   '오필리오 베이그란스'()는 황도군에 합류한 후에도 종교 단체에 남아 있었습니다. 그러나 현재는 신도들의 반발로 신도들과 함께 집단 자살을 하는 것으로 알려졌습니다. 그 후 오필리아 베이 그란스는 자신의 배를 타고 도주하며 종교적인 힘을 이용해 집단을 결속했습니다. 이후 신도들은 이 종교 집단에 다시 합류할 것을 희망하고 있습니다. 하지만 현재는 신도 수가 매우 적어 다시 합류할 확률은 매우 적은 상황입니다.
Rewards (before)/(after) :  tensor([3.3848]) / tensor([2.3184])

Query :  '머크우드'는 어떤 곳인가요?
Response (before) :   '머크 우드'는 마계를 상징하는 지역 중 하나로, 마계의 중심지인 마계 도시입니다. 이곳은 거대한 숲과 계곡이 있어 모험가들의 눈을 사로 잡는 곳이기도 합니다. 현재는 '머크 타운'이라는 이름으로 마계 도시로 자리 잡고 있습니다. 모험가들은 이곳에서 모험을 시작해 마계를 정복하고 마계에 뿌리를 내리려는 야망을 가지고 있습니다..
Response (after) :   '머크 우드'는 노스피스의 북쪽으로, 황량한 사막과 끝없이 펼쳐진 바다가 끝없이 펼쳐지는 곳입니다. 이곳은 모험가들의 성지이며, 신비한 고대 마법진들이 존재하는 곳입니다." 머크우드에는 오래된 마법진이 있는데, 그곳에 들어가면 다양한 마법진을 만나볼 수 있습니다."라고 '머크위드'에 대한 자세한 정보가 제공됩니다. 머크우드는 오래된 고대 마법진이 존재하는 장소로 알려져 있습니다.
Rewards (before)/(after) :  tensor([3.6680]) / tensor([1.8340])
```
