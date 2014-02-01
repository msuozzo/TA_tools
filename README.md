TA_tools
========

Makes TA'ing just a bit easier

###How to Grade
This assumes you have a clic account but assumes little knowledge of the command line. It contains all of the commands you will need to grade.  
Any string enclosed by braces in the commands requires you substitute whatever information is required to make the command work as intended. `{your_uni}` : your uni. `{hw#}` : The assignment number.

- Download the tar file sent your columbia.edu address. The email with have the subject line "Homework {HW#} Grading Assignments" and the attached file will be called `{your_uni}.tar.gz`.
- Navigate at the command line to your Downloads folder (on Mac, `cd Downloads`).
- Copy the tar file to your clic account:  
`scp {your_uni}.tar.gz {your_uni}@clic.cs.columbia.edu://home/{your_uni}`
- SSH into you clic account. If you prefer to use vim to edit files, use the following command:  
`ssh {your_uni}@clic.cs.columbia.edu`  
If you prefer to use a graphical text editor (something like TextEdit on Mac or Notepad on Windows), add a `-X` flag (for X-forwarding):  
`ssh -X {your_uni}@clic.cs.columbia.edu`
- `ls` to check that the tar file is present.
- Untar the file to generate a directory called `hw_{hw#}_grading`:  
`tar -xvf {your_uni}.tar.gz`
You should see a listing of the files contained in the tar.
- Enter the directory:  
`cd hw_{hw#}_grading`
- The ungraded files are located in the `to_grade` directory. `cd` into this directory:  
`cd to_grade`  
If you `ls`, you should see a list of files named with the format `{student_uni}.txt`.
- To grade with a command-line text editor such as vim:  
`vim {student_uni}.txt`  
To grade with a graphical editor (assuming you used the `-X` flag to ssh):  
`gedit {student_uni}.txt`  
Note: Because you're running `gedit` in X Windowing, it will be a bit sluggish. It's kind of a pain.
- After you finish grading an assignment:  
`mv {student_uni}.txt ../graded`
- To email the grade summary to the student, you must be in the top-level `hw_{hw#}_grading` directory. From the `to_grade` directory, `cd ..`. The send script takes all grading summaries in `graded`, emails them to the associated student, and moves the sent summaries to the directory `graded_and_sent`. To the run the script:  
`python send_graded.py`  
__WARNING__: This action emails the student and CCs Paul Blaer. For their sakes, use with caution.


###How to Generate and Send Out Grading Assignments
Example shown in `hw1.py`
- First, a template file must be created in the top-level directory of the repository with the name `hw_{hw#}_template.txt`. This file must contain 2 `%s` arguments (Python string formatting arguments) which represent, in sequence, the student's name and uni.
- The series of commands in `hw1.py` (along with the commented-out `send_ta_assignments` function call) should be run to generate the assignments and then email them to the group.
- To run, simple execute this script. In the case of `hw1.py`:  
`python hw1.py`
- A list of all TAs and their assigned students called `hw_{hw_num}_assignments.txt` is generated upon running the script.
