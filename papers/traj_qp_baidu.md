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