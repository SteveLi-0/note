# notes for contingency planning
## 1. Comprehensive Reactive Safety:No Need For A Trajectory If You Have A Strategy
## 2. MARC: Multipolicy and Risk-Aware ContingencyPlanning for Autonomous Driving
baseline 是 EPSILON
### 2.1 Introdution
**challenges**
- Imperfect Observation: Autonomous vehicles cannot always perfectly observe their surroundings, leading to uncertainty.
- Multimodal Intentions: The intentions of various road users are inherently multimodal and cannot be directly observed.
- False Estimations: Incorrectly estimating the purpose of other road users can cause the autonomous vehicle to behave in an overly cautious or hazardous manner, jeopardizing traffic safety.
  
**related work**
- POMDP:
  - Pros:
    - Mathematically rigorous and theoretically sound.
    - Capable of handling a variety of stochastic scenarios.
  - Cons:
    - **Computationally** intractable as the size of the problem increases.
    - Simplifies the decision-making process, making it hard to handle the multi-modality of real-world interactions.
- Multipolicy-based Pipelines:
  - How they work: These methods decompose the problem into **a limited number of closed-loop policy evaluations, leveraging domain-specific semantic-level policies (like lane-keeping and lane-changing) to approximate the action space**.
  - Pros:
    - Reduces computational complexity by focusing on a smaller subset of possible future evolutions.
  - Cons:
    - Typically designed to generate the best policy over all possible future evolutions.
    - The whole system may struggle to exploit the multi-modality of decision-making due to **the limitation of accounting for a single selected scenario.**
- Contingency Planning:
  - How they work: This involves generating plans for multiple possible futures in the motion planning layers, often formulated as a numerical optimization problem with a tree-structured trajectory to handle environmental uncertainties.
  - Pros:
    - Properly handles uncertainties by optimizing for various potential hazards.
  - Cons:
    - **Limited ability to handle interactions** with many surrounding agents.
    - **High assumptions on the upper-stream modules** can lead to poor integration into the autonomous driving stack.
- MARC:
  - How it works: behavioral planning + motion planning. 
    - Critical scenario sets conditioned on semantic-level policies. 
    - Dynamic branchpoint-based tree-structured representation.
    - Risk-aware contingency planning.
    - Bi-level optimization algorithm that considers multiple future scenarios and user-defined risk tolerance levels.
  - Pros:
    - Efficiently integrates behavior and motion planning.
    - Handles multimodal decision-making effectively.
    - Demonstrates superior performance in various environments according to experimental results.
  - Cons:
    - Complexity in implementation and potential computational demands.
    - **Requires extensive simulations and validations** to ensure robustness across diverse scenarios.
### 2.2 Policy-Conditioned Scenario Tree(PCST)
- tree-structured representation
- dynamic branchpoint-based structure
- forward reachability sets based method + fallback instead of hand defined controller
## 3. RACP:Risk-Aware Contingency Planning with Multi-Modal Predictions
利用 bayesian beliefs 处理多模态预测，防御性规划策略采用 frenet 下横纵采样，branch 时间、数量固定。
他的cost由于分叉时间固定，那么估计出的modal可能由于时间推移就不存在了。
再上贝叶斯的估计模型可能效果不好。
contingency的关键在于分叉时间和风险感知，对于multi modal处理准确，分叉时间就能较好的确定了，对于multi modal的场景，如何感知风险作出规划？
$$\arg\min_{\tau}J_{\mathrm{shared}}(\tau_{0:t_{b}})+\sum_{\lambda\in\Lambda}p(\lambda)J_{\mathrm{conting}}(\tau_{t_{b}:T},\lambda)\\\mathrm{s.t.}\quad g_{j}(\tau)\leq b_{j},\quad j=1,...,n$$
## 4. LookOut: Diverse Multi-Future Prediction and Planning for Self-Driving
