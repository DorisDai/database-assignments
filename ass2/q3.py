#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... print list of rules for a program or stream

import sys
import psycopg2
import re
from helpers import getProgram, getStream, getSubject, checkGetItemNone

# define any local helper functions here
# ...

### set up some globals

usage = f"Usage: {sys.argv[0]} (ProgramCode|StreamCode)"
db = None

### process command-line args

argc = len(sys.argv)
if argc < 2:
  print(usage)
  exit(1)
code = sys.argv[1]
if len(code) == 4:
  codeOf = "program"
elif len(code) == 6:
  codeOf = "stream"
else:
  print("Invalid code")
  exit(1)

def printFormatRequirements(reqList):
  for programName, reqName, reqType, minReq, maxReq, acadobjs in reqs:
    if minReq == maxReq:
      uocString = str(minReq) + 'UOC'
    elif minReq == None:
      uocString = None
    elif minReq == None:
      uocString = 'up to ' + str(maxReq) + ' UOC'
    elif maxReq == None:
      uocString = 'at least ' + str(minReq) + ' UOC'
    
    if reqType == 'uoc':
      print(reqName + ' ' + uocString)
    elif reqType == 'elective':
      print(uocString + ' courses from ' + reqName)
      print('- ' + acadobjs)
    elif reqType == 'free':
      print(uocString + ' of ' + 'Free Electives')
    elif reqType == 'gened':
      print(uocString + ' of ' + 'General Education')
    elif reqType == 'stream':
      # suppose streams' minreq == maxreq 
      print(str(minReq) + ' stream from ' + reqName)
      streamList = acadobjs.split(',')
      for strm in streamList:
        currstrm = getStream(db, strm)
        currstrmStr = checkGetItemNone(currstrm[2])
        print('- ' + strm + ' ' + currstrmStr)
      
    elif reqType == 'core':
      print('all courses from ' + reqName)
      courseList = acadobjs.split(',')
      for course in courseList:
        if '{' in course:
          alternativeC = course.split(';')
          currCourse = getSubject(db, alternativeC[0][1:])
          currCourseStr = checkGetItemNone(currCourse[2])
          print('- ' + alternativeC[0][1:] + ' ' + currCourseStr)
          currCourse = getSubject(db, alternativeC[1][:-1])
          currCourseStr = checkGetItemNone(currCourse[2])
          print('  or ' + alternativeC[1][:-1] + ' ' + currCourseStr)
        else:
          currCourse = getSubject(db, course)
          currCourseStr = checkGetItemNone(currCourse[2])
          print('- ' + course + ' ' + currCourseStr)

try:
  db = psycopg2.connect("dbname=ass2")
  if codeOf == "program":
    progInfo = getProgram(db,code)
    if not progInfo:
      print(f"Invalid program code {code}")
      exit(1)
    #print(progInfo)  #debug
    reqsql = """
    select Pro.name, R.name, rtype, min_req, max_req, acadobjs
    from Requirements as R
    join Programs as Pro on R.for_program = Pro.id
    where Pro.code = %s
    """
    cur = db.cursor()
    cur.execute(reqsql, [code])
    reqs = cur.fetchone()
    print(f"{code} {reqs[0]}")
    print("Academic Requirements:")
    cur.execute(reqsql, [code])
    reqs = cur.fetchall()
    uocString = None
    printFormatRequirements(reqs)


  elif codeOf == "stream":
    strmInfo = getStream(db,code)
    if not strmInfo:
      print(f"Invalid stream code {code}")
      exit(1)
    #print(strmInfo)  #debug

    # List the rules for Stream

    # ... add your code here ...

finally:
  if db:
    db.close()
