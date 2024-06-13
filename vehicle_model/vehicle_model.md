# vehicle dynamics and control
## 1. linear 2 dof dynamics model 
in vehicle body coordinate

$$ \frac{d}{dt}\begin{bmatrix} y \\ \dot{y} \\ \psi \\ \dot{\psi} \end{bmatrix} = \begin{bmatrix} 0 & 1 & 0 & 0 \\ 0 & \frac{C_f+C_r}{mv_x} & 0 & \frac{C_fl_f - C_rl_r}{mv_x} - v_x \\ 0 & 0 & 0 & 1 \\ 0 & \frac{C_fl_f - C_rl_r}{I_zv_x} & 0 & \frac{C_fl_f^2 - C_rl_r^2}{I_zv_x} \\  \end{bmatrix}\begin{bmatrix} y \\ \dot{y} \\ \psi \\ \dot{\psi} \end{bmatrix} + \begin{bmatrix} 0 \\ -\frac{C_f}{m} \\ 0 \\ \frac{C_fl_f}{I_z }  \end{bmatrix} \delta_f $$

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