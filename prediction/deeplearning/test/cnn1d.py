import torch
import torch.nn as nn

class MyConv1d:
    def __init__(self, in_channels, out_channels, kernel_size, stride = 1, padding = 0):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.weight = torch.randn(out_channels, in_channels, kernel_size)
        self.bias = torch.randn(out_channels)
    
    def forward(self, x):
        batch_size, in_channels, length = x.shape
        out_length = (length + 2 * self.padding - self.kernel_size) // self.stride + 1
        output = torch.zeros(batch_size, self.out_channels, out_length)

        for i in range(out_length):
            start = i * self.stride
            end = start + self.kernel_size

            output[:, :, i] = torch.sum(
                x[:, :, start:end].unsqueeze(1) * self.weight, dim=(2,3)
            ) + self.bias

        return output
        
if __name__ == "__main__":
    in_channels = 3
    out_channels = 2
    kernel_size = 3
    stride = 1
    padding = 0

    x = torch.randn(1, in_channels, 10)
    my_conv1d = MyConv1d(in_channels, out_channels, kernel_size, stride, padding)
    my_output = my_conv1d.forward(x)

    torch_conv1d = nn.Conv1d(in_channels, out_channels, kernel_size, stride, padding)
    torch_conv1d.weight.data = my_conv1d.weight.data.clone()
    torch_conv1d.bias.data = my_conv1d.bias.data.clone()

    torch_output = torch_conv1d(x)

    # 打印两个输出并比较
    print("MyConv1d Output:\n", my_output)
    print("Torch Conv1d Output:\n", torch_output)
    print("Difference:\n", torch.abs(my_output - torch_output).sum())