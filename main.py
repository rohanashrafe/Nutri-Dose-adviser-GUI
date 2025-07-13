# main.py (Updated: Show recommendations in a new window)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from logic import NORMAL_RANGES, process_data
from file_io import save_output, load_from_file
import datetime
import os
import json

root = tk.Tk()
root.title("Nutri-Dose-Adviser")
root.geometry("1150x850")
root.configure(bg="#e7ffe6")

entries = {}
user_db = "users.json"
history_options = ["None", "anemia", "diabetes", "hypertension", "obesity", "heart disease"]
last_input_file = None  # for file input saving

# Load user database or create empty file
def load_users():
    if os.path.exists(user_db):
        with open(user_db, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(user_db, 'w') as f:
        json.dump(users, f)

def exit_app():
    root.destroy()

def ask_save_to_txt(result):
    answer = messagebox.askyesno("Save Result", "Do you want to save the result in a text file?")
    if answer:
        filename = filedialog.asksaveasfilename(defaultextension=".txt", title="Save As")
        if filename:
            save_output(result, filename.replace(".txt", ""))

def run_analysis():
    try:
        age = int(age_var.get())
        sex = sex_var.get().lower()
        weight = float(weight_var.get())
        history = history_var.get().lower()

        data = {}
        for param in NORMAL_RANGES:
            val = entries[param].get()
            if val:
                try:
                    data[param] = float(val)
                except:
                    pass

        result = process_data(data, age, sex, weight, history)
        ask_save_to_txt(result)
        show_recommendations(result)

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def show_recommendations(result):
    rec_window = tk.Toplevel(root)
    rec_window.title("Recommendations")
    rec_window.geometry("800x500")
    rec_window.configure(bg="#e7ffe6")

    tk.Label(rec_window, text="Your Personalized Recommendations", font=("Arial", 14, "bold"), bg="#e7ffe6").pack(pady=10)
    box = scrolledtext.ScrolledText(rec_window, height=25, width=95, wrap=tk.WORD)
    box.pack(padx=10, pady=10)
    box.insert(tk.END, "\n".join(result) if result else "All values are within the normal range.")
    box.config(state="disabled")

def fill_from_file_and_show():
    global last_input_file
    path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not path:
        return
    last_input_file = path
    data = load_from_file(path)
    for param in data:
        if param in entries:
            entries[param].delete(0, tk.END)
            entries[param].insert(0, str(data[param]))
    show_form(manual=False)

def save_result_back_to_file(result):
    global last_input_file
    if last_input_file:
        try:
            with open(last_input_file, 'a') as f:
                f.write("\n--- Recommendations ---\n")
                for line in result:
                    f.write(line + "\n")
        except Exception as e:
            messagebox.showerror("File Save Error", str(e))

def show_form(manual=True):
    for widget in root.winfo_children():
        widget.destroy()

    header = tk.Label(root, text="Nutri-Dose-Adviser", bg="#228B22", fg="white", font=("Helvetica", 18, "bold"), pady=10)
    header.pack(fill=tk.X)

    form_frame = tk.Frame(root, bg="#e7ffe6")
    form_frame.pack(pady=5, fill="x")

    global age_var, sex_var, weight_var, history_var
    age_var = tk.StringVar(value="25")
    sex_var = tk.StringVar(value="male")
    weight_var = tk.StringVar(value="60")
    history_var = tk.StringVar(value="None")

    tk.Label(form_frame, text="Age:", bg="#e7ffe6").grid(row=0, column=0, sticky="e")
    tk.OptionMenu(form_frame, age_var, *map(str, range(1, 101))).grid(row=0, column=1)

    tk.Label(form_frame, text="Sex:", bg="#e7ffe6").grid(row=0, column=2, sticky="e")
    tk.OptionMenu(form_frame, sex_var, "male", "female").grid(row=0, column=3)

    tk.Label(form_frame, text="Weight (kg):", bg="#e7ffe6").grid(row=0, column=4, sticky="e")
    tk.OptionMenu(form_frame, weight_var, *map(str, range(30, 151))).grid(row=0, column=5)

    tk.Label(form_frame, text="History:", bg="#e7ffe6").grid(row=1, column=0, sticky="e", pady=5)
    tk.OptionMenu(form_frame, history_var, *history_options).grid(row=1, column=1, columnspan=5, sticky="w")

    body_frame = tk.Frame(root, bg="#e7ffe6")
    body_frame.pack(padx=10, pady=5, fill="both", expand=True)

    input_frame = tk.LabelFrame(body_frame, text="Blood Values Input", bg="#e7ffe6", width=300)
    input_frame.pack(padx=10, fill="both", expand=True)

    global entries
    entries = {}
    last_entry = None
    for i, param in enumerate(NORMAL_RANGES):
        tk.Label(input_frame, text=param + ":", anchor="w", bg="#e7ffe6").grid(row=i, column=0, sticky="w")
        ent = tk.Entry(input_frame)
        ent.grid(row=i, column=1, sticky="w", ipadx=5, ipady=2)
        if last_entry:
            ent.bind("<Up>", lambda e, f=last_entry: f.focus())
        last_entry = ent
        entries[param] = ent

    # Button holder
    button_holder = tk.Frame(root, bg="#e7ffe6")
    button_holder.pack(pady=15)
    tk.Button(button_holder, text="Submit", bg="#228B22", fg="white", width=18, command=run_analysis).grid(row=0, column=0, padx=15)
    tk.Button(button_holder, text="Back to Menu", width=18, command=choose_input_method).grid(row=0, column=1, padx=15)
    tk.Button(button_holder, text="Exit", width=18, command=exit_app).grid(row=0, column=2, padx=15)

def choose_input_method():
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text="Choose Input Method", font=("Arial", 16, "bold"), bg="#e7ffe6").pack(pady=20)
    tk.Button(root, text="Manual Input", width=20, command=show_form).pack(pady=10)
    tk.Button(root, text="Load from File", width=20, command=fill_from_file_and_show).pack(pady=10)
    tk.Button(root, text="Exit", width=20, command=exit_app).pack(pady=10)

def show_login():
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text="Login", font=("Arial", 16, "bold"), bg="#e7ffe6").pack(pady=20)

    user_label = tk.Label(root, text="Username:", bg="#e7ffe6")
    user_label.pack()
    user_entry = tk.Entry(root)
    user_entry.pack()

    pass_label = tk.Label(root, text="Password:", bg="#e7ffe6")
    pass_label.pack()
    pass_entry = tk.Entry(root, show="*")
    pass_entry.pack()

    def login():
        users = load_users()
        user = user_entry.get()
        pwd = pass_entry.get()
        if user in users and users[user] == pwd:
            messagebox.showinfo("Login", "Login successful!")
            choose_input_method()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register():
        users = load_users()
        user = user_entry.get()
        pwd = pass_entry.get()
        if user in users:
            messagebox.showerror("Register Failed", "User already exists")
        else:
            users[user] = pwd
            save_users(users)
            messagebox.showinfo("Register", "Registration successful!")

    tk.Button(root, text="Login", command=login).pack(pady=5)
    tk.Button(root, text="Register", command=register).pack(pady=5)
    tk.Button(root, text="Exit", command=exit_app).pack(pady=10)

# Start the app
show_login()
root.mainloop()
