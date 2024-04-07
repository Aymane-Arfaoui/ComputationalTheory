from graph import Graph


DEV = True
VERBOSE = True

v1cd = 'VERBOSE: VerifyOneColorDup() '


def VfyOneColorDup(I,S,H):
    ## ** HW 2 - replace FALSE with "reasonble" length tests | DONE
    # We only care about the length n of the instance I
    if len(S) > len(I) or len(H) > len(I): 
        if VERBOSE: print(f'{v1cd} unreasonable length hint or solution')
        return 'unsure'
    
    ## ** HW 2 - replace FALSE with appropriate test | Done
    if S == 'no':
        if VERBOSE: print(f'{v1cd} solution != "yes"')
        return 'unsure'
        
    cycle = H.split(',')  # Hint is a comma delimited list of nodes
    if len(cycle) < 2:
        if VERBOSE: print(f'{v1cd} Cycles must have at least 2 nodes.')
        return 'unsure'

    instance_graph, instance_colorings = I.split(';')

    #Use WCBC library function to create a directed, unweighted graph
    g = Graph(instance_graph,directed=True, weighted=False)

    nodes = list(g.nodes)
    nodes_sav = nodes[:]  # clone node list for future reference
    edges = list(g.edges())
    
    for idx in range(len(edges)):
        #convert edges from a list of graph edges to a list of strings
        edges[idx] = str(edges[idx])    
    
    colors = []         # colors 
    node_color_kv = {}  # node->color key/value pairs
    color_count_kv = {} # color->count key/value pairs
    colorings_list = instance_colorings.split()
    for node_color in colorings_list:
        node,color = node_color.split(':')
        node_color_kv[node] = color
        if color not in colors:
            colors.append(color)
            color_count_kv[color] = 0

    ## ** HW 2 Add code that will make test cases 4 through 7 match 'unsure' 
    
    #Rules:
    #All nodes in the cycle must be part of the graph.
    #No consecutive nodes in the cycle should have the same color.
    #Exactly one color occurs twice; no color occurs more than twice.
    
    for node_index in range(len(cycle)):
        actualNode = cycle[node_index]
        #next node is not necessarily just cycle[node_index + 1]
        NextNode = cycle[(node_index+1)%len(cycle)]
        
        #make sure node exists in the graph
        if actualNode not in nodes_sav:
            if VERBOSE: print(f'{v1cd} Node {actualNode} not in the graph')
            return 'unsure'
        
        #check for edges that do not exist usign graph function:
        if not Graph.containsEdge(actualNode, NextNode):
            if VERBOSE: print(f'{v1cd} Edge from {actualNode} to {NextNode} does not exist')
             return 'unsure'

        
        #now let us see if consecutive nodes have same colro
        # #make sure you prevent index out of bounds 
        # node_color_kv defined earleir is a dictionnary so can use get and values methods 
        if node_index < len(cycle) - 1 and node_color_kv.get(actualNode) == node_color_kv.get(NextNode):
            if VERBOSE: print(f'{v1cd} Consecutive nodes {node} and {NextNode} have the same color')
            return 'unsure'
       
    #outside the loop here: check for color count to make sure it is not there more than two time
    colorCount = list(color_count_kv.values())
    #check if exactly one color appears twice and that no colour apears more than once 
    if colorCount.count(2) != 1 or any(count > 2 for count in colorCount):
        if VERBOSE: print(f'{v1cd} Color occurrence condition not met')
        return 'unsure'

    ## ** HW 2 Add code that will make test cases 8 through 10 match 'unsure'
    ## ** You may implemet this as part of the above for loop if you wish
    return 'correct'

if __name__ == '__main__':
    
    def test_case(F,I,S,H,expected,num,comment=''):
        # Evaluate test case to see whether or not it meets expectations.
        #
        err = '** '   # Error flag is on by default
        result = F(I,S,H) # Call the verifier and store the result.

        # Get the function name as a string
        func_name = str(F).split()[1]
        call = f'''{func_name}("{I}","{S}","{H}")'''
        if result == expected:
            err = ''  # turn off error flag when results meet expectations

        e = expected
        print (f'{err}test #{num} {call}: expected "{e}", received "{result}"')
        print (f'test #{num} Explanation: {comment}\n')
        return num + 1

    
    
    F = VfyOneColorDup
    num = 1

    I = 'a,b  b,c  c,d  d,a; a:red b:blue c:yellow d:blue'
    exp = 'solution too long'
    num = test_case(F,I,'maybe','a,b,c,d','unsure',num,exp)

    I = 'a,b  b,c  c,d  d,a; a:red b:blue c:yellow d:blue'
    exp = "can't verify negative instance"
    num = test_case(F,I,'no','a,b,c,d','unsure',num,exp)

    I = 'a,a; a:red'
    exp = 'One node does not a cycle make'
    num = test_case(F,I,'yes','a','unsure',num,exp)
    
    I = 'a,b  b,c  c,d  d,a ; a:red b:blue c:yellow d:blue'
    exp = 'e not in graph'
    num = test_case(F,I,'yes','e,a,b,c,d','unsure',num,exp)

    I = 'a,b  b,a  c,d  d,a ; a:red b:blue c:yellow d:blue'
    exp = '"a" occurs twice'
    num = test_case(F,I,'yes','a,b,a,d','unsure',num,exp)

    I = 'a,b  b,d  c,d  d,a; a:red b:blue c:yellow d:blue'
    exp = 'No b-c edge'
    num = test_case(F,I,'yes','a,b,c,d','unsure',num,exp)    

    I = 'a,b  b,c  c,d  d,a; a:red b:blue c:blue d:yellow'
    exp = 'consecutive blues'
    num = test_case(F,I,'yes','a,b,c,d','unsure',num,exp)

    I = 'a,b  b,c  c,a  d,a; a:red b:blue c:green d:yellow'
    Exp = 'no yellow in cycle'
    num = test_case(F,I,'yes','a,b,c','unsure',num,exp)

    I = 'a,b  b,c  c,d  d,e e,f f,a; a:red b:blue c:red d:blue e:red f:yellow'
    exp = '3 reds'
    num = test_case(F,I,'yes','a,b,c,d,e,f','unsure',num,exp)    

    I = 'a,b  b,c  c,d  d,a; a:red b:blue c:white d:yellow'
    exp = 'no color duplicated'
    num = test_case(F,I,'yes','a,b,c,d','unsure',num,exp)    
    
    I = 'a,b  b,c  c,d  d,a; a:red b:blue c:yellow d:blue'
    exp = 'a-b-c traverses every color; no consecutive nodes in cycle same color; blue occurs twice'
    num = test_case(F,I,'yes','a,b,c,d','correct',num,exp)    
    

    
    
    

    
    
    
