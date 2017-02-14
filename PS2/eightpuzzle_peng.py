from search import *
from nn_puzzle import *
from collections import deque
import sys
import time


"""
[((1, 0, 8, 5, 2, 4, 7, 3, 6), None), 
((1, 2, 8, 5, 0, 4, 7, 3, 6), 'Down'), 
((1, 2, 8, 5, 4, 0, 7, 3, 6), 'Right'), 
((1, 2, 0, 5, 4, 8, 7, 3, 6), 'Up'), 
((1, 0, 2, 5, 4, 8, 7, 3, 6), 'Left'), 
((1, 4, 2, 5, 0, 8, 7, 3, 6), 'Down'), 
((1, 4, 2, 0, 5, 8, 7, 3, 6), 'Left'), 
((1, 4, 2, 7, 5, 8, 0, 3, 6), 'Down'), 
((1, 4, 2, 7, 5, 8, 3, 0, 6), 'Right'), 
((1, 4, 2, 7, 5, 8, 3, 6, 0), 'Right'), 
((1, 4, 2, 7, 5, 0, 3, 6, 8), 'Up'), 
((1, 4, 2, 7, 0, 5, 3, 6, 8), 'Left'), 
((1, 4, 2, 0, 7, 5, 3, 6, 8), 'Left'), 
((1, 4, 2, 3, 7, 5, 0, 6, 8), 'Down'), 
((1, 4, 2, 3, 7, 5, 6, 0, 8), 'Right'), 
((1, 4, 2, 3, 0, 5, 6, 7, 8), 'Up'), 
((1, 0, 2, 3, 4, 5, 6, 7, 8), 'Up'), 
((0, 1, 2, 3, 4, 5, 6, 7, 8), 'Left')]
"""

"""For last question, not sure if I uderstand the question well, I guess 
the question turns to be " what is the running time of heap search?"
my answer is O(n)
"""


class BFS(Search):

    def search(self, initial_state):
        """Given an initial problem state, encode a search-tree
        node representing the state and systematically explore
        the state-space until a goal-state is found.

        Returns:
         a search-tree node representing a goal state (if found)
         or None, if no goal is discovered"""
        
        " visited is for all nodes explored"
        self.visited = {}
        self.visited[initial_state] = (None, 0, None)
        "level is the depth of tree, root level is 0"
        level = 0
        
        "use FIFO deque for DFS"
        "turn list to dqueue since it's more convinient"
        frontier = []
        frontier.append(initial_state)
        dqueue = deque(frontier)
        
        
        while len(dqueue) >0:
            state = dqueue.popleft()
            "get all possible actions of current state"
            nextActions = self.problem.actions(state)
            for action in nextActions:
                newState = self.problem.result(state, action)[0]
                "make sure do not revisit parent node to avoid infinite loop"
                if newState not in dqueue and newState not in self.visited.keys():
                    "add new state into frontier"
                    dqueue.append(newState)
                    "for every visited node, "
                    "record its parent node, its depth in tree and what action to get this state"
                    self.visited[newState] =(state, level+1, action)
                    if self.problem.isgoal(newState):
                        return newState
                        

    def solution(self, node):
        """Returns the 'solution' for the specified node in the search tree.
        That is, this method should return a sequence of tuples:
        [(state_0, action_0), (state_1, action_1), ..., (state_n, action_n)]

        such that:
        state_0 is the initial state in the search
        action_0 is the first action taken
        action_i is the action taken to transition from state_i to state_{i+1}
        state_n is the state encapsulated by the 'search_node' argument
        action_n is None
        """
        path=[]
#        while node!= None and self.visited[node][1]!=0:
        while node!= None:
            path.insert(0,(node,self.visited[node][2]))
            node=self.parent(node)
        return path   
#        raise ValueError("This is unimplemented.")

    def child_node(self, node, action):
        """Create a child node for this search tree given a parent
        search tree node and an action to execute. Don't confuse nodes
        in the search-tree and verticies in the state-space graph."""
        return self.problem.result(node, action)[0]
        

    def parent(self, node):
        """Return the parent of the specified node in the search tree"""
        if node in self.visited.keys():
            return self.visited[node][0]
        return None

    def depth(self, node):
        """Determine how deep the search tree node is in the search tree.
        Consider the initial state (root) to be at depth 0

        Note: this method is NOT required by the Search class interface. But
        if you wanted to implement BFS or DFS or a variant, you'd likely
        want such a function.
        """
        if node in self.visited.keys():
            return self.visited[node][1]
        return -1
    
class AStar(Search):

    def search(self, initial_state):
        """Given an initial problem state, encode a search-tree
        node representing the state and systematically explore
        the state-space until a goal-state is found.

        Returns:
         a search-tree node representing a goal state (if found)
         or None, if no goal is discovered"""
        
        " Key is state and value is (parentNode, deeplevel, action)"
        
        " visited is for all nodes explored"                            
        self.visited = {}
        self.visited[initial_state] = (None, 0, None)
        "level is the depth of tree, root level is 0"
        level = 0
        
        "frontier with nodes and its cost"
        frontier = {}
        frontier[initial_state] = 0
         
        while len(frontier) > 0:
            "find the node with minial cost"
            state = self.findMinimumValue(frontier)
#            print(state)
            "delete the node with minimal cost in frontier"
            frontier.pop(state)
#            print(frontier)
            
           
            nextActions = self.problem.actions(state)
#            print(nextActions)
            level = level + 1
            for action in nextActions:
#                print(action)
                newState = self.problem.result(state, action)[0]
#                print(newState)
                "make sure do not get back to visited node, to avoid loop"
                if newState not in frontier and newState not in self.visited.keys():
                    
                    "get the cost of a node then update frontier"
                    "f(n) = g(n) + h(n)"
                    "g(n) is actually depth of tree in this case, which is variable 'level'  "
                    "h(n) is ManhattanDistance in this case"
                    frontier[newState] = self.ManhattanDistance(newState) + level
                    self.visited[newState] =(state, level, action)
                    if self.problem.isgoal(newState):
                        return newState
                    
                    
    "find the key with minimal value in a dictionary"
    def findMinimumValue(self, dic):
        value = sys.maxsize
        key = None
        for item in dic:
            if dic[item] < value:
                value = dic[item]
                key = item
        return key
    
                
    "get the ManhattanDistance for every state"    
    def ManhattanDistance(self,state):
        
        goalXY = {}
        stateXY = {}
        cost = 0
        """goalXY = {1:(0, 1), 2:(0,2), 3:(1,0), 4:(1,1), 5:(1,2), 6:(2,0), 7:(2,1), 8:(2,2)}"""
        for i in range(9):
            goalXY[i] = (i//3, i%3)
        
        for i in range(9):
            stateXY[state[i]] = (i//3, i%3)
        
        for i in range(1,9):
            cost = cost + abs(goalXY[i][0] - stateXY[i][0]) + abs(goalXY[i][1] - stateXY[i][1])
        
        return cost
        

    def solution(self, node):
        """Returns the 'solution' for the specified node in the search tree.
        That is, this method should return a sequence of tuples:
        [(state_0, action_0), (state_1, action_1), ..., (state_n, action_n)]

        such that:
        state_0 is the initial state in the search
        action_0 is the first action taken
        action_i is the action taken to transition from state_i to state_{i+1}
        state_n is the state encapsulated by the 'search_node' argument
        action_n is None
        """
        path=[]
#        while node!= None and self.visited[node][1]!=0:
        while node!= None:
            path.insert(0,(node,self.visited[node][2]))
            node=self.parent(node)
        return path   
#        raise ValueError("This is unimplemented.")

    def child_node(self, node, action):
        """Create a child node for this search tree given a parent
        search tree node and an action to execute. Don't confuse nodes
        in the search-tree and verticies in the state-space graph."""
        return self.problem.result(node, action)[0]
        

    def parent(self, node):
        """Return the parent of the specified node in the search tree"""
        if node in self.visited.keys():
            return self.visited[node][0]
        else:
            return None

    def depth(self, node):
        """Determine how deep the search tree node is in the search tree.
        Consider the initial state (root) to be at depth 0

        Note: this method is NOT required by the Search class interface. But
        if you wanted to implement BFS or DFS or a variant, you'd likely
        want such a function.
        """
        if node in self.visited.keys():
            return self.visited[node][1]
        else:
            return -1

if __name__ == "__main__":
    
    puzzle = NNPuzzle(3)
    initial = puzzle.get_shuffled_state(18)
    "get the result via BFS"
    solver1 = BFS(puzzle)
    start1 = time.time()
    goal1 = solver1.search(initial)
    runtime1 = time.time() - start1
    print("Initial State", initial)
    print("Found goal", goal1, " in " , runtime1,  " seconds")
    for sa in solver1.solution(goal1):
        puzzle.display(sa)
    
    "get result via AStar"
    solver2 = AStar(puzzle)
    start2 = time.time()
    goal2 = solver2.search(initial)
    runtime2 = time.time() - start2
    print("Initial State", initial)
    print("Found goal", goal2, " in " , runtime2,  " seconds")
    for sa in solver2.solution(goal2):
        puzzle.display(sa)
    "get result for (1,0,8,5,2,4,7,3,6) via AStar"
    initial3 = (1,0,8,5,2,4,7,3,6)
    solver3 = AStar(puzzle)
    goal3 = solver3.search(initial3)
    print("Initial State", initial3)
    print("Found goal", goal3)
    print(solver3.solution(goal3))
    "get result for (1,0,8,5,2,4,7,3,6) via BFS to verify the result of Astar above"
#    initial4 = (1,0,8,5,2,4,7,3,6)
#    solver4 = BFS(puzzle)
#    goal4 = solver4.search(initial4)
#    print("Initial State", initial4)
#    print("Found goal", goal4)
#    for sa in solver4.solution(goal4):
#        puzzle.display(sa)