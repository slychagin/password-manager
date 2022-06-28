import json
import random
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from string import ascii_letters, digits
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    letters_list = [random.choice(ascii_letters) for _ in range(random.randint(8, 10))]
    digits_list = [random.choice(digits) for _ in range(random.randint(2, 4))]
    punctuation_list = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_list = letters_list + digits_list + punctuation_list
    random.shuffle(password_list)
    password = "".join(password_list)

    pass_word_entry.set(password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web = website.get()
    email = user_email.get()
    pass_word = pass_word_entry.get()
    new_data = {
        web: {
            "email": email,
            "password": pass_word,
        }
    }

    if len(web) == 0 or len(pass_word) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, "end")
            password_entry.delete(0, "end")


# ---------------------------- SEARCH --------------------------------- #
def search():
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
        get_password = data[website.get()]["password"]
        get_email = data[website.get()]["email"]
    except KeyError as ex:
        messagebox.showinfo(title="Error", message=f"Not found website{ex}")
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message=f"File not found")
    else:
        messagebox.showinfo(title=f"{website.get()}", message=f"Email: {get_email}\n"
                                                              f"Password: {get_password}")


# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title("Password Manager")

mainframe = ttk.Frame(root, padding="50")
mainframe.grid(column=0, row=0, sticky="N, W, S, E")

canvas = Canvas(mainframe, width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = ttk.Label(mainframe, text="Website:")
website_label.grid(column=0, row=1, sticky="W")
email_label = ttk.Label(mainframe, text="Email/Username:")
email_label.grid(column=0, row=2, sticky="W")
password_label = ttk.Label(mainframe, text="Password:")
password_label.grid(column=0, row=3, sticky="W")

# Entries
website = StringVar()
user_email = StringVar(value="lychagin.sergey@mail.ru")
pass_word_entry = StringVar()

website_entry = ttk.Entry(mainframe, width=35, textvariable=website)
website_entry.grid(column=1, row=1, sticky="W")
email_entry = ttk.Entry(mainframe, textvariable=user_email)
email_entry.grid(column=1, row=2, columnspan=2, sticky="W, E")
password_entry = ttk.Entry(mainframe, width=35, textvariable=pass_word_entry)
password_entry.grid(column=1, row=3, sticky="W")

# Buttons
gen_pass_button = ttk.Button(mainframe, text="Generate Password", command=generate_password)
gen_pass_button.grid(column=2, row=3, sticky="E")
add_button = ttk.Button(mainframe, text="Add", command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="W, E")
search_button = ttk.Button(mainframe, text="Search", command=search)
search_button.grid(column=2, row=1, sticky="W, E")

for child in mainframe.winfo_children():
    child.grid_configure(padx=2, pady=2)

website_entry.focus()
root.mainloop()
