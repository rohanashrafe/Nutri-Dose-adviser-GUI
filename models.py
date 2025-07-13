
class Patient:
    def _init_(self, age, sex, weight, history, parameters):
        self.age = age
        self.sex = sex
        self.weight = weight
        self.history = history.lower()
        self.parameters = parameters