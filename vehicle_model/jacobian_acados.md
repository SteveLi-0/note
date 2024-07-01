# 使用acados计算jacobian

- 通过casadi实现

以二阶系统为例：

```
from casadi import SX, vertcat, Function, jacobian

# 定义状态变量和控制变量
x1 = SX.sym('x1')  # 定义符号变量 x1
x2 = SX.sym('x2')  # 定义符号变量 x2
u = SX.sym('u')    # 定义符号变量 u
x = vertcat(x1, x2)  # 将 x1 和 x2 垂直拼接成一个向量 x

# 定义动力学方程
f = vertcat(x2, -x1 + u)  # 动力学方程 f

# 创建CasADi函数
f_func = Function('f', [x, u], [f])  # 创建CasADi函数，名称为 'f'，输入为 [x, u]，输出为 [f]

# 计算Jacobian
J_fx = jacobian(f, x)  # 计算 f 对 x 的Jacobian矩阵
J_fu = jacobian(f, u)  # 计算 f 对 u 的Jacobian矩阵

# 创建Jacobian的CasADi函数
J_fx_func = Function('J_fx', [x, u], [J_fx])  # 创建Jacobian函数 J_fx，输入为 [x, u]，输出为 [J_fx]
J_fu_func = Function('J_fu', [x, u], [J_fu])  # 创建Jacobian函数 J_fu，输入为 [x, u]，输出为 [J_fu]

# 给定状态和控制输入
x_val = [1.0, 2.0]  # 具体的状态值
u_val = 0.5         # 具体的控制输入值

# 计算具体的Jacobian值
J_fx_val = J_fx_func(x_val, u_val)  # 计算在给定状态和控制输入下的 J_fx 值
J_fu_val = J_fu_func(x_val, u_val)  # 计算在给定状态和控制输入下的 J_fu 值

# 输出结果
print("Jacobian of f with respect to x at x={}, u={}:".format(x_val, u_val))
print(J_fx_val)

print("Jacobian of f with respect to u at x={}, u={}:".format(x_val, u_val))
print(J_fu_val)

```

以二阶系统rk4离散化为例

```
from casadi import SX, vertcat, Function, jacobian

# 定义状态变量和控制变量
x1 = SX.sym('x1')
x2 = SX.sym('x2')
u = SX.sym('u')
x = vertcat(x1, x2)

# 定义动力学方程
f = vertcat(x2, -x1 + u)

# 创建CasADi函数
f_func = Function('f', [x, u], [f])

# RK4离散化函数
def rk4_step(f, x, u, dt):
    k1 = f(x, u)
    k2 = f(x + dt/2 * k1, u)
    k3 = f(x + dt/2 * k2, u)
    k4 = f(x + dt * k3, u)
    x_next = x + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
    return x_next

# 离散化时间步长
dt = 0.1

# 定义RK4离散化后的状态更新方程
x_next = rk4_step(f_func, x, u, dt)

# 计算Jacobian矩阵
J_fx = jacobian(x_next, x)
J_fu = jacobian(x_next, u)

# 创建Jacobian的CasADi函数
J_fx_func = Function('J_fx', [x, u], [J_fx])
J_fu_func = Function('J_fu', [x, u], [J_fu])

# 给定状态和控制输入
x_val = [1.0, 2.0]
u_val = 0.5

# 计算具体的Jacobian值
J_fx_val = J_fx_func(x_val, u_val)
J_fu_val = J_fu_func(x_val, u_val)

# 输出结果
print("Jacobian of discrete f with respect to x at x={}, u={}:".format(x_val, u_val))
print(J_fx_val)

print("Jacobian of discrete f with respect to u at x={}, u={}:".format(x_val, u_val))
print(J_fu_val)

```