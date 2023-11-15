#!/usr/bin/python3
# COMP3311 22T3 Ass2 ... print a transcript for a given student

import sys
import psycopg2
import re
from helpers import getStudent, transcript

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
  # student info qury
  gradesL = transcript(db, zid)
  failUOC = 'AF,FL,UF,E,F'.split(',')
  unrsUOC = 'AS,AW,PW,NA,RD,NF,NC,LE,PE,WD,WJ'.split(',')
  total_achieved_uoc = 0
  total_attempted_uoc = 0
  weighted_mark_sum = 0
  achievedUOC = 'A,B,C,D,HD,DN,CR,PS,XE,T,SY,EC,RC'.split(',')
  wamUOC = 'HD,DN,CR,PS,AF,FL,UF,E,F'
  for CourseCode, Term, SubjectTitle, Mark, Grade, UOC in gradesL:
    # check grade type and form uoc string
    UOCString = f"{UOC:2d}uoc"
    if Grade in failUOC:
      UOCString = ' fail'
    elif Grade in unrsUOC:
      UOCString = ' unrs'
    elif Grade == None:
      UOCString = ''
    
    # format mark and grade string if it is null
    if Mark == None:
      Mark = f"{'-':>3}"
    if Grade == None:
      Grade = f"{'-':>2}"
    if len(SubjectTitle) > 31:
      SubjectTitle = SubjectTitle[:31]
    print(f"{CourseCode} {Term} {SubjectTitle:<32s}{Mark:>3} {Grade:>2s}  {UOCString}")

    # calculate attempted uoc and achieved uoc and weighted_mark
    if Grade in achievedUOC:
      total_achieved_uoc += UOC
    if Grade in wamUOC:
      total_attempted_uoc += UOC
      if Mark == f"{'-':>3}":
        Mark = 0
      weighted_mark_sum += Mark * UOC
  # print achieved uoc and wam
  print(f"UOC = {total_achieved_uoc}, WAM = {round(weighted_mark_sum / total_attempted_uoc, 1)}")
  

finally:
  if db:
    db.close()

