from time import sleep
from solver_tools import WordFilter
from common import *
from time import time
from solver import Solver as OriginalSolver

def test_f(f, *args):
    #print (*args)
    then = time()
    f(*args)
    now = time()
    ellapsed_time = now - then
    return ellapsed_time

def test_n_times(f, n, *args):
    total = 0
    print(f"test result: {f(*args)}")
    for i in range(n):
        total += test_f(f, *args)
    return total/n

total = 0

# test_object A
wf = WordFilter()

# common args. Needs to be created befor object B
a_words = ["abaco" for i in range(6)]
c_words = ["coala" for i in range(7)]
test_list = a_words + c_words
# test_object B
solver = OriginalSolver(test_list)

# args obj A
feedback = [1,0,0,0,0]
n = 100
chute = "chute"
# args obs B
chutes = [[('c',1), ('h',0),('u',0),('t',0), ('e',0)]]
args_list = [(chute, feedback, test_list), (chutes, test_list)]
f_list = {"WordFilter.filter_from_feedback":wf.filter_from_feedback, "Solver.filter_from_hints":solver.filter_from_hints}


# Perform tests and print results
for i, (name, func) in enumerate(f_list.items()):
    run_time = test_n_times(func, n, *args_list[i])
    print(f"Test {name}. Run time:\n{run_time:.9f} seconds")