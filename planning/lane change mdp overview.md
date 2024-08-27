# lane change mdp 逻辑梳理

函数入口是`PolicyEvaluation::Process()`

```cpp
void PolicyEvaluation::Process(const Environment& environment,
                               std::shared_ptr<LCRNode>& node) {
  Reset();
  ForwardSimulation(environment, node);
  BackTracking();
  FindBestTrajectory(node);
  FindLaneKeepTrajectory(node);
  FindFirstTwoBestActions(node);
  FindLongestTrajectory();
}
```

- `ForwardSimulation(environment, node);`负责根据环境和当前的node展开树结构。每个节点都有lane keep和lane change两个子节点（子节点需要满足无碰撞原则，否则在`ExpandNode`中会被排除）。根据不同语义执行动作，计算reward。
- `BackTracking();`内部`PolicyEvaluation::UpdateParentStateAndActionValue()`处理逻辑，从保存所有叶子节点开始遍历，计算叶子的动作价值，叶子父节点的状态价值。从底层开始，层序遍历动作价值和状态价值。
- `FindBestTrajectory(node);` 从根节点开始根据贪婪策略选择child node，选择最佳的子节点作为best child，加入best trajectory。