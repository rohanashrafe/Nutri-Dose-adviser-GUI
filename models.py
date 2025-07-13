# models.py

class Patient:
    def __init__(self, age, sex, weight, history, blood_data):
        self.age = age
        self.sex = sex
        self.weight = weight
        self.history = history
        self.blood_data = blood_data

    def __str__(self):
        return f"Patient(Age: {self.age}, Sex: {self.sex}, Weight: {self.weight}kg, History: {self.history}, Data: {self.blood_data})"


class Recommendation:
    def __init__(self, parameter, status, advice):
        self.parameter = parameter
        self.status = status  # e.g., 'high', 'low'
        self.advice = advice

    def __str__(self):
        return f"{self.parameter} is {self.status}. {self.advice}"
