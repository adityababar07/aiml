graph = {
    'A':['B', 'C'],
    'B':['D', 'E'],
    'C':['F'],
    'D':[],
    'E':['F'],
    'F':[]
}

visited = set()

def dfs(graph, visited, node):
    if node not in visited :
        print(node, end=' ')
        visited.add(node)
        for neighbour in graph[node]:
            dfs(graph, visited, neighbour)
dfs(graph, visited, 'B')
print('\n')