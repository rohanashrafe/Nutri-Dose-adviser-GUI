# logic.py
NORMAL_RANGES = {
    "Hemoglobin": (13.5, 17.5),
    "RBC": (4.7, 6.1),
    "WBC": (4000, 11000),
    "Platelets": (150000, 450000),
    "Glucose": (70, 99),
    "Calcium": (8.6, 10.2),
    "Vitamin D": (20, 50),
    "Vitamin B12": (200, 900),
    "Potassium": (3.6, 5.2),
    "Sodium": (135, 145),
    "Blood Pressure Systolic": (90, 120),
    "Blood Pressure Diastolic": (60, 80),
    "Iron": (60, 170),
    "Creatinine": (0.6, 1.3),
    "LDL": (0, 100),
    "HDL": (40, 60),
    "Total Cholesterol": (125, 200)
}

def process_data(data, age, sex, weight, history):
    suggestions = []
    critical_flag = False

    for param, value in data.items():
        if param in NORMAL_RANGES:
            low, high = NORMAL_RANGES[param]
            if value < low:
                suggestions.append(f"🔻 {param} is LOW ({value}): → {get_recommendation(param, 'low')}")
                if is_critical(param, value, "low"):
                    critical_flag = True
            elif value > high:
                suggestions.append(f"🔺 {param} is HIGH ({value}): → {get_recommendation(param, 'high')}")
                if is_critical(param, value, "high"):
                    critical_flag = True

    if not suggestions:
        suggestions.append("✅ All values are within normal range.")

    if critical_flag:
        suggestions.append("⚠️ Serious imbalance detected. Immediate doctor consultation is advised.")

    return suggestions

def get_recommendation(param, level):
    advice = {
        "Hemoglobin": "Eat spinach, liver, red meat.",
        "RBC": "Boost iron and folate intake.",
        "WBC": "Add citrus fruits, garlic, turmeric.",
        "Platelets": "Try papaya leaf juice, vitamin K foods.",
        "Glucose": {
            "high": "Avoid sweets, walk daily.",
            "low": "Take fruits or fruit juice immediately."
        },
        "Calcium": "Drink milk, eat broccoli, almonds.",
        "Vitamin D": "Get morning sun, consider D3 supplement.",
        "Vitamin B12": "Eat meat, eggs, dairy, or take B12.",
        "Potassium": "Eat bananas, coconut water.",
        "Sodium": {
            "high": "Limit salt, avoid chips/processed food.",
            "low": "Add pinch of salt or electrolyte water."
        },
        "Iron": "Lentils, spinach, red meat help.",
        "Creatinine": "Drink water, consult for kidney checkup.",
        "LDL": "Avoid fried food and red meat.",
        "HDL": "Exercise and eat avocado or olive oil.",
        "Total Cholesterol": "Reduce oily food, walk 30 min."
    }

    exercise = " Do light exercise (30 min walk)."

    if param in advice:
        rec = advice[param]
        if isinstance(rec, dict):
            return rec.get(level, "") + exercise
        return rec + exercise

    return "Maintain a healthy lifestyle with good diet and sleep."

def is_critical(param, value, level):
    if param == "Hemoglobin" and value < 8:
        return True
    if param == "Glucose" and (value < 50 or value > 300):
        return True
    if param == "WBC" and (value < 2000 or value > 20000):
        return True
    if param == "Platelets" and value < 50000:
        return True
    if param == "Creatinine" and value > 2.0:
        return True
    return False
