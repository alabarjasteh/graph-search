# Seach (Artificial Intelligence)

An implementation of `A*`, `IDA*`, `UCS`, `BDS`, `DFS`, `BFS` algorithms to solve 15-puzzle problem.
The search algorithm is written independent of problem (15-puzzle problem in this case) and it can be used to solve other problems as well, like famous [UCB CS188 Packman game](https://inst.eecs.berkeley.edu/~cs188/fa19/project1/).

Search algorithms uses these heuristics: 
* Manhattan Distance
* Linear Conflicts + Manhattan Distance
* Disjoint pattern database
