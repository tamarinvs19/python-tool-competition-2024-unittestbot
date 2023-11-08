class Example:
    def __init__(self, x: int):
        self.x = x

    def f(self):
        if self.x > 0:
            return self.x
        return self.x - 100

    def g(self, x: int):
        if x > self.x:
            return x
        elif x < self.x:
            return self.x
        return 0
