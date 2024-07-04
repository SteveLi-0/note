# cilqr for control
## 1. problem formulation
### 1.1 vehicle model

车辆模型来自论文：Numerically Stable Dynamic Bicycle Model for Discrete-time Control

#### 连续时间非线性方程
$$
\dot{X} = f(X, U) = 
\begin{bmatrix}
    u\cos(\phi) - v\sin(\phi) \\
    u\sin(\phi) + v\cos(\phi) \\
    \omega \\
    a + v\omega-\frac{1}{m}F_{Y1}sin\delta \\
    -u\omega + \frac{1}{m}(F_{Y2}cos\delta+F_{Y2}) \\
    \frac{1}{I_z} (l_f F_{Y1}cos\delta - l_rF_{Y2})
\end{bmatrix}
\\ 
$$

$$
X = 
\begin{bmatrix}
    x \\ y \\ \phi \\ u \\ v \\ \omega
\end{bmatrix},
U = 
\begin{bmatrix}
    a \\ \delta
\end{bmatrix}
$$

$$\begin{aligned}&F_{Y1}=k_{f}\alpha_{1}\approx k_{f}\left(\frac{\nu+l_{f}\omega}{u}-\delta\right)\\&F_{Y2}=k_{r}\alpha_{2}\approx k_{r}\frac{\nu-l_{r}\omega}{u}\end{aligned}$$

#### 数值稳定的离散时间方程
此离散方程具备数值稳定性
$$
X_{k+1} = F(X_k, U_k) =
\begin{bmatrix}
x_k + T_s (u_k \cos \phi_k - v_k \sin \phi_k) \\
y_k + T_s (v_k \cos \phi_k + u_k \sin \phi_k) \\
\phi_k + T_s \omega_k \\
u_k + T_s a_k \\
\frac{m u_k v_k + T_s (l_f k_f - l_r k_r) \omega_k - T_s k_f \delta_k u_k - T_s m u_k^2 \omega_k}{m u_k - T_s (k_f + k_r)} \\
\frac{I_z u_k \omega_k + T_s (l_f k_f - l_r k_r) v_k - T_s l_f k_f \delta_k u_k}{I_z u_k - T_s (l_f^2 k_f + l_r^2 k_r)}
\end{bmatrix}
$$
$$
X = 
\begin{bmatrix}
    x \\ y \\ \phi \\ u \\ v \\ \omega
\end{bmatrix},
U = 
\begin{bmatrix}
    a \\ \delta
\end{bmatrix}
$$
#### 离散时间方程的Jacobian矩阵
根据符号计算，得到Jacobian矩阵
$$
A = \frac{\partial F}{\partial X} = 
\begin{bmatrix}
1 & 0 & -T_s (v \cos(\phi) + u \sin(\phi)) & T_s \cos(\phi) & -T_s \sin(\phi) & 0 \\
0 & 1 & T_s (u \cos(\phi) - v \sin(\phi)) & T_s \sin(\phi) & T_s \cos(\phi) & 0 \\
0 & 0 & 1 & 0 & 0 & T_s \\
0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & - \frac{T_s \delta k_f - m v + 2 T_s m \omega u}{m u - T_s (k_f + k_r)} - \frac{m (m u v + T_s \omega (k_f l_f - k_r l_r) - T_s m \omega u^2 - T_s \delta k_f u)}{(m u - T_s (k_f + k_r))^2} & \frac{m u}{m u - T_s (k_f + k_r)} & \frac{- T_s m u^2 + T_s (k_f l_f - k_r l_r)}{m u - T_s (k_f + k_r)} \\
0 & 0 & 0 & \frac{I_z \omega - T_s \delta k_f l_f}{I_z u - T_s (k_f l_f^2 + k_r l_r^2)} - \frac{I_z (I_z \omega u + T_s v (k_f l_f - k_r l_r) - T_s \delta k_f l_f u)}{(I_z u - T_s (k_f l_f^2 + k_r l_r^2))^2} & \frac{T_s (k_f l_f - k_r l_r)}{I_z u - T_s (k_f l_f^2 + k_r l_r^2)} & \frac{I_z u}{I_z u - T_s (k_f l_f^2 + k_r l_r^2)}
\end{bmatrix}
$$

$$
B = \frac{\partial F}{\partial U} = 
\begin{bmatrix}
0 & 0 \\
0 & 0 \\
0 & 0 \\
T_s & 0 \\
0 & -\frac{T_s k_f u}{m u - T_s (k_f + k_r)} \\
0 & -\frac{T_s k_f l_f u}{I_z u - T_s (k_f l_f^2 + k_r l_r^2)}
\end{bmatrix}
$$
### 1.2 constraints and cost function

#### constraints
可以对状态量和控制量施加约束

$$
\begin{bmatrix}
    x_{min} \\ y_{min} \\ \phi_{min} \\ u_{min} \\ v_{min} \\ \omega_{min}
\end{bmatrix}
\leq
\begin{bmatrix}
    x \\ y \\ \phi \\ u \\ v \\ \omega
\end{bmatrix}
\leq
\begin{bmatrix}
    x_{max} \\ y_{max} \\ \phi_{max} \\ u_{max} \\ v_{max} \\ \omega_{max}
\end{bmatrix}
$$
$$
\begin{bmatrix}
    a_{min} \\ \delta_{min}
\end{bmatrix}
\leq 
\begin{bmatrix}
    a \\ \delta
\end{bmatrix}
\leq
\begin{bmatrix}
    a_{max} \\ \delta_{max}
\end{bmatrix}
$$

#### cost function
$$
\operatorname*{minimize}_{x_{0:N},u_{0:N-1}}\quad\ell_{N}(x_{N})+\sum_{k=0}^{N-1}\ell_{k}(x_{k},u_{k},\Delta t) = \\
x_{N}^T Q_N x_{N} + \sum_{k=0}^{N-1}\left(x_{k}^T Q_{k} x_{k}\right) + \left(u_{k}^T R_{k} u_{k}\right)
$$

### 1.3 optimal control problem
参考 AL_ilqr_tutorial.pdf OCP问题：
$$\begin{aligned}
&\operatorname*{minimize}_{x_{0:N},u_{0:N-1}}\quad\ell_{N}(x_{N})+\sum_{k=0}^{N-1}\ell_{k}(x_{k},u_{k},\Delta t) \\
&\text{subject to} \\
&x_{k+1} = f(x_k, u_k, \Delta t), k=1,\dots,N-1, \\
&g_{k}(x_{k},u_{k})\{\leq0\},\forall k, \\
&h_{k}(x_{k},u_{k})=0,\forall k,
\end{aligned}$$

$$\begin{aligned}
&\operatorname*{minimize}_{x_{0:N},u_{0:N-1}}\quad\ell_{N}(x_{N})+\sum_{k=0}^{N-1}\ell_{k}(x_{k},u_{k},\Delta t) \\
&\text{subject to} \\
&x_{k+1} = f(x_k, u_k, \Delta t), k=1,\dots,N-1, \\
&c_{k}(x_{k},u_{k})\leq0,\forall k,
\end{aligned}$$

增广拉格朗日法（Augmented Lagranguan）常用来处理约束优化问题。
（为什么不采用罚函数？只有当违反约束后罚函数项取无穷大，罚函数法的最优解才收敛至真实的最优解，但是这种方法在有限数值精度下处理ocp问题是不现实的）
（为什么采用增广拉格朗日法？AL根据约束来估计拉格朗日乘子。）
拉格朗日函数
$$\mathcal{L}_A=f(x)+\lambda^Tc(x)+\frac{1}{2}c(x)^TI_\mu c(x)$$
拉格朗日乘子$\lambda$，罚函数乘子$\mu$，等式约束$\mathcal{E}$，不等式约束$\mathcal{I}$
$$I_\mu=\begin{cases}0&\text{if } c_i(x)<0\wedge\lambda_i=0, i\in\mathcal{I}\\\mu_i&\text{otherwise}\end{cases}$$
对于符合条件的不等式约束，$\lambda_i$为0，否则为$\mu_i$

al-ocp求解步骤：
1. holding $\lambda$, $\mu$ constant, solving $min_x\mathcal{L}(x,\lambda,\mu)$
2. update $\lambda$ and $\mu$
$$\lambda_i^+=\begin{cases}\lambda_i+\mu_ic_i(x^*)&i\in\mathcal{E}\\\max(0,\lambda_i+\mu_ic_i(x^*)&i\in\mathcal{I},\end{cases}$$
$$\mu^+=\phi\mu, \phi > 1$$
3. check constraint convergence
4. if tolerance not met, go to step 1

## 2. backward pass

拉格朗日函数：
$$\begin{aligned}
\mathcal{L}_{A}=& \ell_{N}(x_{N})+\left(\lambda_{N}+\frac12c_{N}(x_{N})I_{\mu,N}\right)^{T}c_{N}(x_{N}) \\
& +\sum_{k=0}^{N-1}\left[\ell_k(x_k,u_k,\Delta t)\right] \\
&+\left(\lambda+\frac{1}{2}c_{k}(x_{k},u_{k})^{T}I_{\mu,k}\right)^{T}c_{k}(x_{k},u_{k})] \\
=& \mathcal{L}_{N}(x_{N},\lambda_{N},\mu_{N})+\sum_{k=0}^{N-1}\mathcal{L}_{k}(x_{k},u_{k},\lambda_{k},\mu_{k}) 
\end{aligned}$$

定义 cost-to-go function 和 action-value function
$$V_N(x_N)|_{\lambda,\mu}=\mathcal{L}_N(x_N,\lambda_N,\mu_N)$$
$$\begin{aligned}
V_{k}(x_{k})|_{\lambda,\mu}& =\min_{u_k}\{\mathcal{L}_k(x_k,u_k,\lambda_k,\mu_k) \\
&+V_{k+1}(f(x_k,u_k,\Delta t))|_{\lambda,\mu}\} \\
&=\min_{u_k}Q(x_k,u_k)|_{\lambda,\mu},
\end{aligned}$$

cost-to-go function 2-order approximation:

$$\delta V_k(x)\approx\frac{1}{2}\delta x_k^TP_k\delta x_k+p_k^T\delta x_k$$

minimize state-action function 2-order approximation with respect to $\delta u$.

$$\delta Q_k=\frac{1}{2}\begin{bmatrix}\delta x_k\\\delta u_k\end{bmatrix}^T\begin{bmatrix}Q_{xx}&Q_{xu}\\Q_{ux}&Q_{uu}\end{bmatrix}\begin{bmatrix}\delta x_k\\\delta u_k\end{bmatrix}+\begin{bmatrix}Q_x\\Q_u\end{bmatrix}^T\begin{bmatrix}\delta x_k\\\delta u_k\end{bmatrix}$$

$P_k$和$p_k$ 分别是 k 时刻 cost-to-go function 的 Hessian 和 gradient：

当 $k=N$ 时：
$$p_{N}=\frac{∂V}{∂x}|_{N}=(\ell_N)_x+(c_N)_x^T(\lambda+I_{\mu_N}c_N)$$
$$P_{N}=\frac{∂^2V}{∂x^2}|_{N}=(\ell_N)_{xx}+(c_N)_x^TI_{\mu_N}(c_N)_x$$

当 $k<N$ 时：
$$
\begin{align*}
    Q_x &= \frac{∂J}{∂x}|_{k} + \frac{∂f}{∂x}^{T}|_{k} \frac{∂V}{∂x}^{T}|_{k+1} + (c_k)_x^T(\lambda+I_{\mu_N}c_k) \\
    Q_u &= \frac{∂J}{∂u}|_{k} + \frac{∂f}{∂u}^{T}|_{k} \frac{∂V}{∂x}^{T}|_{k+1} + (c_k)_u^T(\lambda+I_{\mu_N}c_k) \\
    Q_{ux} &= \frac{∂^2J}{∂u∂x}|_{k} +   \frac{∂J}{∂u}|_{k} \frac{∂^2V}{∂x^2}^{T}|_{k+1} \frac{∂J}{∂x}|_{k} + (c_k)_u^TI_{\mu_N}(c_k)_x\\
    Q_{xx} &= \frac{∂^2J}{∂x∂x}|_{k} +   \frac{∂J}{∂x}|_{k} \frac{∂^2V}{∂x^2}^{T}|_{k+1} \frac{∂J}{∂x}|_{k} + (c_k)_x^TI_{\mu_N}(c_N)_x \\
    Q_{uu} &= \frac{∂^2J}{∂u∂u}|_{k} +   \frac{∂J}{∂u}|_{k} \frac{∂^2V}{∂x^2}^{T}|_{k+1} \frac{∂J}{∂u}|_{k} + (c_k)_u^TI_{\mu_N}(c_k)_u
\end{align*}
$$

此处省略$\delta u^*_k$的推导过程，由两部分组成：反馈和前馈。为了保证正则性，需要对$Q_{uu}$进行正则化。
$$\delta u_{k}^{*}=-(Q_{uu}+\rho I)^{-1}(Q_{ux}\delta x_{k}+Q_{u})\equiv K_{k}\delta x_{k}+d_{k}$$
$$K_{k} = -(Q_{uu}+\rho I)^{-1}Q_{ux}$$
$$d_{k} = -(Q_{uu}+\rho I)^{-1}Q_{u}$$

将最优控制率带入 cost-to-go function 2-order approximation，得到 k 时刻 cost-to-go function 的 Hessian 和 gradient 的闭式解以及 cost-to-go 的change：
$$\begin{aligned}
P_{k}& =Q_{xx}+K_{k}^{T}Q_{uu}K_{k}+K_{k}^{T}Q_{ux}+Q_{xu}K_{k} \\
p_{k}& =Q_x+K_k^TQ_{uu}d_k+K_k^TQ_u+Q_{xu}d_k \\
\Delta V_{k}& =d_k^TQ_u+\frac{1}{2}d_k^TQ_{uu}d_k. 
\end{aligned}$$
## 3. forward pass
在backward pass中，我们从终端状态计算最优控制率，在forward pass中，基于上一帧/初始状态的nominal trajectory和当前车辆的状态，通过dynamics前向推演出新的nominal trajectory
$$\begin{aligned}
\delta x_{k}=& \bar{x}_{k}-x_{k} \\
\delta u_{k}=& K_{k}\delta x_{k}+\alpha d_{k} \\
\bar{u}_{k}=& u_k+\delta u_k \\
\bar{x}_{k+1}=& f(\bar{x}_k,\bar{u}_k) 
\end{aligned}$$
### 3.1 line search
## 4. algorithm