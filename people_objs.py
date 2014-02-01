class CU_Person:
  def __init__(self, name, uni, email):
    self.first_name = name.split(", ")[1].split(" ", 1)[0]
    self.name = name
    self.uni = uni
    self.email = email

class Teacher(CU_Person):
  pass

class Student(CU_Person):
  pass

