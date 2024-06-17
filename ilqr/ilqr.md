# ilqr
## 1. vehicle model
$$
\begin{bmatrix}
    \dot{x} \\
    \dot{y} \\
    \dot{\theta} \\
    \dot{\delta} \\
    \dot{v} \\
    \dot{a}
\end{bmatrix}
=
\begin{bmatrix}
    v \cos(\theta) \\
    v \sin(\theta) \\
    \frac{v \tan(\delta)}{L (1 + k v^2)} \\
    u_1 \\
    a \\
    u_2
\end{bmatrix}
$$
## 2. cost
iLQR的成本函数包含三部分：状态误差成本、控制成本和约束成本。公式如下：
#### 状态误差成本
状态误差成本是目标状态与当前状态之间的二次成本：
$$
\text{state\_cost} = (\mathbf{x} - \mathbf{x}_\text{goal})^T \mathbf{Q} (\mathbf{x} - \mathbf{x}_\text{goal})
$$
#### 控制成本
控制成本是控制输入的二次成本：
$$
\text{control\_cost} = \mathbf{u}^T \mathbf{R} \mathbf{u}
$$
#### 约束成本
约束成本是违反约束的成本，由拉格朗日乘数和惩罚因子表示：
$$
\text{constraint\_cost} = \lambda^T \mathbf{g} + 0.5 \mu \mathbf{g}^T \mathbf{I}_\mu \mathbf{g}
$$
其中：
- $ \lambda $ 是拉格朗日乘数
- $ \mathbf{g} $ 是约束函数
- $ \mu $ 是惩罚因子
- $ \mathbf{I}_\mu $ 是惩罚因子的对角矩阵

#### 总成本函数
总成本函数是上述三部分成本的总和：
$$
\text{cost} = \text{state\_cost} + \text{control\_cost} + \text{constraint\_cost}
$$
$$
cost = \sum_{i = 0}^{n-1}{e_i^TQe_i + \lambda^T \mathbf{g} + 0.5 \mu \mathbf{g}^T \mathbf{I}_\mu \mathbf{g}} + \sum_{i = 1}^{n-1} {u_i^TRu_i} + e_N^TQ_Ne_N
$$

## 2. backward

$$
J = \sum_{i = 0}^{n-1}{e_i^TQe_i} + \sum_{i = 1}^{n-1} {u_i^TRu_i} + e_N^TQ_Ne_N  + \lambda^T \mathbf{g} + 0.5 \mu \mathbf{g}^T \mathbf{I}_\mu \mathbf{g}
$$

$$
\begin{align*}
    x_{k+1} &= f(x_k, u_k) \\
    δx_{k+1} &= \frac{∂f}{∂x}δx_k + \frac{∂f}{∂u}δu_k \\
    A &= \frac{∂f}{∂x},  B = \frac{∂f}{∂u}
\end{align*}
$$


$$
\begin{align*}
    Q_x &= \frac{∂J}{∂x}|_{k} + \frac{∂f}{∂x}^{T}|_{k} \frac{∂V}{∂x}^{T}|_{k+1} \\
    Q_u &= \frac{∂J}{∂u}|_{k} + \frac{∂f}{∂u}^{T}|_{k} \frac{∂V}{∂x}^{T}|_{k+1} \\
    Q_{ux} &= \frac{∂^2J}{∂u∂x}|_{k} +   \frac{∂J}{∂u}|_{k} \frac{∂^2V}{∂x^2}^{T}|_{k+1} \frac{∂J}{∂x}|_{k} \\
    Q_{xx} &= \frac{∂^2J}{∂x∂x}|_{k} +   \frac{∂J}{∂x}|_{k} \frac{∂^2V}{∂x^2}^{T}|_{k+1} \frac{∂J}{∂x}|_{k} \\
    Q_{uu} &= \frac{∂^2J}{∂u∂u}|_{k} +   \frac{∂J}{∂u}|_{k} \frac{∂^2V}{∂x^2}^{T}|_{k+1} \frac{∂J}{∂u}|_{k}
\end{align*}
$$

$$
δ u^* = - Q_{uu}^{-1} (Q_{ux}δ x_k + Q_{u}) =K_k δ x_k + d_k
$$

$$
\begin{cases}
    K_k = - Q_{uu}^{-1}Q_{ux}\\
    d_k = - Q_{uu}^{-1}Q_{u}
\end{cases}
$$

$$
\begin{cases}
    \frac{∂V}{∂x} = Q_x + K^T Q_{uu} d + K^T Q_u + Q_{ux}^T d \\
    \frac{∂^2V}{∂x^2} = Q_{xx} + K^T Q_{uu} K + K^T Q_{ux} + Q_{ux}^T K \\
\end{cases}
$$

## 3. forward

