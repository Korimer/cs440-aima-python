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
        def __init__(self, successor: tuple[str,str,float], parent: QueueItem | None) -> None:
            base_node, base_action, base_cost = successor

            self.node = base_node

            self.path = [base_action]
            if parent is not None:
                self.path = parent.path + self.path

            self.cost = base_cost
            if parent is not None:
                self.cost = parent.cost + self.cost

    # TODO: Maintain a queue of already-visited nodes/costs. Don't revisit old/more expensive nodes!
    pqueue = util.PriorityQueue()
    start: str = problem.getStartState()
    cur_node = start
    last_queue_item: QueueItem | None = None
    while not problem.isGoalState(cur_node):
        adjacent_nodes: list[tuple[str,str,float]] = problem.getSuccessors(cur_node)

        for nodeinfo in adjacent_nodes:
            qitem = QueueItem(nodeinfo, last_queue_item)
            pqueue.update(qitem, qitem.cost)

        last_queue_item = pqueue.pop()
        cur_node = last_queue_item.node

        #print(f"pos: {last_queue_item.node} - path - {last_queue_item.path} cost: {last_queue_item.cost}")
        #_=input("")

    return last_queue_item.path

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
