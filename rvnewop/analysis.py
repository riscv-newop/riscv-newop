import networkx as nx


def isCandidate(prog, node, dag):
    """Returns whether node and everything from it makes a feasible candidate subgraph,

    a candidate must:
        - not be a leaf (not a register)
        - not have more than two register nodes connected to it
        - have at least one non-register node connected to it"""

    if dag.nodes[node]["type"] == "register":
        return False

    leaf_count = 0
    has_inst = False
    visited = {node}

    subgraph_nodes = [
        y for x in nx.bfs_edges(dag, source=node) for y in x if y is not node
    ]

    """ Record dst registers of root """
    dst_registers_root = getDstRegisters(dag, node)

    """For liveness check, build list of destination registers
    written to by intermediate instructions"""
    dst_registers = set()
    intermediate_nodes = []

    # for n in dict(nx.bfs_successors(dag, source=node))[node]:
    """Note: nx.bfs_edges returns a set of all edges traversed starting with
    the node, therefore we do not add nodes layer by layer"""
    for n in subgraph_nodes:
        if n not in visited:
            type = dag.nodes[n]["type"]
            if type == "register":
                leaf_count += 1
            if type == "instruction":
                has_inst = True

                # we consider the pc to be a register "source"
                if dag.nodes[n]["instruction"].name == "auipc":
                    leaf_count += 1

                # add dst registers of this instruction to the list
                dst_n = getDstRegisters(dag, n)
                dst_registers.update(dst_n)
                intermediate_nodes.append(n)

            visited.add(n)

    """ Track only those registers that are not also written to by the
    root node of the candidate """
    dst_registers = dst_registers - set(dst_registers_root)

    if leaf_count > 2:
        return False

    if not has_inst:
        return False

    """ check that making a complex single instruction out of this candidate
    does not violate liveness properties of the sub-block's successors"""
    for r in dst_registers:
        if prog.needsToStayLive(dag.graph["sub_block"], r):
            print("Failed due to liveness requirement..")
            return False

    # check that the intermediate dst registers are not required
    # to be live within the subbasicblock itself
    for n in intermediate_nodes:
        for s in dag.predecessors(n):
            # if a node has an edge coming to it from another subgraph
            # this will fail the liveness check
            if s not in subgraph_nodes and s is not node:
                return False

    return True


def createSubtreeFromNode(graph, node):
    """Return sub-DAG with node as its root"""
    # TODO use successors rather than bfs_edges
    return graph.subgraph([y for x in nx.bfs_edges(graph, node) for y in x])


def findCandidateSubgraphs(prog, dag):
    """Searches DAG for candidate subgraphs
    returns an array of candidate starting nodes"""
    return [n for n in dag if isCandidate(prog, n, dag)]


def stringToNum(string):
    """Helper function for hash function"""
    return sum(bytearray(string, "utf-8"))


def hashDAG(dag):
    """Creates a hash out of a DAG, only takes into account instruction names"""
    h = 0
    for n in dag:
        node = dag.nodes[n]
        if node["type"] == "instruction":
            name = n.split()[1]
            h += stringToNum(name)

    for u, v in dag.edges:
        node_u = dag.nodes[u]
        node_v = dag.nodes[v]

        if node_u["type"] == "instruction" and node_v["type"] == "instruction":
            h += stringToNum(u.split()[1]) % stringToNum(v.split()[1])

    return h


def findRoot(dag, node):
    """Finds root of the DAG"""
    parent = list(dag.predecessors(node))
    if len(parent) == 0:
        return node
    else:
        return findRoot(dag, parent[0])


def getDstRegisters(dag, node_key):
    node = dag.nodes[node_key]
    if node["type"] == "instruction":
        return node["instruction"].dest_registers
    return None


def graphToString(dag):
    """converts a graph to a string"""
    out = ""
    depth = 1
    layer_length = 1
    current = 0
    root = findRoot(dag, list(dag)[0])
    to_visit = [root]

    while to_visit:
        for s in dag.successors(to_visit[0]):
            temp = []
            if dag.nodes[s]["type"] == "instruction":
                temp.append(s)

            to_visit += sorted(temp, key=lambda x: x.split()[1])

        out += to_visit[0].split()[1] + ("_" * depth)
        to_visit.pop(0)
        i += 1

        # just to make sure the correct number of
        # underscores are being used
        if layer_length == current:
            depth += 1
            current = 0
            layer_length = len(to_visit)

    return out.strip("_")


def isIsomorphic(a, b):
    """Checks if two DAGs are isomorphic"""
    return graphToString(a) == graphToString(b)


def graphToParenStringRecursive(node, dag):
    """subroutine to converts a graph to a parenthesized string

    used in graphToParenString"""
    if not node or dag.nodes[node]["type"] == "register":
        return ""

    # lexographically sorted children
    lex = sorted(
        [
            child
            for child in dag.successors(node)
            if dag.nodes[child]["type"] == "instruction"
        ],
        key=lambda x: x.split()[1],
    )

    return "({}{})".format(
        node.split()[1],
        "".join([graphToParenStringRecursive(child, dag) for child in lex]),
    )


def graphToParenString(dag):
    """converts a graph to a parenthesized string"""
    root = findRoot(dag, list(dag)[0])

    return graphToParenStringRecursive(root, dag)
