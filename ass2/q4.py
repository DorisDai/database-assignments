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
  select P.zid, family_name, given_names 
  from Students as S
  join People as P on P.id = S.id
  where P.zid = '5893146'
  """
  cur = db.cursor()
  cur.execute(stuQury)
  stuInfo = cur.fetchone()
  print(f"{stuInfo[0]} {stuInfo[1]}, {stuInfo[2]}")


finally:
  if db:
    db.close()

