import time
from os import system, name
import threading

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

command = None
def wait_input():
    command = input("New command: ")

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

real_total_fluid = 0
for p in pipes:
    real_total_fluid += p.fluid

loop = True
toc = 0
first = True

while loop:

    some = time.perf_counter()
    t1 = threading.Thread(target=wait_input, args=())
    t1.start()
    t1.join()
    some2 = time.perf_counter()
    dsome = some2-some
    tic = time.perf_counter()
    if first == True:
        first = False
        toc = tic - dsome
    dtime = tic-toc

    total_fluid = 0
    i = 0
    ofluid = [0, 0, 0]
    nfluid = [0, 0, 0]

    for p in pipes:
        ofluid[i] = p.fluid
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

        nfluid[i] = p.fluid
        num_equals = 0
        current_sum = 0

        for t in range(0, len(ofluid)):
            if ofluid[t] == nfluid[t]:
                num_equals += 1

            if num_equals == len(ofluid):
                for e in range(1, len(pipes)):
                    current_sum += pipes[-e].fluid
                    if pipes[-e].fluid != pipes[-e].volume:
                        if pipes[-e].fluid != 0:
                            fluid_error = real_total_fluid - current_sum
                            pipes[-e].fluid += fluid_error

        i += 1

        total_fluid += p.fluid

    toc = time.perf_counter()

    clear()
    print(f"tic: {tic:0.4f} | toc: {toc:0.4f} | dtime: {dtime:0.4f}")
    for p in pipes:
        print(f"volume: {p.volume} | fluid: {p.fluid:0.4f} | flowrate: {p.flowrate} | position: {p.position} | connections: {p.connections}")
    print(f"total fluid in the system: {total_fluid:0.4f} | real total fluid in the system: {real_total_fluid:0.4f}")
    print("")

    #command = input("New command: ")
