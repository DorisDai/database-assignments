#!/usr/bin/python3
# COMP3311 21T3 Ass2 ... progression check for a given student

import sys
import psycopg2
import re
from helpers import *

# define any local helper functions here

### set up some globals

usage = f"Usage: {sys.argv[0]} zID [Program Stream]"
db = []

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
  print("Invalid student ID")
  exit(1)

progCode = []
strmCode = []

if argc == 4:
  progCode = sys.argv[2]
  strmCode = sys.argv[3]

# manipulate database

def inElectiveList(CourseCode, SelecL):
  for course in SelecL:
    i = 0
    for i in range(0, len(course)):
      if course[i] != '#' and course[i] != CourseCode[i]:
        return False
    return True
def checkLimit(count, max):
  if max == None or count < max:
    return True
  else:
    return False
try:
  db = psycopg2.connect("dbname=ass2")

  stuInfo = getStudent(db,zid)
  if not stuInfo:
    print(f"Invalid student id {zid}")
    exit(1)
  #print(stuInfo) # debug

  if progCode:
    progInfo = getProgram(db,progCode)
    if not progInfo:
      print(f"Invalid program code {progCode}")
      exit(1)
    #print(progInfo)  #debug

  if strmCode:
    strmInfo = getStream(db,strmCode)
    if not strmInfo:
      print(f"Invalid program code {strmCode}")
      exit(1)
    #print(strmInfo)  #debug

  # suppose every students all enrolled in 1 program and 1 stream
  ScoreL = []
  SelecL = []
  CcoreL = []
  CelecL = []
  geneL = []
  freeL = []
  streamReqs = getStreamReq(db, 'COMPA1')
  # assume requirement type at most 1 for program  or stream
  for streamName, reqName, rtype, min_req, max_req, acadobjs in streamReqs:
    if rtype == 'core':
      ScoreL += acadobjs.split(',')
      ScoreL.append(reqName)
    elif rtype == 'elective':
      SelecL += acadobjs.split(',')
      SelecL.append(min_req)
      SelecL.append(max_req)
      SelecL.append(reqName)
    elif rtype == 'free':
      freeL.append(0)
      freeL.append(min_req)
      freeL.append(max_req)
      freeL.append(reqName)
  print(ScoreL, SelecL, geneL, freeL)
  courseReqs = getProReq(db, '3778')
  for streamName, reqName, rtype, min_req, max_req, acadobjs in courseReqs:
    if rtype == 'core':
      CcoreL += acadobjs.split(',')
      CcoreL.append(reqName)
    elif rtype == 'elective':
      CelecL += acadobjs.split(',')
      CelecL.append(0)
      CelecL.append(min_req)
      CelecL.append(max_req)
      CelecL.append(reqName)
    elif rtype == 'gened':
      geneL.append(0)
      geneL.append(min_req)
      geneL.append(max_req)
      geneL.append(reqName)
  print(CcoreL, CelecL, geneL, freeL)
  
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
      Grade = f"{'-':>3}"
    if len(SubjectTitle) > 31:
      SubjectTitle = SubjectTitle[:31]
    
    nameReq = None
    print(CourseCode)
    if Grade in failUOC or Grade in unrsUOC or Grade == None:
      nameReq = ''
    elif CourseCode in ScoreL:
      nameReq = ScoreL[-1]
      ScoreL.remove(CourseCode)
    elif CourseCode in CcoreL:
      nameReq = CcoreL[-1]
      CcoreL.remove(CourseCode)
    elif inElectiveList(CourseCode, SelecL) and checkLimit(SelecL[-4] + UOC, SelecL[-2]):
      nameReq = SelecL[-1]
      SelecL[-4] += UOC
    elif inElectiveList(CourseCode, CelecL) and checkLimit(CelecL[-4] + UOC, CelecL[-2]):
      nameReq = CelecL[-1]
      CelecL[-4] += 1
    elif checkLimit(geneL[-4] + UOC, geneL[-2]):
      nameReq = geneL[-1]
      geneL[-4] += 1
    elif checkLimit(freeL[-4] + UOC, freeL[-2]):
      nameReq = freeL[-1]
      freeL[-4] += 1  
    else:
      nameReq = 'Could not be allocated'
      UOCString = '  0uoc'
    print(CcoreL)      
    print(f"{CourseCode} {Term} {SubjectTitle:<32s}{Mark:>3} {Grade:>2s}  {UOCString}  {nameReq}")
    

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

