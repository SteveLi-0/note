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

## 3. vehicle kinematic model

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

### 4. Runge-Kutta 2nd Order (RK2) Method

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
