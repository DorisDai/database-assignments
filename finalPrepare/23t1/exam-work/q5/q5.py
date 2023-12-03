#! /usr/bin/env python3

# COMP3311 23T1 Final Exam
# Q5: Print details of accounts at a named branch

import sys
import psycopg2

### Constants
USAGE = f"Usage: {sys.argv[0]} <branch name>"

### Globals
db = None

### Queries

### replace this line with any query templates ###

### Command-line args
if len(sys.argv) != 2:
    print(USAGE, file=sys.stderr)
    sys.exit(1)
suburb = sys.argv[1]


try:
    db = psycopg2.connect("dbname=bank")
    cur = db.cursor()
    findsub = """
    select location, assets, id from Branches 
    where location = %s
    """
    cur.execute(findsub, [suburb])
    brInfo = cur.fetchone()
    if not brInfo:
        print(f'No such branch {suburb}')
        exit(1)
    
    print(f'{brInfo[0]} branch ({brInfo[2]}) holds')
    accsQ ="""
    select A.id, C.given || C.family, C.lives_in, A.balance
    from Branches B
    join Accounts A on B.id = A.held_at
    join Held_by H on H.account = A.id
    join Customer C on C.id = H.customer
    where B.id = %s
    """
    cur.execute(accsQ)
    accs = cur.fetchall()
    brsum = 0
    for id, name, livesIn, balance in accs:
        print(f'- account {id} owned by {name} from {livesIn} with {balance}')
        brsum += balance
    print(f'Assets: {brsum}')
    if brsum != brInfo[1]:
        print('Discrepancy between assets and sum of account balances')
    

finally:
    if db is not None:
        db.close()
sys.exit(0)

### replace this line by any helper functions ###
