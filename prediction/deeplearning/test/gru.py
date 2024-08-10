import torch
import torch.nn as nn

class MyGRU(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(MyGRU, self).__init__()
        self.hidden_size = hidden_size
        
        # Note: Input size should be input_size + hidden_size to match the concatenated tensor size
        self.W_z = nn.Linear(input_size + hidden_size, hidden_size)
        self.W_r = nn.Linear(input_size + hidden_size, hidden_size)
        self.W = nn.Linear(input_size + hidden_size, hidden_size)

    def forward(self, x, h_prev):
        combined = torch.cat((x, h_prev), dim=1)
        z_t = torch.sigmoid(self.W_z(combined))
        r_t = torch.sigmoid(self.W_r(combined))
        combined_r = torch.cat((x, r_t * h_prev), dim=1)
        h_tilde = torch.tanh(self.W(combined_r))
        h_t = (1 - z_t) * h_prev + z_t * h_tilde
        return h_t
    
if __name__ == "__main__":
    input_size = 5
    hidden_size = 3

    # Create PyTorch's built-in GRUCell
    pytorch_gru = nn.GRUCell(input_size, hidden_size)

    # Create custom GRU
    gru = MyGRU(input_size, hidden_size)

    # Manually copy weights from PyTorch GRUCell to custom GRU
    with torch.no_grad():
        gru.W_z.weight = torch.nn.Parameter(torch.cat([pytorch_gru.weight_ih[:, :input_size], pytorch_gru.weight_hh[:, :hidden_size]], dim=1))
        gru.W_r.weight = torch.nn.Parameter(torch.cat([pytorch_gru.weight_ih[:, input_size:2*input_size], pytorch_gru.weight_hh[:, hidden_size:2*hidden_size]], dim=1))
        gru.W.weight = torch.nn.Parameter(torch.cat([pytorch_gru.weight_ih[:, 2*input_size:], pytorch_gru.weight_hh[:, 2*hidden_size:]], dim=1))
        
        gru.W_z.bias = torch.nn.Parameter(pytorch_gru.bias_ih[:hidden_size] + pytorch_gru.bias_hh[:hidden_size])
        gru.W_r.bias = torch.nn.Parameter(pytorch_gru.bias_ih[hidden_size:2*hidden_size] + pytorch_gru.bias_hh[hidden_size:2*hidden_size])
        gru.W.bias = torch.nn.Parameter(pytorch_gru.bias_ih[2*hidden_size:] + pytorch_gru.bias_hh[2*hidden_size:])

    # Generate test input and initial hidden state
    x = torch.randn(1, input_size)
    h_prev = torch.zeros(1, hidden_size)

    # Get output from custom GRU
    custom_output = gru(x, h_prev)

    # Get output from PyTorch's GRUCell
    pytorch_output = pytorch_gru(x, h_prev)

    # Print results
    print("Custom GRU Output: ", custom_output)
    print("PyTorch GRU Output: ", pytorch_output)

    # Compare the results
    print("Difference: ", torch.abs(custom_output - pytorch_output).sum().item())
