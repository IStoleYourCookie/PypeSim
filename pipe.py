import time
from os import system, name
import threading

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def wait_input(result, index):
    result[index] = input("New commands[0]: ")

def execute_code(code):
    try:
        exec(code)
    except Exception as e:
        print("Error:", e)

print("Hello World!")

class pipe:
    def __init__(self, volume, fluid, flowrate, position, connections):
        self.volume = volume
        self.fluid = fluid
        self.flowrate = flowrate
        self.position = position
        self.connections = connections

# example pipe system
pipes = [pipe(20, 20, 1, 3, [2]),
         pipe(20, 20, 1, 2, [2]),
         pipe(50, 0, 0, 1, [0])]

real_total_fluid = 0
for p in pipes:
    real_total_fluid += p.fluid

loop = True
toc = 0
first = True
commands = [None] * 100
scripts = [None] * 100
embeds = [None] * 100

while loop:

    # setting up input fuction in another thread to allow time.perf_counter to measure time while the program is waiting for input
    t1 = threading.Thread(target=wait_input, args=(commands, 0))
    t1.start()
    t1.join()

    if [0] != '':
        if len(commands[0]) > 0:

            print("a command was passed to the program")
            print(f"the command: {commands[0]}")

            # deifferent pre-defined commands to control different aspects of the simulation and the attributes of pipes
            if commands[0][0] == 'c':
                if commands[0][1] == 'v':
                    pipes[int(commands[0][2])].volume = int(input("new volume: "))

                elif commands[0][1] == 'f':
                    pipes[int(commands[0][2])].fluid = int(input("new fluid: "))

                elif commands[0][1] == 'F':
                    pipes[int(commands[0][2])].flowrate = int(input("new flowrate: "))

                elif commands[0][1] == 'p':
                    pipes[int(commands[0][2])].position = int(input("new position: "))

                elif commands[0][1] == 'c':
                    pipes[int(commands[0][2])].connections = input("new connections: ")

            # the user can input a multiline python script that is executed in the main thread, in the main process, so that the user has time to write a script
            # without having to worry about the simulation 

            elif commands[0][0] == 'e':
                lines = []
                num = 1
                while True:
                    line = input(f"{num}|  ")
                    if line:

                        if line == "^S":
                            s = input("script index to save to: ")
                            scrpits[int(s)] = '\n'.join(lines)

                        elif line == "^L":
                            s = input("script index to load from: ")
                            execute_code(scripts[int(s)])

                        elif line == "^E":
                            s = input("script index to save to: ")
                            embeds[int(s)] = '\n'.join(lines)

                        lines.append(line)
                        num += 1
                    else:
                        break
                user_code = '\n'.join(lines)
                execute_code(user_code)


    tic = time.perf_counter()
    if first == True:
        first = False
        toc = tic
    dtime = tic-toc

    total_fluid = 0
    i = 0

    # write as many '0' elements to each array as how many pipe objects are there; used for checking if the system has reached an equilibrium
    ofluid = []
    nfluid = []
    for o in range(0, len(pipes)):
        ofluid.append(0)
        nfluid.append(0)

    for e in embeds:
        execute_code(e)

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

                if p.flowrate > 0:
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

    # correcting errors !may be faulty at the moment because the missing fluid only gets added to the first pipe (usually the top-most one)!
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

