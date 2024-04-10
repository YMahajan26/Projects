# rock paper scissors
from tkinter import *
import random

won = 0
lost = 0
draw = 0
# rock-0 paper-1 scissors-2

def winner(user_choice, computer_choice):
    global won, lost, draw
    if user_choice == 0 and computer_choice == 2:
        won += 1
        return "You win!"
    elif computer_choice == 0 and user_choice == 2:
        lost += 1
        return "You lose"
    elif computer_choice > user_choice:
        lost += 1
        return "You lose"
    elif user_choice > computer_choice:
        won += 1
        return "You win!"
    elif computer_choice == user_choice:
        draw += 1
        return "It's a draw"


def reset_screen():
    user_canvas.delete('all')
    comp_canvas.delete('all')
    result_canvas.delete('all')
    result_canvas.config(bg=W_BG)


def reset():             #reset button
    global won, lost, draw
    won = 0
    lost = 0
    draw = 0
    reset_screen()
    rock_button.config(state='normal')
    paper_button.config(state='normal')
    scissor_button.config(state='normal')


def end_game():
    reset_screen()
    result_canvas.config(bg='#FFD966')
    result_canvas.create_text(111, 70, text=f"\n  Score \n"
                                            f" Won :  {won}\n"
                                            f" Lost  :  {lost}\n"
                                            f"Draw :  {draw}", font=L_FONT2)
    rock_button.config(state="disabled")
    paper_button.config(state='disabled')
    scissor_button.config(state='disabled')


def play(user_choice):
    computer_choice = random.randint(0, 2)
    comp_canvas.create_image(111, 113, image=game_images[computer_choice])
    user_canvas.create_image(111, 113, image=game_images[user_choice])
    result = winner(user_choice, computer_choice)
    result_canvas.config(bg=W_BG)
    result_canvas.create_text(111, 50, text=f"{result}", font=L_FONT2)
    result_canvas.create_text(111, 130, text=f"\nScore:\n\n"
                                             f"Won  :  {won}\n"
                                             f"Lost  :  {lost}\n"
                                             f"Draw :  {draw}", font=B_FONT)
    window.after(3000, reset_screen)


def rock_pressed():
    reset_screen()
    user_choice = 0
    play(user_choice)


def paper_pressed():
    reset_screen()
    user_choice = 1
    play(user_choice)


def scissor_pressed():
    reset_screen()
    user_choice = 2
    play(user_choice)


# -----------------UI-----------------#

L_FONT2 = ('Constantia', 20, 'bold', 'italic')
B_FONT = ('Constantia', 15, 'bold')
R_FONT = ('Cubano', 20, 'bold')
W_BG = '#E2EFD9'
B_BG = 'aquamarine4'

window = Tk()
window.title("Rock-Paper-Scissors")
window.config(pady=50, padx=50, bg=W_BG, highlightthickness=0)

label1 = Label(text="Welcome to Rock-Paper-Scissors", font=L_FONT2, bg=W_BG, highlightthickness=0, fg='dark slate grey')
label1.grid(row=0, column=0, columnspan=3, pady=10)

choose_label = Label(text="CHOOSE:", font=L_FONT2, bg=W_BG, highlightthickness=0)
choose_label.grid(row=1, column=1, pady=10)

rock_button = Button(text="ROCK", font=B_FONT, width=12, command=rock_pressed, bg=B_BG, fg='white')
rock_button.grid(row=2, column=0, pady=10, padx=10)

paper_button = Button(text="PAPER", font=B_FONT, width=12, command=paper_pressed, bg=B_BG, fg='white')
paper_button.grid(row=2, column=1, pady=10, padx=10)

scissor_button = Button(text="SCISSOR", font=B_FONT, width=12, command=scissor_pressed, bg=B_BG, fg='white')
scissor_button.grid(row=2, column=2, pady=10, padx=10)

your_label = Label(text="Your Choice: ", font=L_FONT2, bg=W_BG, highlightthickness=0)
your_label.grid(row=3, column=0, pady=10, padx=10)

comp_label = Label(text="Computer Choice: ", font=L_FONT2, bg=W_BG, highlightthickness=0)
comp_label.grid(row=3, column=2, pady=10, padx=10)

rock = PhotoImage(file='Task-4(RPS)\images/rock3.png')
paper = PhotoImage(file='Task-4(RPS)\images/paper3.png')
scissor = PhotoImage(file='Task-4(RPS)\images/scissor3.png')
game_images = [rock, paper, scissor]

user_canvas = Canvas(width=222, height=226, bg=W_BG, highlightthickness=0)
user_canvas.grid(row=4, column=0, pady=10, padx=10)

result_canvas = Canvas(width=222, height=226, bg=W_BG, highlightthickness=0)
result_canvas.grid(row=4, column=1, pady=10, padx=10)

comp_canvas = Canvas(width=222, height=226, bg=W_BG, highlightthickness=0)
comp_canvas.grid(row=4, column=2, pady=10, padx=10)

end_button = Button(text="END GAME", font=B_FONT, width=12, command=end_game, bg='#FFD966')
end_button.grid(row=5, column=0, pady=20, padx=10)

reset_button = Button(text="RESET", font=B_FONT, width=12, command=reset, bg='#FFD966')
reset_button.grid(row=5, column=2, pady=20, padx=10)

window.mainloop()

