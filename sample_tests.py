import blockTiling as P
import random as rand


N = 5
blocks = {"+": 1, "|":1, "Z": 1, "T":1, "L":1,"4":1}

prob = P.Problem(N, blocks)

s1 = prob.create_initial_state()
s1 = prob.random_state()
s1.place_block("+", 0, 0)
print(s1)

neighbors = prob.neighbors(s1)
for n in neighbors:
    print(n)
