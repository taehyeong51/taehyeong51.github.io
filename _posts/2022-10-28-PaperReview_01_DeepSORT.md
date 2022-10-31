---
title: "[논문리뷰] DeepSORT"
date: 2022-10-28T15:25:25.657890+09:00
lastmod: 2022-10-28T15:25:25.657890+09:00
toc: true
toc_sticky: true
hero: 
url: //
description: 
menu:
  sidebar:
    name: 논문리뷰
    identifier: 논문리뷰
    parent: 
    weight: 
categories:
    - 논문리뷰
tags:
    - CV
---


## Simple Online And Realtime Tracking With A Deep Association Metric

writer : Taehyeong Kim at Konkuk Univ.

E-mail : taehyeong1998@konkuk.ac.kr or taehyeong1998@kist.re.kr

Last Updated Date : 2022-04-15

---

## Deep SORT란?

- Object Tracking Frame Work(객체 추적 프레임 워크) 로 SORT(Simple Online and Realtime Tracking)에 **Deep Learning**을 접목시켜 성능향상을 이룬 Frame Work 입니다.
    
    → SORT란 무엇이며, 어떻게 SORT에 Deep Learning을 접목시켜 성능 향상을 이루어냈는지 알아보겠습니다.
    
- 이해를 돕기 위해 다음과 같은 순서대로 설명하겠습니다.

---

---

## 1. Research Background

- Deep SORT 를 이해하기 위한 사전 지식들에 대해 미리 알아보겠습니다.

| Kalman Filter |
| --- |
| Hungarian Algorithm |
| Mahalanobis Distance |
| IoU(Intersection Over Union) |
| SORT(Simple Online and Real time Tracking) |

### Kalman Filter

#### **Kalman Filter란?**

- **이전 프레임(또는 stage)에 등장한 개체를 이용하여 다음 프레임 개체의 위치를 예측하고 측정하는 방법**입니다.
- How does Kalman Filter predict?
    - 이전 프레임의 예측값의 분포(Predicted state estimate) + 현재 프레임의 측정값 분포(Measurement) ⇒ 최적 추정 값(Optimal State Estimate)
        <!-- <img src = "./images/pic-0009.jpg"/> -->
        ![img1.daumcdn.jpg](/_posts/images/pic-0009.jpg)
        
        → 예측값과 측정값의 각각의 Gaussian Distribution을 이용해 상태를 업데이트 해 최적의 추정값을 얻습니다.
        
- Why Do We use Kalman Filter for DeepSORT?
    
    A.  Sensor(Camera)로 받아들이는 Measurement 값 역시 Noise를 포함하고 있기 때문에 Kalman Filter로 처리하는데 효과적이기 때문입니다.
    
    또한 Tracking을 위한 영상에서는 물체의 이동이 선형적이기 때문에 마찬가지로 처리에 용이합니다.
    

### Assignment Problem(할당 문제)

#### Assignment Problem이란?

- 다수의 공급처와 수요처가 존재하며, 수용비용이 모두 다를 때, 총 수송비용의 합이 최소가 되는 최적해를 찾는 문제입니다.
    - ex. “**노동자**(에어컨 수리기사) = **공급처** -> **작업**(에어컨 수리) = **수요처** 에 대해 **가장 적은 비용**의 해법”을 얻는 일련의 과정이라 할 수 있습니다.
- How to Solve Assignment Problem?
    - 할당 문제의 대표적인 해결법으로 Hungarian Algorithm이 있습니다.
    

### Hungarian Algorithm

#### Hungarian Algorithm이란?

- 할당문제 & 헝가리안 알고리즘 : [https://gazelle-and-cs.tistory.com/29](https://gazelle-and-cs.tistory.com/29) 참조

### Mahalanobis Distance

#### Mahalanobis Distance란?

- 평균과의 거리가 표준 편차의 몇 배인지 나타내는 값입니다.
- 좀 더 직관적으로 설명하자면 “어떤 경향이 있을 때, 이를 기준으로 새로운 데이터가 얼마나 일어나기 힘든 값인지?” 를 나타내주는 척도입니다.
    - ex. (0,0) 으로부터 네 점 (1,-1), (1,1), (1,-1), (-1,-1) 의 유클리드 거리는 모두 같지만, Mahalanobis 거리는 (1,-1)과 (-1,1)이 매우 큰 것을 볼 수 있습니다.
        
        ![출처 : [https://kr.mathworks.com/help/stats/mahal.html](https://kr.mathworks.com/help/stats/mahal.html)](images/pic-0002.png)
        
        출처 : [https://kr.mathworks.com/help/stats/mahal.html](https://kr.mathworks.com/help/stats/mahal.html)
        
- Why Do We Use Mahalanobis Distance?
    - 어떤 데이터가 진짜 데이터인지, 가짜 데이터(Noise, False Alarm 등)인지 구별하는 용도로 사용하게 됩니다.

### IoU(Intersection over Union)

#### IoU란?

- 겹치는 영역에 대해 수치화한 값을 말합니다.

$$
IoU = {Overlapping\;Region \over Combined \;Region}  
$$

![image9.png](images/pic-0008.png)

![image12.png](images/pic-0003.png)

### SORT(Simple Online and Realtime Tracking)

#### SORT란?

- 실시간 추적을 위해 Object들을 효율적으로 연관(Associate)지어주는 MOT(Multi Object Tracking) 입니다.
    - MOT란?
        
        A. 다수의 객체들 추적을 위해 탐지된 객체들(Detected Objects) 간 연관지어주는 과정을 뜻합니다.
        
- Flow Chart of SORT
    
    ![출처 : 우측상단 표기](images/pic-0007.png)
    
    출처 : 우측상단 표기
    
- What Exactly Happens in SORT?
    1. Detection : 프레임에서 객체를 탐지합니다.
    2. Estimation : Kalman Filter를 통해 추적을 위한 측정치 예측, 업데이트 과정을 진행합니다.
    3. Data Association :
        1. IoU 유사도를 구합니다.
        2. 추적되고 있던 객체와
            
            추적되지 않는 객체(사라진 객체, New 객체)를 분류합니다.
            
        
        b-1. 추적되고 있던 객체는 다시 Kalman Filter를 통해 다음 예측 값으로 사용됩니다.
        
        b-2. 사라진 객체(Unmatched Tracks)는 일정 시간 이후 삭제되며, New 객체(Unmatched Detections)는 새롭게 Track 생성 후 Track에 추가됩니다.
        
- Limitations of SORT?
    - Occlusion(폐색, 가려짐) 문제에 취약합니다.
        
        ![출처 : Measurement-wise Occlusion in Multi-object Tracking](images/pic-0006.png)
        
        출처 : Measurement-wise Occlusion in Multi-object Tracking
        
    - ID Switching : 다양한 객체들이 움직일 때, 서로의 ID 추적이 변경되는 ID Switching에 취약합니다.
        
        ![image17.png](images/pic-0005.png)
        
    

---

## 2. Research Objectivs

DeepSORT에서는

- SORT 의 문제점인 ID Switching과 Occlusion 문제를 해결하고자 했습니다.
- 동시에 좋은 성능(Good Performance)와 속도(Speed)를 유지하고자 했습니다.

---

## 3. Methodology

앞선 문제점들을 해결하기 위해 Deep SORT에서는 

#### 1. **Deep Appearance Descriptor**로 **Re-identification 모델을 적용**해서 **ID** **Switching** 문제를 해결했습니다.

또한 

#### **2. Matching Cascade** 로직으로 더 정확한 추적을 가능케 하였습니다.

![출처 : [https://www.researchgate.net/figure/Architecture-of-Deep-SORT-Simple-online-and-real-time-tracking-with-deep-association_fig2_353256407](https://www.researchgate.net/figure/Architecture-of-Deep-SORT-Simple-online-and-real-time-tracking-with-deep-association_fig2_353256407)](images/pic-0001.jpg)

출처 : [https://www.researchgate.net/figure/Architecture-of-Deep-SORT-Simple-online-and-real-time-tracking-with-deep-association_fig2_353256407](https://www.researchgate.net/figure/Architecture-of-Deep-SORT-Simple-online-and-real-time-tracking-with-deep-association_fig2_353256407)

아래는 좀 더 자세한 FlowChart입니다.

![출처 : 좌측상단 표기](images/pic-0004.jpg)

출처 : 좌측상단 표기

### Process of DeepSORT

1. Detection
    1. 이미지 input으로 받아 존재하는 물체에 대해 Bounding Box 정보 입력받음
2. Kalman Filter Predict
    1. 칼만 필터 통해 기존 Track 정보로부터 다음 frame 물체 위치 예측
3. Track Check
    1. 해당 Tracks들이 충분한 근거 가진 Track 인지 확인
    2. 3번 이상 물체 탐지해 Track으로 인정될 경우 “Confirm”, 그렇지 않을 경우 “Tentative” 로 표현
4. Matching Cascade
    1. Confirmed 인 Tracks에 대해 Matching 수행
    2. 이전보다 정확한 Track 정보 추출
5. IoU Matching
    1. Match되지 않은 Track, Detection 들에 대해 기존의 SORT에서 사용한 IoU 매칭 진행
    2. 새롭게 발견된 Detection에 대해 적용 / Matching 하지 못한 Track들 보완
6. Tracking Life Cycle
    1. 매칭 결과 기반으로 Track 객체 생애주기 결정
7. Kalman Filter Update
    1. 현재 가진 Matched Tracks를 다음 frame 위해 Bbox 예측 / Track 등장 횟수 3회 이상 시 상태 “Confirmed”로 변경
8. Reculsive

### Matching Cascade

DeepSORT 에서는 Matching Cascade 단계를 추가하여 **개체의 상태를 좀 더 디테일하게 추출**하고자 했습니다.

![Untitled](images/pic-0017.png)

다소 복잡해보이는 과정이지만 보다 보기 간단하게 Flowchart로 나타낸 Matching Cascade 흐름을 따라서 차근차근 알아보겠습니다.

![Untitled](images/pic-0011.png)

- **distance 1 : Mahalanobis Distance**
    - 평균과의 거리가 표준편차의 몇 배인지 나타내는 값입니다.
        
        $d^{(1)}(i,j) = (d_j - y_i)^TS_i^{-1}(d_j-y_i)$
        
    
    | d_j |  j번째 bounding box detection |
    | --- | --- |
    | y_j | track data의 평균 값 |
    | S_i | Track Data의 공분산 행렬 |

- **distance 2 : Cosine Distance**
    - 물체가 가지는 모양을 판단하기 위한 Distance(Cosine 유사도를 활용한 Distance)
    - Cosine 유사도
    
    ![Untitled](images/pic-0012.png)
    
    - Cosine Distance
        
        ![Screenshot from 2022-03-21 18-09-27.png](images/pic-0010.png)
        
        - x4, x0, x1 점과 새로운 점 x14가 주어졌을 때 흔히 생각하는 거리인 유클리드 거리는 점 x4가 가장 가깝지만, 코사인 거리는 점 x1이 가장 가깝게 됩니다.
        
        이러한 cosine distance를 유사도를 판별하는 척도로 활용할 수 있습니다.
        
    - $d^{(2)}(i,j) = min\{1-r_j^Tr_k^{(i)} | r_k^{(i)}\in R_i\}$
        
        
        1. 각 bounding box detction d_j에 대해 절대값이 1인 appearance descriptor “r_j”(appearance descriptor : 외형 유사도를 판별하는 척도) 계산
        
        ![Untitled](images/pic-0013.png)
        
        1. 각 트랙 k에 대한 apperance descriptor 마지막 100개를 가지는 갤러리 R_k를 keep해둠
        
        ![Untitled](images/pic-0014.png)
        
        1. apperance space에서 i번째 track과 j번째 detection 사이의 제일 작은 cosine distance를 측정
            
            ![Untitled](images/pic-0015.png)
            
        
        → 예측된 Track의 Motion 동일한 정도가 높을 경우, 이를 반영하는 지표로써 사용하게 됩니다.
        
        → 장기간 Occlusion 이후 동일성 회복에 유용합니다.
        
        → Hyper parameter lambda 를 이용하여 가중치를 조절하여 사용합니다.
        

### Deep Appearance Descriptor

- CNN Architecture를 사용하여 d2에 들어가는 appearance 유사도를 측정하는 feature를 측정합니다.
- [d2](https://www.notion.so/cfc99ad67ad446afb16eb862c732a556)와 더불어 SORT 알고리즘에 Deep Learning이 필요한 당위성을 보여주는 가장 큰 부분입니다.
    
    깊지 않은 CNN 층을 추적하고자 하는 object 외형의 feature를 추출하는데 사용함으로써 real time을 가능케 하며,
    
    이를 통해 외형 유사도 r_j 는 0~1의 값을 같게 되어 대상을 추적하는 값으로 사용됩니다.
    
    ![Untitled](images/pic-0016.png)
    

---

### 4. Experimental Results

작성중

---

### 5. Conclusion

작성중

[https://www.youtube.com/watch?v=7BtEOCb3wMk](https://www.youtube.com/watch?v=7BtEOCb3wMk)