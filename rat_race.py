from tkinter.messagebox import showinfo
import tkinter
import tkinter.filedialog
import tkinter.font
from maze import random_maze
import a2
import os
import sys

# True if you want the maze to be printed as well as shown in the window.
PRINT_MAZE = True

# The font for the rat race.
FONT = ('Courier New', 18, 'bold')

# Up, down, left, right for player 1.
RAT_1_KEYS = {
    'w': (a2.UP, a2.NO_CHANGE),
    'a': (a2.NO_CHANGE, a2.LEFT),
    's': (a2.DOWN, a2.NO_CHANGE),
    'd': (a2.NO_CHANGE, a2.RIGHT)
}

# Up, down, left, right for player 2.
RAT_2_KEYS = {
    'i': (a2.UP, a2.NO_CHANGE),
    'j': (a2.NO_CHANGE, a2.LEFT),
    'k': (a2.DOWN, a2.NO_CHANGE),
    'l': (a2.NO_CHANGE, a2.RIGHT)
}


class MazeApp(tkinter.Frame):
    """ The frame for the maze in the window. """

    def __init__(self, parent, maze):
        """ (MazeApp, Tk, Maze) -> NoneType

        Set up the window.  parent is the root window; maze is the
        Maze object.
        """

        super().__init__(parent, background="white")
        self.parent = parent
        self.the_maze = maze
        self.parent.title("Rat Race Game!")

        self.parent.resizable(width=False, height=False)
        self.pack(fill=tkinter.BOTH, expand=1)

        button1 = tkinter.Button(
            parent, text="See Controls", padx=10, pady=5, command=controls)
        button = tkinter.Button(parent, text="End Game",
                                padx=10, pady=5, command=parent.destroy)
        maze_frame = tkinter.Frame(parent, background="white")
        maze_frame.pack(fill=tkinter.BOTH, expand=1)

        self.make_maze_labels(maze_frame)
        self.bind_player_keys()

        # Frame for the scores.
        score_frame = tkinter.Frame(parent, background="white")
        score_frame.pack()
        button.pack(side=tkinter.BOTTOM)
        button1.pack(side=tkinter.BOTTOM)

        # rat_1's and rat_2's scores.
        self.rat_1_score_var = tkinter.IntVar()
        self.rat_2_score_var = tkinter.IntVar()

        # Display rat_1's score.
        self.display_score(score_frame, self.rat_1_score_var, a2.RAT_1_CHAR)
        self.display_score(score_frame, self.rat_2_score_var, a2.RAT_2_CHAR)
        # # Display rat_2's score.
        # tkinter.Label(score_frame, text="rat_2: ", font=FONT).pack(
        #     side=tkinter.LEFT, padx=(10, 0))
        # rat_2_score_lbl = tkinter.Label(
        #     score_frame, textvariable=self.rat_2_score_var, font=FONT)
        # rat_2_score_lbl.pack(side=tkinter.LEFT, padx=(0, 10))
        # self.rat_2_score_var.set(0)

        if PRINT_MAZE:
            print(self.the_maze)

    def bind_player_keys(self):
        """ (MazeApp) -> NoneType

        Bind the keys for the two players.
        """

        # Bind the keystrokes.
        for ch in RAT_1_KEYS:
            self.bind_all(ch, self.rat_1_keystroke)

        for ch in RAT_2_KEYS:
            self.bind_all(ch, self.rat_2_keystroke)

    def make_maze_labels(self, maze_frame):
        """ (MazeApp, Frame) -> NoneType

        Make a grid of Labels with backing StringVars so that we can
        update the picture of the maze.
        """

        self.the_maze_vars = []
        for r in range(len(self.the_maze.maze)):

            # Start a new row.
            self.the_maze_vars.append([])

            for c in range(len(self.the_maze.maze[r])):
                self.make_label(r, c, maze_frame)

    def display_score(self, score_frame, score_var, label_text):
        """ (MazeApp, Frame, IntVar, str) -> NoneType

        Add a label for the label_text and a label for the score_var to score_frame.
        """

        tkinter.Label(score_frame, text=label_text, font=FONT).pack(
            side=tkinter.LEFT, padx=(10, 0))
        score_lbl = tkinter.Label(
            score_frame, textvariable=score_var, font=FONT)
        score_lbl.pack(side=tkinter.LEFT, padx=(0, 10))
        score_var.set(0)

    def make_label(self, r, c, maze_frame):
        """ (MazeApp, int, int) -> NoneType

        Create a Label and a backing StringVar.  Also add the StringVar to
        the_maze_vars so we can change the text of the Label as the players
        move.
        """
        ch = self.the_maze.get_character(r, c)
        labelvar = tkinter.StringVar()
        lbl = tkinter.Label(maze_frame, textvariable=labelvar, font=FONT)
        lbl.grid(row=r, column=c)
        labelvar.set(ch)
        self.the_maze_vars[r].append(labelvar)

    def redraw(self):
        """ (MazeApp) -> NoneType

        Reset the StringVars.
        """

        for r in range(len(self.the_maze.maze)):
            for c in range(len(self.the_maze.maze[r])):
                self.the_maze_vars[r][c].set(
                    self.the_maze.get_character(r, c))

        if PRINT_MAZE:
            print(self.the_maze)

    def rat_1_keystroke(self, event):
        """ (MazeApp, Event) -> NoneType

        React to keystroke event for player 1.
        """

        self.the_maze.move(self.the_maze.rat_1,
                           RAT_1_KEYS[event.char][0],
                           RAT_1_KEYS[event.char][1])
        self.rat_1_score_var.set(self.the_maze.rat_1.num_sprouts_eaten)
        self.redraw()

    def rat_2_keystroke(self, event):
        """ (MazeApp, Event) -> NoneType

        React to keystroke event for player 2.
        """

        self.the_maze.move(self.the_maze.rat_2,
                           RAT_2_KEYS[event.char][0],
                           RAT_2_KEYS[event.char][1])
        self.rat_2_score_var.set(self.the_maze.rat_2.num_sprouts_eaten)
        self.redraw()


def controls():
    showinfo("Controls To Play", '''           Moves\nMouse\t    Rat\nW --> Up       I --> Up
A --> Left      J --> Left\nS --> Down   K --> Down\nD --> Right   L --> Right''')


def find_rats_replace_hallway(maze_list):
    """ (list of list of str) -> (Rat, Rat) tuple

    Return the two Rats in a list.  Also modify maze_list so that the rat
    chars are replaced with HALL chars.
    """

    for r in range(len(maze_list)):
        for c in range(len(maze_list[r])):

            if maze_list[r][c] == a2.RAT_1_CHAR:
                rat_1 = a2.Rat(a2.RAT_1_CHAR, r, c)
                maze_list[r][c] = a2.HALL
            elif maze_list[r][c] == a2.RAT_2_CHAR:
                rat_2 = a2.Rat(a2.RAT_2_CHAR, r, c)
                maze_list[r][c] = a2.HALL

    return (rat_1, rat_2)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # pylint: disable=no-member
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main():
    root = tkinter.Tk()
    root.iconbitmap(resource_path(r'rat.ico'))

    maze_list = random_maze()
    rat_1, rat_2 = find_rats_replace_hallway(maze_list)
    the_maze = a2.Maze(maze_list, rat_1, rat_2)
    app = MazeApp(root, the_maze)
    app.mainloop()


if __name__ == '__main__':
    main()
