#bfs

graph = {
    'A':['B', 'C'],
    'B':['D', 'E'],
    'C':['F'],
    'D':[],
    'E':['F'],
    'F':[]
}

visited=[]
queue=[]

def bfs(graph, visited, node):
    visited.append(node)
    queue.append(node)

    while queue:
        m = queue.pop(0)
        print(m, end='')

        for neighbour in graph[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
    
print("the elements visited using bfs :")
bfs(graph, visited, 'A')
