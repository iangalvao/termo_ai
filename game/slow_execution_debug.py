from time import sleep
from game.solver_tools import WordFilter
from game.hint import *
from time import time

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

wf = WordFilter()

a_words = ["abaco" for i in range(6)]
c_words = ["coala" for i in range(7)]
test_list = a_words + c_words

feedback = [1,0,0,0,0]
n = 100
chute = "chute"
args_list = [(chute, feedback, test_list)]
f_list = {"WordFilter.filter_from_feedback":wf.filter_from_feedback}


# Perform tests and print results
for i, (name, func) in enumerate(f_list.items()):
    run_time = test_n_times(func, n, *args_list[i])
    print(f"Test {name}. Run time:\n{run_time:.9f} seconds")