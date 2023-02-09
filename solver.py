# CMPT 317: Simple solver for testing purposes with local search


import math
import sys
import time
import blockTiling as P
import localsearch as search


# process the command line
if len(sys.argv) != 4:
    print('Usage: python', sys.argv[0], '<filename> <RG,RS,HC,HCLR,HCFR> <num_steps>')
    sys.exit()


file = open(sys.argv[1], 'r')
line = file.readline()
blocks = {}
N = int(line)
line = file.readline()

while line:
    line = line.rstrip().split()
    blocks[line[0]] = int(line[1])
    line = file.readline()

    
file.close()

algorithm = sys.argv[2]    
steps = int(sys.argv[3])

theProblem = P.Problem(N, blocks)

print()
print("----")
print("Running", sys.argv)
print("----")

if algorithm == 'RG':
    start = time.perf_counter()
    solution = search.random_guessing(theProblem, steps)
    end = time.perf_counter()
elif algorithm == 'RS':
    start = time.perf_counter()
    solution = search.random_search(theProblem, steps)
    end = time.perf_counter()
elif algorithm == 'HC':
    start = time.perf_counter()
    solution = search.hillclimbing(theProblem, steps)
    end = time.perf_counter()
elif algorithm == 'HCLR':
    # hill climbing with "(L)ong (R)estarts"
    start = time.perf_counter()
    solution = search.random_restart(theProblem, steps // 100, 100)
    end = time.perf_counter()
elif algorithm == 'HCFR':
    # hill climbing with "(F)requent (R)estarts"
    start = time.perf_counter()
    solution = search.random_restart(theProblem, steps // 20, 20)
    end = time.perf_counter()
    
print(solution)
print("Time used:", (end-start), "secs")

