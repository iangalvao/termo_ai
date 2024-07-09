from tree import *
tb = TreeBuilder([])
f = open("resultados/test5.txt","r")
tree = tb.read_from_string(f,0)
tree.print_nodes_and_keys_padding("      ")