# -*- coding: utf-8 -*-

from tkinter import *


class Menubar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master, bd=2, relief=GROOVE)

        filebutton = Menubutton(self, text="File")
        filebutton.pack(side=LEFT)
        filemenu = Menu(filebutton, tearoff=0)
        filemenu.add_command(label="New", command=master.new)
        filemenu.add_command(label="Options", command=master.options)
        filemenu.add_command(label="Exit", command=master.quit)
        filebutton.configure(menu=filemenu)

        helpbutton = Menubutton(self, text="Help")
        helpbutton.pack(side=LEFT)
        helpmenu = Menu(helpbutton, tearoff=0)
        helpmenu.add_command(label="Instructions",
                             command=lambda: master.popup(Ping.instructions))
        helpmenu.add_command(label="About",
                             command=lambda: master.popup(Ping.about))
        helpbutton.configure(menu=helpmenu)


class Gametable(Frame):

    def __init__(self, master, canvas_width, canvas_height):
        Frame.__init__(self, master)

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.canvas = Canvas(self, bg=master.maincolor, highlightthickness=0,
                             width=canvas_width, height=canvas_height)
        self.canvas.bind("<Button-1>", self.flip_neighbours)
        self.canvas.pack(pady=10, padx=10)

        self.rows, self.columns = 4, 4
        self.drawgrid()

    def drawgrid(self):
        """Draw the game grid on the canvas."""

        # create a list to represent the game's state:
        # 0 for a black circle, 1 for white
        self.state = []
        row = [1] * self.columns
        for i in range(self.rows):
            self.state.append(row.copy())

        self.canvas.delete(ALL)
        # determine grid size based on the canvas' size
        self.gridsize = min(self.canvas_width / self.rows,
                            self.canvas_height / self.columns)
        # resize the canvas
        width = self.columns * self.gridsize
        height = self.rows * self.gridsize
        self.canvas.configure(width=width, height=height)
        # draw horizontal lines
        for i in range(1, self.rows):
            self.canvas.create_line(
                0, i * self.gridsize, width, i * self.gridsize,
                fill=self.master.altcolor)
        # draw vertical lines
        for i in range(1, self.columns):
            self.canvas.create_line(
                i * self.gridsize, 0, i * self.gridsize, height,
                fill=self.master.altcolor)
        self.drawstate()

    def drawstate(self):
        """Draw the pieces on the board."""

        for row in range(self.rows):
            for column in range(self.columns):
                # if the given piece is on its white side,
                # this expression is 1
                if self.state[row][column]:
                    self.canvas.create_oval(column * self.gridsize + 5,
                                            row * self.gridsize + 5,
                                            (column + 1) * self.gridsize - 5,
                                            (row + 1) * self.gridsize - 5,
                                            fill="white", width=0)
                else:
                    self.canvas.create_oval(column * self.gridsize + 5,
                                            row * self.gridsize + 5,
                                            (column + 1) * self.gridsize - 5,
                                            (row + 1) * self.gridsize - 5,
                                            fill="black", width=0)

    def flip_neighbours(self, event):
        """Flip the surrounding pieces of the selected piece."""

        row = int(event.y / self.gridsize)
        col = int(event.x / self.gridsize)
        for i in (row - 1, row, row + 1):
            for j in (col - 1, col, col + 1):
                if self.valid(i, j) and (i, j) != (row, col):
                    self.state[i][j] = not self.state[i][j]
        self.drawstate()
        if self.over():
            self.master.popup("Congratulations! You solved the puzzle!")

    def valid(self, row, column):
        """Return a boolean of whether grid is valid."""

        if (0 <= row < self.rows) and (0 <= column < self.columns):
            return True
        else:
            return False

    def over(self):
        """Check if the game has been solved yet."""

        for row in self.state:
            for grid in row:
                # if any of the grids are one, the game hasn't been solved yet
                if grid:
                    return False
        return True

    def setrows(self, rows):
        """Resize the canvas."""

        self.rows = int(rows)
        self.drawgrid()

    def setcolumns(self, columns):
        """Resize the canvas."""

        self.columns = int(columns)
        self.drawgrid()


class Ping(Frame):

    instructions = """Each disc (circles) has a white and a black side.
If you click on one of the discs,
all the surrounding discs will flip (change their color).
The goal is to flip every disc to their black side."""

    about = """Ping game
Created by: Gábor Májerszky
Version: 15/05/2014"""

    def __init__(self, master=None,
                 maincolor="green", altcolor="systembuttonface"):
        Frame.__init__(self, master)
        self.pack()
        self.maincolor = maincolor
        self.altcolor = altcolor
        self.master.title("Ping")

        Menubar(self).pack(fill=X)
        self.table = Gametable(self, 400, 400)
        self.table.pack()

    def new(self):
        """Delete the canvas, and reset the game table."""

        self.table.drawgrid()

    def options(self):
        """Create a new window for configuration."""

        options = Toplevel(bg=self.maincolor)
        Label(options, text="Rows: ", font="12", bg=self.maincolor,
              fg=self.altcolor).grid(row=1, column=1, sticky=E)
        rowscale = Scale(options, orient=HORIZONTAL, from_=1, to=20,
                         bg=self.maincolor, fg=self.altcolor,
                         troughcolor=self.altcolor, length=200,
                         command=self.table.setrows)
        rowscale.set(self.table.rows)
        rowscale.grid(padx=5, pady=5, row=1, column=2)
        Label(options, text="Columns: ", font="12", bg=self.maincolor,
              fg=self.altcolor).grid(row=2, column=1, sticky=E)
        columnscale = Scale(options, orient=HORIZONTAL, from_=1, to=20,
                            bg=self.maincolor, fg=self.altcolor,
                            troughcolor=self.altcolor, length=200,
                            command=self.table.setcolumns)
        columnscale.set(self.table.columns)
        columnscale.grid(padx=5, pady=5, row=2, column=2)
        Button(options, text="OK", width=10, command=options.destroy).grid(
            pady=10, row=3, column=1, columnspan=2)

    def popup(self, message):
        """Create a popup window with a message."""

        popup = Toplevel(bg=self.maincolor)
        lbl = Label(popup, text=message, font="12", fg=self.altcolor,
                    bd=1, bg=self.maincolor, relief=RIDGE)
        lbl.pack(padx=15, pady=15, ipadx=10, ipady=10)
        Button(popup, text="OK", width=10,
               command=popup.destroy).pack(pady=10)
        popup.focus_set()
        # the bind function passes an argument to the event handler,
        # but the destroy function doesn't take any, that's why I use a lambda
        popup.bind("<Escape>", lambda event: popup.destroy())
        popup.bind("<Return>", lambda event: popup.destroy())
        popup.bind("<space>", lambda event: popup.destroy())

if __name__ == "__main__":
    Ping().mainloop()
