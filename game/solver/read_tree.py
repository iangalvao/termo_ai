from game.solver.tree import *

tb = TreeBuilder([])
f = open("game/resultados/out_tree_teste_3.txt", "r")
tree = tb.read_from_string(f, 0)
tree.print_nodes_and_keys_padding("      ")
