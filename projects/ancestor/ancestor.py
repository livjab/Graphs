class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("That vertext does not exist.")

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        s.push([starting_vertex])
        visited = set()
        while s.size() > 0:
            path = s.pop()
            v = path[-1]
            if v not in visited:
                if v == destination_vertex:
                  return path
                visited.add(v)
                for neighbor in self.vertices[v]:
                  copy = path.copy()
                  copy.append(neighbor)
                  s.push(copy)


def earliest_ancestor(ancestors, starting_node):
    #instantiate graph
    graph = Graph()

    # From inputs, get set of all vertices
    ancestor_list = set([ i for i, j in ancestors ] + [ j for i, j in ancestors ])

    # add each vertex to graph
    for ancestor in ancestor_list:
        graph.add_vertex(ancestor)

    # add connections to vertices
    for i,j in ancestors:
        # add edges backwards so that earliest ancestors point to empty sets
        graph.add_edge(j,i)

    # get list of all possible earliest ancestors to use as destinations
    earlies = []
    for vertex in graph.vertices:
        if len(graph.vertices[vertex]) == 0:
            earlies.append(vertex)

    # if starting node is in "earlies", return -1
    if starting_node in earlies:
        return -1

    # run a dfs from starting index to each of the "earlies" destinations
    # save all paths in a list to compare in next step
    paths = []
    for dude in earlies:
        paths.append(graph.dfs(starting_node, dude))
    # remove Nones from path list
    valid_paths = [x for x in paths if x is not None]

    # find longest path
    longest_path = max(valid_paths, key = len)

    # if there is a longest path, return last value in that path
    if longest_path:
        return longest_path[-1]
    else:
        # if tie, return path with lowest numeric id for ancestor
        min_ancestors = []
        for path in valid_paths:
                min_ancestors.append(path[-1])
        return min(min_ancestors)




#test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
#earliest_ancestor(test_ancestors, 3)
