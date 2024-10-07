from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

# ----------------------------Flash Cards Creation------------------------------
card_in_hand = {}
to_learn = {}

try:
    file = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('data/zulu_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = file.to_dict(orient='records')


def next_card():
    global card_in_hand
    global flip_timer
    window.after_cancel(flip_timer)
    card_in_hand = random.choice(to_learn)
    canvas.itemconfig(card_title, text='IsiZulu', fill='black')
    canvas.itemconfig(card_word, text=card_in_hand['IsiZulu'], fill='black')
    canvas.itemconfig(card_background, image=front_card_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=card_in_hand['English'], fill='white')
    canvas.itemconfig(card_background, image=back_card_img)


def is_known():
    to_learn.remove(card_in_hand)
    outstanding_words = len(to_learn)
    data = pd.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)
    next_card()


# ----------------------------UI Setup---------------------------------
window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card_img = PhotoImage(file='images/card_front.png')
back_card_img = PhotoImage(file='images/card_back.png')

card_background = canvas.create_image(400, 263, image=front_card_img)
card_title = canvas.create_text(400, 150, text='', font=('Ariel', 40, 'italic'))
card_word = canvas.create_text(400, 263, text='', font=('Ariel', 60, 'bold'))

canvas.grid(row=0, column=0, columnspan=2)

unknown_img = PhotoImage(file='images/wrong.png')
unknown_btn = Button(image=unknown_img, highlightthickness=0, command=next_card)
unknown_btn.grid(row=1, column=0)

known_img = PhotoImage(file='images/right.png')
known_btn = Button(image=known_img, highlightthickness=0, command=is_known)
known_btn.grid(row=1, column=1)

next_card()

window.mainloop()
