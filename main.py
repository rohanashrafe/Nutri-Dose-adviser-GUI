# main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from logic import process_data
from file_io import save_output, load_from_file
from models import Patient

PARAMETERS = [
    "Hemoglobin", "RBC", "WBC", "Platelets", "Glucose",
    "Calcium", "Vitamin D", "Vitamin B12", "Potassium", "Sodium",
    "Blood Pressure Systolic", "Blood Pressure Diastolic", "Iron",
    "Creatinine", "LDL", "HDL", "Total Cholesterol"
]


def show_recommendations(results):
    top = tk.Toplevel()
    top.title("Health Recommendations")
    top.geometry("700x500")

    text_output = tk.Text(top, wrap=tk.WORD)
    scrollbar = ttk.Scrollbar(top, orient="vertical", command=text_output.yview)
    text_output.configure(yscrollcommand=scrollbar.set)

    text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    for line in results:
        text_output.insert(tk.END, line + "\n")
    text_output.config(state=tk.DISABLED)


def submit_data(entries, age_var, sex_var, weight_var, history_var):
    blood_data = {}
    for param in PARAMETERS:
        try:
            blood_data[param] = float(entries[param].get())
        except ValueError:
            continue

    patient = Patient(age_var.get(), sex_var.get(), weight_var.get(), history_var.get(), blood_data)
    results = process_data(patient.blood_data, patient.age, patient.sex, patient.weight, patient.history)
    show_recommendations(results)

    should_save = messagebox.askyesno("Save Report", "Do you want to save this report?")
    if should_save:
        filename = simpledialog.askstring("Save As", "Enter file name (without extension):")
        if filename:
            save_output(results, filename)


def browse_file(entries, age_var, sex_var, weight_var, history_var):
    path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not path:
        return
    data = load_from_file(path)
    for param in PARAMETERS:
        if param in data:
            entries[param].delete(0, tk.END)
            entries[param].insert(0, str(data[param]))
    submit_data(entries, age_var, sex_var, weight_var, history_var)


def main_window():
    root = tk.Tk()
    root.title("Nutri-Dose-Adviser")
    root.geometry("600x720")

    frame = ttk.Frame(root, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    # Dropdown inputs
    ttk.Label(frame, text="Age").grid(row=0, column=0, sticky="w")
    age_var = tk.StringVar(value="25")
    age_menu = ttk.Combobox(frame, textvariable=age_var, values=list(range(10, 101)), state="readonly", width=10)
    age_menu.grid(row=0, column=1, sticky="w")

    ttk.Label(frame, text="Sex").grid(row=1, column=0, sticky="w")
    sex_var = tk.StringVar(value="Male")
    sex_menu = ttk.Combobox(frame, textvariable=sex_var, values=["Male", "Female", "Other"], state="readonly", width=10)
    sex_menu.grid(row=1, column=1, sticky="w")

    ttk.Label(frame, text="Weight (kg)").grid(row=2, column=0, sticky="w")
    weight_var = tk.StringVar(value="60")
    weight_menu = ttk.Combobox(frame, textvariable=weight_var, values=list(range(30, 121)), state="readonly", width=10)
    weight_menu.grid(row=2, column=1, sticky="w")

    ttk.Label(frame, text="Medical History").grid(row=3, column=0, sticky="w")
    history_var = tk.StringVar(value="None")
    history_menu = ttk.Combobox(frame, textvariable=history_var,
                                values=["None", "Anemia", "Hypertension", "Diabetes", "Heart Disease", "Kidney Issue"],
                                state="readonly", width=18)
    history_menu.grid(row=3, column=1, sticky="w")

    ttk.Separator(frame).grid(row=4, columnspan=2, sticky="ew", pady=10)

    entries = {}
    row = 5
    for param in PARAMETERS:
        ttk.Label(frame, text=param).grid(row=row, column=0, sticky="w", pady=2)
        entry = ttk.Entry(frame, width=15)
        entry.grid(row=row, column=1, sticky="w")
        entries[param] = entry
        row += 1

    ttk.Button(frame, text="Submit",
               command=lambda: submit_data(entries, age_var, sex_var, weight_var, history_var)).grid(row=row, column=0,
                                                                                                     pady=10)
    ttk.Button(frame, text="Browse Input File",
               command=lambda: browse_file(entries, age_var, sex_var, weight_var, history_var)).grid(row=row, column=1,
                                                                                                     pady=10)

    root.mainloop()


if __name__ == "__main__":
    main_window()
