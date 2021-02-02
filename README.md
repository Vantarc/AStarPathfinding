# AStarPathfinfing
A simple A* implementation with GUI

This program was created to help me understand the pathfinding algorithm A*.

=================================

### Requirements ###
The program is written for Python 3.8

Required libraries:
- pygame
- numpy

To install these libraries use the following command:
```
pip install pygame numpy
```

### Running ###

To run the program execute the file main.py with python:

```
python main.py
```

### Controls ###

**Leftclick:** convert tile to wall

**Rightclick:** convert tile to fre space

**Middleclick:** move the map around

**Scroll:** zoom in and out

### Run the algorithm ###
The algorithm has two run modes:

**Solve:** The complete map is solved and the shortest path is computed

**Solve step-by-step:** One iteration of the algorithm is executed after which the button has to be pressed again to execute the next iteration.

### Colors ###

**Black:** wall

**White:** free space

**Blue:** start/end/path

**Green:** tiles which are in the open list

**Red:** tiles which are in the closed list
