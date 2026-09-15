# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #tuple (x,y)
    #print("Start:", problem.getStartState())
    #boolean
    #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #Triple (nextState, action, cost)
    #print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    #table agent code from project0
    #table agent used breadth first logic to build the precept table 
    #util.Queue() constructor builds empty queue
    #buffered queue from table not needed
    #vacuum agent history was the table of agent's percepts and actions
    #vacuum agent used breadth first logic to build the precept table
    #the search agent computes one path for the actual start state, using a goal test to know when to stop.

    """def buildTable(depth):
  table = {}
  histories = []

  #for each location in the grid space...
  for location in LOC:
    for status in ['Clean','Dirty']:
    #create percept
      percept = (location, status)
    #create history
      history = (percept,)
    #create a starting history
      histories.append(history)

    #determine action associated w/ history


    #add history/action to table
  for i in range(depth):    #made depth of table-not needed for search agent
    nextHist = []           #use goal test to know when to stop

    for history in histories:
      percept = history[-1]
      action = actionPerc(percept) #actions aren't chosen in the search agent, we just try all of them
      table[history] = action

      for newPerc in nextPerc(percept, action):
        nextHist.append(history + (newPerc,))

    histories = nextHist    #not needed for search agent bc util.Queue() constructor builds empty queue


  return table"""
    #use queue, bfs, graph search, and goal test to know when to stop
    frontier = util.Queue()
    visited = set()
    #push start state location and empty list of actions onto the queue
    frontier.push((problem.getStartState(), []))

    while not frontier.isEmpty():
        #pop the next state and actions from the queue
        state, actions = frontier.pop()
        if state in visited:
            continue
        visited.add(state)
        if problem.isGoalState(state):
            return actions
        for nextState, action, cost in problem.getSuccessors(state):
            next_actions = actions + [action]
            frontier.push((nextState, next_actions))
            
    return []  # Return an empty list if no solution is found

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    # Helper class for organizing the PriorityQueue
    class QueueItem:
        node: str
        path: list[str]
        cost: float
        def __init__(self, node: str, path: list[str], cost: float) -> None:
            self.node = node
            self.path = path
            self.cost = cost

        def createChild(self, successor: tuple[str,str,float]):
            return QueueItem(
                node = successor[0],
                path = self.path + [successor[1]],
                cost = self.cost + successor[2]
            )

    start: str = problem.getStartState()
    to_visit = util.PriorityQueue()
    visited_nodes = { start }

    cur_node = start
    cur_queue_item: QueueItem = QueueItem(start, [], 0)
    while not problem.isGoalState(cur_node):
        adjacent_nodes: list[tuple[str,str,float]] = problem.getSuccessors(cur_node)

        # Note all adjacent nodes
        for nodeinfo in adjacent_nodes:
            qitem = cur_queue_item.createChild(nodeinfo)
            to_visit.update(qitem, qitem.cost)

        # Find the cheapest unvisited node to explore
        potential_next_node = to_visit.pop()
        while potential_next_node.node in visited_nodes:
            potential_next_node = to_visit.pop()

        cur_queue_item: QueueItem = potential_next_node
        visited_nodes.add(cur_queue_item.node)
        cur_node = cur_queue_item.node

    return cur_queue_item.path

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    start = problem.getStartState()
    fringe = util.PriorityQueue()
    fringe.push((start, [], 0), heuristic(start, problem))
    visited = {}

    while not fringe.isEmpty():
        state, path, cost = fringe.pop()
        if state in visited and cost >= visited[state]:
            continue
        else:
            visited[state] = cost
        if problem.isGoalState(state):
            return path
        
        for successor, action, stepCost in problem.getSuccessors(state):
            new_cost = cost + stepCost
            if successor not in visited or new_cost < visited[successor]:
                new_path = path + [action]
                fringe.push((successor, new_path, new_cost), new_cost + heuristic(successor, problem))

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
