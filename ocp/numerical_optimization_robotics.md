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

definition

examples

### 4. hign order info of functions

Function

Gradient

Hessian

Approx at zero

Jacobian

#### useful notation of differential
https://en.wikipedia.org/wiki/Matrix_calculus

### 5. Convex Functions

Jensen's inequality

Epigraph 

why convex functions?

#### convex functions property

### 6. Unconstrained Optimization for Nonconvex Functions

#### Line search steepest gradient descent

### 7. Modified Damped Newton's Method


