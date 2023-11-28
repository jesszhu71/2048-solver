from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

# MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MOVES = {0: 'left', 1: 'up', 2: 'right', 3:'down'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (state[0], state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        if (len(self.children) == 0):
            return True
        else:
            return False
        # pass

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions: 
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move
    def print_board(self, mat):
        print("--------------------")
        for i in mat:
            print(i)
        print("--------------------")

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node = None, depth = 0):
        # pass
        # print("tree", depth)
        # self.print_board(self.simulator.tile_matrix)
        if depth == 0:
            return
        if (node == None):
            return
        # build current node?
        if node.player_type == MAX_PLAYER:
            # print("curr is max")
            for dir in range(4):
                # print("Direction: " + MOVES[dir])
                if (self.simulator.move(dir)):
                    # yes 
                    newNode = Node(self.simulator.current_state(), CHANCE_PLAYER)
                    node.children.append((dir, newNode))
                    # self.print_board(self.simulator.tile_matrix)
                    self.build_tree(newNode, depth-1)
                self.simulator.undo()
                # print("fall back to:")
                # self.print_board(self.simulator.tile_matrix)
        elif node.player_type == CHANCE_PLAYER:
            # print("curr is chance")
            open_tiles = self.simulator.get_open_tiles()
            for space in open_tiles:
                # can be 2:
                i, j = space
                self.simulator.addToUndo()
                # print("placing at", i," ", j)
                self.simulator.tile_matrix[i][j] = 2
                newNode = Node(self.simulator.current_state(), MAX_PLAYER)
                # self.print_board(self.simulator.tile_matrix)
                node.children.append((None, newNode))
                # print(self.simulator.tile_matrix)
                self.build_tree(newNode, depth-1)
                self.simulator.undo()
                # print("fall back to:")
                # self.print_board(self.simulator.tile_matrix)
                    # self.simulator.tile_matrix[i][j] = 0
        else:
            return "error"
        return



    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER

    # utility(u, player)
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        # return random.randint(0, 3), 0
        # print("expectimax " + str(node.player_type) + str((node.children)))

        # does node=None mean we aare at the root node?
        if node == None:
            print("idk bro")
            return

        if node.is_terminal():
            # return node.compute_decision() #payoff(node)
            # print("is terminal")
            # print("terminal", node.state[1])
            return (None, node.state[1])
        elif node.player_type == MAX_PLAYER:
            # print("is max player")
            value = (None, float('-inf'))
            for n in node.children:
                dir, state = n
                swipe, val = self.expectimax(state)
                if (value[1] < val):
                    value = (dir, val)
            # print("max val ", value[1])
            return value
        elif node.player_type == CHANCE_PLAYER:
            # print("is chance player")
            # value = float('inf')
            value = 0
            chance = 1/len(node.children)
            for n in node.children:
                # value = min(value, self.expectimax(n))
                dir, state = n
                dir, val = self.expectimax(state)
                value = value + val*chance # whats chance
            # print("chance", value)
            return (None, value)
        else:
            return "error"

    # Return decision at the root
    def compute_decision(self):
        # print("depth", self.search_depth)
        self.build_tree(self.root, self.search_depth)
        # print("tree built")
        # print(self.root.children)
        direction, _ = self.expectimax(self.root)
        # print("direction", direction)
        # print("compute 3")
        return direction
    
    # def ab_minimax(self, node, alpha, beta):
    #     if node == None:
    #         print("idk bro")
    #         return

    #     if node.is_terminal():
    #         # return node.compute_decision() #payoff(node)
    #         # print("is terminal")
    #         return (None, node.state[1])
    #     elif node.player_type == MAX_PLAYER:
    #         # print("is max player")
    #         value = (None, float('-inf'))
    #         for n in node.children:
    #             dir, state = n
    #             swipe, val = self.ab_minimax(state, alpha, beta)
    #             if (value[1] < val):
    #                 value = (dir, val)
    #             alpha = max(alpha, value[1])
    #             # print("alpha", alpha)
    #             if (alpha >= beta):
    #                 break
    #         return value
    #     elif node.player_type == CHANCE_PLAYER:
    #         # print("is chance player")
    #         # value = float('inf')
    #         value = 0
    #         chance = 1/len(node.children)
    #         for n in node.children:
    #             # value = min(value, self.expectimax(n))
    #             dir, state = n
    #             dir, val = self.ab_minimax(state, alpha, beta)
    #             value = value + val*chance # whats chance
    #             beta = min(beta, value)
    #         # beta = max(beta, value)
    #             # print("beta", beta)
            
    #         return (None, value)
    #     else:
    #         return "error"
    def expectimax2(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        # return random.randint(0, 3), 0
        # print("expectimax " + str(node.player_type) + str((node.children)))

        # does node=None mean we aare at the root node?
        if node == None:
            print("idk bro")
            return

        if node.is_terminal():
            # return node.compute_decision() #payoff(node)
            # print("is terminal")
            # print("terminal", node.state[1])
            return (None, node.state[1])
        elif node.player_type == MAX_PLAYER:
            # print("is max player")
            value = (None, float('-inf'))
            for n in node.children:
                dir, state = n
                swipe, val = self.expectimax2(state)
                if (value[1] < val):
                    value = (dir, val)
            # print("max val ", value[1])
            return value
        elif node.player_type == CHANCE_PLAYER:
            # print("is chance player")
            # value = float('inf')
            value = 0
            chance = 1/len(node.children)
            for n in node.children:
                # value = min(value, self.expectimax(n))
                dir, state = n
                dir, val = self.expectimax2(state)
                value = value + val*chance # whats chance
            # print("chance", value)
            return (None, value)
        else:
            return "error"
    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        # return random.randint(0, 3)
        self.build_tree(self.root, 3)
        alpha = float('-inf')
        beta = float('inf')
        # direction, _ = self.ab_minimax(self.root, alpha, beta)
        direction, _ = self.expectimax2(self.root)
        return direction


