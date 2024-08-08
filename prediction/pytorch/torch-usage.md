## 随手记
### nn.Linear()
默认作用于最后一维度
### torch.bmm
对两个批矩阵做矩阵乘法
### .eval()
用于评估模式，在评估下dropout和batch norm行为会有不同。
- 训练模式：在训练模式下，Dropout 会随机丢弃一部分神经元，BatchNorm 会使用当前批次的均值和标准差进行标准化。
- 评估模式：在评估模式下，Dropout 层被禁用，所有神经元都会被激活。BatchNorm 会使用训练期间累积的全局均值和标准差。
- 调用位置：model.eval() 通常在模型评估和推理之前调用，以确保模型在推理期间的行为与训练期间有所区别。
- 还原模式：在模型评估完成后，如果需要继续训练模型，应调用 model.train() 将模型还原为训练模式。
## squeeze 和 unsqueeze 在深度学习中的常见用法

在深度学习中，张量操作是非常常见的任务。`squeeze` 和 `unsqueeze` 是两个重要的张量操作函数，用于调整张量的形状，以适应各种计算需求。以下将详细介绍这两个函数的作用及其在深度学习中的常见用法。

### 基本概念

- `unsqueeze(dim)`：在指定的维度 `dim` 插入一个大小为1的维度。
- `squeeze(dim=None)`：移除所有大小为1的维度，如果指定了 `dim`，则只移除该维度。

### 基本用法

#### unsqueeze
`unsqueeze` 的作用是增加一个新的维度，常用于准备数据以适应特定的网络层要求。

```python
import torch

# 定义一个 1D 张量
x = torch.tensor([1, 2, 3])
print("Original shape:", x.shape)  # 输出: torch.Size([3])

# 在第0维插入一个新的维度
y = x.unsqueeze(0)
print("After unsqueeze(0):", y.shape)  # 输出: torch.Size([1, 3])

# 在第1维插入一个新的维度
z = x.unsqueeze(1)
print("After unsqueeze(1):", z.shape)  # 输出: torch.Size([3, 1])
```
#### squeeze
`squeeze` 的作用是移除所有大小为1的维度，常用于简化数据形状以便于后续处理。

```python
# 定义一个包含多个大小为1的维度的张量
a = torch.tensor([[[1], [2], [3]]])
print("Original shape:", a.shape)  # 输出: torch.Size([1, 3, 1])

# 移除所有大小为1的维度
b = a.squeeze()
print("After squeeze:", b.shape)  # 输出: torch.Size([3])

# 仅移除第0维的大小为1的维度
c = a.squeeze(0)
print("After squeeze(0):", c.shape)  # 输出: torch.Size([3, 1])
```

### 深度学习中的常见用法
#### 准备数据
在处理图像数据时，卷积层通常期望输入的形状为 (batch_size, channels, height, width)。如果只有单个图像，可能需要用 unsqueeze 添加一个批次维度。

### 从单张图像转换回批次
在训练模型后，单张图像的预测结果可能具有多余的批次维度，可以使用 squeeze 移除。

```python
output = torch.randn(1, 10)  # 单张图像的输出 (1, num_classes)
output = output.squeeze(0)  # 移除批次维度 (num_classes)
```

### 与注意力机制结合
在实现注意力机制时，通常需要调整查询、键和值的形状，以进行广播求和。例如，加性注意力机制中，unsqueeze 和 squeeze 被用于调整张量形状。

```python
queries, keys = self.W_q(queries), self.W_k(keys)
features = queries.unsqueeze(2) + keys.unsqueeze(1)  # 广播求和
scores = self.w_v(features).squeeze(-1)  # 移除最后的单维度
```

### 总结
squeeze 和 unsqueeze 是两个非常重要的张量操作函数，广泛应用于深度学习模型的设计和数据处理过程中。通过掌握这两个函数的使用，可以更灵活地调整张量的形状，从而满足不同的计算需求。希望通过这篇教学，你能更好地理解和使用 squeeze 和 unsqueeze。

## 教学：深度学习中的广播机制

在深度学习中，处理不同形状的张量是常见的任务。广播机制（broadcasting）是一种强大的工具，它允许不同形状的张量在进行数学运算时自动扩展，使它们具有相同的形状，从而可以进行逐元素操作。以下将详细介绍广播机制的概念、规则及其在深度学习中的常见用法。

### 广播机制的基本概念

广播机制允许两个形状不同的张量进行逐元素运算，按照特定规则自动扩展较小的张量，使其形状与较大的张量兼容。

### 广播规则

1. 如果两个张量在某个维度上的长度不同，但其中一个张量在该维度上的长度为1，则该张量会沿着此维度复制其元素以匹配另一个张量的长度。
2. 如果两个张量在某个维度上的长度不同，且其中一个张量在该维度上的长度不为1，则无法进行广播，会引发错误。
3. 广播是从最后一个维度开始的，即从右向左匹配。

### 广播机制的示例

#### 示例 1：基本示例

```python
import torch

# 张量a的形状是 (2, 3, 1)
a = torch.tensor([[[1], [2], [3]], [[4], [5], [6]]])
# 张量b的形状是 (2, 1, 4)
b = torch.tensor([[[1, 2, 3, 4]], [[5, 6, 7, 8]]])

# 广播后的形状为 (2, 3, 4)
c = a + b
print(c)
```

在这个例子中：

a 的形状为 (2, 3, 1)，即在最后一个维度上只有一个元素。
b 的形状为 (2, 1, 4)，即在中间的维度上只有一个元素。
根据广播规则：

a 的最后一个维度将被扩展以匹配 b 的最后一个维度4。
b 的中间维度将被扩展以匹配 a 的中间维度3。
最终的结果形状为 (2, 3, 4)，对应位置的元素进行相加。

#### 示例 2：与标量的广播
```python
# 张量a的形状是 (3, 4)
a = torch.tensor([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
# 标量b
b = 10

# 广播后的形状为 (3, 4)
c = a + b
print(c)
```

### 深度学习中的常见用法
#### 批量处理
在处理批量数据时，通常需要将每个样本与同一个参数进行操作，可以使用广播机制。

```python
batch_size = 32
num_features = 10

# 批量数据的形状是 (batch_size, num_features)
data = torch.randn(batch_size, num_features)
# 参数的形状是 (num_features,)
params = torch.randn(num_features)

# 广播后的形状是 (batch_size, num_features)
result = data + params
print(result.shape)
```

#### 与注意力机制结合
在实现注意力机制时，通常需要调整查询、键和值的形状，以进行广播求和。

``` python
batch_size = 2
num_queries = 3
num_key_value_pairs = 4
num_hiddens = 5

# 初始化示例数据
queries = torch.randn(batch_size, num_queries, num_hiddens)
keys = torch.randn(batch_size, num_key_value_pairs, num_hiddens)

# 维度扩展后
queries_expanded = queries.unsqueeze(2)  # 形状: (batch_size, num_queries, 1, num_hiddens)
keys_expanded = keys.unsqueeze(1)        # 形状: (batch_size, 1, num_key_value_pairs, num_hiddens)

# 广播求和
features = queries_expanded + keys_expanded  # 形状: (batch_size, num_queries, num_key_value_pairs, num_hiddens)
print(features.shape)
```

### 总结
广播机制是深度学习中处理不同形状张量的强大工具。通过了解和掌握广播规则，可以更灵活地进行张量操作，简化代码并提升计算效率。希望通过这篇教学，你能更好地理解和使用广播机制。