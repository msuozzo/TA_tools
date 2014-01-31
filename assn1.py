from people import students_by_uni, tas_by_uni, instructor
from distro_tools import grading_assignments, generate_tar, send_ta_assignments

assn1_tas = tas_by_uni
del assn1_tas["szz2002"]
grading_assns = grading_assignments(assn1_tas, students_by_uni, 1)
for ta in assn1_tas.values():
  generate_tar(ta, grading_assns[ta.uni], 1)
#send_ta_assignments(tas["ms4249"], 1)
