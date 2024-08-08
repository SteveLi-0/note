# lane change mdp + idm
## code 
- `PolicyEvaluation`
  - constructor: `PolicyEvaluation(policy_selection_environment, gamma);`
  - main: `void Process(environment, node);`
    - `Reset();`
    - `ForwardSimulation(environment, node);`
    - `BackTracking();`
    - `FindBestTrajectory(node);`
    - `FindLaneKeepTrajectory(node);`
    - `FindFirstTwoBestActions(node);`
    - `FindLongestTrajectory();`

### ForwardSimulation
该方法进行前向模拟，生成节点树。通过扩展节点来探索可能的动作和状态转移，将生成的子节点添加到队列中进行进一步扩展，直到所有可能的节点都被处理。

由于树的展开已经根据规则进行了剪枝，所以这里就用BFS进行扩展。

```cpp
auto front_node_children =
    policy_selection_environment_ptr_->ExpandNode(environment, front_node);
```

- 调用 `ExpandNode` 方法扩展当前节点，生成其子节点。
- `ExpandNode` 方法会根据当前节点的状态和环境，计算出可能的动作及其对应的子节点。

```cpp
if (front_node_children.empty()) {
  leaves_.emplace_back(*front_node);
  leaf_nodes_.emplace_back(front_node);
}
```
- 如果当前节点没有子节点（`front_node_children` 为空），则将其标记为叶子节点，添加到 `leaves_` 和 `leaf_nodes_ `容器中。

```cpp
for (const auto& child : front_node_children) {
  if (child->action.lc_type == LCRActionType::kLaneChange) {
    front_node->lc_child = child;
  } else {
    front_node->lk_child = child;
  }
  child->parent = front_node;
  node_que.emplace_back(child);
}
```
- 遍历当前节点(`front_node_children`)的所有子节点。
- 根据子节点的动作类型（车道保持或车道变更），将其添加到当前节点的 lc_child 或 lk_child。
- 设置子节点的父节点为当前节点。
- 将子节点添加到队列 node_que 中，以便进一步扩展。

#### ExpandNode
`PolicySelectionEnvironment::ExpandNode` 方法负责扩展给定的节点，生成其子节点集合。它根据当前节点的状态和环境，计算出可能的动作及其对应的子节点。
##### 更新代理状态
```cpp
agent_ptr_->UpdateState(*node);
```
将当前节点的状态更新到代理（`agent_ptr_`）中。
##### 获取当前车道的障碍物未来状态列表
```cpp
auto curr_rl_obs_states_list =
    (node->state.rl_info_type == ReferenceLineInfoType::kEgo)
        ? ego_lane_obs_future_states_
        : target_lane_obs_future_states_;
```
根据当前节点的参考线信息类型（`rl_info_type`），选择自车道或目标车道的障碍物未来状态列表。
```cpp
enum class ReferenceLineInfoType {
  kEgo,
  kTarget,
};
```
这个枚举类定义了两种不同的参考线信息类型：自车道（kEgo）和目标车道（kTarget）。
`node->state.rl_info_type` 在 `TakeAction` 方法中更新，如果当前节点为自车道，则其值为 kEgo；否则，其值为 kTarget。
###### 未来障碍物状态预测
纵向障碍物状态预测由IDM模型完成，横向没有变化。即，s状态根据加速度更新，l状态保持不变。

##### 检查节点与障碍物重叠
```cpp
if (HasNodeOverlapWithObsFutureStates(*node, curr_rl_obs_states_list)) {
  return {};
}
```
使用 `HasNodeOverlapWithObsFutureStates` 方法检查当前节点是否与障碍物未来状态重叠。如果重叠，则返回空的子节点集合。
##### 获取可执行的未来动作
```cpp
auto actions = agent_ptr_->GetAgentAvaliableFutureActions();
```
获取代理（`agent_ptr_`）可执行的未来动作集合。这些动作通常包括保持车道（`kLaneKeep`）和变更车道（`kLaneChange`）。
可以施加一些剪枝的策略，比如：策略切换次数的限制。纵向只能切换一次，横向最多切换两次。
##### 生成子节点集合
```cpp
std::vector<std::shared_ptr<LCRNode>> children;
for (auto action : actions) {
  std::shared_ptr<LCRNode> child = TakeAction(action, environment);
  if (child == nullptr) {
    continue;
  }

  if (!IsValidNode(*child)) {
    continue;
  }

  auto child_rl_obs_states_list =
      (child->state.rl_info_type == ReferenceLineInfoType::kEgo)
          ? ego_lane_obs_future_states_
          : target_lane_obs_future_states_;

  if (HasNodeOverlapWithObsFutureStates(*child, child_rl_obs_states_list)) {
    continue;
  }

  children.emplace_back(child);
}
```
遍历每个可执行动作，调用 `TakeAction` 方法生成对应的子节点。
如果 `TakeAction` 返回 `nullptr` 或生成的子节点无效（`IsValidNode` 返回 `false`），则跳过该子节点。
检查子节点是否与障碍物未来状态重叠，如果重叠，则跳过该子节点。
将生成的有效子节点添加到子节点集合 `children` 中。
###### TakeAction
`PolicySelectionEnvironment::TakeAction` 方法负责在给定的环境下，根据指定的动作生成下一个状态节点。它模拟自车在执行动作后的状态转移，并评估新状态的有效性和奖励。
- 更新 next_state：
  - level
  - lane change count / lane change type
- 根据 action 更新 rl
- 根据 action，rl 更新 状态
- 更新 reward
  - `CalculateStateTransitionReward(agent_ptr_->GetState(), *next_state);`
  - progress cost + lane change cost

##### 计算子节点的联合概率
```cpp
const size_t children_size = children.size();
double union_prob =
    (children_size > 0) ? static_cast<double>(1.0 / children_size) : 0.0;

std::for_each(children.begin(), children.end(), [&union_prob](auto& iter) {
  iter->action.prob = union_prob;
});
```
计算子节点的数量 `children_size`。
如果子节点集合不为空，则计算每个子节点的联合概率 `union_prob`（即 1 除以子节点数量），否则联合概率为 0。
遍历每个子节点，设置其动作的概率为 `union_prob`。
##### 返回子节点集合
```cpp
return children;
```

### BackTracking
```cpp
void PolicyEvaluation::BackTracking() {
  if (leaf_nodes_.empty()) {
    return;
  }

  UpdateParentStateAndActionValue();
}
```
此方法执行回溯更新，更新父节点的状态和值。如果没有叶子节点，则无需回溯。否则，调用 `UpdateParentStateAndActionValue` 方法更新父节点的状态和值。

`PolicyEvaluation::UpdateParentStateAndActionValue` 方法的主要功能是从叶子节点开始，递归地更新树中各节点的状态值和动作值。这是一个典型的从下往上更新的过程，用于策略评估中的值迭代。

#### 初始设置和叶子节点处理
- 初始化父节点队列：创建一个双端队列 parents，用于存储需要更新的父节点。
  - 遍历叶子节点：
  - 如果当前节点及其父节点不为空：
    - 计算当前节点的动作值 action_value，公式为：
    - ```cur_node->action_value = gamma_ * cur_node->state_value + cur_node->reward;```
    - 输出当前节点的动作值。
    - 更新父节点的状态值 state_value，公式为：
    - ```cur_node->parent->state_value += cur_node->action.prob * cur_node->action_value;```
    - 输出更新后的父节点状态值。
    - 标记当前节点为已更新。
    - 将父节点添加到 parents 队列中。
#### 更新父节点的状态值和动作值
- 处理队列中的父节点：
  - 当队列不为空时，取出队首节点 front_node。
  - 如果 front_node 为空或已更新，则跳过。
  - 如果 front_node 有父节点：
    - 计算 front_node 的动作值 action_value，公式为：
    - ```front_node->action_value = gamma_ * front_node->state_value + front_node->reward;```
    - 更新父节点的状态值 state_value，公式为：
    - ``` front_node->parent->state_value += front_node->action.prob * front_node->action_value;```
    - 输出更新后的父节点状态值。
    - 标记 front_node 为已更新。
    - 将父节点添加到 parents 队列中。
