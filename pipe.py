import time
from os import system, name
import threading

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def wait_input(command):
    command = input("New command: ")

print("Hello World!")

class pipe:
    def __init__(self, volume, fluid, flowrate, position, connections):
        self.volume = volume
        self.fluid = fluid
        self.flowrate = flowrate
        self.position = position
        self.connections = connections

pipes = [pipe(20, 20, 1, 2, [2]),
         pipe(20, 20, 1, 2, [2]),
         pipe(50, 0, 0, 1, [0])]

real_total_fluid = 0
for p in pipes:
    real_total_fluid += p.fluid

loop = True
toc = 0
first = True
command = ' '

while loop:

    # setting up input fuction in another thread to allow time.perf_counter to measure time while the program is waiting for input
    t1 = threading.Thread(target=wait_input, args=(command))
    t1.start()
    t1.join()

    if command[0] != '':
        if command[0] == 'c':
            if command[1] == 'v':
                pipes[command[2]].volume = input("new volume: ")

            elif command[1] == 'f':
                pipes[command[2]].fluid = input("new fluid: ")

            elif command[1] == 'F':
                pipes[command[2]].flowrate = input("new flowrate: ")

            elif command[1] == 'p':
                pipes[command[2]].position = input("new position: ")

            elif command[1] == 'c':
                pipes[command[2]].connections = input("new connections: ")

    tic = time.perf_counter()
    if first == True:
        first = False
        toc = tic
    dtime = tic-toc

    total_fluid = 0
    i = 0
    # this currently needs to be set up manually like so: write as many '0' elements to each array as many pipe objects are there
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

        # checking if the system has reached an equilibrium
        nfluid[i] = p.fluid
        num_equals = 0
        current_sum = 0

        for t in range(0, len(ofluid)):
            if ofluid[t] == nfluid[t]:
                num_equals += 1        

        i += 1

        total_fluid += p.fluid

    # correcting errors !may be faulty at the moments because the missing fluid only gets added to the first pipe (usually the top-most one)!
    fluid_error = real_total_fluid - total_fluid

    if num_equals == len(ofluid):
            print("nothing has changed")
            if fluid_error != 0:
                for t in pipes:
                   if t.fluid != 0:
                       t.fluid += fluid_error

    toc = time.perf_counter()

    # debug stuff
    clear()
    print(f"tic: {tic:0.4f} | toc: {toc:0.4f} | dtime: {dtime:0.4f}")
    for p in pipes:
        print(f"volume: {p.volume} | fluid: {p.fluid:0.4f} | flowrate: {p.flowrate} | position: {p.position} | connections: {p.connections}")
    print(f"total fluid in the system: {total_fluid:0.4f} | real total fluid in the system: {real_total_fluid:0.4f} | error in fluid calculations: {fluid_error:0.4f}")
    print("")

