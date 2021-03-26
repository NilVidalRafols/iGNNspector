import torch


class PyG_gcn(torch.nn.Module):
    def __init__(self, layers):
        super(PyG_gcn, self).__init__()
        for layer in layers:
            self.add_module(layer[0], layer[1])
        
    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        layers = list(self.named_children())
        for _, layer in layers:
            x = layer(x, edge_index)
            if layer != layers[-1]:
                x = torch.nn.functional.relu(x)
                x = torch.nn.functional.dropout(x, training=self.training)

        return torch.nn.functional.log_softmax(x, dim=1)


class simple_PyG_gcn(torch.nn.Module):
    def __init__(self, layers):
        super(simple_PyG_gcn, self).__init__()
        for layer in layers:
            self.add_module(layer[0], layer[1])

    def forward(self, data):
        x, edge_index, adj_t = data.x, data.edge_index, data.adj_t

        layers = list(self.named_children())
        for _, layer in layers:
            if isinstance(layer, simple_gcn_layer):
                _, x = layer((adj_t.to_dense(), x))
            else:
                x = layer(x, edge_index)

            if layer != layers[-1]:
                x = torch.nn.functional.relu(x)
                x = torch.nn.functional.dropout(x, training=self.training)

        return torch.nn.functional.log_softmax(x, dim=1)


class simple_gcn_layer(torch.nn.Module):
    def __init__(self, input_size, output_size, left_to_right=True):
        """
        A layer for a graph convolutional network.

        :param input_size: Output size of the previous layer, in the first layer this is the number of attributes in a
        node.
        :param output_size: Number of attributes to return, in the last layer this is the final output of the gcn.
        :param activation: An activation function for the layer.
        :param left_to_right: If True, the order of operations is (adj * x) * w, otherwise it is adj * (x * w).
        """
        super(simple_gcn_layer, self).__init__()
        self.w = torch.nn.Parameter(torch.rand([input_size, output_size]))
        self.left_to_right = left_to_right

    def forward(self, inputs):
        adj, x = inputs
        if self.left_to_right:
            adj_x = torch.mm(adj, x)
            adj_x_w = torch.mm(adj_x, self.w)
            return adj, adj_x_w
        else:
            x_w = torch.mm(x, self.w)
            adj_x_w = torch.mm(adj, x_w)
            return adj, adj_x_w


class simple_gcn(torch.nn.Module):

    def __init__(self, *layers):
        super(simple_gcn, self).__init__()
        self.layers = torch.nn.Sequential(*layers)

    def forward(self, data):
        _, x = self.layers((data.adj_t.to_dense(), data.x))
        x = torch.nn.functional.relu(x)
        return x
