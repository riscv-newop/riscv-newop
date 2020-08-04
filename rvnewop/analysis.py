import networkx as nx


def isCandidate(node, dag):
    """Returns whether node and everything from it makes a feasible candidate subgraph,

    a candidate must:
        - not be a leaf (not a register)
        - not have more than two register nodes connected to it
        - have at least one non-register node connected to it"""

    if dag[node]["type"] == "register":
        return False

    leaf_count = 0
    has_inst = False
    visited = {node}
    for n in nx.bfs_edges(dag, source=node):
        if n not in visited:
            if n["type"] == "register":
                leaf_count += 1
            if n["type"] == "instruction":
                has_inst = True
            visited.add(n)

    if leaf_count > 2:
        return False

    if not has_inst:
        return False

    return True


def findCandidateSubgraphs(dag):
    """Searches DAG for candidate subgraphs"""
    return [n for n in dag if isCandidate(n, dag)]
