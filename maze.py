import random
import a2


def random_maze():
    side = random.randint(10, 20)
    maze = [[a2.HALL]*side for i in range(side)]
    for i in range(side):
        maze[0][i] = a2.WALL
        maze[side - 1][i] = a2.WALL
        maze[i][0] = a2.WALL
        maze[i][side-1] = a2.WALL

# Blocks
    for i in range(1, side-1):
        for _ in range(random.randint(1, (side % 5)+1)):
            index = random.randint(1, side-1)
            maze[i][index] = a2.WALL

# Food
    food_items = (random.randint(1, abs((side-3-random.randint(1, 6))%7)+1))%10 + (side%40)
    for _ in range(food_items):
        row = random.randint(1, side-2)
        col = random.randint(1, side-2)
        maze[row][col] = a2.SPROUT

# Position Of J
    maze[random.randint(1, side-2)][random.randint(1, side-2)] = a2.RAT_1_CHAR
# Position Of P
    maze[random.randint(1, side-2)][random.randint(1, side-2)] = a2.RAT_2_CHAR

# buffer data
    return maze
