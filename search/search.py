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

from typing import List

import util
from game import Directions


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
    visited = set()
    fringe = util.Stack()
    fringe.push((problem.getStartState(), [])) # (state, direction_to_reach_state)
    while not fringe.isEmpty():
        cur_state, directions = fringe.pop()

        if cur_state in visited: continue
        visited.add(cur_state)

        if problem.isGoalState(cur_state):
            return directions

        for successor, action, _ in problem.getSuccessors(cur_state):
            if successor not in visited:
                fringe.push((successor, directions + [action]))

    # Return empty list if no path found
    return directions

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    visited = set()
    fringe = util.Queue()
    fringe.push((problem.getStartState(), [])) # (state, direction_to_reach_state)
    while not fringe.isEmpty():
        cur_state, directions = fringe.pop()

        if cur_state in visited: continue
        visited.add(cur_state)

        if problem.isGoalState(cur_state):
            return directions

        for successor, action, _ in problem.getSuccessors(cur_state):
            if successor not in visited:
                fringe.push((successor, directions + [action]))

    # Return empty list if no path found
    return directions

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    visited = set()
    fringe = util.PriorityQueue()
    fringe.push((problem.getStartState(), [], 0), 0) # (state, direction_to_reach_state, acc_cost)
    while not fringe.isEmpty():
        cur_state, directions, acc_cost = fringe.pop()

        if cur_state in visited: continue
        visited.add(cur_state)

        if problem.isGoalState(cur_state):
            return directions

        for successor, action, step_cost in problem.getSuccessors(cur_state):
            if successor not in visited:
                fringe.push((successor, directions + [action], acc_cost + step_cost), acc_cost + step_cost)

    # Return empty list if no path found
    return directions

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    best_cost = {}  # Dictionary to store the best cost to each state, this is to deal with "inconsistent" heuristics
    fringe = util.PriorityQueue()
    
    # Initialize with the start state
    initial_state = problem.getStartState()
    initial_heuristic = heuristic(initial_state, problem)
    fringe.push((initial_state, [], 0), 0 + initial_heuristic) # ((state, path, accumulated_cost)

    best_cost[initial_state] = 0

    while not fringe.isEmpty():
        cur_state, directions, acc_cost = fringe.pop()

        # If the goal is found, return the path to it
        if problem.isGoalState(cur_state):
            return directions

        # Explore successors
        for successor, action, step_cost in problem.getSuccessors(cur_state):
            new_cost = acc_cost + step_cost
            if successor not in best_cost or new_cost < best_cost[successor]:
                best_cost[successor] = new_cost
                f_value = new_cost + heuristic(successor, problem)
                fringe.push((successor, directions + [action], new_cost), f_value)

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
