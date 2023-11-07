#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... track proportion of overseas students

import sys
import psycopg2
import re

# define any local helper functions here
# ...

### set up some globals

db = None
ifINTL= '!='
### process command-line args
selectString = f"""
select T.code, count(distinct S.id)
from Program_enrolments Pe
join Terms T on Pe.term = T.id
join Students S on S.id = Pe.student
where S.status {ifINTL} 'INTL'
group by T.code
"""

try:
  db = psycopg2.connect("dbname=ass2")
  cur = db.cursor()
  cur.execute(selectString)
  lStudentCount = cur.fetchall()

  ifINTL = '='
  cur.execute(selectString)
  iStudentCount = cur.fetchall()
  for lterm, lSCount in lStudentCount:
    for sterm, iScount in iStudentCount:
      if (lterm == sterm):

        print(f"{sterm} {lSCount:6d} {iScount:6d} {lSCount/iScount:6.1f}")
          
except Exception as err:
  print(err)
finally:
  if db:
    db.close()
