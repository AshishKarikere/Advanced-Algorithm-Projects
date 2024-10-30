""" The class Vertex is used to create objects of vertices in a graph"""

"""Preamble : in the Graph class, Every Vertex Id is mapped to it corresponding Vertex object.
                This Vertex object contains all the information regarding the index,
                vertex_id, rank, outdegree, adjacencylist(members are vertex objects).
                Each vertex object corresponds to a row,
                a collection of them in dictionary(or just values, in key-value pair)
                should correspond to a Table. graph_dict is the dictionary.
                Dictionary look ups take linear time, for loops on lists take linear time."""
class Vertex:

    number = -1

    # The constructor function initializes all the object variables
    # Associated with a given vertex
    def __init__(self, vertexId, numberofvertexes):
        self._index = numberofvertexes
        self._vertexId = vertexId
        self._pageRank = 0.0
        self._outDegree = 0
        self._revDegree = 0
        self._outGoingEdges = [] #List of outgoing edges in string format
        self._inComingEdges = [] # List of incoming edges in String format
        self._adjacencyList = [] #List of Vertices but as objects of Vertex class
        self._adjacencyListVertices = [] # Adjacency list with only Vertex IDs

    # Function does operations accordingly if a edge originates from it
    def add_out_degree(self, edge):
        self._outDegree = self._outDegree + 1
        self._outGoingEdges.append(edge)
        self._pageRank = self._pageRank + 1

    #Function Does operation accordinly when an edge is pointed to it
    def add_in_degree(self, edge):
        self._revDegree = self._revDegree + 1
        self._inComingEdges.append(edge)
        self._pageRank = self._pageRank + 1

    #Populating the adjacency list accordinly
    def add_to_adjacencylist(self, vert, vertID):
        self._adjacencyList.append(vert)
        self._adjacencyListVertices.append(vertID)

    # Function associated with printing the values for every node
    def get_values(self):

        print("Vertex ", self._vertexId,": rank = ", self._pageRank, ", out-degree = ", self._outDegree,"\n")
        print("Edges from ", self._vertexId, "to :", self._adjacencyListVertices)

    #Helps in preparing the output string associated with a vertex
    def prep_output_string(self):

        out_str = self._vertexId + " " + str(self._outDegree)
        for vert in self._adjacencyListVertices:
            out_str = out_str + " " + vert
        out_str = out_str + "\n"
        return out_str

"""Class Graph is used to create objects of Graph"""
class Graph:

    # Constructor function
    def __init__(self):
        self.edge_list = []
        self.graph_dict = {} # Stored in the format where VertexID maps to the corresponding Vertex object
        self.countVetexes = -1 #Tracks the number of vertices along with helping in index initialization

    # Function receives an edge and updates all the necessary information
    def update_edge_info(self, edge):
        self.edge_list.append(edge)
        vertexID1 = edge[0] # vertex from where edge originates
        vertexID2 = edge[2] # vertex where the edge ends

        # The if else blocks creates a vertice if it is not there,
        # and updates it if it is already there
        if (vertexID2 in self.graph_dict.keys()):
            self.graph_dict[vertexID2].add_in_degree(edge)
        else:
            self.countVetexes = self.countVetexes + 1
            self.graph_dict[vertexID2] = Vertex(vertexID2, self.countVetexes)
            self.graph_dict[vertexID2].add_in_degree(edge)

        # This if else block is for the vertice from where the edge begins
        if (vertexID1 in self.graph_dict.keys()):
            self.graph_dict[vertexID1].add_out_degree(edge)
            self.graph_dict[vertexID1].add_to_adjacencylist(self.graph_dict[vertexID2], vertexID2)

        else:
            self.countVetexes = self.countVetexes + 1
            self.graph_dict[vertexID1] = Vertex(vertexID1, self.countVetexes)
            self.graph_dict[vertexID1].add_out_degree(edge)
            self.graph_dict[vertexID1].add_to_adjacencylist(self.graph_dict[vertexID2], vertexID2)

    #Function associated with printing the input
    def print_graph_info(self):
        for vertex in self.graph_dict.values():
            vertex.get_values()
            print("\n")

    # Function that prepares the output list to be written
    def prep_output_file(self):
        out_list = []
        for vertex in self.graph_dict.values():
            out_list.append(vertex.prep_output_string())
        return out_list

if __name__ == "__main__":

    # Opening the input file which is already in the same directory
    file = open("input.txt", "r")
    edge = file.readline()

    # Opening the output file which is in the same directory
    file2 = open("output.txt", "w")

    G = Graph()# Object of class Graph

    # Evaluates the edges as long as there in the input file
    while True:
        if not edge:
            print("End of Inputs")
            break

        else:

            G.update_edge_info(edge) # Calls the update edge info

        edge = file.readline() # Reads each line which contains one edge

    G.print_graph_info() # Prints the necessary output
    out_list = G.prep_output_file() #Prepares the list for writong the output
    file2.writelines(out_list) # Writes the output into output file

    file.close() # Closes the input file
    file2.close() # closes the output file