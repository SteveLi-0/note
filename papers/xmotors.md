# Optimal Vehicle Trajectory Planning for Static Obstacle Avoidance using Nonlinear Optimization

## problem formulation 

### vehicle kinematic model

control input: linear jerk and curvature change rate 

positional increment functions are difficult to comuppte, so we use Gaussian-Legendra quadrature to approximate the positional increment function.

10th order approximation is adopted in the paper.

**加速度更新公式**
\[ a_1 = a_0 + j \Delta t \]
其中：
- \(a_1\) 是更新后的加速度。
- \(a_0\) 是初始加速度。
- \(j\) 是线性冲击（加速度的变化率）。
- \(\Delta t\) 是时间间隔。

**速度更新公式**
\[ v_1 = v_0 + a_0 \Delta t + \frac{1}{2} j \Delta t^2 \]
其中：
- \(v_1\) 是更新后的速度。
- \(v_0\) 是初始速度。
- \(a_0\) 是初始加速度。
- \(j\) 是线性冲击。
- \(\Delta t\) 是时间间隔。

**曲率更新公式**
\[ \kappa_1 = \kappa_0 + \dot{\kappa} \Delta t \]
其中：
- \(\kappa_1\) 是更新后的曲率。
- \(\kappa_0\) 是初始曲率。
- \(\dot{\kappa}\) 是曲率变化率（曲率的时间导数）。
- \(\Delta t\) 是时间间隔。

**航向角更新公式**
\[ \theta_1 = \theta_0 + \kappa_0 v_0 \Delta t + \frac{1}{2} (\kappa_0 a_0 + v_0 \dot{\kappa}) \Delta t^2 + \frac{1}{3} \left( \frac{1}{2} \kappa_0 j + a_0 \dot{\kappa} \right) \Delta t^3 + \frac{1}{8} \dot{\kappa} j \Delta t^4 \]
其中：
- \(\theta_1\) 是更新后的航向角。
- \(\theta_0\) 是初始航向角。
- \(\kappa_0\) 是初始曲率。
- \(v_0\) 是初始速度。
- \(a_0\) 是初始加速度。
- \(\dot{\kappa}\) 是曲率变化率。
- \(j\) 是线性冲击。
- \(\Delta t\) 是时间间隔。

**位置更新公式**
位置更新涉及到对 \(x\) 和 \(y\) 坐标的更新。由于其积分较复杂，通常通过数值积分方法（如高斯-勒让德求积法）近似求解。给定的公式为：
\[ x_1 = x_0 + \int_0^{\Delta t} \cos(\theta(s(t))) s'(t) dt \]
\[ y_1 = y_0 + \int_0^{\Delta t} \sin(\theta(s(t))) s'(t) dt \]
其中：
- \(x_1\) 和 \(y_1\) 是更新后的 \(x\) 和 \(y\) 坐标。
- \(x_0\) 和 \(y_0\) 是初始 \(x\) 和 \(y\) 坐标。
- \(\theta(s(t))\) 是时间 \(t\) 时刻的航向角。
- \(s(t)\) 是车辆在时间 \(t\) 时刻的路径长度（或行驶距离）。
- \(s'(t)\) 是路径长度相对于时间的导数（即速度）。

在高斯-勒让德求积法下，上述积分近似为：
\[ x_1 \approx x_0 + \frac{1}{2} \Delta t \sum_{i=1}^{N} w_i \cos\left(\theta\left(\frac{1}{2} \Delta t \xi_i + \frac{1}{2} \Delta t\right)\right) s'\left(\frac{1}{2} \Delta t \xi_i + \frac{1}{2} \Delta t\right) \]
\[ y_1 \approx y_0 + \frac{1}{2} \Delta t \sum_{i=1}^{N} w_i \sin\left(\theta\left(\frac{1}{2} \Delta t \xi_i + \frac{1}{2} \Delta t\right)\right) s'\left(\frac{1}{2} \Delta t \xi_i + \frac{1}{2} \Delta t\right) \]
其中：
- \(N\) 是高斯-勒让德求积法的阶数，决定了近似的精度。
- \(\xi_i\) 和 \(w_i\) 分别是第 \(i\) 个高斯节点和对应的权重。


### trajectroy planning problem input

vehicle initial state, vehicle parameters and kinematic bounds, vehicle model, reference line and drivable corridor, target speed

### objective formulation

The optimal evaluation of a vehicle trajectory is a weighted summatin of the following terms:
- centripetal acceleration
- centripetal jerk
- curavature change rate
- linear jerk
- distance to RL
- closeness to target speed

The author emphasize the **Huber loss** in distance to RL and the closeness to target speed. 

If a quadratic form of the cost is used, at the beginning of the lane change, this cost factor will become excessively large numerically, which causes other cost factors essentially become ineffective and leads to drastic lateral motions. The same idea applies to the closeness to target speed factor during ego vehicle starts from a static state to avoid drastic longitudinal motions

### Constraints

- Equality coonstraints for trajectory continuty
- Collision avoidance constraints: two disk model
- Kinematic limit and pose constraints:
  - vehicle state constraints
  - heading angle difference: not necessary but helpful on convergence rate in large curvature scenarios

## Implementation

- Initial guess and warm start can reduce the number of interation to 2 or 3
  - P controller 
  - previous cycle 
- The smoothness and density of the drivable corridor boundaries can greatly influence the convergence rate
  - smooth out the sharp corner
  - interpolate the boundaries to a high resoluion 1m to 0.1 m
- The prjection function is one of the bottleneck of the comuputation time.
  - using R tree to index the polyline before the optimaization can reduce the computation time to O(logN)
  
  
