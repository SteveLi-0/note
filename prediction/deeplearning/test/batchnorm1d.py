import torch
import torch.nn as nn

class MyBatchNorm(nn.Module):
    def __init__(self, num_features, eps=1e-5, momentum=0.1):
        super(MyBatchNorm, self).__init__()
        self.num_features = num_features
        self.eps = eps
        self.momentum = momentum

        self.gamma = nn.Parameter(torch.ones(num_features))
        self.bata = nn.Parameter(torch.zeros(num_features))

        self.register_buffer('running_mean', torch.zeros(num_features))
        self.register_buffer('running_var', torch.ones(num_features))

    def forward(self, x):
        if self.training:
            batch_mean = x.mean(dim=0)
            batch_var = x.var(dim=0, unbiased=False)
            self.running_mean = self.momentum * batch_mean + (1 - self.momentum) * self.running_mean
            self.running_var = self.momentum * batch_var + (1 - self.momentum) * self.running_var
            x_norm = (x - batch_mean) / torch.sqrt(batch_var + self.eps)
        else:
            x_norm = (x - self.running_mean) / torch.sqrt(self.running_var + self.eps)
        out = self.gamma * x_norm + self.bata
        return out
    
if __name__ == "__main__":
    num_features = 10
    batch_size = 5
    my_bn = MyBatchNorm(num_features)
    torch_bn = nn.BatchNorm1d(num_features)

    x = torch.randn(batch_size, num_features)

    torch_bn.weight.data = my_bn.gamma.data.clone()
    torch_bn.bias.data = my_bn.bata.data.clone()

    torch_bn.running_mean = my_bn.running_mean.clone()
    torch_bn.running_var = my_bn.running_var.clone()

    output_my_bn = my_bn(x)
    output_torch_bn = torch_bn(x)

    # 对比输出结果
    print("MyBatchNorm1d output:\n", output_my_bn)
    print("\nPyTorch BatchNorm1d output:\n", output_torch_bn)

    # 对比两个实现的输出差异
    diff = torch.abs(output_my_bn - output_torch_bn).sum().item()
    print("\nDifference between outputs:", diff)