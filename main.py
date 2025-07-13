main.py (GUI with Registration, Login, Dropdowns, File Input)

import tkinter as tk from tkinter import ttk, filedialog, messagebox, scrolledtext from logic import NORMAL_RANGES, process_data from file_io import save_output, load_from_file import datetime import os import json

Initialize main window

root = tk.Tk() root.title("Nutri-Dose-Adviser") root.geometry("900x750") root.configure(bg="#d0f0c0")

Global widgets

entries = {} output_box = None user_db = "users.json"

def run_analysis(): try: age = int(age_var.get()) sex = sex_var.get().lower() weight = float(weight_var.get()) history = history_entry.get().lower()

data = {}
    for param in NORMAL_RANGES:
        val = entries[param].get()
        if val:
            try:
                data[param] = float(val)
            except:
                pass

    result = process_data(data, age, sex, weight, history)
    output_box.delete(1.0, tk.END)
    if result:
        for line in result:
            output_box.insert(tk.END, line + "\n")
    else:
        output_box.insert(tk.END, "All values normal.\n")

    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if filename:
        save_output(result, filename.replace(".txt", ""))

except Exception as e:
    messagebox.showerror("Error", f"Invalid input: {e}")

def fill_from_file_and_show(): data = load_from_file() for param in data: if param in entries: entries[param].delete(0, tk.END) entries[param].insert(0, str(data[param])) show_form(manual=False)

def show_form(manual=True): for widget in root.winfo_children(): widget.destroy()

header = tk.Label(root, text="Nutri-Dose-Adviser", bg="#004d00", fg="white", font=("Helvetica", 16, "bold"), pady=10)
header.pack(fill=tk.X)

form_frame = tk.Frame(root, bg="#d0f0c0")
form_frame.pack(pady=10, fill="x")

global age_var, sex_var, weight_var, history_entry
age_var = tk.StringVar(value="25")
sex_var = tk.StringVar(value="male")
weight_var = tk.StringVar(value="60")

tk.Label(form_frame, text="Age:", bg="#d0f0c0").grid(row=0, column=0, sticky="e")
tk.OptionMenu(form_frame, age_var, *map(str, range(1, 101))).grid(row=0, column=1)

tk.Label(form_frame, text="Sex:", bg="#d0f0c0").grid(row=0, column=2, sticky="e")
tk.OptionMenu(form_frame, sex_var, "male", "female").grid(row=0, column=3)

tk.Label(form_frame, text="Weight (kg):", bg="#d0f0c0").grid(row=0, column=4, sticky="e")
tk.OptionMenu(form_frame, weight_var, *map(str, range(30, 151))).grid(row=0, column=5)

tk.Label(form_frame, text="History:", bg="#d0f0c0").grid(row=1, column=0, sticky="e", pady=5)
history_entry = tk.Entry(form_frame, width=60)
history_entry.grid(row=1, column=1, columnspan=5, sticky="w")

tk.Label(root, text="\nEnter blood values (leave blank if not tested):", bg="#d0f0c0", font=("Helvetica", 12)).pack()

param_frame = tk.Frame(root, bg="#d0f0c0")
param_frame.pack(pady=10, fill="both", expand=True)

global entries
entries = {}
for i, param in enumerate(NORMAL_RANGES):
    tk.Label(param_frame, text=param + ":", anchor="w", bg="#d0f0c0").grid(row=i, column=0, sticky="w")
    ent = tk.Entry(param_frame)
    ent.grid(row=i, column=1, sticky="w")
    entries[param] = ent

tk.Button(root, text="Submit", bg="#004d00", fg="white", command=run_analysis).pack(pady=10)

global output_box
output_box = scrolledtext.ScrolledText(root, height=10, width=100)
output_box.pack(pady=10)

def show_login(): for widget in root.winfo_children(): widget.destroy()

tk.Label(root, text="Nutri-Dose-Adviser Login", font=("Helvetica", 16), bg="#d0f0c0").pack(pady=20)

login_frame = tk.Frame(root, bg="#d0f0c0")
login_frame.pack()

tk.Label(login_frame, text="Username:", bg="#d0f0c0").grid(row=0, column=0)
username = tk.Entry(login_frame)
username.grid(row=0, column=1)

tk.Label(login_frame, text="Password:", bg="#d0f0c0").grid(row=1, column=0)
password = tk.Entry(login_frame, show="*")
password.grid(row=1, column=1)

def verify():
    if os.path.exists(user_db):
        with open(user_db, 'r') as f:
            users = json.load(f)
        if username.get() in users and users[username.get()] == password.get():
            choose_input_method()
            return
    messagebox.showerror("Login Failed", "Incorrect username or password")

def go_to_register():
    show_register()

tk.Button(root, text="Login", command=verify, bg="#004d00", fg="white").pack(pady=10)
tk.Button(root, text="Register", command=go_to_register).pack()

def show_register(): for widget in root.winfo_children(): widget.destroy()

tk.Label(root, text="Register New Account", font=("Helvetica", 16), bg="#d0f0c0").pack(pady=20)

register_frame = tk.Frame(root, bg="#d0f0c0")
register_frame.pack()

tk.Label(register_frame, text="New Username:", bg="#d0f0c0").grid(row=0, column=0)
new_username = tk.Entry(register_frame)
new_username.grid(row=0, column=1)

tk.Label(register_frame, text="New Password:", bg="#d0f0c0").grid(row=1, column=0)
new_password = tk.Entry(register_frame, show="*")
new_password.grid(row=1, column=1)

def register():
    if not new_username.get() or not new_password.get():
        messagebox.showerror("Error", "Fields cannot be empty")
        return
    users = {}
    if os.path.exists(user_db):
        with open(user_db, 'r') as f:
            users = json.load(f)
    users[new_username.get()] = new_password.get()
    with open(user_db, 'w') as f:
        json.dump(users, f)
    messagebox.showinfo("Success", "User registered successfully")
    show_login()

tk.Button(root, text="Register", command=register, bg="#004d00", fg="white").pack(pady=10)
tk.Button(root, text="Back to Login", command=show_login).pack()

def choose_input_method(): for widget in root.winfo_children(): widget.destroy()

tk.Label(root, text="Choose Input Method", font=("Helvetica", 16), bg="#d0f0c0").pack(pady=20)

tk.Button(root, text="Manual Input", width=30, command=lambda: show_form(manual=True)).pack(pady=10)
tk.Button(root, text="Load from File", width=30, command=fill_from_file_and_show).pack(pady=10)



show_login()
root.mainloop()