# KD tree

## 概述

KD树（K维树）是一种空间划分的数据结构，用于在K维空间中组织点。它是一种二叉树，每个节点代表一个K维点。KD树特别适用于范围搜索和最近邻搜索等应用，常用于2D或3D等多维空间。

## 构建

KD树的构建通过递归地在每次分割时选择一个维度进行分割。具体步骤如下：

1. **选择分割维度**：根据树的深度选择维度，维度在所有维度间循环。
2. **排序并选择中位数**：根据选择的维度对点进行排序，并选择中位数作为根节点，这样可以确保树的平衡性。
3. **递归构建子树**：将中位数两边的点分别递归构建左子树和右子树。

## 示例代码

以下是一个简单的KD树在Python中的实现示例：

```python
class Node:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

def build_kdtree(points, depth=0):
    if not points:
        return None

    k = len(points[0])  # 假设所有点具有相同的维度
    axis = depth % k

    points.sort(key=lambda x: x[axis])
    median = len(points) // 2

    return Node(
        point=points[median],
        left=build_kdtree(points[:median], depth + 1),
        right=build_kdtree(points[median + 1:], depth + 1)
    )

# 使用示例：
points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
kdtree = build_kdtree(points)
```

## 最近邻搜索
KD树允许高效的最近邻搜索。搜索过程涉及递归遍历树，从根节点开始。在每个节点，算法比较查询点与当前节点的分割维度的距离，并决定进入哪个子树。可能还需要回溯以检查其他子树是否有更近的点。

```python
def nearest_neighbor(root, point, depth=0, best=None):
    if root is None:
        return best

    k = len(point)
    axis = depth % k

    next_best = None
    next_branch = None

    if best is None or (point[axis] < root.point[axis]):
        next_best = root.point
        next_branch = root.left
    else:
        next_best = best
        next_branch = root.right

    best = nearest_neighbor(next_branch, point, depth + 1, next_best)

    if (point[axis] - root.point[axis]) ** 2 < distance(point, best):
        best = nearest_neighbor(root.left if next_branch == root.right else root.right, point, depth + 1, best)

    return best

def distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))
```

## 应用
最近邻搜索：在机器学习中（如KNN算法）、计算机图形学、机器人等领域非常有用。
范围搜索：高效查找指定范围内的所有点。
## 结论
KD树是一种处理多维数据的强大工具。通过其快速搜索能力，KD树在高维空间应用中大大减少了查询操作的复杂性，使得许多算法在实践中变得更为高效。