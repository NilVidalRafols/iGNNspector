from experiments.subclases import A

class B(A):
    def __init__(self):
        super(B, self).__init__()

    def abstract(self):
        self.b = 2