from random import shuffle, choice
from subprocess import call
import operator
import os


conflict_list = [
  ("ms4249", "ak3533"),
]

def remove_conflicts(assignments):
  # Conflict resolution
  resolved = [False for i in xrange(len(conflict_list))]
  while not reduce(operator.and_, resolved):
    for conflict_ta, conflict_student in conflict_list:
      if conflict_student in assignments[conflict_ta]:
        # Make sure selecting different ta to swap with
        swap_ta = conflict_ta
        while swap_ta == conflict_ta:
          swap_ta = choice(assignments.keys())
        random_student = choice(assignments[swap_ta])
        # switch random student to conflict ta
        assignments[swap_ta].remove(random_student)
        assignments[conflict_ta].append(random_student)
        # switch conflict student to swap ta
        assignments[conflict_ta].remove(conflict_student)
        assignments[swap_ta].append(conflict_student)
    for i in xrange(len(conflict_list)):
      conflict_ta, conflict_student = conflict_list[i]
      resolved[i] = conflict_student not in assignments[conflict_ta]
  return assignments

def grading_assignments(tas, students, hw_num):
  base_assns_per_ta = len(students) / len(tas)
  num_assns_to_grade = [base_assns_per_ta for i in xrange(len(tas))]
  for i in xrange(len(students) % len(tas)):
    num_assns_to_grade[i] += 1
  student_lst_by_uni = sorted(students.values(), key=lambda s: s.uni)
  partitioned_students = []
  base = 0
  for num_assns in num_assns_to_grade:
    student_lst = student_lst_by_uni[base:base + num_assns]
    partitioned_students.append(student_lst)
    base += num_assns
  keys = tas.keys()
  ta_assignments = {}
  for i in xrange(len(keys)):
    ta = keys[i]
    section = partitioned_students[hw_num - i - 1]
    ta_assignments[ta] = section
  ta_assignments = remove_conflicts(ta_assignments)
  return ta_assignments


def grading_assignments_random(tas, students):
  # Generate the most even distribution of students that is possible
  # given the number of tas
  base_assns_per_ta = len(students) / len(tas)
  num_assns_to_grade = [base_assns_per_ta for i in xrange(len(tas))]
  for i in xrange(len(students) % len(tas)):
    num_assns_to_grade[i] += 1
  shuffle(num_assns_to_grade)

  # Randomizes the students and assigns them in sequence to the tas
  shuffled_students = students.values()
  shuffle(shuffled_students)
  partitioned_students = []
  base = 0
  for num_assns in num_assns_to_grade:
    student_lst = shuffled_students[base:base + num_assns]
    partitioned_students.append(student_lst)
    base += num_assns
  ta_assignments = dict(zip(tas.keys(), partitioned_students))
  ta_assignments = remove_conflicts(ta_assignments)
  return ta_assignments


def generate_assignment_summary(ta_assignments, hw_num):
  with open("hw_%s_assignments.txt" % hw_num, "w") as f:
    for ta_uni, student_lst in ta_assignments.iteritems():
      f.write("TA: %s\n" % ta_uni)
      for student in student_lst:
        f.write("%s\n" % student.uni)
      f.write("\n")


def get_file_template(hw_num):
  with open("hw_%s_template.txt" % hw_num, "r") as file_:
    rubric = file_.read()
  return rubric


to_fname = lambda uni: "".join((uni, ".txt"))
to_tar_fname = lambda uni: "".join((uni, ".tar.gz"))

def generate_tar(ta, students, hw_num):
  # Will raise ValueError if hw_num is invalid
  # We use 'rm -rf' so better safe than sorry
  hw_num = int(hw_num)
  # Will raise an error if 'hw_{num}_template.txt' is not found
  file_template = get_file_template(hw_num)
  top_level = "hw_%d_grading" % hw_num
  dir_names = ["to_grade", "graded", "graded_and_sent", "send_utils"]
  grading_dirs = map(lambda name: os.path.join(top_level, name), dir_names)
  os.mkdir(top_level)
  for dir_ in grading_dirs:
    os.mkdir(dir_)
  for student in students:
    file_contents = file_template % (student.name, student.uni)
    file_name = os.path.join(grading_dirs[0], to_fname(student.uni))
    with open(file_name, "w") as f:
      f.write(file_contents)
  code_dir = grading_dirs[3]
  settings_fname = os.path.join(code_dir, "settings.py")
  with open(settings_fname, "w") as f:
    f.write("ta_uni=\"%s\"\n" % ta.uni)
    f.write("hw_num=%d\n" % hw_num)
  call("cp people.py %s" % code_dir, shell=True)
  call("cp students.pkl %s" % code_dir, shell=True)
  init_path = os.path.join(code_dir, "__init__.py")
  call("touch %s" % init_path, shell=True)
  call("cp send_graded.py %s" % top_level, shell=True)
  call("cp people_objs.py %s" % top_level, shell=True)
  assignments_path = os.path.join(top_level, "assignments.txt")
  with open(assignments_path, "w") as f:
    for student in students:
      f.write("%s\n" % student.uni)

  tar_fname = to_tar_fname(ta.uni)
  call("tar -czf %s %s" % (tar_fname, top_level), shell=True)
  call("rm -rf %s" % top_level, shell=True)


def send_ta_assignments(ta, hw_num):
  tar_fname = to_tar_fname(ta.uni)
  encode_cmd = "uuencode \"%s\" hw_%d_grading.tar.gz" % (tar_fname, hw_num)
  mail_cmd = "mail -aREPLY-TO:\"%s\" -s \"Homework %d Grading Assignments\" \"%s\"" % ("ms4249@columbia.edu", hw_num, ta.email)
  call("%s | %s" % (encode_cmd, mail_cmd), shell=True)
  call("make clean", shell=True)


