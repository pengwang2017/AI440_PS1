"""Base classes for search/search problems, ala Russell and Norvig"""
import sys

class SearchProblem():
    """A minimalist representation of a problem to be solved using search"""

    def __init__(self):
        pass

    def isgoal(self, state):
        """Checks whether the specified state statisfies the goal condition"""
        return True

    def actions(self, state):
        """Returns a (possibly empty) list of action names (strings)
           that can be executed in the specified state"""

        return []

    def result(self, state, action):
        """Computes the new state that results from taking the specified action
        in the supplied state"""

        return None

    def display(self, state_action_pair, stream=sys.stdout):
        """Prints the state and action in a meaninful way to the output stream"""
        pass


class Search():
    """A Base Class for Search Algorithms"""

    def __init__(self, problem):
        """Initialize by passing in a SearchProblem instance.
        This is stored for use by the other methods"""

        self.problem = problem

    def search(self, initial_state):
        """Here, perform a search from the specified initial_state to a
        state that satisfies the goal test of the SearchProblem.
        We assume that the inital_state supplied is meaningful and valid.

        The result of this method should either:
         - None, if no solution is found
         - A search tree node that satisfies the search problem's goal test.

        NOTE: this is slightly different than the book's function, as we don't
        return the solution path -- but instead must get that from a call to
        solution() using the node returned here...

        Each particular Search algorithm may allow solution nodes to be
        queried in a variety of ways. ALL algorithms must support
        solution() though.
         """
        pass

    def child_node(self, parent_node, action):
        """Create a child node for this search tree given a parent
        search tree node and an action to execute. Don't confuse nodes
        in the search-tree and verticies in the state-space graph."""
        pass

    def parent(self, node):
        """Return the parent of the specified node in the search tree"""
        pass

    def solution(self, search_node):
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
        pass
