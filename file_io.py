# file_io.py
import datetime

def save_output(result, filename):
    try:
        with open(filename + ".txt", 'w', encoding='utf-8') as f:
            f.write("NutriDose Report\n")
            f.write("Generated on: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            for line in result:
                f.write(line + "\n")
    except Exception as e:
        print("Error saving file:", e)

def load_from_file(filepath):
    data = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    try:
                        data[key.strip()] = float(value.strip())
                    except:
                        pass
    except Exception as e:
        print("Error reading file:", e)
    return data
