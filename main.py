import tkinter as tk
import random
from tkinter import messagebox


class StonesOfThePharaoh:
    def __init__(self, root):
        self.root = root
        self.root.title("Stones of the Pharaoh")

        self.grid_size = 9
        self.colors = ["red", "blue", "green"]
        self.grid = [
            [None for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]

        self.create_ui()

    def create_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.buttons = [
            [None for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                btn = tk.Button(
                    self.frame,
                    text="",
                    width=4,
                    height=2,
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                self.buttons[row][col] = btn

        self.reset_button = tk.Button(
            self.root,
            text="Start over",
            command=self.init_game,
        )
        self.reset_button.pack(pady=10)

        self.status_label = tk.Label(
            self.root, text="Click on a group of 2 or more to break pads."
        )
        self.status_label.pack()

        self.init_game()

    def init_game(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.grid[row][col] = random.choice(self.colors)
                self.set_button_color(row, col)

    def set_button_color(self, row, col):
        color = self.grid[row][col]
        btn = self.buttons[row][col]
        if color:
            btn.config(bg=color, state="normal")
        else:
            btn.config(bg="white", state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = StonesOfThePharaoh(root)
    root.mainloop()
