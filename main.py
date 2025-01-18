import tkinter as tk
from tkinter import messagebox

# Initialize main window
root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("600x700")
root.configure(bg="#2a2d3e")  # Dark modern background

# Variables
player1_name = tk.StringVar()
player2_name = tk.StringVar()
current_player = None
board = []
player1_wins = 0
player2_wins = 0
draw_count = 0
timer_value = 30
timer_running = False


def start_game():
    """Starts the game after entering player names."""
    global current_player, timer_running
    if not player1_name.get() or not player2_name.get():
        messagebox.showwarning("Missing Info", "Please enter names for both players!")
        return
    current_player = player1_name.get()  # Player 1 starts
    intro_frame.pack_forget()
    game_frame.pack()
    update_status()
    update_score()  # Ensure scores are displayed from the beginning
    timer_running = True
    start_timer()


def button_click(row, col):
    """Handles button clicks on the game board."""
    global current_player, player1_wins, player2_wins, draw_count, timer_value
    if board[row][col]["text"] == "":
        board[row][col]["text"] = "X" if current_player == player1_name.get() else "O"
        board[row][col]["fg"] = "#87CEFA" if current_player == player1_name.get() else "#FF7F7F"  # Light blue and light red
        board[row][col]["font"] = ("Helvetica", 14, "bold")  # Bold text


        if check_winner():
            winner = current_player
            messagebox.showinfo("Game Over", f"{winner} wins!")
            if winner == player1_name.get():
                player1_wins += 1
            else:
                player2_wins += 1
            update_score()
            reset_board()
        elif all(board[i][j]["text"] != "" for i in range(3) for j in range(3)):
            messagebox.showinfo("Game Over", "It's a draw!")
            draw_count += 1
            update_score()
            reset_board()
        else:
            switch_player()


def check_winner():
    """Checks if the current player has won."""
    for i in range(3):
        if board[i][0]["text"] == board[i][1]["text"] == board[i][2]["text"] != "":
            return True
        if board[0][i]["text"] == board[1][i]["text"] == board[2][i]["text"] != "":
            return True
    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] != "":
        return True
    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] != "":
        return True
    return False


def update_score():
    """Updates the score display."""
    score_label.config(
        text=f"{player1_name.get()}: {player1_wins} Wins   |   {player2_name.get()}: {player2_wins} Wins   |   Draws: {draw_count}"
    )


def reset_board():
    """Resets the game board."""
    global timer_value
    for i in range(3):
        for j in range(3):
            board[i][j]["text"] = ""
    timer_value = 30
    switch_player()


def reset_game():
    """Resets the entire game including scores."""
    global player1_wins, player2_wins, draw_count
    player1_wins = 0
    player2_wins = 0
    draw_count = 0
    update_score()
    reset_board()


def quit_game():
    """Exits the application."""
    root.destroy()


def switch_player():
    """Switches the current player and resets the timer."""
    global current_player, timer_value
    current_player = player1_name.get() if current_player == player2_name.get() else player2_name.get()
    update_status()
    timer_value = 30


def update_status():
    """Updates the status label to show the current player's turn."""
    status_label.config(text=f"{current_player}'s Turn")


def start_timer():
    """Starts the 30-second timer."""
    def countdown():
        global timer_value, timer_running
        if timer_value > 0:
            timer_label.config(text=f"Time Left: {timer_value}s")
            timer_value -= 1
            root.after(1000, countdown)
        else:
            messagebox.showinfo("Time Up", f"{current_player}'s time is up! Switching turn.")
            switch_player()
            start_timer()

    countdown()


# Introduction Screen
intro_frame = tk.Frame(root, bg="#2a2d3e")
tk.Label(intro_frame, text="Tic Tac Toe", font=("Helvetica", 24, "bold"), bg="#2a2d3e", fg="#ffcc29").pack(pady=20)
tk.Label(intro_frame, text="Player 1 Name (X):", font=("Helvetica", 14), bg="#2a2d3e", fg="white").pack(pady=5)
tk.Entry(intro_frame, textvariable=player1_name, font=("Helvetica", 14), width=20).pack(pady=5)
tk.Label(intro_frame, text="Player 2 Name (O):", font=("Helvetica", 14), bg="#2a2d3e", fg="white").pack(pady=5)
tk.Entry(intro_frame, textvariable=player2_name, font=("Helvetica", 14), width=20).pack(pady=5)
tk.Button(intro_frame, text="Start Game", font=("Helvetica", 16, "bold"), bg="#ff5733", fg="white", command=start_game).pack(pady=20)
intro_frame.pack()

# Game Screen
game_frame = tk.Frame(root, bg="#2a2d3e")

# Game title
tk.Label(game_frame, text="Tic Tac Toe", font=("Helvetica", 24, "bold"), bg="#2a2d3e", fg="#ffcc29").pack(pady=20)

# Game status label
status_label = tk.Label(game_frame, text="", font=("Helvetica", 16), bg="#2a2d3e", fg="white")
status_label.pack(pady=5)

# Timer label
timer_label = tk.Label(game_frame, text="", font=("Helvetica", 16), bg="#2a2d3e", fg="#ff5733")
timer_label.pack(pady=5)

# Score label
score_label = tk.Label(game_frame, text="", font=("Helvetica", 14), bg="#2a2d3e", fg="white")
score_label.pack(pady=10)

# Game board buttons
board_frame = tk.Frame(game_frame, bg="#2a2d3e")
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(
            board_frame,
            text="",
            width=6,
            height=3,
            bg="#445c6e",
            activebackground="#4caf50",
            font=("Helvetica", 14),
            command=lambda i=i, j=j: button_click(i, j),
        )
        btn.grid(row=i, column=j, padx=5, pady=5)
        row.append(btn)
    board.append(row)
board_frame.pack(pady=10)

# Control buttons
control_frame = tk.Frame(game_frame, bg="#2a2d3e")
tk.Button(control_frame, text="Reset Game", font=("Helvetica", 14), bg="#4caf50", fg="white", command=reset_game).pack(side="left", padx=20)
tk.Button(control_frame, text="Quit Game", font=("Helvetica", 14), bg="#f44336", fg="white", command=quit_game).pack(side="right", padx=20)
control_frame.pack(pady=20)

game_frame.pack_forget()

# Run the main loop
root.mainloop()
