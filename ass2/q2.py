#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... track satisfaction in a given subject

import sys
import psycopg2
import re
from helpers import * 

# define any local helper functions here
# ...

### set up some globals

usage = f"Usage: {sys.argv[0]} SubjectCode"
db = None

### process command-line args

argc = len(sys.argv)
if argc < 2:
  print(usage)
  exit(1)
subject = sys.argv[1]
check = re.compile("^[A-Z]{4}[0-9]{4}$")
if not check.match(subject):
  print("Invalid subject code")
  exit(1)

try:
  qury = """
  select Terms.code, C.satisfact, C.nresponses, P.full_name, count(Ce.student)
  from Subjects as Sub
  right join Courses as C on Sub.id = C.subject
  join Terms on Terms.id = C.term
  join People as P on P.id = C.convenor
  left join Course_enrolments as Ce on C.id = Ce.course
  where Sub.code = %s and Terms.code ~ '(19T[1-3]|20T[0-3]|21T[0-3]|22T[0-3]|23T[0-3])'
  group by Terms.code, C.satisfact, C.nresponses, P.full_name
  order by Terms.code
  """
  db = psycopg2.connect("dbname=ass2")
  subjectInfo = getSubject(db,subject)
  if not subjectInfo:
    print(f"Invalid subject code {subject}")
    exit(1)
  cur = db.cursor()
  cur.execute(qury, [subjectInfo[1]])
  resultL = cur.fetchall()
  print(f"{subject} {subjectInfo[2]}")
  print("Term  Satis  #resp   #stu  Convenor")
  for term, sf, nResp, name, nStu in resultL:
    # format string and print message
    if sf == None:
      sf = f"{'?':>6} "
    else:
      sf = f"{sf:6d} "

    if nResp == None:
      nResp = f"{'?':>6} "
    else:
      nResp = f"{nResp:6d} "

    if name == None:
      name = f"{'?':>6}"
    print(f"{term} " + sf + nResp + f"{nStu:6d}  " + name)
  
except Exception as err:
  print(err)
finally:
  if db:
    db.close()
