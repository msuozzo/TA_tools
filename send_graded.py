import os
import re
import shutil
import sys
from subprocess import call
from send_utils.people import tas_by_uni, students_by_uni
from send_utils.settings import ta_uni, hw_num

ta = tas_by_uni[ta_uni]

lst = os.listdir("graded")
for fname in lst:
  if re.match("^[a-zA-Z][a-zA-Z][a-zA-Z]?\d\d?\d?\d?\.txt$", fname):
    student_uni = fname.split(".")[0]
    student = students_by_uni[student_uni]
    curr_path = os.path.join("graded", fname)
    new_path = os.path.join("graded_and_sent", fname)
    #mail_cmd = "mail -a\"Reply-to:%s\" -s \"Assignment %d Grade Report\" -c \"psb15@columbia.edu\" %s" % (ta.email, hw_num, student.email)
    mail_cmd = "mail -a\"Reply-to:%s\" -s \"Assignment %d Grade Report\" -c \"ms4249@columbia.edu\" %s" % (ta.email, hw_num, student.email)
    call("%s < %s" % (mail_cmd, fname), shell=True)
    shutil.move(curr_path, new_path)
