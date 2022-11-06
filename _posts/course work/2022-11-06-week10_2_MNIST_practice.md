---
title: "[학부수업] 딥러닝의 이해 - 10주차-2 : MNIST 분류하기 with Simple CNN, Pytorch"
excerpt: "딥러닝의 이해 - 10주차-2 수업 내용"

date: 2022-11-06T14:49:25.657890+09:00
lastmod: 2022-11-06T14:49:25.657890+09:00
toc: true
toc_sticky: true
hero: 
url: //
description: 
tags: 
menu:
  sidebar:
    name: 학부수업
    identifier: 학부수업
    parent: 
    weight: 
categories:
    - 학부수업
tags:
    - CV
    - DeepLearning
    - Pytorch
    - CNN
    - MNIST
use_math: true
---

딥러닝의 이해 10주차 2차시 수업 과정인 CNN으로 MNIST 분류하기 진행하겠습니다.

# 1. Dataset Import


```python
import torch
import torchvision.datasets as dsets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import torch.nn as nn
import matplotlib.pyplot as plt
import random
import torch.nn.functional as F

# torch.cuda.is_availbe() 를 통해 GPU가 사용가능한 status인지 아닌지를 bool형태(True or False)로 리턴
USE_CUDA = torch.cuda.is_available() 

# 만약 USE_CUDA = True (GPU 사용가능)이면 device = "cuda", USE_CUDA = False (GPU 사용 불가능하면 CPU 사용)이면 device = "CPU"
device = torch.device("cuda" if USE_CUDA else "cpu") 

# 사용 device 출력
print("다음 기기로 학습합니다. :", device)
```
>출력

    다음 기기로 학습합니다. : cuda
    
<br>


<br>

# 2. 초기설정 : Batch, Epoch,Seed


```python
#for reproducibility (재현성을 위해 동일한 방식으로 Shuffle 하기 위한 Random 값 고정)
random.seed(777)
torch.manual_seed(777)
if device == 'cuda':
  torch.cuda.manual_seed_all(777)

# hyperparameters

# Epcoh 횟수 = 15
training_epochs = 15 
# Batch 크기 = 100
batch_size = 100 
# learning rate = 0.001
learning_rate = 0.001
```
<br>


<br>

# 3. MNIST Dataset


``` python
torchvision.datasets.MNIST(root: str, train: bool = True, transform: Optional[Callable] = None, target_transform: Optional[Callable] = None, download: bool = False)
```

- **`root`**(string) : `MNIST/raw/train-images-idx3-ubyte`와 `MNIST/raw/t10k-images-idx3-ubyte` 가 저장될 경로를 지정합니다.

- **`train`**(*bool*,optional) : data를 통해 train할 때 `True`로 설정합니다. 만약 `True` 로 설정되면 `train-images-idx3-ubyte`로부터 dataset을 형성합니다. `False`이면 `t10k-images-idx3-ubyte`로부터 dataset을 형성합니다. 

- **`download`**(*bool*,optional) : True이면 인터넷을 통해 dataset을 download하고 설정한 root directory에 저장합니다. 만약 이미 download된 파일이 있다면 다시 download하지 않습니다. 

- **`transform`**(*callable*, optional) : PIL 이미지를 입력받아 transformed 된 결과를 return하는 함수입니다. <br>E.g, `transforms.RandomCrop`

이외 parameter에 대한 상세한 설명은 [pytorch - MNIST](https://pytorch.org/vision/stable/generated/torchvision.datasets.MNIST.html#torchvision.datasets.MNIST) 를 참조하시기 바랍니다.

<br>

---

<br>

**MNIST Dataset Download**
```python
'''
torchvision에서 dsets로 import 한 datasets 통해 
built-in datasets 중 하나인 MNIST dataset download
'''



mnist_train = dsets.MNIST(root='MNIST_data/', # download 받을 경로 지정
                          train = True, # train을 위한 data이므로 True로 설정
                          transform = transforms.ToTensor(), # Data를 Tensor로 변환
                          download = True)

mnist_test = dsets.MNIST(root='MNIST_data/',
                         train = False, # test를 위한 data이므로 False로 설정
                         transform = transforms.ToTensor(), # Data를 Tensor로 변환
                         download = True)

#dataset loader
data_loader = DataLoader(dataset = mnist_train,
                         batch_size = batch_size, # 앞서 설정한 batch_size를 통해 batch로 나눔
                         shuffle = True, # shuffle = True로 설정해 데이터를 무작위로 섞음, 이때 앞서 설정한 random.seed(777)을 통해 randomnize됨
                         drop_last = True) # batch단위로 데이터를 불러올 때, 나누어 떨어지지않는다면 남은 데이터는 버림
                                           # ex. data크기 = 27, batch_size = 5 => 마지막 batch의 크기는 2이므로 버림

```

<br>



<br>

# 4. CNN Network, Loss and Optimizer
**Network, loss, and Optimizer**

class를 정의

`conv2d` - [Pytorch Conv2d 함수 다루기](https://gaussian37.github.io/dl-pytorch-conv2d/)




```python
# MNIST data image of shape 28 x 28 = 784

# Non-linear Architecture including hidden layer


class Net(nn.Module):
  def __init__(self):
    super().__init__()
    self.conv1 = nn.Conv2d(in_channels = 1,out_channels=32,kernel_size = 3,stride = 1,padding = 1)
    self.conv2 = nn.Conv2d(32,64,3,1,1)
    self.pool = nn.MaxPool2d(kernel_size = 2,stride = 2)
    self.fc = nn.Linear(64*7*7,10,bias = True)
    torch.nn.init.xavier_uniform_(self.fc.weight)
  def forward(self,x):
    # L1 Imgin shape = (batch_size,1,28,28)
    # "self.conv1(x)" => (batch_size,32,28,28)
    # "self.pool(x)" => (batch_size,32,14,14), Conv2d에서 padding = 1 설정함으로써 MaxPooling 통해 가장 자리 삭제되는 것 방지
    x = self.pool(F.relu(self.conv1(x)))

    # L2 Imgin shappe = (batch_size,32,14,14)
    # "self.conv1(x)" => (batch_size,64,14,14)
    # "self.pool(x)" => (batch_size,64,7,7)
    x = self.pool(F.relu(self.conv2(x)))

    # L3 FC 64x7x7(3136) inputs -> 10 outputs
    # "torch.flatten(x,1)"" => (batch_size,1024)
    x = torch.flatten(x,1) # 0,1,2 차원으로 flatten.. 1차원 => width*height
    x = self.fc(x)
    return x

net = Net().to(device)

# Loss function and optimizer
criterion = nn.CrossEntropyLoss().to(device) # 내부적으로 Softmax 함수 포함하고 있음
optimizer = torch.optim.Adam(net.parameters(), lr = learning_rate)
```

<br>



<br>

# 5. Training & Inference
**Training**


```python
total_batch = len(data_loader)

for epoch in range(training_epochs):
  avg_cost = 0
  for X,Y in data_loader:
    # 배치 크기 = 100
    X = X.to(device) # Batch, Channel, Width, Height
    Y = Y.to(device)
    optimizer.zero_grad()

    # Hypothesis for Non-linear Architecture
    hypothesis = net(X)

    # cost, optimizer
    cost = criterion(hypothesis,Y)
    cost.backward()
    optimizer.step()

    avg_cost += cost / total_batch
  
  print(f"Epoch: {epoch+1:04d}, cost = {avg_cost:.9f}")

print("Learning Finished")
```
>출력 

    Epoch: 0001, cost = 0.225624949
    Epoch: 0002, cost = 0.062987588
    Epoch: 0003, cost = 0.046228435
    Epoch: 0004, cost = 0.037454057
    Epoch: 0005, cost = 0.031482313
    Epoch: 0006, cost = 0.026145909
    Epoch: 0007, cost = 0.021883152
    Epoch: 0008, cost = 0.018382354
    Epoch: 0009, cost = 0.016457239
    Epoch: 0010, cost = 0.013288155
    Epoch: 0011, cost = 0.010470187
    Epoch: 0012, cost = 0.010075552
    Epoch: 0013, cost = 0.008410202
    Epoch: 0014, cost = 0.007457465
    Epoch: 0015, cost = 0.006478167
    Learning Finished
    

<br>

---

<br>


**Test Accuracy**


```python
with torch.no_grad():
  X_test = mnist_test.test_data.reshape(-1,1,28,28).float().to(device)  # Test Data도 Batch, Channel, Width, Height로 reshpae
  Y_test = mnist_test.test_labels.to(device)
  prediction = net(X_test)
  correct_prediction = torch.argmax(prediction,1) == Y_test
  accuracy = correct_prediction.float().mean()
  print("Accuracy:", accuracy.item())

  # MNIST 테스트 데이터에서 무작위로 하나 뽑아서 예측
  r = random.randint(0,len(mnist_test) - 1)
  X_single_data = mnist_test.test_data[r:r+1].reshape(-1,1,28,28).float().to(device) # Test Data도 Batch, Channel, Width, Height로 reshpae
  Y_single_data = mnist_test.test_labels[r:r+1].to(device)

  print("Label:",Y_single_data.item())
  single_prediction = net(X_single_data)
  print("Prediction :", torch.argmax(single_prediction,1).item())

  plt.imshow(mnist_test.test_data[r:r+1].view(28,28), cmap='Greys', interpolation = 'nearest')
  plt.show()
```
>출력 

    Accuracy: 0.9830999970436096
    Label: 8
    Prediction : 8
    


    
![output_14_2](https://user-images.githubusercontent.com/107748183/200156018-f47c8bdc-9949-4b84-9c14-830dedea238d.png)
    

<br>

---

<br>



**Reference**

1. Conv2d 함수 : https://gaussian37.github.io/dl-pytorch-conv2d/

2. Channel Size Fix : https://discuss.pytorch.org/t/runtimeerror-expected-3d-unbatched-or-4d-batched-input-to-conv2d-but-got-input-of-size-1-1-374-402-3/154535

3. nn.functional : https://thebook.io/080289/ch05/02-16/

4. Pytorch로 시작하는 딥러닝 입문 : https://wikidocs.net/63565
