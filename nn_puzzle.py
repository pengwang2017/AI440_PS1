"""The NNPuzzle search problem, for generating arbitrary (N^2)-1 puzzles"""

import sys
import random
import math
from search import SearchProblem


class NNPuzzle(SearchProblem):
    """A Puzzle problem formulated as a 'SearchProblem'"""

    def __init__(self, n=3):
        SearchProblem.__init__(self)  # to placate pylint
        self.goal = tuple([r for r in range(0, n*n)])
        self.n = n

    def isgoal(self, state):
        """A goal test for the NNPuzzle"""
        return state == self.goal


    def actions(self, state):
        """Returns a list of actions available in the specified state.

        This is some subset of ['Up', 'Down', 'Left', 'Right'] based on the
        location of the empty tile"""

        actions = []

        blank_index = state.index(0)
        blank_row = blank_index // self.n
        blank_col = blank_index % self.n

        # can we move down?
        if blank_row < (self.n-1):
            actions.append('Down')
        # can we move up?
        if blank_row > 0:
            actions.append('Up')
        # can we move left?
        if blank_col > 0:
            actions.append('Left')
        # can we move right?
        if blank_col < (self.n-1):
            actions.append('Right')

        return actions

    def result(self, state, action):
        """Returns a (cost, new state) pair where
        'cost' is the cost of performing the action in the specified state
        'new state' is the state that results from applying the  specified
            action to the specified state"""

        blank_index = state.index(0)
        blank_row = blank_index // self.n
        blank_col = blank_index % self.n
        new_state = list(state)  # copy the state into the new state

        # now, we just need to swap two values
        if action == 'Up': # move the blank up
            new_state[blank_index] = state[(blank_row-1)*self.n + blank_col]
            new_state[(blank_row-1)*self.n + blank_col] = 0

        elif action == 'Down': # move the blank down
            new_state[blank_index] = state[(blank_row+1)*self.n + blank_col]
            new_state[(blank_row+1)*self.n + blank_col] = 0

        elif action == 'Left': # move the blank left
            new_state[blank_index] = state[(blank_row)*self.n + blank_col-1]
            new_state[(blank_row)*self.n + blank_col-1] = 0

        elif action == 'Right': # move the blank right
            new_state[blank_index] = state[(blank_row)*self.n + blank_col+1]
            new_state[(blank_row)*self.n + blank_col+1] = 0

        return (tuple(new_state), 1)

    def display(self, state_action_pair, stream=sys.stdout):
        """Display the state of the puzzle on the specified output stream"""
        s, a = state_action_pair
        n = self.n

        tilesize = int(math.log10(n*n) + 1)
        blanks = '   '
        border = blanks + '-'*((tilesize+3)*self.n+1)
        tileformat = '{0:>'+str(tilesize)+'s}'

        print(border, file=stream)
        for r in range(n):
            row = [blanks, '| ']
            for c in range(n):
                row.append(tileformat.format(str(s[r*self.n+c])))
                row.append(' | ')
            print(''.join(row), file=stream)
            print(border, file=stream)
        print(blanks+"Moving: ", a, file=stream)

    def get_shuffled_state(self, steps):
        """Generate a valid state by shuffling the puzzle"""
        state = self.goal
        for _ in range(steps):
            actions = self.actions(state)
            state = self.result(state, random.choice(actions))[0]
        return state
