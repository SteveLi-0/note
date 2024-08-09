import torch 
import torch.nn as nn

class MyBatchNorm2d(nn.Module):
    def __init__(self, num_features, eps=1e-5, momentum=0.1):
        super(MyBatchNorm2d, self).__init__()
        self.num_features = num_features
        self.eps = eps
        self.momentum = momentum

        self.gamma = nn.Parameter(torch.ones(num_features))
        self.beta = nn.Parameter(torch.zeros(num_features))

        self.register_buffer('moving_mean', torch.zeros(num_features))
        self.register_buffer('moving_var', torch.ones(num_features))

    def forward(self, x):
        if self.training:
            batch_mean = torch.mean(x, dim=(0, 2, 3))
            batch_var = torch.var(x, dim=(0, 2, 3))

            self.moving_mean = self.momentum * self.moving_mean + (1 - self.momentum) * batch_mean
            self.moving_var = self.momentum * self.moving_var + (1 - self.momentum) * batch_var

            x_normalized = (x - batch_mean[None, :, None, None]) / torch.sqrt(batch_var[None, :, None, None] + self.eps)
        else:
            x_normalized = (x - self.moving_mean[None, :, None, None]) / torch.sqrt(self.moving_var[None, :, None, None] + self.eps)

        return x_normalized * self.gamma[None, :, None, None] + self.beta[None, :, None, None]
    
if __name__ == "__main__":
    num_features = 3
    batch_size = 2
    height, width = 4, 4
    
    my_bn = MyBatchNorm2d(num_features)
    torch_bn = nn.BatchNorm2d(num_features)

    torch_bn.weight.data = my_bn.gamma.data.clone()
    torch_bn.bias.data = my_bn.beta.data.clone()

    torch_bn.running_mean.data = my_bn.moving_mean.data.clone()
    torch_bn.running_var.data = my_bn.moving_var.data.clone()

    x = torch.randn(batch_size, num_features, height, width)

    output_my_bn = my_bn(x)
    output_torch_bn = torch_bn(x)

    # 对比输出结果
    print("MyBatchNorm2d output:\n", output_my_bn)
    print("\nPyTorch BatchNorm2d output:\n", output_torch_bn)

    # 对比两个实现的输出差异
    diff = torch.abs(output_my_bn - output_torch_bn).sum().item()
    print("\nDifference between outputs:", diff)    