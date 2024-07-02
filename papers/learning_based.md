# DLP
## 1. Jointly Learnable Behavior and Trajectory Planning for Self-Driving Vehicles
### 1.1 abstract

过去的研究将BP和TP分开设计，这就导致BP和TP的目标可能不一致。BP的改变将严重影响TP的输出。本文的优势有：

- BP 和 TP 共享一个 cost function
- interpretable cost on top of preception prediction and vsd

### 1.2 intro

gap:

- 过去 BP 和 TP 往往是独立设计的，因此他们的 cost 是不同的，BP cost 改变往往带来 TP cost tunning 巨大的工作量

contribution：

- e2e： cost function 不需要手动调整
- 舒适安全、可以处理复杂场景

