# vehicle dynamics and control
## 1. linear 2 dof dynamics model 
in vehicle body coordinate

$$
 \frac{d}{dt}\begin{bmatrix} y \\ \dot{y} \\ \psi \\ \dot{\psi} \end{bmatrix} = \begin{bmatrix} 0 & 1 & 0 & 0 \\ 0 & \frac{C_f+C_r}{mv_x} & 0 & \frac{C_fl_f - C_rl_r}{mv_x} - v_x \\ 0 & 0 & 0 & 1 \\ 0 & \frac{C_fl_f - C_rl_r}{I_zv_x} & 0 & \frac{C_fl_f^2 - C_rl_r^2}{I_zv_x} \\  \end{bmatrix}\begin{bmatrix} y \\ \dot{y} \\ \psi \\ \dot{\psi} \end{bmatrix} + \begin{bmatrix} 0 \\ -\frac{C_f}{m} \\ 0 \\ \frac{C_fl_f}{I_z }  \end{bmatrix} \delta_f
$$


## 2. linear 2 dof dynamics model in frenet coordinate

$$
\frac{d}{dt}\begin{bmatrix} e_d \\ \dot{e_d} \\ e_\psi \\ \dot{e_\psi} \end{bmatrix} = \begin{bmatrix} 
0 & 1 & 0 & 0 \\
0 & \frac{C_f+C_r}{mv_x} & -\frac{C_f+C_r}{m} & \frac{C_fl_f - C_rl_r}{mv_x} \\
0 & 0 & 0 & 1 \\
0 & \frac{C_fl_f - C_rl_r}{I_zv_x} & -\frac{C_fl_f - C_rl_r}{I_z} & \frac{C_fl_f^2 + C_rl_r^2}{I_zv_x} \end{bmatrix}
\begin{bmatrix} e_d \\ \dot{e_d} \\ e_\psi \\ \dot{e_\psi} \end{bmatrix} \\ + 
\begin{bmatrix} 0 \\ -\frac{C_f}{m} \\ 0 \\ -\frac{C_fl_f}{I_z }  \end{bmatrix} \delta_f  + 
\begin{bmatrix} 0 \\  \frac{C_fl_f - C_rl_r}{mv_x} - v_x \\ 0 \\ \frac{C_fl_f^2 + C_rl_r^2}{I_zv_x} \end{bmatrix} \dot{\psi}_{des}
$$

$$
x_{ss} = \begin{bmatrix} \delta_{ff} \\ 0 \\ 0 \\ 0 \end{bmatrix} \\ + \begin{bmatrix} -\frac{1}{k_1}\frac{mv_x^2}{R(l_f+l_r)}(-\frac{l_r}{C_f}+\frac{l_f}{C_r}-\frac{l_f}{C_r}k_3)-\frac{1}{k_1R}(l_f+l_r-l_rk_3) \\ 0 \\ 
-\frac{1}{RC_r(l_f+f_r)}(C_rl_fl_r+C_rl_r^2+l_fmv_x^2) \\ 0 \end{bmatrix}
$$

$$
\delta_{ff} = \frac{mv_x^2}{RL}(-\frac{l_r}{C_f}+\frac{l_f}{C_r}-\frac{l_f}{C_r}k_3)+\frac{1}{k_1R}(L-l_rk_3)
$$

### 2.1 转向特性建模

#### 一阶惯性
将转向指令和转向响应之间建模成一阶惯性环节
$$
\frac{\delta_{sw}(s)}{\delta_{cmd}(s)} = G(s)=\frac K{\tau s+1}
$$
$$
\tau\dot{\delta}_{sw}(t)+\delta_{sw}(t)=K\delta_{sw}(t) \\
\dot{\delta}_{sw}(t) = -\frac{1}{\tau}\delta_{sw}(t)+\frac{K}{\tau}\delta_{sw}(t)
$$

#### 积分环节
转向速率和转向指令之间是积分环节
$$
\dot{\delta}_{cmd} = \dot{\delta} = u
$$

#### 状态空间表达式

$$
\begin{bmatrix} \dot{\delta}_{sw} \\ \dot{\delta}_{cmd} \end{bmatrix} = 
\begin{bmatrix} -\frac{1}{\tau} & \frac{K}{\tau} \\ 0 & 0 \end{bmatrix} 
\begin{bmatrix} {\delta}_{sw} \\ {\delta}_{cmd} \end{bmatrix} +
\begin{bmatrix} 0 \\ 1 \end{bmatrix} u
$$

### 2.2 包含转向延迟特性的 linear 2 dof error model
$$
\frac{d}{dt}\begin{bmatrix} e_d \\ \dot{e_d} \\ e_\psi \\ \dot{e_\psi} \\ \delta_{sw} \\ \delta_{cmd} \end{bmatrix} = \begin{bmatrix} 
0 & 1 & 0 & 0 & 0 & 0 \\
0 & \frac{C_f+C_r}{mv_x} & -\frac{C_f+C_r}{m} & \frac{C_fl_f - C_rl_r}{mv_x} & -\frac{C_f}{m} & 0\\
0 & 0 & 0 & 1 & 0 & 0\\
0 & \frac{C_fl_f - C_rl_r}{I_zv_x} & -\frac{C_fl_f - C_rl_r}{I_z} & \frac{C_fl_f^2 + C_rl_r^2}{I_zv_x} & -\frac{C_fl_f}{I_z } & 0 \\
0 & 0 & 0 & 0 & -\frac{1}{\tau} & \frac{K}{\tau} \\
0 & 0 & 0 & 0 & 0 & 0 
 \end{bmatrix}
\begin{bmatrix} e_d \\ \dot{e_d} \\ e_\psi \\ \dot{e_\psi} \\ \delta_{sw} \\ \delta_{cmd} \end{bmatrix} \\ + 
\begin{bmatrix} 0 \\ 0 \\ 0 \\ 0 \\ 0 \\ 1  \end{bmatrix} \dot{\delta}_{cmd}  + 
\begin{bmatrix} 0 \\  \frac{C_fl_f - C_rl_r}{mv_x} - v_x \\ 0 \\ \frac{C_fl_f^2 + C_rl_r^2}{I_zv_x} \\ 0 \\ 0 \end{bmatrix} \dot{\psi}_{des}
$$

## 3. vehicle kinematic model

### 3.1 形式一：控制量：转向角增量，加速度增量
#### 连续时间方程
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

#### 离散方程
RK2离散

#### RK2离散下的Jacobian矩阵
$$
J_x = \frac{\partial f_d}{\partial x} \\ =
\begin{bmatrix}
1 & 0 & -dt \sin\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right) \left(v + \frac{a dt}{2}\right) & -\frac{dt^2 v \sin\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right) (\tan^2(\delta) + 1) \left(v + \frac{a dt}{2}\right)}{2L(k v^2 + 1)} & dt \cos\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right) - dt \sin\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right) \left(\frac{dt \tan(\delta)}{2L(k v^2 + 1)} - \frac{dt k v^2 \tan(\delta)}{L(k v^2 + 1)^2}\right) \left(v + \frac{a dt}{2}\right) & \frac{dt^2 \cos\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right)}{2} \\
0 & 1 & dt \cos\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right) \left(v + \frac{a dt}{2}\right) & \frac{dt^2 v \cos\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right) (\tan^2(\delta) + 1) \left(v + \frac{a dt}{2}\right)}{2L(k v^2 + 1)} & dt \sin\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right) + dt \cos\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right) \left(\frac{dt \tan(\delta)}{2L(k v^2 + 1)} - \frac{dt k v^2 \tan(\delta)}{L(k v^2 + 1)^2}\right) \left(v + \frac{a dt}{2}\right) & \frac{dt^2 \sin\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right)}{2} \\
0 & 0 & 1 & \frac{dt (\tan^2(\delta + \frac{dt u1}{2}) + 1) \left(v + \frac{a dt}{2}\right)}{L(k (v + \frac{a dt}{2})^2 + 1)} & \frac{dt \tan(\delta + \frac{dt u1}{2})}{L(k (v + \frac{a dt}{2})^2 + 1)} - \frac{dt k \tan(\delta + \frac{dt u1}{2}) (2v + a dt) \left(v + \frac{a dt}{2}\right)}{L(k (v + \frac{a dt}{2})^2 + 1)^2} & \frac{dt^2 \tan(\delta + \frac{dt u1}{2})}{2L(k (v + \frac{a dt}{2})^2 + 1)} - \frac{dt^2 k \tan(\delta + \frac{dt u1}{2}) \left(v + \frac{a dt}{2}\right)^2}{L(k (v + \frac{a dt}{2})^2 + 1)^2} \\
0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & dt \\
0 & 0 & 0 & 0 & 0 & 1
\end{bmatrix}
$$

$$
J_u = \frac{\partial f_d}{\partial u} \\ =
\begin{bmatrix}
0 & 0 \\
0 & 0 \\
\frac{dt^2 (\tan^2\left(\delta + \frac{dt u_1}{2}\right) + 1) \left(v + \frac{a dt}{2}\right)}{2L \left(k \left(v + \frac{a dt}{2}\right)^2 + 1\right)} & 0 \\
dt & 0 \\
0 & \frac{dt^2}{2} \\
0 & dt \\
\end{bmatrix}
$$

### 3.2 形式二 控制量：转向角增量
#### 连续方程
$$
\begin{bmatrix}
    \dot{x} \\
    \dot{y} \\
    \dot{\theta} \\
    \dot{\delta} \\
\end{bmatrix}
=
\begin{bmatrix}
    v \cos(\theta) \\
    v \sin(\theta) \\
    \frac{v \tan(\delta)}{L (1 + k v^2)} \\
    u_1 \\
\end{bmatrix}
$$
#### RK2离散
#### RK2下Jacobian矩阵
$$
J_x = \frac{\partial f_d}{\partial x} \\ =
\begin{bmatrix}
1 & 0 & -dt v \sin\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right) & -\frac{dt^2 v^2 \sin\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right) (\tan^2(\delta) + 1)}{2L(k v^2 + 1)} \\
0 & 1 & dt v \cos\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right) & \frac{dt^2 v^2 \cos\left(\theta + \frac{dt v \tan(\delta)}{2L(k v^2 + 1)}\right) (\tan^2(\delta) + 1)}{2L(k v^2 + 1)} \\
0 & 0 & 1 & \frac{dt v (\tan^2(\delta + \frac{dt u_1}{2}) + 1)}{L(k v^2 + 1)} \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

$$
J_u = \frac{\partial f_d}{\partial u} \\ =
\begin{bmatrix}
0 \\
0 \\
\frac{dt^2 v (\tan^2\left(\delta + \frac{dt u_1}{2}\right) + 1)}{2L(k v^2 + 1)} \\
dt \\
\end{bmatrix}
$$

## 4. Runge-Kutta 2nd Order (RK2) Method

RK2方法，也称为中点法，是一种常用的数值积分方法。公式如下：

$$
\begin{aligned}
    k_1 &= f(t_n, y_n), \\
    k_2 &= f(t_n + \frac{h}{2}, y_n + \frac{h}{2} k_1), \\
    y_{n+1} &= y_n + h k_2,
\end{aligned}
$$

其中：
- $ t_n $ 是当前时间步
- $ y_n $ 是当前状态
- $ h $ 是时间步长
- $ f $ 是状态的导数函数

### 5. Runge-Kutta 4th Order (RK4) Method

RK4方法是一种更高精度的数值积分方法，公式如下：

$$
\begin{aligned}
    k_1 &= f(t_n, y_n), \\
    k_2 &= f(t_n + \frac{h}{2}, y_n + \frac{h}{2} k_1), \\
    k_3 &= f(t_n + \frac{h}{2}, y_n + \frac{h}{2} k_2), \\
    k_4 &= f(t_n + h, y_n + h k_3), \\
    y_{n+1} &= y_n + \frac{h}{6} (k_1 + 2k_2 + 2k_3 + k_4),
\end{aligned}
$$

其中：
- $ t_n $ 是当前时间步
- $ y_n $ 是当前状态
- $ h $ 是时间步长
- $ f $ 是状态的导数函数

## 6. stop and go model (continuous and discreted)

    参考论文：Numerically Stable Dynamic Bicycle Model for Discrete-time Control

### 连续时间非线性方程
$$
\dot{x} = f(X, U) = 
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

### 数值稳定的离散时间方程
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

### 离散时间方程的Jacobian矩阵

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
