# D2L
## MLP
### 激活函数
#### ReLU
当输入为负时，ReLU函数的导数为0，而当输入为正时，ReLU函数的导数为1。 注意，当输入值精确等于0时，ReLU函数不可导。 在此时，我们默认使用左侧的导数，即当输入为0时导数为0。
使用ReLU的原因是，它求导表现得特别好：要么让参数消失，要么让参数通过。 这使得优化表现得更好，并且ReLU减轻了困扰以往神经网络的梯度消失问题（稍后将详细介绍）。
#### Sigmoidal
#### Tanh
### underfitting & overfitting
### weight decay
### dropout
### forward & backward & compute graph
