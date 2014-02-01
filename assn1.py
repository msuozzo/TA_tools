from people import students_by_uni, tas_by_uni, instructor
from distro_tools import grading_assignments, generate_tar, send_ta_assignments

assn1_tas = tas_by_uni
# Stephem did the Recitation so he's not grading this week
del assn1_tas["szz2002"]

assn_num = 1

grading_assns = grading_assignments(assn1_tas, students_by_uni, assn_num)
for ta in assn1_tas.values():
  generate_tar(ta, grading_assns[ta.uni], assn_num)
#send_ta_assignments(tas, assn_num)
