import pickle
from people_objs import Teacher, Student

def students_from_roster():
  roster_lines = open("roster_1_30.txt").read().splitlines()
  students = {}
  for i in xrange(0, len(roster_lines), 4):
    if not roster_lines[i]: break
    name, uni, email = roster_lines[i:i + 3]
    students[uni] = Student(name, uni, email)
  return students

def pickle_students():
  students_by_uni = students_from_roster()
  with open("students.pkl", "wb") as pkl_file:
    pickle.dump(students_by_uni, pkl_file)

def get_students():
  students_by_uni = None
  try:
    pkl_file = open("students.pkl", "rb")
  except IOError:
    pkl_file = open("send_utils/students.pkl", "rb")
  students_by_uni = pickle.load(pkl_file)
  pkl_file.close()
  return students_by_uni

#pickle_students()
students_by_uni = get_students()

ta_list = [
  Teacher("Teng, Anna", "awt2116", "awt2116@columbia.edu"),
  Teacher("Matthieson, Cooper", "ctm2126", "ctm2126@columbia.edu"),
  Teacher("Joo, Hyonjee", "hj2339", "hj2339@columbia.edu"),
  Teacher("Lin, James", "jl3782", "jl3782@columbia.edu"),
  Teacher("Wen, James", "jrw2175", "jrw2175@columbia.edu"),
  Teacher("Suozzo, Matthew", "ms4249", "ms4249@columbia.edu"),
  Teacher("Chang, Nai Chen", "nc2539", "nc2539@columbia.edu"),
  Teacher("Zhou, Stephen", "szz2002", "szz2002@columbia.edu"),
  Teacher("He, Lucy", "lh2574", "lh2574@columbia.edu")
]
tas_by_uni = dict(((ta.uni, ta) for ta in ta_list))

instructor = Teacher("Blaer, Paul", "psb15", "psb15@columbia.edu")
