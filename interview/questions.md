# 问题整理
## 解释一下什么是数值稳定的全速动力学模型？
车辆动力学模型在采用运动学计算轮胎侧偏角的时候，u是在分母上，所以对于低速工况无法使用。采用前向欧拉会引入额外的能量，在dt比较大的时候会造成数值不稳定，rk4等方法又会让方程变得复杂。
数值稳定的全速动力学模型是指在不同车速下（尤其是低速），通过离散化方法从连续时间系统转化而来的模型，能够保持数值解的稳定性，不会因为速度变化或时间步长增大而导致解发散或不准确。通过对传统动力学单车模型进行适当的离散化处理实现的。状态量包括：
- **\(x\)**: 车辆质心的横向位置
- **\(y\)**: 车辆质心的纵向位置
- **\(\phi\)**: 车辆的航向角（航向角描述了车辆的朝向方向）
- **\(u\)**: 车辆的纵向速度（即车辆前进方向上的速度）
- **\(v\)**: 车辆的横向速度（即车辆垂直于前进方向的速度）
- **\(\omega\)**: 车辆的横摆角速度（即车辆绕其垂直轴的旋转速度）

动态自行车模型的离散化过程

在论文中，离散化过程主要通过以下步骤实现：

1. **离散化目标**：
   - 将连续时间的动力学模型转换为离散时间的差分方程，以便于控制器建模和轨迹规划的应用。

2. **受向后欧拉法启发的离散化**：
   - 为了确保数值稳定性，采用了一种受向后欧拉法（Backward Euler Method）启发的变体方法。

3. **逐变量离散化**：
   - 对于状态量 \(x\)、\(y\) 和 \(\phi\) 使用正向欧拉法（Forward Euler Method）进行离散化。
   - 对于状态量 \(v\) 和 \(\omega\) 通过求解显式方程获得离散形式，这些方程是基于线性侧滑力模型推导的。
   - 对于状态量 \(u\) 使用简化的正向欧拉法进行离散化。

4. **数值稳定性**：
   - 通过这种混合离散化方法，模型在不同速度下都能保持数值稳定性，即使在低速场景下也能保持良好的预测精度和计算效率。

## 解释一下史密斯预估器
由于执行器存在响应延迟，特别是采用的执行器在小转角小转速下延迟很大（超过500ms）所以采用采用了两套预测时间参数。
史密斯预估器模型是

\[\dot{\mathbf{x}} = \mathbf{A} \mathbf{x} + \mathbf{B} \mathbf{u}\]

其中：

\[
\mathbf{x} = \begin{bmatrix}
v_x \\
v_y \\
\psi \\
r \\
X \\
Y \\
\delta \\
\theta
\end{bmatrix},
\]
\[
\mathbf{u} = \begin{bmatrix}
\delta_f \\
a_y \\
\theta_d
\end{bmatrix}
\]

### 状态矩阵 \( \mathbf{A} \)

\[
\mathbf{A} = \begin{bmatrix}
-\frac{C_f + C_r}{m \cdot v_y} & 0 & 0 & \frac{C_f \cdot l_f - C_r \cdot l_r}{m \cdot v_y} + v_y & 0 & 0 & -\frac{C_f}{m} & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\
\frac{C_f \cdot l_f - C_r \cdot l_r}{I_z \cdot v_y} & 0 & 0 & -\frac{C_f \cdot l_f^2 + C_r \cdot l_r^2}{I_z \cdot v_y} & 0 & 0 & \frac{C_f \cdot l_f}{I_z} & 0 \\
\frac{v_x \cdot \left( \cos(\psi + \beta + \theta) + (\psi + \beta + \theta) \cdot \sin(\psi + \beta + \theta) \right)}{\sqrt{v_x^2 + v_y^2}} & \frac{v_y \cdot \left( \cos(\psi + \beta + \theta) + (\psi + \beta + \theta) \cdot \sin(\psi + \beta + \theta) \right)}{\sqrt{v_x^2 + v_y^2}} & -\sin(\psi + \beta + \theta) \cdot \sqrt{v_x^2 + v_y^2} & 0 & 0 & 0 & 0 & -\sin(\psi + \beta + \theta) \cdot \sqrt{v_x^2 + v_y^2} \\
\frac{v_x \cdot \left( \sin(\psi + \beta + \theta) - (\psi + \beta + \theta) \cdot \cos(\psi + \beta + \theta) \right)}{\sqrt{v_x^2 + v_y^2}} & \frac{v_y \cdot \left( \sin(\psi + \beta + \theta) - (\psi + \beta + \theta) \cdot \cos(\psi + \beta + \theta) \right)}{\sqrt{v_x^2 + v_y^2}} & \cos(\psi + \beta + \theta) \cdot \sqrt{v_x^2 + v_y^2} & 0 & 0 & 0 & 0 & \cos(\psi + \beta + \theta) \cdot \sqrt{v_x^2 + v_y^2} \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
\end{bmatrix}
\]

### 控制矩阵 \( \mathbf{B} \)

\[
\mathbf{B} = \begin{bmatrix}
-\frac{C_f}{m} & 0 & 9.8 \\
0 & 1 & 0 \\
0 & 0 & 0 \\
\frac{C_f \cdot l_f}{I_z} & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0 \\
\end{bmatrix}
\]

### 符号含义

- \( \mathbf{x} \)：状态向量，包含以下状态量：
  - \( v_x \)：车辆的纵向速度（前进速度）
  - \( v_y \)：车辆的横向速度（侧滑速度）
  - \( \psi \)：车辆的偏航角（航向角）
  - \( r \)：车辆的偏航率
  - \( X \)：车辆在全局坐标系下的横向位置
  - \( Y \)：车辆在全局坐标系下的纵向位置
  - \( \delta \)：车辆的转向角
  - \( \theta \)：车辆的横摆角（偏航角扰动）

- \( \mathbf{u} \)：控制向量，包含以下控制量：
  - \( \delta_f \)：前轮的转向角
  - \( a_y \)：横向加速度
  - \( \theta_d \)：扰动量（如侧风引起的扰动）

- \( \mathbf{A} \)：状态矩阵，描述状态量之间的动态关系。
- \( \mathbf{B} \)：控制矩阵，描述控制输入对状态量的影响。

## 性能分析与优化是怎么实现的？

通过perf和火焰图，分析函数调用的开销。发现用于求解的开销只占osqp mpc类的三分之一，剩下的都是数据的准备。原来是每次求解osqp都构造一次数据，现在是将求解器作为一个控制器的成员变量，并修改mpc osqp中的数据结构，在控制器初始化的时候就根据问题的规模分配vector的容量。在求解的时候，更新这些求解器相关数据，就避免了构造析构、内存开辟的开销。

## osqp实现原理？

##  不依赖 Frenet 的 MPC 
##  求解稳定性优化
## KKT

## 策略树展开与仿真
### 如何展开策略树？
### 如何前向仿真
## 反应式轨迹规划
## CP tree如何求解

## 全局轨迹规划
## 预测
### 什么是向量化表征
### 怎么做交互
### 什么是自注意力机制
### 如何出轨迹
## 效率变道MDP的规则是什么样的
## 如何计算reward
## ST图是怎么构建的？
## 横纵向采样轨迹是怎么产生的？

