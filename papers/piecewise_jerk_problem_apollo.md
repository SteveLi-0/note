# Optimal Vehicle Path Planning Using Quadratic Optimization for Baidu Apollo Open Platform

This paper is about the trajectory optimaization in Baidu Apollo Open Platform. Compared with 5order polinomial, piecewise-jerk path formulation shows more degree of freedom.

The optimaization problem is to find the safe and kinematically feasibale solution from the given drivable corridor in a frenet frame. 

## problem formulation

### Objective function

- Collision-free 
- Minimal lateral deviation
- Minimal lateral movement
- (Optional) Maximal obstabcle distance

The optimization objective function is:

$$\begin{aligned}
&\boldsymbol{f}(\boldsymbol{l}(s)) =w_{l}*\int\boldsymbol{l}(s)^{2}ds+w_{l^{\prime}}*\int\boldsymbol{l^{\prime}}(s)^{2}ds \\
& +w_{l^{\prime\prime}}*\int\boldsymbol{l''}(s)^{2}ds+w_{l^{\prime\prime\prime}}*\int\boldsymbol{l'''}(s)^{2}ds \\
&+w_{obs}*\int(\boldsymbol{l}(s)-0.5*(\boldsymbol{l}_{B}(s)_{min}+\boldsymbol{l}_{B}(s)_{max}))^{2}ds
\end{aligned}$$

subject to:

$$\boldsymbol{l}(s)\in \boldsymbol{l}_B(s), \forall s \in [0, s_{max}] $$


Discretization:

$$\begin{aligned}
\tilde{\boldsymbol{f}}(\boldsymbol{l}(s))& =w_{l}*\sum_{i=0}^{n-1}l_{i}^{2}+w_{l'}*\sum_{i=0}^{n-1}l_{i}^{\prime2}+w_{l''}*\sum_{i=0}^{n-1}l_{i}^{\prime\prime2} \\
& +w_{l^{\prime\prime\prime}}*\sum_{i=0}^{n-2}\left(\frac{l_{i+1}^{\prime\prime}-l_i^{\prime\prime}}{\Delta s}\right)^2 \\
&+w_{obs}*\sum_{i=0}^{n-1}\left(l_i-0.5*(l_{min}^i+l_{max}^i)\right)^2
\end{aligned}$$

### Kinematically feasible

The most important factor for kinematic feasibility is the curvature of the path

$$\kappa=\frac{\left(\frac{((l''+(\kappa_rl+\kappa_rl')\tan\Delta\theta)\cos^2\Delta\theta}{1-\kappa_rl}+\kappa_r\right)\cos\Delta\theta}{1-\kappa_rl}$$

$\kappa$ is approximated as follows:

$$\kappa\approx\frac{\kappa_r}{1-\kappa_r*l}$$

$$\kappa_{max}=\frac{\alpha_{max}}{L}$$

## Implementation

Here are detailed derivation of the optimization problem.

The standarization of the quradric optimization problem is:

$$\begin{aligned}&\text{minimize}&&\frac12x^TPx+q^Tx\\&\text{subject to}&&l\leq Ax\leq u\\&x\in\mathbf{R}^n&&P\in\mathbf{S}_+^n&&q\in\mathbf{R}^n\end{aligned}$$

The objective function is:

$$\begin{aligned}
\tilde{\boldsymbol{f}}(\boldsymbol{l}(s))& =w_{l}*\sum_{i=0}^{n-1}l_{i}^{2}+w_{l'}*\sum_{i=0}^{n-1}l_{i}^{\prime2}+w_{l''}*\sum_{i=0}^{n-1}l_{i}^{\prime\prime2} \\
& +w_{l^{\prime\prime\prime}}*\sum_{i=0}^{n-2}\left(\frac{l_{i+1}^{\prime\prime}-l_i^{\prime\prime}}{\Delta s}\right)^2 \\
&+w_{obs}*\sum_{i=0}^{n-1}\left(l_i-0.5*(l_{min}^i+l_{max}^i)\right)^2 
\end{aligned}$$

The constraint is:

Boundary constraint of $l, l^\prime, l^{\prime\prime}, l^{\prime\prime\prime}$

Kinematically feasible constraint:

$$\begin{aligned}
&l_{i+1}'' =l''_i+\int_0^{\Delta s}l''''_{i\to i+1}ds=l''_i+l'''_{i\to i+1}*\Delta s \\
&l'_{i+1} =l_i^{\prime}+\int_0^{\Delta s}\boldsymbol{l''}(s)ds=l_i^{\prime}+l_i^{\prime\prime}*\Delta s+\frac12*l_{i\to i+1}^{\prime\prime\prime}*\Delta s^2 \\
&l_{i+1} =l_i+\int_0^{\Delta s}\boldsymbol{l'}(s)ds \\
&=l_i+l_i^{\prime}*\Delta s+\frac12*l_i^{\prime\prime}*\Delta s^2+\frac16*l_{i\to i+1}^{\prime\prime\prime}*\Delta s^3
\end{aligned}$$

$$l_i^{\prime\prime\prime}=\frac{l_{i+1}^{\prime\prime}-l_i^{\prime\prime}}{\Delta s}$$

here is the kinematically feasible constraint:
$$\begin{aligned}
&l'_{i+1} =l_i^{\prime}+\frac12l_i^{\prime\prime}*\Delta s+\frac12*l_{i+1}^{\prime\prime}*\Delta s^2 \\
&l_{i+1} =l_i+l_i^{\prime}*\Delta s+\frac13*l_i^{\prime\prime}*\Delta s^2+\frac16*l_{i+1}^{\prime\prime\prime}*\Delta s^2
\end{aligned}$$

### Objective function matrix

$$P = P_1 + P_2 + P_3$$
$$q = q_1 + q_2 + q_3$$

$$x = \begin{bmatrix}
    l_0 & l_1 & \cdots & l_{n-1} & l^{\prime}_0 & l^{\prime}_1 & \cdots & l^{\prime}_{n-1} & l^{\prime\prime}_1 & \cdots & l^{\prime\prime}_{n-1}
\end{bmatrix}^T$$
#### $P_1, q_1$: cost of $l, l^\prime, l^{\prime\prime}, l^{\prime\prime\prime}$

$$P_1 = 
\begin{bmatrix}
w_l   & \cdots & \cdots & 0       \\
\vdots & \ddots &        & \vdots \\
\vdots &        & \ddots & \vdots \\
0      & \cdots & \cdots & w_l    \\
&&&&   w_{dl}   & \cdots & \cdots & 0        \\
&&&&   \vdots   & \ddots &        & \vdots   \\
&&&&   \vdots   &        & \ddots & \vdots   \\
&&&&   \vdots   & \cdots & \cdots & w_{dl}   \\
&&&&&&&& w_{ddl}+\frac{w_{dddl}}{\Delta s^2} & 0 \\
&&&&&&&& -2\frac{w_{dddl}}{\Delta s^2}       & w_{ddl}+2\frac{w_{dddl}}{\Delta s^2} \\
&&&&&&&&& \ddots                             & \ddots \\
&&&&&&&&&& \ddots                            & w_{ddl}+2\frac{w_{dddl}}{\Delta s^2} \\
&&&&&&&&&&& -2\frac{w_{dddl}}{\Delta s^2}    & w_{ddl}+\frac{w_{dddl}}{\Delta s^2} \\
\end{bmatrix}
$$

$$q_1 = 0$$

#### $P_2, q_2$: cost of obstacles (cost of reference)

$$P_2 = \begin{bmatrix}
    w_{obs}   & \cdots & \cdots & 0        \\
    \vdots & \ddots &        & \vdots      \\
    \vdots &        & \ddots & \vdots      \\
    0      & \cdots & \cdots & w_{obs}     \\
&&&& 0 \\
&&&&& \ddots \\
&&&&&& \ddots \\ 
&&&&&&& 0 \\
\end{bmatrix}$$ 



