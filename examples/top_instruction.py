import rvnewop as rv

from glob import glob
from itertools import accumulate
import json

import matplotlib.pyplot as plt
#from networkx.drawing.nx_agraph import graphviz_layout

import networkx as nx
from networkx.readwrite import json_graph

def getOpcode(ins_num):
    # we use custom_0 or custom_1 space
    if ins_num <= 7:
        # custom_0
        return 11 #00_010_11
    else:
        # custom_1
        return 43 #01_010_11

def getFunct3(ins_num):
    # we use custom_0 or custom_1 space
    if ins_num <= 7:
        # custom_0
        return ins_num
    else:
        # custom_1
        return ins_num - 8

#FILENAME = "./embench_hst/matmult-int.hst"
FILENAME = "./compute.hst"
print("Processing {}...".format(FILENAME))

OUT_FILENAME = "./insns.json"
out_file = open(OUT_FILENAME, "w")

prog = rv.Histogram.parse(FILENAME, isa="32ICM")
prog.findBasicBlocks()

prog.addLivenessValuesToGraph()

# total cycles = sum of all the frequencies
total_cycles = sum(
    [inst.freq for bb in prog.basicBlocks for inst in bb.bbInstructions()]
)

new_instructions = []

for i, b in enumerate((prog.getSubBlocks())):
    graph = b.constructDAG()

    # temp will store every permutation of candidate subgraphs
    temp = []
    for n in rv.analysis.findCandidateSubgraphs(prog, graph):
        subtree = rv.analysis.createSubtreeFromNode(graph, n)
        root = n

        temp.append(rv.Subgraph(subtree, root))

    # add candidate subgraph with highest score to new instructions list
    current_nodes = set()
    temp = sorted(temp, key=lambda sg: sg.score, reverse=True)
    while temp:
        if any([(n in current_nodes) for n in temp[0].graph.nodes]):
            temp.pop(0)
        else:
            current_nodes.update(temp[0].graph.nodes)
            new_instructions.append(temp.pop(0))

new_instructions = sorted(new_instructions, key=lambda sg: sg.score, reverse=True)

inst_dict = {}
for subgraph in new_instructions:
    key = rv.analysis.graphToParenString(subgraph.graph)

    if key in inst_dict:
        inst_dict[key].score += subgraph.score

        curr_range = inst_dict[key].imm_range
        additional_range = subgraph.imm_range

        if curr_range is None:
            inst_dict[key].imm_range = additional_range
        elif additional_range is None:
            inst_dict[key].imm_range = curr_range
        else:
            inst_dict[key].imm_range = (
                min(curr_range[0], additional_range[0]),
                max(curr_range[1], additional_range[1]),
            )
    else:
        inst_dict[key] = subgraph

new_instructions = [inst_dict[key] for key in inst_dict]

max_depth = 0
max_mult_depth = 0
for sg in new_instructions:
    if sg.containsMultiplyInstruction():
        max_mult_depth = max(max_mult_depth, sg.depth)
    else:
        max_depth = max(max_depth, sg.depth)

saved_cycles = sum([sg.score for sg in new_instructions])
percent_cycles = float(saved_cycles) / total_cycles * 100

out_json = '{\n'
out_json += "\"instructions\":[\n"

i = 0
n_i = len(new_instructions[:10])
for sg in new_instructions[:10]:
    print("instruction #{}".format(i))
    print("range: {}".format(sg.imm_range))

    #plt.clf()
    #pos = graphviz_layout(sg.graph, prog="dot")
    #nx.draw(sg.graph, pos, with_labels=True, font_size=7)

    #plt.savefig("test{}.png".format(i))

    num_consts = 0
    for n in sg.graph:
        if sg.graph.nodes[n]["type"] == "constant":
            num_consts += 1

    if num_consts > 2:
        print("Instruction can not be encoded as it has " + str(num_consts) + " constants")
        i += 1
        continue

    # print out JSON
    for n in sg.graph:
        if sg.graph.nodes[n]["type"] == "instruction":
            try:
                del sg.graph.nodes[n]["instruction"]
            except:
                pass

    new_insn_name = (rv.analysis.graphToParenString(sg.graph)).replace('(','_').replace(')','_').replace('.','_')
    new_insn_json = ''
    new_insn_json += '{\n'
    new_insn_json += '"insn_name":' + '"' + new_insn_name + '",\n'
    new_insn_json += '"insn_fields":' + '[\n'
    new_insn_json += '{\n'
    new_insn_json += '"type":"opcode",\n' 
    new_insn_json += '"value":' + str(getOpcode(i))+',\n'
    new_insn_json += '"start":' + str(0)+',\n'
    new_insn_json += '"width":' + str(7)+'\n'
    new_insn_json += '},\n'
    new_insn_json += '{\n'
    new_insn_json += '"type":"funct3",\n' 
    new_insn_json += '"value":' + str(getFunct3(i))+',\n'
    new_insn_json += '"start":' + str(12)+',\n'
    new_insn_json += '"width":' + str(3)+'\n'
    new_insn_json += '},\n'
    new_insn_json += '{\n'
    new_insn_json += '"type":"rs1",\n' 
    new_insn_json += '"start":' + str(15)+',\n'
    new_insn_json += '"width":' + str(5)+'\n'
    new_insn_json += '},\n'
    new_insn_json += '{\n'
    new_insn_json += '"type":"rs2",\n' 
    new_insn_json += '"start":' + str(20)+',\n'
    new_insn_json += '"width":' + str(5)+'\n'
    new_insn_json += '},\n'
    new_insn_json += '{\n'
    new_insn_json += '"type":"rd",\n' 
    new_insn_json += '"start":' + str(7)+',\n'
    new_insn_json += '"width":' + str(5)+'\n'
    new_insn_json += '}\n'
    if num_consts > 0:
        new_insn_json += ',\n'

        const_field_start = 25
        const_field_width = 3
        c = 0
        for n in sg.graph:
            if sg.graph.nodes[n]["type"] == "constant":
                # add a constant field to instruction
                new_insn_json += '{\n'
                new_insn_json += '"type":"imm' + str(c) +'",\n' 
                new_insn_json += '"start":' + str(const_field_start)+',\n'
                new_insn_json += '"width":' + str(const_field_width)+'\n'
                new_insn_json += '}\n'

                # link this field information into the node in the graph
                sg.graph.nodes[n]["offset"] = const_field_start
                  
                const_field_start += const_field_width
                c+= 1
                if c < num_consts:
                    new_insn_json += ',\n'
        
    new_insn_json += '],\n'
    new_insn_json += '"match":' + '"' + hex(getOpcode(i) | getFunct3(i) << 12) + '",\n'
    new_insn_json += '"mask":' + '"0x707f",\n'

    data = json_graph.adjacency_data(sg.graph)
    new_insn_json += "\"graph\":\n"
    new_insn_json += json.dumps(data)
    new_insn_json += '}\n'
    out_json += new_insn_json
    if i < (n_i-1):
        out_json += ','
    
    i += 1

out_json +=']\n'
out_json +='}'
out_file.write(out_json)

print(
    """Saved {} cycles out of {} ({:.4}%) with {} new instructions""".format(
        saved_cycles, total_cycles, percent_cycles, len(new_instructions)
    )
)
print("max depth: {}\nmax mult depth: {}".format(max_depth, max_mult_depth))
