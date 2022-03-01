#!/usr/bin/python3


from CS4412Graph import *
import time
from collections import defaultdict
import sys


class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS4412Graph )
        self.network = network

    #this returns the shortest path from the source to the destination
    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE

        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = 3
        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        return {'cost':total_length, 'path':path_edges}

    # run Dijkstras here
    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)

        #if use_heap:
            # code here
            #return
        #else:

        """
        graph = Graph(9)
        graph.addEdge(0, 1, 4)
        graph.addEdge(0, 7, 8)
        graph.addEdge(1, 2, 8)
        graph.addEdge(1, 7, 11)
        graph.addEdge(2, 3, 7)
        graph.addEdge(2, 8, 2)
        graph.addEdge(2, 5, 4)
        graph.addEdge(3, 4, 9)
        graph.addEdge(3, 5, 14)
        graph.addEdge(4, 5, 10)
        graph.addEdge(5, 6, 2)
        graph.addEdge(6, 7, 1)
        graph.addEdge(6, 8, 6)
        graph.addEdge(7, 8, 7)
        graph.D(srcIndex)
        """

        # get the number of vertices in the graph
        n = len(self.network.nodes)
        # this is the list of distances from the starting index
        distances = []
        # instance of heap implementation
        minHeap = Heap()

        for v in range(n):
            distances.append(1e7)
            minHeap.array.append(minHeap.newMinHeapNode(v, distances[v]))
            minHeap.pos.append(v)
        
        minHeap.pos[srcIndex] = srcIndex
        distances[srcIndex] = 0
        minHeap.decreaseKey(srcIndex, distances[srcIndex])
        minHeap.size = n

        while minHeap.isEmpty() == False:
            newHeapNode = minHeap.extractMin()
            u = newHeapNode[0]

            for edge in self.network.nodes[u].neighbors:
                destination = edge.dest

                if minHeap.isInMinHeap(destination.node_id) and distances[u] != 1e7 and edge.length + distances[u] < distances[destination.node_id]:
                    distances[destination.node_id] = edge.length + distances[u]
                    # update the distance value in min heap also
                    minHeap.decreaseKey(destination.node_id, distances[destination.node_id])
        
        printArr(distances, n)

        """
        while minHeap.isEmpty() == False:
            # Extract the vertex with the minimum distance value
            newHeapNode = minHeap.extractMin()
            u = newHeapNode[0]
            # u represents the current node that has been popped from the heap.
            # u is the integer value of the node, so u should return as an integer

            # here pCrawl represents the edge of the currently selected node u. pCrawl[0]
            # represents the edge destination and pCrawl[1] represents the weight of the edge
            # so v is set the the destination node currently being looked at from u
            for pCrawl in self.network.nodes[u].neighbors:
                v = pCrawl[0]

                # if minHeap.isInMinHeap checks to see if the destination node v is in the min heap
                # just takes in an integer index and checks the pos list
                #
                # if distances[u] != 1e7 just checks to see if the distance is infinite
                #
                # if pCrawl[1] + dist[u] < dist[v]
                # pCrawl[1] is the weight from the current node and dist[u] is the recorded length from the
                # source to the current node. dist[v] is the current recorded distance of the destination node
                # being looked at by u. So essentially it is determining:
                #   edge.length + distance at current node < distance at destination node
                if minHeap.isInMinHeap(v) and distances[u] != 1e7 and pCrawl[1] + dist[u] < dist[v]:
                    # update the distance value in the list of the destination node to be the
                    # new updated distance
                    distances[v] = pCrawl[1] + distances[u]
                    # update the distance value in min heap also
                    minHeap.decreaseKey(v, dist[v])

        printArr(distances, n)
        """

        t2 = time.time()
        return (t2-t1)



def printArr(dist, n):
    print("Vertex\tDistance from Source")
    for i in range(n):
        print("%d\t\t%d" % (i, dist[i]))


# the minimum heap implementation that acts as our priority queue
class Heap():
    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []
    
    def newMinHeapNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode
    
    def swapMinHeapNode(self, a, b):
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t
    
    def minHeapify(self, idx):
        smallest = idx
        left = 2*idx + 1
        right = 2*idx + 2
        if left < self.size and self.array[left][1] < self.array[smallest][1]:
            smallest = left
        if right < self.size and self.array[right][1] < self.array[smallest][1]:
            smallest = right
        if smallest != idx:
            # swap position
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest
            # swap nodes
            self.swapMinHeapNode(smallest, idx)
            self.minHeapify(smallest)
    
    def extractMin(self):
        if self.isEmpty():
            return

        # store the root node
        root = self.array[0]
        # replace the root node with the last node
        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode
        # update position of last Node
        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1
        # Reduce heap size and heapify root
        self.size -= 1
        self.minHeapify(0)
        return root
    
    def isEmpty(self):
        if self.size == 0:
            return True
        else:
            return False

    def decreaseKey(self, v, dist):
        # get the index of v in heap array
        i = self.pos[v]
        # get the node and upfate its dist value
        self.array[i][1] = dist
        # travel up while the complete tree is not heapified.
        # this is an O(Log n ) loop
        while i > 0 and self.array[i][1] < self.array[(i - 1) // 2][1]:
            # swap the node and its parent
            self.pos[self.array[i][0]] = (i - 1) // 2
            self.pos[self.array[(i-1) // 2][0]] = i
            self.swapMinHeapNode(i, (i - 1) // 2)
            # move to parent index
            i = (i - 1) // 2
    
    # utility function to check if a given vertex in in the min heap or not
    def isInMinHeap(self, v):
        if self.pos[v] < self.size:
            return True
        return False

class Graph():
 
    def __init__(self, V):
        self.V = V
        self.graph = defaultdict(list)
 
    # Adds an edge to an undirected graph
    def addEdge(self, src, dest, weight):
 
        # Add an edge from src to dest.  A new node
        # is added to the adjacency list of src. The
        # node is added at the beginning. The first
        # element of the node has the destination
        # and the second elements has the weight
        newNode = [dest, weight]
        self.graph[src].insert(0, newNode)
 
        # Since graph is undirected, add an edge
        # from dest to src also
        newNode = [src, weight]
        self.graph[dest].insert(0, newNode)
    
    def D(self, src):
        V = self.V
        dist = []
        minHeap = Heap()
        for v in range(V):
            dist.append(1e7)
            minHeap.array.append( minHeap.newMinHeapNode(v, dist[v]))
            minHeap.pos.append(v)
        
        minHeap.pos[src] = src
        dist[src] = 0
        minHeap.decreaseKey(src, dist[src])
        minHeap.size = V

        ##########################################################
        while minHeap.isEmpty() == False:
            newHeapNode = minHeap.extractMin()
            u = newHeapNode[0]
            print("========================================================")
            print("The current min node being extracted from the heap is {}".format(u))

            for pCrawl in self.graph[u]:
                v = pCrawl[0]
                print("Items in pCrawl: Destination {}, Weight {}".format(pCrawl[0], pCrawl[1]))
                print("from {} looking at vertex {}".format(u, v))
                # If shortest distance to v is not finalized
                # yet, and distance to v through u is less
                # than its previously calculated distance
                print("The current distance to node {} from the source is {}".format(u, dist[u]))
                print("The weight of the edge from u plus the distance is {}, compared to the distance in the list {}".format(pCrawl[1] + dist[u], dist[v]))
                if (minHeap.isInMinHeap(v) and dist[u] != 1e7 and pCrawl[1] + dist[u] < dist[v]):
                        dist[v] = pCrawl[1] + dist[u]
                        # update distance value
                        # in min heap also
                        minHeap.decreaseKey(v, dist[v])
        
        printArr(dist, V)

