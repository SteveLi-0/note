# 机器人中的数值优化
## 1. preliminaries
### 1. Introduction
#### optimization problem 

$$
\begin{array}{c}\min&f(x)\\\mathrm{s.t.}&g(x)\leq0\\&h(x)=0\end{array}
$$

default assumptions:

- the objective function is lower bounded
    - lower bounded : 目标函数有下界 $$ f(x)\geq L $$
    - 保证 物理限制和实际约束、 优化问题的稳定性 
- the objective function has bounded sub-level sets
    - bounded sub-leveled set: 有界次水平集
    - $$ S_\alpha=\{u\mid J(u)\leq\alpha\} $$ 
    - 可行解的存在性和可行域的有限性：有界次水平集保证了可行解集不会无限扩展。也就是说，在寻找最优解时，算法不会无穷无尽地搜索整个控制策略空间。
    - 算法的收敛性：优化算法在有界次水平集上工作时，能够确保算法逐步逼近最优解，不会陷入无穷大范围的搜索。这对保证算法的收敛性和计算效率至关重要。
### 2.Convexity
#### why convexity?
- 凸函数在凸集合上的优化已经被充分研究
- 优化算法利用凸函数/集合的性质来分析收敛性
- 一些重要的问题具有凸的公式化/松弛:很多实际问题可以被转化为凸优化问题，或通过松弛技术近似为凸优化问题。这使得我们可以利用凸优化的方法来解决原本非凸的问题，从而简化求解过程
- 许多非凸函数在感兴趣的局部极小值附近是局部凸的
- 在实际中，非凸函数的局部极小值可能已经足够好

### 3.Convex sets

#### definition

A set is convex if all **convex combinations** of its points are also in the set.

convex cobinations: $$ \sum \theta_1 x_1 + \theta _2 x_2 + \theta _3 x_3 $$ $$ \sum \theta _i = 1 $$

#### examples

超平面、版空间、球、多项式

Cone 锥不一定是凸的

Cone：$ x \in C \Rightarrow ax \in C, \forall a \geq 0 $

Second-order cone SOC: $ C_2 = \left\{ (x, t) \mid \|x\| \leq t \right\} \in \mathbb{R}^{n+1} $ 是凸的

Semi-definite cone: $\mathcal{S}_+^n=\left\{A\in\mathbb{R}^{n\times n}\mid A=A^T,A\succeq0\right\}$ 是凸的

#### properties of convex sets

保凸性：
- The intersection of convex sets is convex：多面体
- set sum $A+B=\{x+y\mid x\in A,y\in B\}$
- set product $A\times B=\{(x, y)\mid x\in A,y\in B\}$

### 4. hign order info of functions

Function
$$f(x)=f(x_1,x_2,x_3)$$
Gradient
$$\nabla f(x)=\begin{pmatrix}\partial_1f(x)\\\partial_2f(x)\\\partial_3f(x)\end{pmatrix}$$

Hessian: Symmetric for smooth function 对于光滑函数是对称的
$$\nabla^2f(x)=\begin{pmatrix}\partial_1^2f(x)&\partial_1\partial_2f(x)&\partial_1\partial_3f(x)\\\partial_2\partial_1f(x)&\partial_2^2f(x)&\partial_2\partial_3f(x)\\\partial_3\partial_1f(x)&\partial_3\partial_2f(x)&\partial_3^2f(x)\end{pmatrix}$$

Approximation
$$f(x)=f(x-x_0)+x^T\nabla f(x-x_0)+\frac12x^T\nabla^2f(x-x_0)x+O\left(\left\|x-x_0\right\|^3\right)$$

Jacobian

The extension of the gradient to higher order.
$$f(x): \mathbb R^n \to \mathbb R^m $$
$$f'(x)=\frac{df}{dx^T}=\begin{pmatrix}\frac{\partial f_1}{\partial x_1}&\frac{\partial f_1}{\partial x_2}&\cdots&\frac{\partial f_1}{\partial x_n}\\\frac{\partial f_2}{\partial x_1}&\frac{\partial f_2}{\partial x_2}&\cdots&\frac{\partial f_2}{\partial x_n}\\\vdots&\vdots&\ddots&\vdots\\\frac{\partial f_m}{\partial x_1}&\frac{\partial f_m}{\partial x_2}&\cdots&\frac{\partial f_m}{\partial x_n}\end{pmatrix}$$

#### useful notation of differential
https://en.wikipedia.org/wiki/Matrix_calculus

$$\begin{aligned}
&dA=0 \\
&d(\alpha X)=\alpha(dX) \\
&d(AXB)=A(dX)B \\
&d(X+Y)=dX+dY \\
&d(X^\top)=(dX)^\top \\
&d(XY)=(dX)Y+X(dY) \\
&d\langle X,Y\rangle=\langle dX,Y\rangle+\langle X,dY\rangle \\
&d\biggl(\frac{X}{\phi}\biggr)=\frac{\phi dX-(d\phi)X}{\phi^{2}} \\
&d(tr(X)) = I \\
&df(g(x))=\frac{df}{dg}\cdot dg(x)
\end{aligned}$$

### 5. Convex Functions

Jensen's inequality
$$f(\theta x+(1-\theta)y)\leq\theta f(x)+(1-\theta)f(y)$$

Epigraph：上方图
$$\mathrm{epi}(f)=\{(x,y)\mid f(x)\leq y\}$$
convex function == convex epigraph

why convex functions?
- 凸函数有凸的次水平集
- 凸函数的性质相对容易保持
    - 拟凸函数的和不一定是凸的
- 凸函数任何局部最优解就是全局最优解
- 凸函数在局部极小值附近是局部凸的
- 凸函数的许多运算是保凸的：
    - 非负加权和
    - 仿射变换
    - 绝对值
    - 范数
    - 最大特征值
    - trace
    - 线性运算

#### convex functions property

- 凸函数在线性近似的上方
- 一阶导数为0 就是最优解（只对凸函数成立）
- 如果光滑函数对于任何X的hessian是半正定的，那么它是凸的
- 对于非凸函数，极小值点的hessian是半正定的
- The Hessian is a good local model of a smooth function

### 6. Unconstrained Optimization for Nonconvex Functions

#### Line search steepest gradient descent

### 7. Modified Damped Newton's Method


