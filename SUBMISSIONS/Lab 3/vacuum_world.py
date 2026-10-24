# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# %pip install ipywidgets

# %%
%pip install -r requirements.txt

# %%
import math
import os, sys
# walk up from the current directory to the repo root (the one holding `aima/`)
_root = os.path.abspath(os.getcwd())
while _root != os.path.dirname(_root) and not os.path.isdir(os.path.join(_root, 'aima')):
    _root = os.path.dirname(_root)
if _root not in sys.path:
    sys.path.insert(0, _root)

# %% [markdown]
# # THE VACUUM WORLD   
#
# In this notebook, we will be discussing **the structure of agents** through an example of the **vacuum agent**. The job of AI is to design an **agent program** that implements the agent function: the mapping from percepts to actions. We assume this program will run on some sort of computing device with physical sensors and actuators: we call this the **architecture**:
#
# <h3 align="center">agent = architecture + program</h3>

# %% [markdown]
# ## Setup

# %%
# Imports
from aima.agents import *
from aima.mdp import MDP


# %%
# Helper class/functions for the environment
class DirectionType(type):
    """Fancy python trickery that allows us to use either
        >> Direction.Right
        or
        >> Direction["Right"]
    and get the same outcome (1,0)
    """
    Right = (1,0)
    Left  = (-1,0)
    Down  = (0,-1)
    Up    = (0,1)
    
    def __getitem__(self, key):
        match key.lower():
            case "right": return self.Right
            case "left": return self.Left
            case "down": return self.Down
            case "up": return self.Up
            case _: return (0,0) # default case

class Directions(metaclass=DirectionType):
    """A simple helper class for moving around a 2d grid."""
    pass

all_literal_directions = ["Right","Left","Up","Down"]

def add_direction(position, direction):
    if direction in all_literal_directions:
        direction_offset = Directions[direction]
    else:
        direction_offset = direction
    return (position[0] + direction_offset[0], position[1] + direction_offset[1])


# %% [markdown]
# ## Formatting util (since we need to display a record of the path taken)

# %%
class BoxFormatter:
    def __init__(self) -> None:
        self.contents: list[tuple[str,int]]
        self.width: int
        self.by_line: list[list[str]]

        self.contents = []
        self.width = -1
        self.by_line = []

    def append(self, itm):
        itm_str = str(itm)
        itm_data = itm_str, len(itm_str)
        self.contents.append(itm_data)
        self.update_dimensions()

    def totallen(self):
        return sum([itm[1]+1 for itm in self.contents])

    def minlen(self):
        return max([itm[1] for itm in self.contents])+1

    def target_width(self):
        largest_elem = self.minlen()
        mid_len = self.totallen() // 2
        return max(largest_elem, mid_len)

    def update_lines(self, x: int, y: int|None = None):
        self.width = x
        lines: list[list[str]] = [[]]
        cur_len = 0
        for itm in self.contents:
            itm_len = itm[1] + 1
            if cur_len + itm_len > x:
                lines += [[]]
                cur_len = 0
            lines[-1].append(itm[0])
            cur_len += itm_len

        if y is not None:
            while len(lines) < y:
                lines += [[]]

        self.by_line = lines

    def update_dimensions(self, width: int|None = None):
        if width is None:
            width = self.target_width()
        self.width = width
        self.update_lines(width)

    def get_line(self, y: int):
        full_line = ",".join(self.by_line[y])
        return full_line.center(self.width)


# %% [markdown]
# The actual environment

# %%
grid4x4 = [
    (x,y)
    for x in range(4)
    for y in range(4)
]
gridLiteral = [
    [0, 0, 0, 0,],
    [0, "X", 0, 0 ,],
    [0, 0, 0, 0 ,],
    [0,-1, 0, 10 ,],
]

gridValues = [
    [gridLiteral[3-y][x] for y in range(4)]
    for x in range(4)
] # Flips the gridLiteral so you can index it like [x][y] instead of having to do [3-y][x]
# Thus gridValues[0][0] is the bottom left, and gridValues[3][3] is the top right (the starting point)

startingLocation = (3,3)
# %%

class VacuumEnvironment2d(Environment):

    def __init__(self, gridValues):
        super().__init__()
        # We're overriding the status they set here
        self.history: list[tuple[int,int]] = []
        #self.history.append(self.default_location(None))

        self.status = {
                location: gridValues[location[0]][location[1]]
                for location in grid4x4
                }


    def execute_action(self, agent, action):
        """Score -1 for each move. Score +x, where x is the dirt level of the current tile.
        Lose no score from an action that isn't a move."""

        if action in all_literal_directions:
            agent.performance = self.status[agent.location]
            destination = add_direction(agent.location, Directions[action])
            # Only move if it is to a location inside the grid
            if destination in self.status:
                agent.location = destination
                self.history.append(destination)

    def default_location(self, thing):
        """Agents start at the top-right by default."""
        return startingLocation

    def percept(self, agent):
        """Returns the current location, its dirt level,
        and a dictionary of adjacent locations and their dirt levels.
        Ex: return (0,0), 7, {"up":0, "right":9}
        """
        neighbors = {}
        def add_neighbor(direction):
            neighbor = add_direction(agent.location, direction)
            if neighbor in self.status:
                neighbors[direction] = self.status[neighbor]

        for direction in all_literal_directions:
            add_neighbor(direction)

        return agent.location, self.status[agent.location], neighbors

    def displayPathing(self):
        """Prints a formatted grid, representing the complete history of the Agent's movement"""
        self.history = [self.default_location(None)] + self.history
        grid = [[BoxFormatter() for _ in range(4)] for _ in range(4)]
        num_moves = len(self.history)

        steps = [str(i) for i in range(num_moves)]
        if num_moves > 1:
            steps[0] = "start"
            steps[-1] = "end"
        if num_moves == 1:
            steps[0] = "start+end"

        for i, (x, y) in enumerate(self.history):
            grid[x][y].append(steps[i])

        all_widths = [box.width for row in grid for box in row if box.width > 0]
        min_x = max(all_widths) if all_widths else 1
        min_y = max([len(box.by_line) for row in grid for box in row])

        for row in grid:
            for box in row:
                box.update_lines(min_x, min_y)

        boxwidth = 1+((min_x+3)*4)
        divider = " "+("-" * boxwidth)

        grid = [
            [grid[x][3-y] for x in range(4)]
            for y in range(4)
        ]
        print(divider)
        for row in grid:
            line_count = len(row[0].by_line)
            for i in range(line_count):
                for box in row:
                    print(" | ", end="")
                    print(box.get_line(i), end="")
                print(" | ")
            print(divider)

# %% [markdown]
# ## MDP Agent
#

# %%
from aima.mdp import GridMDP, value_iteration, best_policy

# %%
# can use aima/mdp.py as reference

#all possible actions for the agent to take, and their corresponding direction offsets
actions = {(1,0): "Right", (-1,0): "Left", (0,1): "Up", (0,-1): "Down"}
class MDPVacuumAgent:
    def __init__(self, cost, gamma=0.9):
        #buid a grid from gridLiteral
        #wall becomes None, which GridMDP trats as "not a state"
        #every 0 becomes the living cost, and the 10 and -1 stay the same
        grid = [[None if val =="X" else (cost if val == 0 else val) for val in row]
                for row in gridLiteral]
        #the recharge spot and the trap in (x,y) coordinates are terminal states
        self.mdp = GridMDP(grid, terminals = [(3,0), (1,0)], init=startingLocation, gamma=gamma)
        #bellman update until it converges then returns U mapping (x,y) to utility value
        self.U = value_iteration(self.mdp, epsilon=0.001)
        #best policy picks the action with the highest expected utility in each cell
        #returns dict mapping (x,y) to action tuple
        self.policy = best_policy(self.mdp, self.U)

    def program(self, percept):
        location, dirt_value, neighbours = percept
        return actions.get(self.policy[location]) 

# %% [markdown]
# Testing different living costs:

# %%
#normal
brain = MDPVacuumAgent(-0.04)
for row in brain.mdp.to_arrows(brain.policy):
    print(" ".join(str(c) for c in row))

# %%
#desparate
brain = MDPVacuumAgent(-4)
for row in brain.mdp.to_arrows(brain.policy):
    print(" ".join(str(c) for c in row))

# %%
#stay alive
brain = MDPVacuumAgent(2)
for row in brain.mdp.to_arrows(brain.policy):
    print(" ".join(str(c) for c in row))

# %%
from aima.utils import turn_left, turn_right, vector_add
import random

class StochasticVacuumEnvironment(VacuumEnvironment2d):
    """The same environment, but moves follow the Grid World rule:
    80% in the intended direction, 10% to each side.
    The agent cannot leave the grid or enter the obstacle X."""

# Same as GridMDP.go: stay put if the move leaves the grid or hits X
    def go(self, state, direction):
        state1 = vector_add(state, direction)
        return state1 if state1 in self.status and self.status[state1] != "X" else state

    def calculate_T(self, state, action):
        return [(0.8, self.go(state, action)),
                (0.1, self.go(state, turn_right(action))),
                (0.1, self.go(state, turn_left(action)))]

    def execute_action(self, agent, action):
        if action in all_literal_directions:
            agent.performance = self.status[agent.location]
            x = random.uniform(0, 1)
            cumulative_probability = 0.0
            for probability, state in self.calculate_T(agent.location, Directions[action]):
                cumulative_probability += probability
                if x < cumulative_probability:
                    break
            if state != agent.location:
                agent.location = state
                self.history.append(state)


living_costs = {"normal": -0.04, "desperate": -4, "stay alive": 2}

for name, cost in living_costs.items():
    env = StochasticVacuumEnvironment(gridValues)
    agent = Agent(MDPVacuumAgent(cost).program)
    env.add_thing(agent)
    env.run(50)
    x, y = agent.location
    print(f"Living cost {cost} ({name})")
    print(f"History: {env.history}")
    print(f"Ended on a square with value: {gridValues[x][y]}")
    env.displayPathing()
    print()

# %%
# Bonus: showcasing the desperate-costed agent intentionally entering a negative terminal state early
env = VacuumEnvironment2d(gridValues)
env.default_location = lambda _ : (0,3)
agent = Agent(MDPVacuumAgent(-4).program)
env.add_thing(agent)
env.run(50)
x, y = agent.location
print(f"Living cost -4 (desperate)")
print(f"History: {env.history}")
print(f"Ended on a square with value: {gridValues[x][y]}")
env.displayPathing()
print()
