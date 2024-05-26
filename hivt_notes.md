# HiVT 笔记

## 1. 代码详解

### 1.1 数据处理

argoverse v1.1 trajectory forecasting dataset 的数据格式是 

- TIMESTAMP 时间戳 采样频率10Hz，总长度5s，预测一般采用2s的数据预测未来3s的轨迹
- TRACK_ID 跟踪ID 每个对象的唯一ID
- OBJECT_TYPE 目标类别 自车AV、其他车AGENT、其他对象OTHERS
- X, Y 坐标
- CITY_NAME 城市 迈阿密和底特律

处理argoverse数据，包括agent和lane数据

处理agent数据

```python
def process_argoverse(split: str, raw_path: str, am: ArgoverseMap, radius: float) -> Dict:
    df = pd.read_csv(raw_path)

    # filter out actors that are unseen during the historical time steps
    # 历史轨迹20个样本点进行预测
    # hivt只预测av和agents
    timestamps = list(np.sort(df['TIMESTAMP'].unique()))
    historical_timestamps = timestamps[: 20]
    historical_df = df[df['TIMESTAMP'].isin(historical_timestamps)]
    actor_ids = list(historical_df['TRACK_ID'].unique())
    df = df[df['TRACK_ID'].isin(actor_ids)]
    num_nodes = len(actor_ids)

    av_df = df[df['OBJECT_TYPE'] == 'AV'].iloc
    av_index = actor_ids.index(av_df[0]['TRACK_ID'])
    agent_df = df[df['OBJECT_TYPE'] == 'AGENT'].iloc
    agent_index = actor_ids.index(agent_df[0]['TRACK_ID'])
    city = df['CITY_NAME'].values[0]

    # make the scene centered at AV
    # 计算第二秒末作为原点，计算theta和旋转矩阵
    # 这个操作其实是不需要的
    # hivt是旋转不变的
    origin = torch.tensor([av_df[19]['X'], av_df[19]['Y']], dtype=torch.float)
    av_heading_vector = origin - torch.tensor([av_df[18]['X'], av_df[18]['Y']], dtype=torch.float)
    theta = torch.atan2(av_heading_vector[1], av_heading_vector[0])
    rotate_mat = torch.tensor([[torch.cos(theta), -torch.sin(theta)],
                               [torch.sin(theta), torch.cos(theta)]])

    # initialization
    # x - nodes的xy
    # edge_index - nodes之间的边。permutations构建排列
    # padding_mask - agent在时间上的有效性
    # bos_mask - 
    # rotate_angles - agent的旋转角度
    x = torch.zeros(num_nodes, 50, 2, dtype=torch.float)
    edge_index = torch.LongTensor(list(permutations(range(num_nodes), 2))).t().contiguous()
    padding_mask = torch.ones(num_nodes, 50, dtype=torch.bool)
    bos_mask = torch.zeros(num_nodes, 20, dtype=torch.bool)
    rotate_angles = torch.zeros(num_nodes, dtype=torch.float)

    # df.groupby('TRACK_ID') 按照 TRACK_ID 对df分类
    # actor_id 某个 TRACK_ID actor_df 是 TRACK_ID 的df
    for actor_id, actor_df in df.groupby('TRACK_ID'):
        # node_idx 在 actor ids 中的 index 0 - num_node-1
        # node_steps 在 timestamps 中的 index 0 - 49
       	# padding_mask 初始化均为 True ，T 代表无效，需要padding
        # 出现的位置改 false，F 代表有效，不需要 padding
        node_idx = actor_ids.index(actor_id)
        node_steps = [timestamps.index(timestamp) for timestamp in actor_df['TIMESTAMP']]
        padding_mask[node_idx, node_steps] = False
        # 如果当前时刻 index == 19 不存在（True），后面就没必要预测了，这些时间步将被填充，不做预测
        if padding_mask[node_idx, 19]:  # make no predictions for actors that are unseen at the current time step
            padding_mask[node_idx, 20:] = True
        # 当前agent的xy转换成tensor
        xy = torch.from_numpy(np.stack([actor_df['X'].values, actor_df['Y'].values], axis=-1)).float()
        x[node_idx, node_steps] = torch.matmul(xy - origin, rotate_mat)
        # 历史index，计算theta，如果index数量小于2，不预测
        node_historical_steps = list(filter(lambda node_step: node_step < 20, node_steps))
        if len(node_historical_steps) > 1:  # calculate the heading of the actor (approximately)
            heading_vector = x[node_idx, node_historical_steps[-1]] - x[node_idx, node_historical_steps[-2]]
            rotate_angles[node_idx] = torch.atan2(heading_vector[1], heading_vector[0])
        else:  # make no predictions for the actor if the number of valid time steps is less than 2
            padding_mask[node_idx, 20:] = True

    # bos_mask is True if time step t is valid and time step t-1 is invalid
    # 如果padding_mask t 有效 t - 1 无效，bos_mask = T
    bos_mask[:, 0] = ~padding_mask[:, 0]
    bos_mask[:, 1: 20] = padding_mask[:, : 19] & ~padding_mask[:, 1: 20]

    # 预测原始位置
    # x - [num nodes, timestamps, 2(xy)]
    positions = x.clone()
    # 平移不变
    # 未来轨迹，相对当前时刻增量
    x[:, 20:] = torch.where((padding_mask[:, 19].unsqueeze(-1) | padding_mask[:, 20:]).unsqueeze(-1),
                            torch.zeros(num_nodes, 30, 2),
                            x[:, 20:] - x[:, 19].unsqueeze(-2))
    # 历史轨迹，相邻时刻增量
    x[:, 1: 20] = torch.where((padding_mask[:, : 19] | padding_mask[:, 1: 20]).unsqueeze(-1),
                              torch.zeros(num_nodes, 19, 2),
                              x[:, 1: 20] - x[:, : 19])
    x[:, 0] = torch.zeros(num_nodes, 2)

    # get lane features at the current time step
    # 当前时刻的输入，获得lane feature
    df_19 = df[df['TIMESTAMP'] == timestamps[19]]
    node_inds_19 = [actor_ids.index(actor_id) for actor_id in df_19['TRACK_ID']]
    node_positions_19 = torch.from_numpy(np.stack([df_19['X'].values, df_19['Y'].values], axis=-1)).float()
    (lane_vectors, is_intersections, turn_directions, traffic_controls, lane_actor_index,
     lane_actor_vectors) = get_lane_features(am, node_inds_19, node_positions_19, origin, rotate_mat, city, radius)

    y = None if split == 'test' else x[:, 20:]
    seq_id = os.path.splitext(os.path.basename(raw_path))[0]

    return {
        'x': x[:, : 20],  # [N, 20, 2]
        'positions': positions,  # [N, 50, 2]
        'edge_index': edge_index,  # [2, N x N - 1]
        'y': y,  # [N, 30, 2]
        'num_nodes': num_nodes,
        'padding_mask': padding_mask,  # [N, 50]
        'bos_mask': bos_mask,  # [N, 20]
        'rotate_angles': rotate_angles,  # [N]
        'lane_vectors': lane_vectors,  # [L, 2]
        'is_intersections': is_intersections,  # [L]
        'turn_directions': turn_directions,  # [L]
        'traffic_controls': traffic_controls,  # [L]
        'lane_actor_index': lane_actor_index,  # [2, E_{A-L}]
        'lane_actor_vectors': lane_actor_vectors,  # [E_{A-L}, 2]
        'seq_id': int(seq_id),
        'av_index': av_index,
        'agent_index': agent_index,
        'city': city,
        'origin': origin.unsqueeze(0),
        'theta': theta,
    }
```

处理lane数据

- 输入
  - `am`：ArgoverseMap 对象，用于访问地图数据。
  - `node_inds`：节点的索引列表。
  - `node_positions`：节点的位置张量，形状为 `[num_nodes, 2]`。
  - `origin`：原点坐标张量，形状为 `[2]`。
  - `rotate_mat`：旋转矩阵，形状为 `[2, 2]`。
  - `city`：字符串，表示城市名称。
  - `radius`：浮点数，表示搜索半径。

```python
def get_lane_features(am: ArgoverseMap, node_inds: List[int], node_positions: torch.Tensor, origin: torch.Tensor, rotate_mat: torch.Tensor, city: str, radius: float) 
-> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    # 初始化
    lane_positions, lane_vectors, is_intersections, turn_directions, traffic_controls = [], [], [], [], []
    lane_ids = set()
    # 遍历每个node位置
    # 根据node位置、城市、半径 获得车道id -> lane_ids
    for node_position in node_positions:
        lane_ids.update(am.get_lane_ids_in_xy_bbox(node_position[0], node_position[1], city, radius))
    # 每个node位置 转换到原点
    node_positions = torch.matmul(node_positions - origin, rotate_mat).float()
    # 遍历 lane id 
    for lane_id in lane_ids:
        # 获取车道的中心线，并将其坐标转换为张量。对中心线坐标进行平移和旋转变换。
        lane_centerline = torch.from_numpy(am.get_lane_segment_centerline(lane_id, city)[:, : 2]).float()
        lane_centerline = torch.matmul(lane_centerline - origin, rotate_mat)
        # 获取该车道是否在交叉口内的信息。
        is_intersection = am.lane_is_in_intersection(lane_id, city)
        # 获取该车道的转向方向信息。
        turn_direction = am.get_lane_turn_direction(lane_id, city)
        # 获取该车道是否有交通控制措施的信息。
        traffic_control = am.lane_has_traffic_control_measure(lane_id, city)
        # 将变换后的中心线的所有点（除了最后一个点）添加到 lane_positions 列表中。
        lane_positions.append(lane_centerline[:-1])
        # 计算中心线各点之间的向量，并添加到 lane_vectors 列表中。
        lane_vectors.append(lane_centerline[1:] - lane_centerline[:-1])
        # 记录每段中心线是否在交叉口的信息
        count = len(lane_centerline) - 1
        is_intersections.append(is_intersection * torch.ones(count, dtype=torch.uint8))
        if turn_direction == 'NONE':
            turn_direction = 0
        elif turn_direction == 'LEFT':
            turn_direction = 1
        elif turn_direction == 'RIGHT':
            turn_direction = 2
        else:
            raise ValueError('turn direction is not valid')
        # 将转向方向编码为整数，并记录每段中心线的转向方向。
        turn_directions.append(turn_direction * torch.ones(count, dtype=torch.uint8))
       	# 记录每段中心线是否有交通控制措施。
        traffic_controls.append(traffic_control * torch.ones(count, dtype=torch.uint8))
    lane_positions = torch.cat(lane_positions, dim=0)
    lane_vectors = torch.cat(lane_vectors, dim=0)
    is_intersections = torch.cat(is_intersections, dim=0)
    turn_directions = torch.cat(turn_directions, dim=0)
    traffic_controls = torch.cat(traffic_controls, dim=0)

	# A-L features
    # 车道段index和节点index的笛卡尔积
    lane_actor_index = torch.LongTensor(list(product(torch.arange(lane_vectors.size(0)), node_inds))).t().contiguous()
    # 每个车道段位置和每个节点位置之间的向量差
    # lane_positions 张量在第0维度上进行重复插值 node_positions 张量在第0维度上重复 num_lane_segments 次
    lane_actor_vectors = \
        lane_positions.repeat_interleave(len(node_inds), dim=0) - node_positions.repeat(lane_vectors.size(0), 1)
    # 半径小于radius mask false
    mask = torch.norm(lane_actor_vectors, p=2, dim=-1) < radius
    lane_actor_index = lane_actor_index[:, mask]
    lane_actor_vectors = lane_actor_vectors[mask]

    return lane_vectors, is_intersections, turn_directions, traffic_controls, lane_actor_index, lane_actor_vectors
```



