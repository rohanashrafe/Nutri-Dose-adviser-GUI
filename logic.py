

NORMAL_RANGES = {
    'Hemoglobin': (12.0, 17.5),
    'Vitamin D': (20.0, 50.0),
    'Calcium': (8.5, 10.5),
    'Iron': (60.0, 170.0),
    'Vitamin B12': (200, 900),
    'Magnesium': (1.7, 2.2),
    'Potassium': (3.5, 5.1),
    'Zinc': (70, 120),
    'Sugar': (70, 110),
    'LDL': (0, 100),
    'HDL': (40, 60),
    'Triglycerides': (0, 150),
    'Creatinine': (0.6, 1.3),
    'Uric Acid': (3.5, 7.2),
    'Total Cholesterol': (0, 200),
    'Blood Pressure (Systolic)': (90, 120),
    'Blood Pressure (Diastolic)': (60, 80)
}

DOCTOR_CONTACTS = {
    'anemia': 'Dr. Laila Ferdous - +8801711002233',
    'diabetes': 'Dr. Rafiq Uddin - +8801700112233',
    'hypertension': 'Dr. Asif Rahman - +8801612345678'
}

def get_recommendation(param, value, age, sex, weight, history):
    low, high = NORMAL_RANGES[param]
    rec = ""

    if value < low:
        if param == 'Hemoglobin':
            rec = "Low Hb → Iron 30 mg/day + spinach/liver" if sex == 'female' else "Low Hb → Iron 15–30 mg/day + protein diet"
        elif param == 'Vitamin D': rec = "Vit D ↓ → 2000 IU/day + 15m sun"
        elif param == 'Calcium': rec = "Ca ↓ → Milk, almonds + 500 mg/day"
        elif param == 'Vitamin B12': rec = "B12 ↓ → Eggs/meat + 500 mcg/day"
        elif param == 'Iron': rec = "Iron ↓ → Meat, lentils, 15–30 mg/day"
        elif param == 'Magnesium': rec = "Mg ↓ → Nuts, greens, 250 mg/day"
        elif param == 'Potassium': rec = "K ↓ → Banana, coconut water"
        elif param == 'Zinc': rec = "Zn ↓ → Nuts, eggs, 10 mg/day"
        elif param == 'Sugar': rec = "Sugar ↓ → Take glucose or sweets"
        else: rec = f"{param} low → consult doctor"
    elif value > high:
        if param == 'LDL': rec = "LDL ↑ → Avoid fried food, walk 20m"
        elif param == 'Sugar': rec = "Sugar ↑ → Cut carbs/sugar, walk 30m"
        elif param == 'Triglycerides': rec = "TG ↑ → Less sugar/oil, exercise"
        elif param == 'Total Cholesterol': rec = "Chol ↑ → No red meat, exercise"
        elif param == 'Creatinine': rec = "Cr ↑ → Check kidney, hydrate"
        elif param == 'Uric Acid': rec = "UA ↑ → Avoid red meat, drink more"
        elif param == 'Blood Pressure (Systolic)': rec = "BP ↑ → Low salt, calm routine"
        elif param == 'Blood Pressure (Diastolic)': rec = "BP ↑ → Avoid stress, walk daily"
        else: rec = f"{param} high → consult doctor"

    for keyword in DOCTOR_CONTACTS:
        if keyword in history:
            rec += f" | Consult: {DOCTOR_CONTACTS[keyword]}"
            break

    return rec if rec else "Normal"

def process_data(data, age, sex, weight, history):
    output = []
    for param, value in data.items():
        if param in NORMAL_RANGES:
            rec = get_recommendation(param, value, age, sex, weight, history)
            if rec != "Normal":
                output.append(f"{param}: {value} | {rec}")
    return output