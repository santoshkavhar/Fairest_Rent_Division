def get_input_nodes():
    nodes = []
    num_nodes = int(input("Enter number of students or rooms: "))
    for i in range(num_nodes):
        # nodes will start from 1
        nodes.append(i+1)
    return(nodes)
    

def get_input_weights(nodes):
    wt = {}
    for u in nodes:
        wt[u] = {}
        for v in nodes:
            wt[u][v] = int(input("Enter the preffered rent by student "+ str(u)+ " for room "+ str(v) +" : "))
    return(wt)