import torch

class prova(torch.nn.Module):
    def __init__(self):
        super(prova, self).__init__()
        self.add_module("neunet1", torch.nn.Linear(16, 8))
        self.add_module("neunet2", torch.nn.Linear(8, 4))

        name, layer = self.get_submodule("neunet1")
        print(name)
        print(layer)

prova()