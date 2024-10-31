""" The class Vertex is used to create objects of vertices in a graph"""

"""Preamble : in the Graph class, Every Vertex Id is mapped to it corresponding Vertex object.
                This Vertex object contains all the information regarding the index,
                vertex_id, rank, outdegree, adjacencylist(members are vertex objects).
                Each vertex object corresponds to a row,
                a collection of them in dictionary(or just values, in key-value pair)
                should correspond to a Table. graph_dict is the dictionary.
                Dictionary look ups take linear time, for loops on lists take linear time."""

"""For assignment 2 I have added the Graph reverse class which is the same as 
                    Graph class but the edges have been reversed in the main() function. Both these 
                    graphs have been related to one another as their reverse using the Pagerank
                    function. input.txt is the standard input, input2. txt introduces a source vertex,
                    and input3.txt introduces a sink vertex along with a source vertex."""
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

    #Function Does operation accordingly when an edge is pointed to it
    def add_in_degree(self, edge):
        self._revDegree = self._revDegree + 1
        self._inComingEdges.append(edge)

    #Populating the adjacency list accordinly
    def add_to_adjacencylist(self, vert, vertID):
        self._adjacencyList.append(vert)
        self._adjacencyListVertices.append(vertID)

    # Function associated with printing the values for every node
    def get_values(self, adjL):

        print(self._vertexId,":\t", self._pageRank,";\t", self._outDegree,":\t", self._revDegree,":\t", adjL,";\t", self._adjacencyListVertices)

    #Helps in preparing the output string associated with a vertex
    def prep_output_string(self, indegree, adjacencyL):

        out_str = self._vertexId + ":\t" + str(self._pageRank)+ ";\t" + str(indegree) + ";\t" + str(self._outDegree) + ";\t"
        for vert in adjacencyL:
            out_str = out_str + " " + vert
        out_str = out_str + ";\t"
        for vert in self._adjacencyListVertices:
            out_str = out_str + " " + vert
        out_str = out_str + "\n"
        return out_str

    #Used to access the outdegree of a vertex
    def get_outdegree(self):
        return self._outDegree

    #Used to access the indegree of a vertex
    def get_indegree(self):
        return self._revDegree

    #Used  to access the adjacency list of a vertex
    def get_adjacencylist(self):
        return self._adjacencyListVertices

    #Used to set the calculated Page Rank of a vertex
    def set_pagerank(self, pagerank):
        self._pageRank = pagerank

"""Class Graph is used to create objects of Graph"""
class Graph:

    # Constructor function
    def __init__(self):
        self.edge_list = []
        self.graph_dict = {} # Stored in the format where VertexID maps to the corresponding Vertex object
        self.countVetexes = -1 #Tracks the number of vertices along with helping in index initialization
        self.Gr = 0

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

    #Function that adds a new vertex to the Graph if a source or sink vertex is detected
    def vertices_check(self):

        add_edges = [] #Will contain the new edges associated with the new vertex if there is a source or sink vertex
        count = 0#Becomes 1 if there is a sink or source vertex

        #Loops through all the vertexes to detect if there is sink or source vertex
        for vertex in self.graph_dict.values():
            #Condition to check a source or sink vertex
            if vertex.get_outdegree() == 0 or vertex.get_indegree() == 0:
                new_vertex = "V"
                count = 1

                #Create edges associated with the newly added vertex
                for vertex_id in self.graph_dict.keys():
                    add_edges.append(new_vertex + " " + vertex_id)
                    add_edges.append(vertex_id + " " +  new_vertex)

                break

        self.countVetexes = self.countVetexes + count #Add the new vertex to the count of vertexes

        #Add the edges to the Graph
        for edge in add_edges:
            self.update_edge_info(edge)


"""Class Graph is used to create objects of Graph Reverse"""
class GraphReverse:

    # Constructor function
    def __init__(self):
        self.edge_list = []
        self.graph_dict = {} # Stored in the format where VertexID maps to the corresponding Vertex object
        self.countVetexes = -1  #Tracks the number of vertices along with helping in index initialization
        self.G = 0  #Used to store the graph(of which this graph is a reverse of)

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
        for vertexID in self.graph_dict.keys():
            self.graph_dict[vertexID].get_values(self.G.graph_dict[vertexID].get_adjacencylist())
            print("\n")

    # Function that prepares the output list to be written
    def prep_output_file(self):
        out_list = []
        for vertexID in self.graph_dict.keys():
            out_list.append(self.graph_dict[vertexID].prep_output_string(self.G.graph_dict[vertexID].get_outdegree(), self.G.graph_dict[vertexID].get_adjacencylist()))
        return out_list


    def vertices_check(self):

        add_edges = []
        count = 0

        for vertex in self.graph_dict.values():
            if vertex.get_outdegree() == 0 or vertex.get_indegree() == 0:
                new_vertex = "V"
                count = 1

                for vertex_id in self.graph_dict.keys():
                    add_edges.append(new_vertex + " " + vertex_id)
                    add_edges.append(vertex_id + " " +  new_vertex)

                break

        self.countVetexes = self.countVetexes + count

        for edge in add_edges:
            self.update_edge_info(edge)

    # Calculates the PageRank using recursion
    def calculate_pagerank(self, G, t=0, out_dict={}, outr_dict={}, rankzdict={}, modV=0):

        #Checks if t is between 1 to 50
        if t >= 1 and t <= 50:
            ranktdict = {} #stores the value of Pagerank for each vertex in the current iteration
            #Loops through all the vertexes in this graph to assign them a pagerank for each iteration
            for vertexID in self.graph_dict.keys():
                ranktdict[vertexID] = 0
                for adjvertex in self.graph_dict[vertexID].get_adjacencylist():
                    ranktdict[vertexID] += rankzdict[adjvertex]/outr_dict[adjvertex]
                ranktdict[vertexID] = 0.9*ranktdict[vertexID] + 0.1/modV

            #Assignment of pagerank to the vertex object happens only after the last iteration
            if t == 50:
                for vertexID in ranktdict.keys():
                    self.graph_dict[vertexID].set_pagerank(ranktdict[vertexID])
            t = t + 1
            self.calculate_pagerank(G, t, out_dict, outr_dict, ranktdict, modV)

        #This condition is for initially assigning values
        elif t == 0:
            t = 0 #Reflects the iteration
            modV = self.countVetexes + 1  # Gives a count of the vertices
            self.G = G
            out_dict = {} #Stores the out(v)
            outr_dict = {} #stores the out(v) for the reverse graph
            rankz_dict = {} #pagerank for 0th  iteration
            for vertexID in self.graph_dict.keys():
                out_dict[vertexID] = G.graph_dict[vertexID].get_outdegree()
                outr_dict[vertexID] = self.graph_dict[vertexID].get_outdegree()
                rankz_dict[vertexID] = 1/modV

            t = t + 1
            self.calculate_pagerank(Gr, t, out_dict, outr_dict, rankz_dict, modV)

if __name__ == "__main__":

    # Opening the input file which is already in the same directory
    file = open("input.txt", "r") #File from which the input is taken
    edge = file.readline()

    G = Graph()# Object of class Graph
    Gr = GraphReverse()# Object of reverse Graph

    # Evaluates the edges as long as there in the input file
    while True:
        if not edge:
            print("End of Inputs")
            break

        else:

            G.update_edge_info(edge) # Calls the update edge info
            edge_r = edge[2] + " " + edge[0]
            Gr.update_edge_info(edge_r) #Updates the edge for reverse graph

        edge = file.readline() # Reads each line which contains one edge

    G.vertices_check() #Both these function calls are for checking if there are sources or sinks
    Gr.vertices_check() #and adding a new edge accordingle

    Gr.calculate_pagerank(G=G) #Function to calculate the pagerank

    # Takes the input from the user regarding the output he wants to take
    choice = input("Enter Output to get the output on the screen and Pagerank to get the output on a file")

    # Expects to give the appropriate input
    while choice != "Output" and choice != "Pagerank":
        print("Your Choice is not appropriate, Please enter the correct choice")
        choice = input("Enter Output to get the output on the screen and Pagerank to get the output on a file")

    # Condition to print the output on the Screen
    if choice == "Output":
        Gr.print_graph_info()  # Prints the necessary output

    # Condition to print the output in the output file
    else:
        out_list = Gr.prep_output_file()  # Prepares the list for writong the output
        file3 = open("Pagerank.txt", "w")  # File to which the output is written
        file3.writelines(out_list)  # Writes the output into output file
        file3.close()  # Closing the output file
        print("Please check the output file")

    file.close() # Closes the input file
