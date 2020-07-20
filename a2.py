# The visual representation of a wall.
WALL = "\U0001F9F1"
# The visual representation of a hallway.
HALL = "\U0001F573"
# The visual representation of a brussels sprout.
SPROUT = "\U0001F353"
# Constants for the directions. Use these to make Rats move.
# The left direction.
LEFT = -1
# The right direction.
RIGHT = 1
# No change in direction.
NO_CHANGE = 0
# The up direction.
UP = -1
# The down direction.
DOWN = 1
# The letters for rat_1 and rat_2 in the maze.
RAT_1_CHAR = "\U0001F401"
RAT_2_CHAR = "\U0001F400"


class Rat:
    """ A rat caught in a maze. """
    def __init__(self, symbol, row, col):
        self.symbol = symbol
        self.row = row
        self.col = col
        self.num_sprouts_eaten = 0

    def set_location(self, row, col):
        self.row = row
        self.col = col

    def eat_sprout(self):
        self.num_sprouts_eaten += 1

    def __str__(self):
        return "{0} at ({1}, {2}) ate {3}".format(self.symbol, self.row, self.col, self.num_sprouts_eaten)


class Maze:
    """ A 2D maze. """
    def __init__(self, maze, rat_1, rat_2):
        self.maze = maze
        self.rat_1 = rat_1
        self.rat_2 = rat_2
        self.num_sprouts_left = 0
        for row in maze:
            self.num_sprouts_left += row.count(SPROUT)

    def is_wall(self, row, col):
        return self.maze[row][col] == WALL

    def get_character(self, row, col):
        if self.rat_1.row == row and self.rat_1.col == col:
            return self.rat_1.symbol
        if self.rat_2.row == row and self.rat_2.col == col:
            return self.rat_2.symbol
        return self.maze[row][col]

    def move(self, rat, ver, hor):
        if self.is_wall(rat.row+ver, rat.col+hor):
            return False
        if self.get_character(rat.row+ver, rat.col+hor) == SPROUT:
            rat.eat_sprout()
            self.num_sprouts_left -= 1
            self.maze[rat.row+ver][rat.col+hor] = HALL
        rat.set_location(rat.row+ver, rat.col+hor)
        return True

    def __str__(self,):
        maze = "\n".join(["".join(row) for row in self.maze])
        maze += "\n"
        maze += str(self.rat_1)
        maze += "\n"
        maze += str(self.rat_2)
        return maze
