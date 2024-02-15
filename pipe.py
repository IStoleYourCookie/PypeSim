print("Hello World!")

class pipe:
    def __init__(self, volume, flowrate, position, connections):
        self.volume = volume
        self.flowrate = flowrate
        self.position = position
        self.connections = connections

pipes = [pipe(60, 1, 3, [2, 1]),
         pipe(60, 1, 2, [2, 3]),
         pipe(60, 1, 1, [3])]

