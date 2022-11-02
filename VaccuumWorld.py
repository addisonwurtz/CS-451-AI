# Addison Wurtz
# CS 551
# HW 1, Problem 10
import random


vacuum = "@"
clean = "_"
dirt_pile = "X"


class grid:
    def __init__(self):
        self.rooms = (["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"])

    def print_grid(self):
        print()
        print(self.rooms[0])
        print(self.rooms[1])
        print(self.rooms[2])
        print("Vacuum location: " + str(my_vacuum.row) + ", " + str(my_vacuum.col))
        print()


class vacuum:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.moves = 0
        self.dirt_piles_found = 0

    def suck(self, grid):
        # if (random.randint(0, 3) == 1):
        if grid.rooms[self.row][self.col] == dirt_pile:
            grid.rooms[self.row][self.col] = clean
            self.dirt_piles_found = self.dirt_piles_found + 1
        else:
            grid.rooms[self.row][self.col] = dirt_pile
            print("dropped dirt!")
            #self.dirt_piles_found = self.dirt_piles_found - 1
        self.moves += 1

    def suck(self, grid, num_dirt_piles):
        # if (random.randint(0, 3) == 1):
        if grid.rooms[self.row][self.col] == dirt_pile:
            grid.rooms[self.row][self.col] = clean
            self.dirt_piles_found = self.dirt_piles_found + 1
        else:
            grid.rooms[self.row][self.col] = dirt_pile
            print("dropped dirt!")
            num_dirt_piles += 1
        self.moves += 1
        return num_dirt_piles

    def up(self):
        # print('up')
        if (self.row != 0):
            self.row = self.row - 1
        self.moves = self.moves + 1

    def down(self):
        # print('down')
        if self.row != 2:
            self.row = self.row + 1
        self.moves = self.moves + 1

    def right(self):
        # print('right')
        if self.col != 2:
            self.col = self.col + 1
        self.moves = self.moves + 1

    def left(self):
        # print('left')
        if self.col != 0:
            self.col = self.col - 1
        self.moves = self.moves + 1


def generate_vacuum_world(vacuum, grid, num_dirt_piles):
    row = 0
    col = 0
    for i in range(0, 2):
        for j in range(0, 2):
            grid.rooms[i][j] = '_'

    dirty_rooms = random.sample(range(0, 8), num_dirt_piles)
    for num in dirty_rooms:
        if num == 0:
            grid.rooms[0][0] = dirt_pile
        if num == 1:
            grid.rooms[0][1] = dirt_pile
        if num == 2:
            grid.rooms[0][2] = dirt_pile
        if num == 3:
            grid.rooms[1][0] = dirt_pile
        if num == 4:
            grid.rooms[1][1] = dirt_pile
        if num == 5:
            grid.rooms[1][2] = dirt_pile
        if num == 6:
            grid.rooms[2][0] = dirt_pile
        if num == 7:
            grid.rooms[2][1] = dirt_pile
        if num == 8:
            grid.rooms[2][2] = dirt_pile

    vacuum.row = random.randint(0, 2)
    vacuum.col = random.randint(0, 2)


# Simple Reflex Agent
def reflex_agent_trial(my_vacuum, grid, num_dirt_piles):
    generate_vacuum_world(my_vacuum, grid, num_dirt_piles)
    grid.print_grid()

    for x in range(50):
        # print('row = ' + str(my_vacuum.row) + ', col = ' + str(my_vacuum.col))
        if (my_vacuum.dirt_piles_found == num_dirt_piles):
            break
        if grid.rooms[my_vacuum.row][my_vacuum.col] == dirt_pile:
            if (random.randint(0, 9) != 0):
                my_vacuum.suck(grid)
        elif (random.randint(0, 9) == 0):
            my_vacuum.suck(grid)
            num_dirt_piles = num_dirt_piles + 1
        elif my_vacuum.row == 0:
            if my_vacuum.col == 0:
                my_vacuum.right()
            elif my_vacuum.col == 1:
                if my_vacuum.moves % 3 == 0:
                    my_vacuum.down()
                else:
                    my_vacuum.right()
            elif my_vacuum.col == 2:
                my_vacuum.down()
        elif my_vacuum.row == 1:
            if my_vacuum.col == 0:
                if my_vacuum.moves % 3 == 0:
                    my_vacuum.right()
                else:
                    my_vacuum.up()
            if my_vacuum.col == 1:
                if my_vacuum.moves % 2 == 1:
                    my_vacuum.up()
                else:
                    my_vacuum.down()
            if my_vacuum.col == 2:
                if my_vacuum.moves % 3 == 0:
                    my_vacuum.left()
                else:
                    my_vacuum.down()
        elif my_vacuum.row == 2:
            if my_vacuum.col == 0:
                my_vacuum.up()
            if my_vacuum.col == 1:
                my_vacuum.left()
            if my_vacuum.col == 2:
                my_vacuum.left()

# randomized agent


def random_agent_trial(my_vacuum, grid, num_dirt_piles):
    generate_vacuum_world(my_vacuum, grid, num_dirt_piles)
    grid.print_grid()

    for x in range(100):
        #print('row = ' + str(my_vacuum.row) + ', col = ' + str(my_vacuum.col))
        if (my_vacuum.dirt_piles_found == num_dirt_piles):
            break
        else:
            rand_num = random.randint(0, 4)
            if rand_num == 0:
                if (random.randint(0, 9) != 0):
                    num_dirt_piles = my_vacuum.suck(grid, num_dirt_piles)
            if rand_num == 1:
                my_vacuum.up()
            if rand_num == 2:
                my_vacuum.down()
            if rand_num == 3:
                my_vacuum.left()
            if rand_num == 4:
                my_vacuum.right()


# Trials Agent
moves_sum = 0
dirt_piles_collected_sum = 0
for trial in range(0, 99):
    my_vacuum = vacuum()
    my_grid = grid()
    #reflex_agent_trial(my_vacuum, my_grid, 5)
    random_agent_trial(my_vacuum, my_grid, 5)
    moves_sum += my_vacuum.moves
    dirt_piles_collected_sum += my_vacuum.dirt_piles_found
print("Average number of moves = " + str(moves_sum/100))
print("Average number of dirt piles collected = " +
      str(dirt_piles_collected_sum/100))
