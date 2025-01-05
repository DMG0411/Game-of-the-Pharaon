import tkinter as tk
import random
from tkinter import messagebox


class StonesOfThePharaoh:
    def __init__(self, root):
        self.root = root
        self.root.title("Stones of the Pharaoh")
        self.root.configure(bg="#f7f3e9")

        self.grid_size = 9
        self.base_colors = ["#f28b82", "#aecbfa"]
        self.level = 1
        self.colors = self.base_colors[:2]
        self.grid = [
            [None for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]
        self.score = 0
        self.lives = 3

        self.create_main_screen()
        self.create_game_screen()

    def create_main_screen(self):
        self.main_frame = tk.Frame(self.root, bg="#f7f3e9")
        self.main_frame.pack(fill="both", expand=True)

        title_label = tk.Label(
            self.main_frame,
            text="Stones of the Pharaoh",
            font=("Helvetica", 28, "bold"),
            bg="#f7f3e9",
            fg="#5e548e",
        )
        title_label.pack(pady=30)

        play_button = tk.Button(
            self.main_frame,
            text="Play",
            font=("Helvetica", 16),
            bg="#ffcc80",
            fg="#5e548e",
            activebackground="#ffb74d",
            activeforeground="white",
            relief="raised",
            bd=2,
            command=self.start_game,
        )
        play_button.pack(pady=20)

    def create_game_screen(self):
        self.game_frame = tk.Frame(self.root, bg="#f7f3e9")

        self.grid_frame = tk.Frame(self.game_frame, bg="#f7f3e9")
        self.grid_frame.pack(pady=20)

        self.buttons = [
            [None for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                btn = tk.Button(
                    self.grid_frame,
                    text="",
                    width=4,
                    height=2,
                    bg="#ffffff",
                    fg="#5e548e",
                    font=("Helvetica", 10, "bold"),
                    command=lambda r=row, c=col: self.cell_clicked(r, c),
                    relief="groove",
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                btn.bind("<Enter>", lambda e, r=row, c=col: self.highlight_group(r, c))
                btn.bind("<Leave>", lambda e: self.reset_highlight())
                self.buttons[row][col] = btn

        self.reset_button = tk.Button(
            self.game_frame,
            text="Start over",
            font=("Helvetica", 14),
            bg="#ffcc80",
            fg="#5e548e",
            activebackground="#ffb74d",
            activeforeground="white",
            relief="raised",
            bd=2,
            command=self.init_game,
        )
        self.reset_button.pack(pady=10)

        self.score_label = tk.Label(
            self.game_frame,
            text=f"Score: {self.score}",
            font=("Helvetica", 16),
            bg="#f7f3e9",
            fg="#5e548e",
        )
        self.score_label.pack()

        self.lives_label = tk.Label(
            self.game_frame,
            text=f"Lives: {self.lives}",
            font=("Helvetica", 16),
            bg="#f7f3e9",
            fg="#5e548e",
        )
        self.lives_label.pack()

        self.status_label = tk.Label(
            self.game_frame,
            text="Click on a group of 2 or more to break pads.",
            font=("Helvetica", 12),
            bg="#f7f3e9",
            fg="#5e548e",
        )
        self.status_label.pack(pady=10)

    def start_game(self):
        self.main_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        self.score = 0
        self.lives = 3
        self.level = 1
        self.colors = self.base_colors[:2]
        self.init_game()

    def init_game(self):
        self.update_status(f"Level {self.level}")
        self.update_score_label()
        self.update_lives_label()
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.grid[row][col] = random.choice(self.colors)
                self.set_button_color(row, col)

    def set_button_color(self, row, col):
        color = self.grid[row][col]
        btn = self.buttons[row][col]
        if color:
            btn.config(bg=color, state="normal", relief="groove")
        else:
            btn.config(bg="#ffffff", state="disabled", relief="flat")

    def cell_clicked(self, row, col):
        color = self.grid[row][col]
        if not color:
            return
        group = self.find_connected_blocks(row, col, color)

        if len(group) > 1:
            self.remove_blocks(group)
            self.apply_gravity()
            self.update_score(len(group))
        else:
            self.grid[row][col] = None
            self.set_button_color(row, col)
            self.apply_gravity()
            self.lives -= 1
            self.update_lives_label()

            if self.lives <= 0:
                self.game_over()
            else:
                self.status_label.config(text="No group! You lost a life!")
        if self.is_level_complete():
            self.level_up()

    def is_level_complete(self):
        return all(
            self.grid[row][col] is None
            for row in range(self.grid_size)
            for col in range(self.grid_size)
        )

    def level_up(self):
        if self.lives > 0:
            self.level += 1
            self.colors.append(self.generate_new_color())
            messagebox.showinfo("Level Up", f"Level {self.level}")
            self.init_game()

    def generate_new_color(self):
        while True:
            new_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            if new_color not in self.colors:
                return new_color

    def update_status(self, text):
        self.status_label.config(text=text)

    def highlight_group(self, row, col):
        color = self.grid[row][col]
        if not color:
            return
        group = self.find_connected_blocks(row, col, color)
        for r, c in group:
            self.buttons[r][c].config(relief="solid", bd=1)

    def reset_highlight(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.grid[row][col]:
                    self.buttons[row][col].config(relief="groove", bd=2)
                else:
                    self.buttons[row][col].config(relief="flat", bd=0)

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

    def apply_gravity(self):
        for col in range(self.grid_size):
            non_empty = [
                self.grid[row][col]
                for row in range(self.grid_size)
                if self.grid[row][col]
            ]
            for row in range(self.grid_size):
                if row < self.grid_size - len(non_empty):
                    self.grid[row][col] = None
                else:
                    self.grid[row][col] = non_empty[
                        row - (self.grid_size - len(non_empty))
                    ]
        self.shift_columns()

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.set_button_color(row, col)

    def shift_columns(self):
        non_empty_columns = [
            col
            for col in range(self.grid_size)
            if any(self.grid[row][col] for row in range(self.grid_size))
        ]

        new_grid = [
            [None for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]

        shift_start = self.grid_size - len(non_empty_columns)

        for new_col, old_col in enumerate(non_empty_columns, start=shift_start):
            for row in range(self.grid_size):
                new_grid[row][new_col] = self.grid[row][old_col]

        self.grid = new_grid

    def update_score(self, blocks_removed):
        self.score += blocks_removed * 100
        self.update_score_label()

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.score}")

    def update_lives_label(self):
        self.lives_label.config(text=f"Lives: {self.lives}")

    def game_over(self):
        messagebox.showinfo(
            "Game Over", f"Game over! Your final score is: {self.score}"
        )
        self.game_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = StonesOfThePharaoh(root)
    root.mainloop()
