# CMPT 317: Block Tiling Problem Model Solution for Local Search

# Copyright (c) 2022, Jeff Long
# Department of Computer Science, University of Saskatchewan

# This file is provided solely for the use of CMPT 317 students.  Students are permitted
# to use this file for their own studies, and to make copies for their own personal use.

# This file should not be posted on any public server, or made available to any party not
# enrolled in CMPT 317.

# This implementation is provided on an as-is basis, suitable for educational purposes only.
#
import random
import random as rand
import math as M

class State(object):
    """The Problem State is an array of Boolean values, which we represent by a nested list.  True means a green tile, False a red tile.
       
    """
    def __init__(self, gridsize, blocks, used, library, grid=None):
        """
        Initialize the State object.
        
        gridsize: Integer. The size of a square grid to fill
        blocks: Dictionary mapping block names to the number
                still available of that block
        used: List-of-tuples indicating which blocks have been
            placed on the grid and where
        library: Dictionary mapping block names to what they
            look like.  This is NOT copied, but just for reference
        
        """
        self.N = gridsize

        # create a copy of the available block counts
        self.blocks = dict(blocks)

        # create a copy of current block locations
        self.used = [x for x in used]

        # DON'T copy the library, there's no need since
        # it shouldn't change
        self.lib = library

        # store the grid contents to make it easier 
        # to check if pieces can be added later
        if grid == None:
            # if no grid is given, make a blank one
            self.grid = self.make_grid(self.N)
        else:
            # if a grid is given, copy it
            self.grid = []
            for row in grid:
                new_row = [x for x in row]
                self.grid.append(new_row)


    def make_grid(self, N):
        """ creates a list-of-lists-of-strings that represents the 
        grid.
        We pad it with a border to make the logic for 
        out-of-bounds checks easier.
        
        . means empty, * means block, # means border
        
        N: integer, the size of the grid
        """
        grid = []
        for i in range(N):
            row = ["."] * N + ["#"] * 3
            grid.append(row)
        for j in range(3):
            row = ["#"] * (N+3)
            grid.append(row)

        return grid

    def place_block(self, b, row, col):
        """ places the block b onto the grid at the given
        row and col location.
        
        pre-condition: the placement is legal
        """
        move = (b, row, col)
        self.blocks[b] -= 1
        self.used.append(move)
        shape = self.lib[b]
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x] == "*":
                    self.grid[row+y][col+x] = shape[y][x]

    def remove_block(self, b, row, col):
        """ remove a block from the grid at location row, col
        
        pre-condition: there is a correct block at that location
        """
        move = (b, row, col)
        self.blocks[b] += 1
        self.used.remove(move)
        shape = self.lib[b]
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x] == "*":
                    self.grid[row+y][col+x] = "."

    def legal_move(self, b, row, col):
        """ returns true if it is legal to place block b
        at location row, col
        """
        # No block of that type
        if b not in self.blocks or self.blocks[b] < 1:
            return False

        legal = True
        shape = self.lib[b]
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x] == "*":
                    if self.grid[row+y][col+x] != ".":
                        legal = False
        return legal

    def __str__(self):
        """ A string representation of the State 
        Display the grid, cutting off the internal padding,
        and the number of blocks remaining """
        s = []
        for row in self.grid:
            row = "".join(row[0:-3])
            s.append(row)

        s = s[0:-3]
        s = "\n".join(s)
        s += "\n"
        s += "Block locations: \n"
        s += str(self.used)
        s += "\n"
        s += "Fitness score:\n"
        s += str(self.get_score())
        s += "\n"
        s += "Unused blocks: \n"
        s += str(self.blocks)
        return s

    def __eq__(self, other):
        """ Two states are the same if they have put the blocks
        in the same place and have the same blocks left.
        
        """
        # use 'set()' because we don't care about order
        # of blocks in the list of used blocks
        return set(self.used) == set(other.used) and self.blocks == other.blocks



    def get_score(self):
        """ compute the fitness score for a state
        """
        #TODO: Decide on a fitness score, implement it
        # fitness score = number of empty grid spaces
        empty_grid_spaces = 0                       # Initialize number of empty grid spaces to 0
        for y in range(len(self.grid)):             # Loop through all columns in grid
            for x in range(len(self.grid[y])):      # Loop through all rows in grid
                if self.grid[y][x] == ".":          # Check if grid space is empty
                    empty_grid_spaces += 1          # Increment total number of empty grid spaces if empty
        return empty_grid_spaces                    # Return total number of empty grid spaces


    def is_better_than(self, other):
        """ 
            Return True if self is a better solution than other.
            Smaller score is better.
            :param: other: a State object
            :return: boolean
        """

        return self.get_score() < other.get_score()

    def is_equal_to(self, other):
        """ 
            Return True if self is as good a solution as other
            :param: other: a State object
            :return: boolean
        """
        return self.get_score() == other.get_score()

    def quantity_of_block_remaining(self, block):
        """
            Return True if remaining quantity of given block is greater than one
            :param: str: a block
            :return: boolean
        """
        if self.blocks[block] > 0:
            return True
        else:
            return False


class Problem(object):
    """The Problem class defines aspects of the problem.

    """

    def __init__(self, gridsize, blocks):
        """ The problem is defined by an empty grid.
        We want to place blocks to cover as much
        of the grid as possible.

            :param gridsize: dimension for a square grid
            :param blocks: dictionary mapping block names
                to the number available of that block
        """
        # dimensions of the grid to fill
        self.N = gridsize

        # initial available blocks
        self.blocks = blocks

        # show which spaces on a grid each block
        # would actually cover
        self.library = { "+" : [".*.",
                                "***",
                                ".*."],
                         "|" : ["*",
                                "*",
                                "*",
                                "*"],
                         "L" : ["*..",
                                "*..",
                                "***"],
                         "Z" : ["**.",
                                ".**"],
                         "T" : ["***",
                                ".*.",
                                ".*."],
                         "4" : ["*.", # ok it doesn't really look like a 4...
                                "**",
                                ".*"],
                        }


    def create_initial_state(self):
        """ returns an initial state.
        """
        s = State(self.N, self.blocks, [], self.library)
        return s

    def objective_function(self, state):
        """
            score calculation is done at the state level
        """
        return state.get_score()

    def n_choose_k(self, n, k):
        return M.factorial(n) / ( M.factorial(n-k) * M.factorial(k) )

    def random_state(self):
        """ Return a random State, completely independent of any other State.
    
        """
        #TODO: Implement an algorithm that will generate a reasonably random state
        # Place a random number of blocks on the grid at random points if allowed
        shapes = {0: "+", 1: "|", 2: "L", 3: "Z", 4: "T", 5: "4"}
        state = self.create_initial_state()
        total_number_of_blocks = sum(self.blocks.values())
        number_of_random_blocks = random.randint(0, total_number_of_blocks)
        number_of_random_attempts = random.randint(1, 100)
        print('Number of random blocks trying to place: ' + str(number_of_random_blocks) + '\nNumber of random attempts to place each block: ' + str(number_of_random_attempts))
        while number_of_random_blocks > 0:
            block = shapes[random.randint(0, 5)]
            move_successful = False
            if state.quantity_of_block_remaining(block):
                #print('Trying to place block: ' + str(block))
                attempts_remaining = number_of_random_attempts
                while attempts_remaining > 0 and move_successful == False:
                    place_x = random.randint(0, self.N - 1)
                    place_y = random.randint(0, self.N - 1)
                    if state.legal_move(block, place_x, place_y):
                        state.place_block(block, place_x, place_y)
                        move_successful = True
                        #print('SUCCESSFULLY placed at position (' + str(place_x) + ',' + str(place_y) + ')')
                    #else:
                        #print('FAILED to place at position (' + str(place_x) + ',' + str(place_y) + ')')
                    attempts_remaining -= 1
                number_of_random_blocks -= 1
        return state


    def neighbors(self, s):
        """ return a list of all neighbors of the given state.
    
      
        """
        # list of states that are neighbors to the given state
        neighbors = []
        shapes = {0: "+", 1: "|", 2: "L", 3: "Z", 4: "T", 5: "4"}
        # example of how to make one copy of the given state, s

        #TODO: Define a neighborhood and fill the list of neighbors
        # with all the neighboring states to s
        new_state = State(s.N, s.blocks, s.used, s.lib, s.grid)
        # Remove each block
        for i in range(len(s.used)):
            move = s.used[i]
            block = move[0]
            x_pos = move[1]
            y_pos = move[2]
            new_state.remove_block(block, x_pos, y_pos)
            neighbors.append(new_state)
            new_state = State(s.N, s.blocks, s.used, s.lib, s.grid)
        new_state = State(s.N, s.blocks, s.used, s.lib, s.grid)
        # Add each type of block
        for i in range(5):
            block = shapes[i]
            # at each possible location
            for y in range(self.N - 1):  # Loop through all columns in grid
                for x in range(self.N - 1):  # Loop through all rows in grid
                    if s.legal_move(block, x, y):
                        new_state.place_block(block, x, y)
                        neighbors.append(new_state)
                        new_state = State(s.N, s.blocks, s.used, s.lib, s.grid)
        return neighbors

    def random_step(self, state):
        """ Return a State that is a random neighbour of the given State.
            :param: state: A State object
        """
        A = self.neighbors(state)
        return rand.choice(A)


    def best_step(self, state):
        """ Return the best neighbouring State for the given State.
            It doesn't have to be better than the given State!
            :param: state: A State object
        """
        A = self.neighbors(state)
        best = A[0]
        for s in A:
            if s.get_score() < best.get_score():
                best = s
        return best

    def random_better(self, state):
        """ Return a State that is a random BETTER neighbour of the given State.
            Should return None if there isn't one!
            :param: state: A State object
        """
        better = []
        A = self.neighbors(state)
        for s in A:
            if s.get_score() < state.get_score():
                better.append(s)

        if len(better) > 0:
            return rand.choice(better)
        else:
            return None





# end of file

