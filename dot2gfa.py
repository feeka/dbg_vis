from collections import Counter

def de_bruijn_ize(st, k):
    """ Return a list holding, for each k-mer, its left
        k-1-mer and its right k-1-mer in a pair """
    edges = []
    nodes = set()
    for i in range(len(st) - k + 1):
        edges.append((st[i:i+k-1], st[i+1:i+k]))
        nodes.add(st[i:i+k-1])
        nodes.add(st[i+1:i+k])
    return nodes, edges

def counter(edges):
    edge_string = []
    def re_arrange_edges():
        for src,dest in edges:
            edge_string.append(src+dest[-1])
    re_arrange_edges()
    return Counter(edge_string)

def visualize_de_bruijn(st, k):
    """ Visualize a directed multigraph using graphviz """
    nodes, edges = de_bruijn_ize(st, k)
    count_dict = counter(edges)
    with open("multiplicity.txt","w") as mult:
        for k,v in count_dict.items():
            mult.write(str(k)+":"+str(v))
            mult.write("\n")
    dot_str = 'digraph "DeBruijn graph" {\n'
    nodes_list = list(nodes)
    for i in range(0,len(nodes_list)):
        dot_str += '  %s [label="%s"] ;\n' % (nodes_list[i], i)
    for src, dst in edges:
        dot_str += '  %s -> %s ;\n' % (src, dst)
    return dot_str + '}\n'

import re

usz = 256

def convert_dot_to_gfa(input_file, output_file,k=23):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        nodes = {}
        edges = []

        for line in infile:
            line = line.strip()
            if '->' in line:
                match = re.match(r'(\S+)\s->\s(\S+)', line)
                if match:
                    edges.append((match.group(1), match.group(2)))
            else:
                match = re.match(r'(\S+)\s\[label="(\d+)"\]', line)
                if match:
                    nodes[match.group(1)] = match.group(2)

        for node, label in nodes.items():
            outfile.write(f"S\t{label}\t*\n")

        for edge in edges:
            outfile.write(f"L\t{nodes[edge[0]]}\t+\t{nodes[edge[1]]}\t+\t0M\n")

DNA="GCACGGTTACGGAT"
dot_str = visualize_de_bruijn(DNA,4)
print(len(DNA))
with open("input.dot", "w") as text_file:
    text_file.write(dot_str)



convert_dot_to_gfa('input.dot', 'output.gfa')
