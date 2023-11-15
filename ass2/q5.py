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
  returned = False
  for course in SelecL:
    i = 0
    matched = True
    if type(course) == str and len(course) == 8:
      for i in range(0, len(course)):
        
        if course[i] != '#' and course[i] != CourseCode[i]:
          matched = False
      if matched:
        return True
  if not returned:
    return False
def checkLimit(count, upperLimit):
  if upperLimit == None or count <= upperLimit:
    return True
  else:
    return False
def checkLowerLimit(count, lowerLimit):
  if lowerLimit == None or count >= lowerLimit:
    return True
  else:
    return False
def checkInCoreList(courseCode, coreLists):
  for coreList in coreLists:
    for course in coreList:
      if courseCode in course:
        return True
  return False
def removeFromCoreList(courseCode, coreLists):
  for coreList in coreLists:
    for course in coreList:
      if courseCode in course:
        coreList.remove(course)
        return coreList[-1]
  return False

def getNumUocRemain(db, coreList):
  result = []
  # result = [(coreInfo1), (coreInfo2),...., totalNumUoc]
  totalUoc = 0
  for core in coreList:
    if len(core) == 8:
      courseInfo = getCourseUOCAndName(db, core)
      result.append(courseInfo)
      totalUoc += courseInfo[2]
    elif len(core) == 19 and '{' in core and ';' in core:
      alternativeC = core.split(';')
      alt = []
      course1Info = getCourseUOCAndName(db, alternativeC[0][1:])
      alt.append(course1Info)
      course2Info = getCourseUOCAndName(db, alternativeC[1][:-1])
      alt.append(course2Info)
      result.append(alt)
      totalUoc += course2Info[2]
  if result != []:
    result.append(totalUoc)
  return result

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
  streamReqs = getStreamReq(db, strmCode)
  print(streamReqs)
  # assume requirement type at most 1 for program  or stream
  for streamName, reqName, rtype, min_req, max_req, acadobjs in streamReqs:
    if rtype == 'core':
      newCoreL = acadobjs.split(',')
      newCoreL.append(reqName)
      ScoreL.append(newCoreL)
    elif rtype == 'elective':
      SelecL += acadobjs.split(',')
      SelecL.append(0)
      SelecL.append(min_req)
      SelecL.append(max_req)
      SelecL.append(reqName)
    elif rtype == 'free':
      freeL.append(0)
      freeL.append(min_req)
      freeL.append(max_req)
      freeL.append(reqName)
  courseReqs = getProReq(db, progCode)
  print(courseReqs)
  for streamName, reqName, rtype, min_req, max_req, acadobjs in courseReqs:
    if rtype == 'core':
      newCoreL = acadobjs.split(',')
      newCoreL.append(reqName)
      CcoreL.append(newCoreL)
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
    GradeString = Grade
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
    
    nameReq = None
    if Grade in failUOC or Grade in unrsUOC or Grade == f"{'-':>2}":
      nameReq = ''
    elif checkInCoreList(CourseCode, ScoreL):
      nameReq = removeFromCoreList(CourseCode, ScoreL)
    elif checkInCoreList(CourseCode, CcoreL):
      nameReq = removeFromCoreList(CourseCode, CcoreL)
    elif inElectiveList(CourseCode, SelecL) and checkLimit(SelecL[-4] + UOC, SelecL[-2]):
      nameReq = SelecL[-1]
      SelecL[-4] += UOC
    elif inElectiveList(CourseCode, CelecL) and checkLimit(CelecL[-4] + UOC, CelecL[-2]):
      nameReq = CelecL[-1]
      CelecL[-4] += UOC
    elif geneL != [] and checkLimit(geneL[-4] + UOC, geneL[-2]):
      nameReq = geneL[-1]
      geneL[-4] += UOC
    elif freeL != [] and checkLimit(freeL[-4] + UOC, freeL[-3]):
      nameReq = freeL[-1]
      freeL[-4] += UOC  
    else:
      nameReq = 'Could not be allocated'
      UOCString = ' 0uoc'  
    print(f"{CourseCode} {Term} {SubjectTitle:<32s}{Mark:>3} {Grade:>2s}  {UOCString}  {nameReq}")
    

    # calculate attempted uoc and achieved uoc and weighted_mark
    if Grade in achievedUOC and UOCString != ' 0uoc':
      total_achieved_uoc += UOC
    if Grade in wamUOC:
      total_attempted_uoc += UOC
      if Mark == f"{'-':>3}":
        Mark = 0
      weighted_mark_sum += Mark * UOC
  # print achieved uoc and wam
  print(f"UOC = {total_achieved_uoc}, WAM = {round(weighted_mark_sum / total_attempted_uoc, 1)}")

  allCompleted = True
  if ScoreL != []:
    for courseL in ScoreL:
      if len(courseL) > 1:
        subjInfoL = getNumUocRemain(db, courseL)
        if subjInfoL != []:
          print(f"Need {subjInfoL[-1]} more UOC for {courseL[-1]}")
          for subj in subjInfoL:
            if not isinstance(subj, (int, list)):
              print(f"- {subj[0]} {subj[1]}")
            elif isinstance(subj, list):
              course1 = subj[0]
              course2 = subj[1]
              print(f"- {course1[0]} {course1[1]}")
              print(f"  or {course2[0]} {course2[1]}")
              
  if CcoreL != []:
    
    for courseL in CcoreL:
      if len(courseL) > 1:
        subjInfoL = getNumUocRemain(db, courseL)
        if subjInfoL != []:
          print(f"Need {subjInfoL[-1]} more UOC for {courseL[-1]}")
          for subj in subjInfoL:
            if not isinstance(subj, (int, list)):
              print(f"- {subj[0]} {subj[1]}")
            elif isinstance(subj, list):
              course1 = subj[0]
              course2 = subj[1]
              print(f"- {course1[0]} {course1[1]}")
              print(f"  or {course2[0]} {course2[1]}")

  if SelecL != [] and not checkLowerLimit(SelecL[-4], SelecL[-3]):
    print(f"Need {SelecL[-3] - SelecL[-4]} more UOC for {SelecL[-1]}")
  if CelecL != [] and not checkLowerLimit(CelecL[-4], CelecL[-3]):
    print(f"Need {CelecL[-3] - CelecL[-4]} more UOC for {CelecL[-1]}")
  if freeL != [] and not checkLowerLimit(freeL[-4], freeL[-3]):
    print(f"Need {freeL[-3] - freeL[-4]} more UOC for {freeL[-1]}")
  if geneL != [] and not checkLowerLimit(geneL[-4], geneL[-3]):
    print(f"Need {geneL[-3] - geneL[-4]} more UOC for {geneL[-1]}")

finally:
  if db:
    db.close()

