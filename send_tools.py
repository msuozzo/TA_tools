import os
import re
import shutil

lst = os.listdir("finished")
for fname in lst:
  
  if re.match("^[a-zA-Z][a-zA-Z][a-zA-Z]?\d\d\d?\d?\.txt$", fname):
    curr_path = os.path.join("finished", fname)
    new_path = os.path.join("finished_and_sent", fname)
    shutil.move(path, )
    os.path


def send_student_summary(student, ta, hw_num):
  fname = to_fname(student.uni)
  student_email = student.email
  #mail_cmd = "mail -a\"Reply-to:%s\" -s \"Assignment %d Grade Report\" -c \"psb15@columbia.edu\" %s" % (ta.email, hw_num, student.email)
  mail_cmd = "mail -a\"Reply-to:%s\" -s \"Assignment %d Grade Report\" -c \"ms4249@columbia.edu\" %s" % (ta.email, hw_num, student.email)
  call("%s < %s" % (mail_cmd, fname), shell=True)


