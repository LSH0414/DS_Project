# Dungeon & Figher Chatbot(RLHF) 프로젝트(수정중)

ChatGPT와 LLM을 fine-tuning을 통해 나만의 모델을 만들어보자!

ChatGPT를 통해 데이터셋을 구축하고 강화학습(PPO), RLHF, QLoRA를 사용하여 특정 분야(던전앤파이터 세계관)에 대한 질문에 잘 대답할 수 있는 모델을 만드는 프로젝트입니다.</br>
  - sLLM 모델을 QLoRA를 사용하여 Colab환경에서 프로젝트를 진행하였습니다.</br>
  - 실습환경: Jupyter or Colab, 선수 지식: 파이썬

### PPO
프로젝트는 PPO알고리즘을 활용하여 다음과 같은 흐름으로 훈련이 진행되었습니다.
- Trainable Model : Supervised fine-tuning polyglot-1.3b
- Freeze Model : Supervised fine-tuning polyglot-1.3b
- Reward Model : TextClassfication 1-label fine-tuning polyglot-1.3b

![image](https://github.com/LSH0414/Project/assets/119479455/e2034621-1d2e-4130-9255-7004a21eebb0)


####  DnF Chatbot 실습 Requirement
- 베이스 모델 : [polyglot-1.3b](https://github.com/EleutherAI/polyglot)
  - 12.8b로 가장 큰 모델을 선택할 경우 QLoRA를 사용한 SFT는 가능하지만 PPO의 inference 과정에서 MMO문제가 발생합니다. 환경에 맞추어 베이스 모델을 수정하시면됩니다.
- 데이터 : [data_kochatgpt](https://github.com/LSH0414/Project/tree/master/DnF_Chatbot/data)
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

던전앤파이터 세계관을 이해시키기에는 훈련 데이터가 많지 않았습니다. 
