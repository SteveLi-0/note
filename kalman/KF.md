# 卡尔曼滤波器介绍
卡尔曼滤波器是一种递归算法，用于通过一系列观测值估计动态系统的状态。它假设系统和观测噪声都是高斯分布，并根据噪声的协方差矩阵对系统状态进行优化估计。卡尔曼滤波器分为两个主要步骤：**预测步骤**和**更新步骤**。其计算公式如下：

### 1. 预测步骤 (Prediction Step)
- **状态预测**：
  
  \[
  \hat{x}_{k|k-1} = A_k \hat{x}_{k-1|k-1} + B_k u_k
  \]

  其中，$\hat{x}_{k|k-1}$是时刻$k$对状态的预测，$A_k$是状态转移矩阵，$\hat{x}_{k-1|k-1}$是时刻$k-1$的状态估计值，$B_k$是控制矩阵，$u_k$是控制输入。

- **协方差预测**：

  \[
  P_{k|k-1} = A_k P_{k-1|k-1} A_k^T + Q_k
  \]

  其中，$P_{k|k-1}$是预测状态的协方差矩阵，$P_{k-1|k-1}$是先前估计状态的协方差矩阵，$Q_k$是过程噪声的协方差矩阵。

### 2. 更新步骤 (Update Step)
- **卡尔曼增益**：

  \[
  K_k = P_{k|k-1} H_k^T (H_k P_{k|k-1} H_k^T + R_k)^{-1}
  \]

  其中，$K_k$是卡尔曼增益，$H_k$是观测矩阵，$R_k$是观测噪声的协方差矩阵。

- **状态更新**：

  \[
  \hat{x}_{k|k} = \hat{x}_{k|k-1} + K_k (z_k - H_k \hat{x}_{k|k-1})
  \]

  其中，$\hat{x}_{k|k}$是更新后的状态估计，$z_k$是观测值，$H_k \hat{x}_{k|k-1}$是观测预测值。

- **协方差更新**：

  \[
  P_{k|k} = (I - K_k H_k) P_{k|k-1}
  \]

  其中，$P_{k|k}$是更新后的协方差矩阵，$I$是单位矩阵。

卡尔曼滤波器通过上述预测和更新步骤反复迭代，逐步优化对系统状态的估计。
