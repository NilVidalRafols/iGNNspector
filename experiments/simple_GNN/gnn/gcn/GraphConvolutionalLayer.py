import torch


class GraphConvolutionalLayer(torch.nn.Module):

    def __init__(self, input_size, output_size, activation=torch.nn.functional.relu, left_to_right=True):
        """
        A layer for a graph convolutional network.

        :param input_size: Output size of the previous layer, in the first layer this is the number of attributes in a
        node.
        :param output_size: Number of attributes to return, in the last layer this is the final output of the gcn.
        :param activation: An activation function for the layer.
        :param left_to_right: If True, the order of operations is (adj * x) * w, otherwise it is adj * (x * w).
        """
        super(GraphConvolutionalLayer, self).__init__()
        self.w = torch.nn.Parameter(torch.rand([input_size, output_size]))
        self.activation = activation
        self.left_to_right = left_to_right

    def forward(self, inputs):
        adj, x = inputs
        if self.left_to_right:
            adj_x = torch.mm(adj, x)
            adj_x_w = torch.mm(adj_x, self.w)
            return adj, self.activation(adj_x_w)
        else:
            x_w = torch.mm(x, self.w)
            adj_x_w = torch.mm(adj, x_w)
            return adj, self.activation(adj_x_w)
