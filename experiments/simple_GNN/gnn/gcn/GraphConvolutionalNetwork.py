import torch


class GraphConvolutionalNetwork(torch.nn.Module):

    def __init__(self, *layers):
        super(GraphConvolutionalNetwork, self).__init__()
        self.layers = torch.nn.Sequential(*layers)

    def forward(self, inputs):
        _, x = self.layers(inputs)
        return x
