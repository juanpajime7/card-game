import tkinter
from tkinter import *
from PIL import Image, ImageTk
import csv
import random
import pandas as pd
from threading import Timer

BACKGROUND_COLOR = "#B1DDC6"

# --- User Interface ---
window = Tk()
window.config(background=BACKGROUND_COLOR)
window.title("Languages Flashes")
window.geometry("600x600+2800+150")

# --- Updating the flashcard ---
file_to_use = "data/spanish_words.csv"
data_frame = pd.read_csv(file_to_use)
words_organized = data_frame.to_dict(orient="records")
random_word = random.choice(words_organized)



def update_word():
    global random_word
    random_word = random.choice(words_organized)
    canvas.create_image(50, 100, anchor=NW, image=new_front)
    first_word = canvas.create_text(300, 150, text="Spanish", font=("Ariel", 40, "italic"))
    second_word = canvas.create_text(300, 350, text="", font=("Ariel", 60, "bold"))
    canvas.itemconfig(second_word, text=random_word['Spanish'])
    window.after(3000, func=flip)


# --- Flipping the flashcard ---
def flip():
    canvas.create_image(50, 100, anchor=NW, image=new_back)
    first_new_word = canvas.create_text(300, 150, text="English", font=("Ariel", 40, "italic"), fill="white")
    canvas.create_text(300, 350, text=random_word['English'], font=("Ariel", 60, "bold"), fill="white")


# --- Storing the words that need to be studied ---
def words_to_learn():
    # words_organized.remove(random_word)
    # new_file = pd.DataFrame(words_organized)
    # try:
    #     new_file.to_csv("data/words_to_learn.csv", mode="w")
    # except FileExistsError:
    #     new_data_frame = pd.read_csv("data/words_to_learn.csv")
    #     new_words_organized = new_data_frame.to_dict(orient="records")
    #     new_words_organized.remove(random_word)
    # else:
    #     new_file.to_csv("data/words_to_learn.csv", mode="w")
    # finally:
    #     update_word()
    global file_to_use
    if file_to_use == "data/spanish_words.csv":
        update_word()
    else:
        words_organized.remove(random_word)
        new_file = pd.DataFrame(words_organized)
        file_to_use = "data/words_to_learn.csv"
        update_word()




# --- Buttons ---
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=update_word)
wrong_button.place(x=400, y=450)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=words_to_learn)
right_button.place(x=100, y=450)

# --- Canvas ---
canvas = Canvas(window, width=550, height=450, background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=2, row=2)
front_card_image = Image.open("images/card_front.png")
back_card_image = Image.open("images/card_back.png")
resized_front = front_card_image.resize((500, 350))
resized_back = back_card_image.resize((500, 350))
new_front = ImageTk.PhotoImage(resized_front)
new_back = ImageTk.PhotoImage(resized_back)
# canvas.create_image(50, 100, anchor=NW, image=new_front)

update_word()

t = Timer(3.0, flip)
t.start()

window.mainloop()
