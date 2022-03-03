# Project 3
In this project you will implement Dijkstra’s algorithm to find paths through a graph representing a network routing problem.

## Installation
In order to run the program, simply fork the repository and install the four Python files Proj3GUI.py, NetworkRoutingSolver.py, CS4412Graph.py, and which_pyqt.py. These four files can be placed in whatever directory you wish. </br>
This project uses [PyQt5](https://pypi.org/project/PyQt5/) in order to build the GUI for the application. Assuming you have installed [Python](https://www.python.org/downloads/) and your PATH variable is set up properly to run Python commands from the terminal, use the following command to install PyQt5:
```bash
$ pip install PyQt5
```
After PyQt5 has been installed, simply run the following command from the directory where the project is located:
```bash
$ python Proj3GUI.py
```

## Usage
**Goals:**
1. Understand Dijkstra’s algorithm in the context of a real world problem.
2. Implement a priority queue with worst-case logarithmic operations.
3. Compare two different priority queue data structures for implementing Dijkstra’s and empirically verify their differences.
4. Understand the importance of proper data structures/implementations to gain the full efficiency potential of algorithms.

When you hit “Generate” the framework for this project generates a random set of nodes, V, each with 3 randomly selected edges to other nodes. The edges are directed and the edge cost is the Euclidean distance between the nodes. Thus all nodes will have an out-degree of 3, but no predictable value for in-degree. You will be passed a graph structure which is comprised of |V| nodes, each with 3 edges, thus |E| = 3 |V| = O(|V|). The nodes have an (x,y) location and the edges include the start/end nodes and the edge length. The nodes are drawn on the display in the provided framework. You can hit “Generate” again to build a new graph (if you change the random seed).

After generating, clicking on a node (or entering its index in the appropriate box) will highlight the source in green, and clicking another (or, again entering its index in the box) will highlight the destination in red. Each click alternates between the two. After these nodes are selected you can hit “Compute”, and your code should draw the shortest path starting from the source node and following all intermediate nodes until the destination node. Next to each edge between two nodes, display the cost of that segment of the route. Also, in the "Total Path Cost" box, display the total path cost. If the destination cannot be reached from the source then put “unreachable” in the total cost box. Clicking on the screen again will clear the current path while allowing you to set another source/destination pair.

The “Compute” button should (potentially) call two different versions of Dijkstra’s, one that uses an array to implement the priority queue, and one that uses a heap. (Use the standard Dijkstra's algorithm from the text which puts all nodes initially in the queue and finds the shortest path from the source node to all nodes in the network; after running that, then you just need to show the path from the source to the destination.) Both versions should give you the same path cost. While both versions have the same "high-level" big-O complexity for the graphs they generate, they will differ significantly in their runtime (why?). Each time you hit solve and show a path, display the time required for each version, and the times speedup of the heap implementation over the array implementation.
