# notes for contingency planning
## 1. Comprehensive Reactive Safety:No Need For A Trajectory If You Have A Strategy
## 2. MARC: Multipolicy and Risk-Aware ContingencyPlanning for Autonomous Driving
baseline 是 EPSILON

## 3. RACP:Risk-Aware Contingency Planning with Multi-Modal Predictions
利用 bayesian beliefs 处理多模态预测，防御性规划策略采用 frenet 下横纵采样，branch 时间、数量固定。
他的cost由于分叉时间固定，那么估计出的modal可能由于时间推移就不存在了。
再上贝叶斯的估计模型可能效果不好。
contingency的关键在于分叉时间和风险感知，对于multi modal处理准确，分叉时间就能较好的确定了，对于multi modal的场景，如何感知风险作出规划？
$$\arg\min_{\tau}J_{\mathrm{shared}}(\tau_{0:t_{b}})+\sum_{\lambda\in\Lambda}p(\lambda)J_{\mathrm{conting}}(\tau_{t_{b}:T},\lambda)\\\mathrm{s.t.}\quad g_{j}(\tau)\leq b_{j},\quad j=1,...,n$$
## 4. LookOut: Diverse Multi-Future Prediction and Planning for Self-Driving
