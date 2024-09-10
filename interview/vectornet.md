# vectornet 
## 1. 数据处理

1. 获取场景信息：

- 使用 get_scenario_map 和 ScenarioMapping 创建场景映射对象；
- 使用 NuPlanScenarioBuilder 构建场景生成器对象，所需参数包括数据路径、地图路径、传感器根路径、数据库文件、地图版本和场景映射；
- 使用 ScenarioFilter 和 get_filter_parameters 过滤需要的场景；
- 启用 SingleMachineParallelExecutor 并行处理以提高处理速度；
- 使用场景生成器和执行过滤器来获取符合条件的场景。

2. 将所有信息转换到统一坐标系：

- 为确保网络输入输出的一致性，需要将 Agent 和 Lane 的信息都旋转到自车坐标系中进行处理。
- NuPlan 提供了相应的工具，可参考 /nuplan/planning/training/preprocessing/features/trajectory_utils.py。
- 使用 convert_absolute_to_relative_poses 函数将绝对坐标转换为相对坐标。

3. 构建向量图输入：

- VectorNet 需要向量形式的输入，包括向量的起点、终点坐标以及类别信息，并将所有交通参与者和地图信息合成一个大 Tensor 输入。

4. 生成输入数据的序列格式：

- 输出为 Agent 的未来轨迹，采用增量的形式记录轨迹点，如 [Δx, Δy] 序列，以减少网络负担并保证输出轨迹的精确性。

TODO：embedding 第一个元素是增量的吗？x和y都是增量的吗？

5. 轨迹编码细节
- nuplan api 能获得ego和agent过去和未来轨迹数据。
- 对特征进行表征是不是增量的。
- 每个轨迹都属于一个子图。
- 在轨迹编码中，有一个map记录了每个子图的开始结束的index。
- 对ground truth编码过程中，x0是历史的最后一个状态，在x0基础上增量编码。gt只有xy两个量。
```python
# create an empty trajectory subgraph
# each node is a 1 * 8 tensor 
# [start_x, start_y, end_x, end_y, x, x, x, subgraph_ID]
# agent type is one hot encoded
trajectory_subgraph = np.empty((0, 8))
agent_subgraph = np.hstack((
            agent[ :-1, 0].reshape(-1, 1),    
            agent[ :-1, 1].reshape(-1, 1),     
            agent[1:  , 0].reshape(-1, 1),
            agent[1:  , 1].reshape(-1, 1),  
            np.zeros((len(agent) - 1, 1)),
            np.zeros((len(agent) - 1, 1)), 
            np.zeros((len(agent) - 1, 1)),  
            np.ones ((len(agent) - 1, 1)) * subgraph_ID            
        ))
```

6. 地图编码细节
- 地图有`crosswalks`,`rount lanes`两种。
- 地图按照轨迹过去方式编码。
- 最后的feature是轨迹子图和地图子图拼在一起。
TODO：地图增量表达？
TODO：多少秒历史预测多少秒未来？