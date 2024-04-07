from graph import Graph

DEV = True
VERBOSE = True

v1cd = 'VERBOSE: VerifyOneColorDup() '


# F is a computational problem:
# An instance of OneColorDup (F) is a white-space delimited list of edges, separated by a
# semi-colon (';') from a white-space delimited list of node colorings. An edge is formatted as two node
# names separated by a comma (e.g., "a,b"), and a node coloring as a node name and a color separated by
# a colon (e.g., "b:blue"). For example, 'a,b b,c c,d d,a ; a:red b:blue c:yellow d:blue' is an
# instance of OneColorDup.


# I is an instance of the problem
# S is a proposed solution to the problem
# H is a hint to the problem
def VfyOneColorDup(I, S, H):
    ## ** HW 2 - replace FALSE with "reasonble" length tests
    if len(S) > len(I) or len(H) > len(I):
        if VERBOSE: print(f'{v1cd} unreasonable length hint or solution')
        return 'unsure'

    ## ** HW 2 - replace FALSE with appropriate test
    if S != "yes":
        if VERBOSE: print(f'{v1cd} solution != "yes"')
        return 'unsure'

    cycle = H.split(',')  # Hint is a comma delimited list of nodes
    if len(cycle) < 2:
        if VERBOSE: print(f'{v1cd} Cycles must have at least 2 nodes.')
        return 'unsure'

    instance_graph, instance_colorings = I.split(';')

    # Use WCBC library function to create a directed, unweighted graph
    g = Graph(instance_graph, directed=True, weighted=False)

    nodes = list(g.nodes)
    nodes_sav = nodes[:]  # clone node list for future reference
    edges = list(g.edges())

    for idx in range(len(edges)):
        # convert edges from a list of graph edges to a list of strings
        edges[idx] = str(edges[idx])

    colors = []  # colors
    node_color_kv = {}  # node->color key/value pairs
    color_count_kv = {}  # color->count key/value pairs
    colorings_list = instance_colorings.split()  # splits on space
    for node_color in colorings_list:
        node, color = node_color.split(':')
        node_color_kv[node] = color
        if color not in colors:
            colors.append(color)
            color_count_kv[color] = 0

    for node in nodes:
        color = node_color_kv[node]
        color_count_kv[color] = color_count_kv[color] + 1

    # test case 4
    for node in str(H).split(','):
        if node not in node_color_kv.keys():
            # print("case 4 check")
            return 'unsure'

    # test case 6
    # use double for loop to split the instance graph
    edge_count = len(edges)
    for edge_index in range(edge_count):
        for next_edge in range(edge_index, edge_count):
            if str(edges[edge_index]) == str(edges[next_edge])[::-1]:
                # print("case6 check")
                return 'unsure'

    solution_edges = []
    hint_nodes = H.split(',')

    # Create a list of edges
    solution_edges = [','.join([nodes[i], nodes[i + 1]]) for i in range(len(nodes) - 1)]

    # case 6+
    for edge in solution_edges:
        if str(edge) not in edges:
            # print("case 6")
            return 'unsure'

        # case 7
        for node in hint_nodes:
            # print(f"node:{node}")
            for neighbor in g.neighbors(node):
                # print(f"neighbor:{neighbor}")
                if node_color_kv[str(node)] == node_color_kv[str(neighbor)]:
                    # "case 7"
                    return 'unsure'
    # case 8
    hint_nodes = H.split(',')
    hint_colors = []
    for node in hint_nodes:
        hint_colors.append(node_color_kv[str(node)])

    for color in colors:
        if color not in hint_colors:
            # print("case 8")
            return 'unsure'



    #case 9
    for color in colors:
       if color_count_kv[color] > 2:
           # print("case 9")
           return 'unsure'

    #case 10
    #  I = 'a,b  b,c  c,d  d,a; a:red b:blue c:white d:yellow'
    #     exp = 'no color duplicated'
    #     num = test_case(F, I, 'yes', 'a,b,c,d', 'unsure', num, exp)

    count_1 = []
    # print(f"color count: {color_count_kv}")
    for count in color_count_kv.values():
        if count == 1:
            count_1.append(1)
        else:
            count_1.append(0)

    if all(count_1):
        # print("case 10")
        return 'unsure'




        #
        # for graph_edge in edges:
        #     if str(edge) != str(graph_edge):
        #         print("case6+ check")
        #         return 'unsure'

    ## ** HW 2 Add code that will make test cases 4 through 7 match 'unsure'
    # for node_index in range(len(cycle)):
    #     pass

    ## ** HW 2 Add code that will make test cases 8 through 10 match 'unsure'
    ## ** You may implemet this as part of the abov for loop if you wish
    return 'correct'


if __name__ == '__main__':

    def test_case(F, I, S, H, expected, num, comment=''):
        # Evaluate test case to see whether or not it meets expectations.
        #
        err = '** '  # Error flag is on by default
        result = F(I, S, H)  # Call the verifier and store the result.

        # Get the function name as a string
        func_name = str(F).split()[1]
        call = f'''{func_name}("{I}","{S}","{H}")'''
        if result == expected:
            err = ''  # turn off error flag when results meet expectations

        e = expected
        print(f'{err}test #{num} {call}: expected "{e}", received "{result}"')
        print(f'test #{num} Explanation: {comment}\n')
        return num + 1


    F = VfyOneColorDup
    num = 1

    I = 'a,b  b,c  c,d  d,a; a:red b:blue c:yellow d:blue'
    exp = 'solution too long'
    num = test_case(F, I, 'maybe', 'a,b,c,d', 'unsure', num, exp)

    I = 'a,b  b,c  c,d  d,a; a:red b:blue c:yellow d:blue'
    exp = "can't verify negative instance"
    num = test_case(F, I, 'no', 'a,b,c,d', 'unsure', num, exp)

    I = 'a,a; a:red'
    exp = 'One node does not a cycle make'
    num = test_case(F, I, 'yes', 'a', 'unsure', num, exp)

    I = 'a,b  b,c  c,d  d,a ; a:red b:blue c:yellow d:blue'
    exp = 'e not in graph'
    num = test_case(F, I, 'yes', 'e,a,b,c,d', 'unsure', num, exp)

    I = 'a,b  b,a  c,d  d,a ; a:red b:blue c:yellow d:blue'
    exp = '"a" occurs twice'
    num = test_case(F, I, 'yes', 'a,b,a,d', 'unsure', num, exp)

    I = 'a,b  b,d  c,d  d,a; a:red b:blue c:yellow d:blue'
    exp = 'No b-c edge'
    num = test_case(F, I, 'yes', 'a,b,c,d', 'unsure', num, exp)

    I = 'a,b  b,c  c,d  d,a; a:red b:blue c:blue d:yellow'
    exp = 'consecutive blues'
    num = test_case(F, I, 'yes', 'a,b,c,d', 'unsure', num, exp)

    # colorings for group in colorings

    I = 'a,b  b,c  c,a  d,a; a:red b:blue c:green d:yellow'
    exp = 'no yellow in cycle'
    num = test_case(F, I, 'yes', 'a,b,c', 'unsure', num, exp)

    I = 'a,b  b,c  c,d  d,e e,f f,a; a:red b:blue c:red d:blue e:red f:yellow'
    exp = '3 reds'
    num = test_case(F, I, 'yes', 'a,b,c,d,e,f', 'unsure', num, exp)

    I = 'a,b  b,c  c,d  d,a; a:red b:blue c:white d:yellow'
    exp = 'no color duplicated'
    num = test_case(F, I, 'yes', 'a,b,c,d', 'unsure', num, exp)

    I = 'a,b  b,c  c,d  d,a; a:red b:blue c:yellow d:blue'
    exp = 'a-b-c traverses every color; no consecutive nodes in cycle same color; blue occurs twice'
    num = test_case(F, I, 'yes', 'a,b,c,d', 'correct', num, exp)
