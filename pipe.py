import time
from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

print("Hello World!")

class pipe:
    def __init__(self, volume, fluid, flowrate, position, connections):
        self.volume = volume
        self.fluid = fluid
        self.flowrate = flowrate
        self.position = position
        self.connections = connections

pipes = [pipe(60, 60, 1, 3, [1]),
         pipe(10, 0, 1, 2, [2]),
         pipe(10, 0, 0, 1, [0])]

loop = True
toc = 0
first = True

while loop:

    tic = time.perf_counter()
    if first == True:
        first = False
        toc = tic
    dtime = tic-toc

    for p in pipes:
        if p.fluid > 0:
            valid_cons = 0

            for d in p.connections:
                if pipes[d].fluid != pipes[d].volume:
                    valid_cons += 1

            p.fluid -= p.flowrate * valid_cons * dtime

        if p.fluid > p.volume:
            p.fluid = p.volume
        if p.fluid < 0:
            p.fluid = 0

        for c in p.connections:

            if pipes[c].position < p.position:
                
                pipes[c].fluid += p.flowrate * dtime

                if pipes[c].fluid > pipes[c].volume:
                    pipes[c].fluid = pipes[c].volume
                if pipes[c].fluid < 0:
                    pipes[c].fluid = 0

    toc = time.perf_counter()
    clear()
    print(f"tic: {tic:0.4f} | toc: {toc:0.4f} | dtime: {dtime:0.4f}")
    for p in pipes:
        print(f"volume: {p.volume} | fluid: {(p.fluid):0.4f} | flowrate: {p.flowrate} | position: {p.position} | connections: {p.connections}")
    print("")
    #command = input("New command: ")
