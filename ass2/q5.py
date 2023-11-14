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
  coreL = []
  elecL = []
  geneL = []
  freeL = []
  currCoreL = []
  currElecL = []
  currGeneL = []
  currFreeL = []
  streamReqs = getStreamReq(db, 'COMPA1')
  # assume requirement type at most 1 for program  or stream
  for streamName, reqName, rtype, min_req, max_req, acadobjs in streamReqs:
    if rtype == 'core':
      coreL = acadobjs.split(',')
      coreL.append(reqName)
    elif rtype == 'elective':
      elecL = acadobjs.split(',')
      elecL.append(min_req)
      elecL.append(max_req)
      elecL.append(reqName)
    elif rtype == 'gened':
      geneL.append(min_req)
      geneL.append(max_req)
      geneL.append(reqName)
    elif rtype == 'free':
      freeL.append(min_req)
      freeL.append(max_req)
      freeL.append(reqName)
  print(coreL, elecL, geneL, freeL)
  courseReqs = getProReq(db, '3707')

except Exception as err:
  print("DB error: ", err)
finally:
  if db:
    db.close()

