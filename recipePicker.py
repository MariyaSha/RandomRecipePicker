import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
import random
import pyglet

bg_colour = "#3d6466"
btn_colour = "#28393a"

# CUSTOM FONTS - WINDOWS ONLY!
pyglet.font.add_file('fonts/Ubuntu-Bold.ttf')
pyglet.font.add_file('fonts/Shanti-Regular.ttf')

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def fetch_db():
    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%';")
    all_tables = cursor.fetchall()

    idx = random.randint(0, len(all_tables) -1)
    my_table = all_tables[idx]

    title = my_table[1][:-6]
    title = "".join([a if a.islower() else " " + a for a in title])

    cursor.execute("SELECT * FROM " + my_table[1])
    ingredients = cursor.fetchall()

    return title, ingredients

def frame1():
    f1.tkraise()
    f1.pack_propagate(0)

    # load app logo
    logo = Image.open("assets/RRecipe_logo.png")
    logo = logo.resize((300, 300))
    logo = ImageTk.PhotoImage(logo)
    # display logo
    my_img = tk.Label(f1, image=logo, bg=bg_colour)
    my_img.image = logo
    my_img.pack()

    tk.Label(
        f1, 
        text="ready for your random recipe?", 
        font=('Shanti',14), 
        bg=bg_colour,
        fg="white"
        ).pack(pady=15)

    tk.Button(
        f1, 
        text='Shuffle'.upper(), 
        font=("Ubuntu", 20), 
        command=lambda:frame2(), 
        bg=btn_colour, 
        fg="white",
        activebackground="#BADEE2", 
        activeforeground="black",
        cursor="hand2"
        ).pack()

    clear_frame(f2)

def frame2():
    f2.tkraise()
    clear_frame(f1)

    title, ingredients = fetch_db()

    # load app logo
    logo2 = Image.open("assets/RRecipe_logo_bottom.png")
    logo2 = logo2.resize((125, 125))
    logo2 = ImageTk.PhotoImage(logo2)
    # display logo
    my_img = tk.Label(f2, image=logo2, bg=bg_colour)
    my_img.image = logo2
    my_img.pack(pady=20)

    # recipe title
    tk.Label(f2, text=title, font=("Ubuntu", 18), bg=bg_colour, fg="white").pack(pady=25)

    # ingredients
    for i in ingredients:
        # [0] id [1] name [2] qty [3] unit
        my_string = i[2] + " " + i[3] + " " + "of" + " " + i[1]
        tk.Label(f2, text=my_string, font=('Shanti',12), bg="#28393a", fg="white").pack(fill="both")

    # back to frame1
    tk.Button(
        f2, 
        text='Back'.upper(), 
        font=("Ubuntu", 18),
        bg=btn_colour,
        fg="white",
        activebackground="#BADEE2", 
        activeforeground="black",
        cursor="hand2",
        command=lambda:frame1()
        ).pack(pady=25)

root = tk.Tk()
root.title("Random Recipe")
root.eval('tk::PlaceWindow . center')

f1 = tk.Frame(root, width=500, height=600, bg=bg_colour)
f2 = tk.Frame(root, bg=bg_colour)

for frame in (f1, f2):
    frame.grid(row=0, column=0, sticky='nsew')

frame1()
root.mainloop()