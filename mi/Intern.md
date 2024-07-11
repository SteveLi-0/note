# Intern

## 1. 总览

1. 工作环境配置
2. 通过龙格库塔、双线性变换离散化状态方程，比较不同离散方法下的离散化误差
3. 通过casadi设置离散model
4. 比较linear 2dof model引入的近似误差
5. clang-tidy 代码检查
6. 排查bug：cnoa接管结束从新进入cnoa，仍然保持上次接管结束时的方向盘转角。
7. 如何将2dof err model的稳态误差加入mpc模型？
8. 上车调试的遇到的问题。
9. alm ilqr for control
10. mpc state中的delta的ref是否应该为0？
11. penalty ilqr for control？

## mpc的疑问
1. mpc的稳态误差因为什么产生？
2. incre mpc为什么可以消除稳态误差？
3. incre mpc为什么对延迟的鲁帮性不好？
4. lqr mpc和icre mpc的在实际场景中的优势劣势分别是那些？
5. 换道过程中ref的更新问题。
6. mpc预测的远端有鲁棒性保证吗？
7. 为什么说mpc是渐进稳定的？