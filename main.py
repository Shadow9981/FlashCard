import pandas
from tkinter import *
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_LANG = ('Ariel', 40, 'italic')
FONT_WORD = ('Ariel', 60, 'bold')
current_card = {}
data_dict = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")


# ---------------------------- GENERATE CARDS ------------------------------- #
def generate_card():
    global TIMER, current_card
    window.after_cancel(TIMER)
    current_card = random.choice(data_dict)
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(language, text="French", fill="black")
    window.after(5000, flip_card)


def flip_card():
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")


def known():
    data_dict.remove(current_card)
    data = pandas.DataFrame(data_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    generate_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

TIMER = window.after(5000, flip_card)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
right_image = PhotoImage(file="images/wrong.png")
wrong_image = PhotoImage(file="images/right.png")

wrong_button = Button(image=wrong_image, highlightthickness=0, command=generate_card)
wrong_button.grid(row=1, column=1)

right_button = Button(image=right_image, highlightthickness=0, command=known)
right_button.grid(row=1, column=0)

canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
card_image = canvas.create_image(400, 263, image=card_front)
language = canvas.create_text(400, 150, text="Title", font=FONT_LANG)
word = canvas.create_text(400, 263, text="word", font=FONT_WORD)
canvas.grid(row=0, column=0, columnspan=2)

window.mainloop()
