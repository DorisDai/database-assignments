#!/usr/bin/python3
# COMP3311 22T3 Ass2 ... print a transcript for a given student

import sys
import psycopg2
import re
from helpers import getStudent

# define any local helper functions here

### set up some globals

usage = f"Usage: {sys.argv[0]} zID"
db = None

### process command-line args

argc = len(sys.argv)
if argc < 2:
  print(usage)
  exit(1)
zid = sys.argv[1]
if zid[0] == 'z':
  zid = zid[1:8]
digits = re.compile("^\d{7}$")
if not digits.match(zid):
  print(f"Invalid student ID {zid}")
  exit(1)

# manipulate database

try:
  db = psycopg2.connect("dbname=ass2")
  stusInfo = getStudent(db,zid)
  if not stusInfo:
    print(f"Invalid student ID {zid}")
    exit()

  stuQury = """
  select P.zid, family_name, given_names, S.id 
  from Students as S
  join People as P on P.id = S.id
  where P.zid = '5893146'
  """
  cur = db.cursor()
  cur.execute(stuQury)
  stuInfo = cur.fetchone()
  print(f"{stuInfo[0]} {stuInfo[1]}, {stuInfo[2]}")
  sId = stuInfo[3]
  print(sId)
  proQury = """
  select Pg.code, Sr.code, Pg.name
  from Program_enrolments as Pe
  join Programs as Pg on Pe.program = Pg.id
  join Stream_enrolments as Se on Se.part_of = Pe.id
  join Streams as Sr on Sr.id = Se.stream
  where Pe.student = %s
  order by Pe.term desc
  """
  cur.execute(proQury, [sId])
  proEnrol = cur.fetchone()
  print(f"{proEnrol[0]} {proEnrol[1]} {proEnrol[2]}")
  transcriptQ = """
  select Subj.code, T.code, Subj.title, Ce.mark, Ce.grade, Subj.uoc
  from Course_enrolments as Ce
  join Courses as C on C.id = Ce.course
  join Subjects as Subj on Subj.id = C.subject
  join Terms as T on T.id = C.term
  where Ce.student = %s
  order by T.code, Subj.code
  """
  cur.execute(transcriptQ, [sId])
  gradesL = cur.fetchall()
  xUOC = 'A,B,C,D,HD,DN,CR.PS,XE,T,SY,EC,RC'.split(',')
  failUOC = 'AF,FL,UF,E,F'.split(',')
  unrsUOC = 'AS,AW,PW,NA,RD,NF,NC,LE,PE,WD,WJ'.split(',')
  total_achieved_uoc = 0
  total_attempted_uoc = 0
  weighted_mark_sum = 0
  achievedUOC = 'A,B,C,D,HD,DN,CR,PS,XE,T,SY,EC,RC'.split(',')
  wamUOC = 'HD,DN,CR,PS,AF,FL,UF,E,F'
  for CourseCode, Term, SubjectTitle, Mark, Grade, UOC in gradesL:
    UOCString = f"{UOC:2d}uoc"
    if Grade in failUOC:
      UOCString = ' fail'
    elif Grade in unrsUOC:
      UOCString = ' unrs'
    elif Grade == None:
      UOCString = ''
    if Mark == None:
      Mark = f"{'-':>3}"
    if Grade == None:
      Grade = f"{'-':>3}"
    if len(SubjectTitle) > 31:
      SubjectTitle = SubjectTitle[:31]
    print(f"{CourseCode} {Term} {SubjectTitle:<32s}{Mark:>3} {Grade:>2s}  {UOCString}")
    if Grade in achievedUOC:
      total_achieved_uoc += UOC
    if Grade in wamUOC:
      total_attempted_uoc += UOC
      if Mark == f"{'-':>3}":
        Mark = 0
      weighted_mark_sum += Mark
  print(weighted_mark_sum, total_attempted_uoc)
  print(f"UOC = {total_achieved_uoc}, WAM = {weighted_mark_sum / total_attempted_uoc}")
  

finally:
  if db:
    db.close()

