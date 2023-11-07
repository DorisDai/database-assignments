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
selectString = """
select T.code, count(distinct S.id)
from Program_enrolments Pe
join Terms T on Pe.term = T.id
join Students S on S.id = Pe.student
where S.status %s 'INTL'
group by T.code
"""

try:
  db = psycopg2.connect("dbname=ass2")
  cur = db.cursor()
  cur.execute(selectString, ["!="])
  for lStudentCount in cur.fetchall():
    print(f"{lStudentCount[0]} {lStudentCount[1]}")
  # show term, #locals, #internationals, fraction

  # ... add your code here ...

except Exception as err:
  print(err)
finally:
  if db:
    db.close()
