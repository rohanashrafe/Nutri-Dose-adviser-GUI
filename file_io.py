

import datetime
import csv
from tkinter import filedialog, messagebox
from logic import NORMAL_RANGES

def save_output(output, filename):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename + ".txt", "w") as f:
        f.write(f"NutriDose Report ({now})\n")
        for line in output:
            f.write(line + "\n")
    with open(filename + ".csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Parameter", "Value", "Recommendation"])
        for line in output:
            parts = line.split(" | ")
            if len(parts) == 2:
                param_value = parts[0].split(": ")
                if len(param_value) == 2:
                    writer.writerow([param_value[0], param_value[1], parts[1]])

def load_from_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    data = {}
    try:
        with open(filepath, 'r') as file:
            for line in file:
                if ':' in line:
                    parts = line.strip().split(':')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        if key in NORMAL_RANGES:
                            try:
                                data[key] = float(parts[1].strip())
                            except:
                                pass
    except:
        messagebox.showerror("Error", "Could not read file.")
    return data