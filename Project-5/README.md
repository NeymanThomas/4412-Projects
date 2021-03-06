# Project 5 
The TSP problem consists of the following: </br>
- Given: a directed graph and a cost associated with each edge
- Return: the lowest cost complete simple tour of the graph

A complete simple tour is a path through the graph that visits every vertex in the graph exactly once and ends at the starting point, also known as a 
Hamiltonian cycle or Rudrata cycle. Note that as formulated here, the TSP problem is an optimization problem, in so far as we are searching for the simple 
tour with minimum cost.

## Installation 
In order to run the program, simply fork the repository and install the four Python files Proj5GUI.py, TSPClasses.py, TSPSolver.py, and which_pyqt.py. These four 
files can be placed in whatever directory you wish. </br>
This project uses [PyQt5](https://pypi.org/project/PyQt5/) in order to build the GUI for the application. Assuming you have installed [Python](https://www.python.org/downloads/) 
and your PATH variable is set up properly to run Python commands from the terminal, use the following command to install PyQt5:
```bash
$ pip install PyQt5
```
After PyQt5 has been installed, simply run the following command from the directory where the project is located:
```bash
$ python Proj5GUI.py
```

## Usage
**goals**
1. Write a branch and bound algorithm (your TSP solver) to find the shortest complete simple tour through the City objects in the array Cities. You will use the 
reduced cost matrix for your lower bound function and “partial path” as your state space search approach. Implement your solver in the following method: 
TSPSolver.branchAndBound().
2. Your solver should include a time-out mechanism so that it will terminate and report the best solution so far (BSSF) after 60 seconds of execution time (you can 
use the "private" member TSPSolver._time_limit, which is set to the default value 60 and automatically updates whenever the Time Limit field is edited in the 
application form. Note that it is not critical that you use precisely 60 seconds. Running a timer and checking the time on every iteration through your branch 
and bound algorithm is sufficient, if slightly imprecise. You can use timers to interrupt your search if you want to be more precise about ending exactly at 60 seconds.
3. Assign the "private" member TSPSolver._bssf to a TSPSolution object that contains the path you have discovered. You should be creative with your initial BSSF 
value as it can have a significant impact on early pruning. One suggestion is to implement the simple greedy algorithm outlined in P6 and use the solution from 
the greedy algorithm as your initial BSSF.
4. To display your solution, populate the results array with the cost of the discovered tour, the elapsed time that it took you to discover it and the number of 
intermediate solutions considered, respectively (for an example of how to do this, you can look at the default algorithm ProbemAndSolver.defaultRandomTour() method. 
When counting intermediate solutions, do not include your initial BSSF (this intermediate count will be 0 if the BSSF is optimal or time expires).
5. For this project, the performance analysis will focus on both time and space. You will need a mechanism to report the total number of child states generated 
(whether they are put on the queue or not), and also the number of states pruned due to your evolving BSSF. This includes all child states generated that never 
get expanded, either because they are not put on the queue, pruned when dequeued, or because they never get dequeued before termination. You will also report the 
maximum size of the queue which is the upper bound of memory used.
6. There are three difficulty levels that govern the city distributions: Easy (symmetric), Normal (asymmetric), Hard (asymmetric and some infinite distances). You 
can play with all of them during testing but just use the Hard level for all of your reporting below. Note Easy employs a Euclidean distance function; Normal, a 
metric distance function; and Hard, a non-metric distance function. With a Euclidean distance function, the optimal tour can not have crossed paths; however, in 
the case of a non-metric distance function, the optimal tour may have crossed paths.
7. Most of your results should include multiple BSSF updates (# of Solutions reported in GUI), especially for smaller numbers of cities. Because this can only 
happen when the search reaches a leaf node (finds a complete tour), and because each state can add many children states to the queue, you must think carefully 
about your search strategy and come up with a priority key for the queue that implements it. While it is tempting (and probably useful) to visit states with a 
low bound, it is also important to find complete tours (so the BSSF can be updated and the tree can be pruned more), so your prioritization of states should consider 
both bound and tree depth (and anything else you can think of that improves performance---be creative).

Clicking the "Generate Scenario" button resets the problem instance for the given "Current Seed". Clicking the "Randomize Seed" button chooses a new 3-digit random seed 
and updates the "Current Seed" field. You can control the problem size using the “Problem Size” field, as shown in the following figure: The "Difficulty" drop-down menu 
allows you to select from one of three problem difficulty levels: Easy, Normal and Hard. The "Algorithm" pop-up menu allows you to select different algorithms for 
solving the problem. A simple random tour "Default" algorithm is already implemented. In the following figure, that default algorithm has been run on a random problem 
of size 20 of difficulty level Normal with a random seed of 312. The cost of the tour, the time spent finding the tour, and the number of solutions found are reported 
in the respective text boxes.
