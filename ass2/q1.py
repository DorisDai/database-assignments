#!/usr/bin/python3
# COMP3311 23T3 Ass2 ... track proportion of overseas students

import sys
import psycopg2
import re

# define any local helper functions here
# ...

### set up some globals

db = None

### process command-line args
localStString = f"""
select T.code, count(distinct S.id)
from Program_enrolments Pe
join Terms T on Pe.term = T.id
join Students S on S.id = Pe.student
where S.status != 'INTL'
group by T.code
having T.code ~ '(19T[1-3]|20T[0-3]|21T[0-3]|22T[0-3]|23T[0-3])'
order by T.code
"""

interStString = f"""
select T.code, count(distinct S.id)
from Program_enrolments Pe
join Terms T on Pe.term = T.id
join Students S on S.id = Pe.student
where S.status = 'INTL'
group by T.code
having T.code ~ '(19T[1-3]|20T[0-3]|21T[0-3]|22T[0-3]|23T[0-3])'
order by T.code
"""

try:
  db = psycopg2.connect("dbname=ass2")
  cur = db.cursor()
  year = 20
  cur.execute(localStString)
  lStudentCount = cur.fetchall()

  cur.execute(interStString)
  iStudentCount = cur.fetchall()
  print('Term  #Locl  #Intl Proportion')
  for lterm, lSCount in lStudentCount:
    for sterm, iScount in iStudentCount:
      if (lterm == sterm):
        print(f"{sterm} {lSCount:6d} {iScount:6d} {lSCount/iScount:6.1f}")
      
except Exception as err:
  print(err)
finally:
  if db:
    db.close()
