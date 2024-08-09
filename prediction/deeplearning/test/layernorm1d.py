import torch
import torch.nn as nn

class LayerNorm1D(nn.Module):
    def __init__(self, normalized_shape, eps=1e-5):
        super(LayerNorm1D, self).__init__()
        self.eps = eps

        self.gamma = nn.Parameter(torch.ones(normalized_shape))
        self.beta = nn.Parameter(torch.zeros(normalized_shape))
    
    def forward(self, x):
        mean = x.mean(dim=-1, keepdim=True)
        var = x.var(dim=-1, keepdim=True, unbiased=False)

        x_normalized = (x - mean) / (torch.sqrt(var + self.eps))

        return self.gamma * x_normalized + self.beta
    
if __name__ == '__main__':
    batch_size = 2
    seq_len = 3
    feature_size = 4

    my_ln = LayerNorm1D(feature_size)
    torch_ln = nn.LayerNorm(feature_size)

    x = torch.randn(batch_size, seq_len, feature_size)

    torch_ln.weight.data = my_ln.gamma.data.clone()
    torch_ln.bias.data = my_ln.beta.data.clone()

    # 前向传播
    output_my_ln = my_ln(x)
    output_torch_ln = torch_ln(x)

    # 对比输出结果
    print("MyLayerNorm output:\n", output_my_ln)
    print("\nPyTorch LayerNorm output:\n", output_torch_ln)

    # 对比两个实现的输出差异
    diff = torch.abs(output_my_ln - output_torch_ln).sum().item()
    print("\nDifference between outputs:", diff)