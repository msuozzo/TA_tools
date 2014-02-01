from people import students_by_uni, tas_by_uni, instructor
from distro_tools import grading_assignments, generate_tar, send_ta_assignments, generate_assignment_summary

hw1_tas = tas_by_uni
# Stephem did the Recitation so he's not grading this week
del hw1_tas["szz2002"]

hw_num = 1

grading_assns = grading_assignments(hw1_tas, students_by_uni, hw_num)
generate_assignment_summary(grading_assns, hw_num)
for ta_uni, ta in hw1_tas.iteritems():
  generate_tar(ta, grading_assns[ta_uni], hw_num)
#send_ta_assignments(tas, assn_num)
