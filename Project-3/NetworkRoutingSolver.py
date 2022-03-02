#!/usr/bin/python3


from CS4412Graph import *
import time

class NetworkRoutingSolver:
    FinalList = []
    FinalEdges = []

    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS4412Graph )
        self.network = network

    #this returns the shortest path from the source to the destination
    def getShortestPath( self, destIndex ):
        self.dest = destIndex

        # This shows the table of shortest paths from the source node
        print("Node\tDistance from Source")
        for i in range(len(self.network.nodes)):
            print("%d\t\t%d" % (i+1, self.FinalList[i]))

        return {'cost':self.FinalList[destIndex], 'path':self.FinalEdges}

    # run Dijkstras here
    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()

        # get the number of vertices in the graph
        n = len(self.network.nodes)
        # this is the list of distances from the starting index
        distances = []
        # instance of heap implementation
        heap = CS4412Heap()

        for i in range(n):
            # 10000000 just acts as a very large number kind of like infinity
            distances.append(10000000)
            # fill the heap with infinite values
            heap.array.append(heap.createNode(i, distances[i]))
            # fill the position list to keep track of nodes
            heap.pos.append(i)
        
        # set the position to the source node chosen
        heap.pos[srcIndex] = srcIndex
        # set its distance value to '0'
        distances[srcIndex] = 0
        heap.decreaseKey(srcIndex, distances[srcIndex])
        heap.size = n

        while heap.isEmpty() == False:
            # Extract the vertex with the minimum distance value
            newHeapNode = heap.deleteMin()
            current = newHeapNode[0]
            # current represents the current node that has been removed from the heap.

            # here edge represents one edge of the currently selected node current. edge.dest
            # represents the edge destination and edge.length represents the weight of the edge
            # destination is set to the destination node currently being looked at from current
            for edge in self.network.nodes[current].neighbors:
                destination = edge.dest

                if heap.isInHeap(destination.node_id) and distances[current] != 10000000 and edge.length + distances[current] < distances[destination.node_id]:
                    distances[destination.node_id] = edge.length + distances[current]
                    # update the distance value in min heap also
                    heap.decreaseKey(destination.node_id, distances[destination.node_id])
        
        # This is simply used to get the shortest path tlo the getShortestPath function
        self.FinalList = distances

        t2 = time.time()
        return (t2-t1)


# the heap implementation that acts as our priority queue
class CS4412Heap():
    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []
    
    def createNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode
    
    def swapNode(self, a, b):
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t
    
    # this heapify function shuffles the highest priority item to the head of the queue
    def minHeapify(self, index):
        shortest = index
        left = 2*index + 1
        right = 2*index + 2
        if left < self.size and self.array[left][1] < self.array[shortest][1]:
            shortest = left
        if right < self.size and self.array[right][1] < self.array[shortest][1]:
            shortest = right
        if shortest != index:
            # swap position
            self.pos[self.array[shortest][0]] = index
            self.pos[self.array[index][0]] = shortest
            # swap nodes
            self.swapNode(shortest, index)
            self.minHeapify(shortest)
    
    def deleteMin(self):
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
        # get the node and update its distance value
        self.array[i][1] = dist
        # travel up while the complete heap is not shuffled
        # this is an O(Log n ) loop
        while i > 0 and self.array[i][1] < self.array[(i - 1) // 2][1]:
            # swap the node and its parent
            self.pos[self.array[i][0]] = (i - 1) // 2
            self.pos[self.array[(i-1) // 2][0]] = i
            self.swapNode(i, (i - 1) // 2)
            # move to parent index
            i = (i - 1) // 2
    
    # utility function to check if a given vertex in in the min heap or not
    def isInHeap(self, v):
        if self.pos[v] < self.size:
            return True
        return False