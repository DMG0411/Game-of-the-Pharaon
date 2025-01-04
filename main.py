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
        self.score = 0

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
                    command=lambda r=row, c=col: self.cell_clicked(r, c),
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                self.buttons[row][col] = btn

        self.reset_button = tk.Button(
            self.root,
            text="Start over",
            command=self.init_game,
        )
        self.reset_button.pack(pady=10)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}")
        self.score_label.pack()

        self.status_label = tk.Label(
            self.root, text="Click on a group of 2 or more to break pads."
        )
        self.status_label.pack()

        self.init_game()

    def init_game(self):
        self.score = 0
        self.update_score_label()
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

    def cell_clicked(self, row, col):
        color = self.grid[row][col]
        if not color:
            return
        group = self.find_connected_blocks(row, col, color)

        if len(group) > 1:
            self.remove_blocks(group)
            self.update_score(len(group))
        else:
            self.status_label.config(text="No group to remove. Select a group.")

    def find_connected_blocks(self, row, col, color):
        to_check = [(row, col)]
        connected = set()

        while to_check:
            r, c = to_check.pop()
            if (r, c) in connected or not (
                0 <= r < self.grid_size and 0 <= c < self.grid_size
            ):
                continue
            if self.grid[r][c] == color:
                connected.add((r, c))
                to_check.extend([(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)])

        return connected

    def remove_blocks(self, group):
        for row, col in group:
            self.grid[row][col] = None
            self.set_button_color(row, col)

    def update_score(self, blocks_removed):
        self.score += blocks_removed * 100
        self.update_score_label()

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.score}")


if __name__ == "__main__":
    root = tk.Tk()
    app = StonesOfThePharaoh(root)
    root.mainloop()
