# Project 2
The convex hull of a set Q of points is the smallest convex polygon P for which each point in Q is either on the boundary of P or in its interior. 
To be rigorous, a polygon is a piecewise-linear, closed curve in the plane. That is, it is a curve, ending on itself that is formed by a sequence 
of straight-line segments, called the sides of the polygon. A point joining two consecutive sides is called a vertex of the polygon. If the polygon 
is simple , as we shall generally assume, it does not cross itself. The set of points in the plane enclosed by a simple polygon forms the interior of 
the polygon, the set of points on the polygon itself forms its boundary , and the set of points surrounding the polygon forms its exterior . A simple 
polygon is convex if, given any two points on its boundary or in its interior, all points on the line segment drawn between them are contained in the 
polygon's boundary or interior.

## Installation
In order to run the program, simply fork the repository and install the three Python files Proj2GUI.py, convex_hull.py, and which_pyqt.py. These three files 
can be placed in whatever directory you wish. </br>
This project uses [PyQt5](https://pypi.org/project/PyQt5/) in order to build the GUI for the application. Assuming you have installed [Python](https://www.python.org/downloads/) and your PATH variable is set up properly to run Python commands from the terminal, use the following command to install PyQt5:
```bash
$ pip install PyQt5
```
After PyQt5 has been installed, simply run the following command from the directory where the project is located:
```bash
$ python Proj2GUI.py
```

## Usage
More generally beyond two dimensions, the convex hull for a set of points Q in a real vector space V is the minimal convex set containing Q .

Algorithms for some other computational geometry problems start by computing a convex hull. Consider, for example, the two-dimensional farthest-pair problem: we are given a set of n points in the plane and wish to find the two points whose distance from each other is maximum. This pair is also referred to as the diameter of the set of points. You can prove that these two points must be vertices of the convex hull.

The problem of finding convex hulls also finds its practical applications in pattern recognition, image processing, statistics and GIS.
