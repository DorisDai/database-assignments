# COMP3311 21T3 Ass2 ... Python helper functions
# add here any functions to share between Python scripts 
# you must submit this even if you add nothing

def getProgram(db,code):
  cur = db.cursor()
  cur.execute("select * from Programs where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getStream(db,code):
  cur = db.cursor()
  cur.execute("select * from Streams where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getStudent(db,zid):
  cur = db.cursor()
  qry = """
  select p.*
  from   People p
         join Students s on s.id = p.id
  where  p.zid = %s
  """
  cur.execute(qry,[zid])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getSubject(db, subject):
  cur = db.cursor()
  qury = 'select s.* from Subjects as s where code = %s'
  cur.execute(qury, [subject])
  subjectInfo = cur.fetchone()
  cur.close()
  if not subjectInfo:
    return None
  else:
    return subjectInfo

def convertNoneToString(string):
  if string == None:
    return 'None'
  else:
    return string
  
def transcript(db, zid):
  stuQury = """
  select P.zid, family_name, given_names, S.id 
  from Students as S
  join People as P on P.id = S.id
  where P.zid = %s
  """
  cur = db.cursor()
  cur.execute(stuQury, [zid])
  stuInfo = cur.fetchone()
  print(f"{stuInfo[0]} {stuInfo[1]}, {stuInfo[2]}")

  sId = stuInfo[3]
  # student enrolled program and stream info qury
  proQury = """
  select Pg.code, Sr.code, Pg.name
  from Program_enrolments as Pe
  join Programs as Pg on Pe.program = Pg.id
  join Stream_enrolments as Se on Se.part_of = Pe.id
  join Streams as Sr on Sr.id = Se.stream
  where Pe.student = %s
  order by Pe.term desc
  """
  cur.execute(proQury, [sId])
  proEnrol = cur.fetchone()
  print(f"{proEnrol[0]} {proEnrol[1]} {proEnrol[2]}")

  # students' courses' grades info qury
  transcriptQ = """
  select Subj.code, T.code, Subj.title, Ce.mark, Ce.grade, Subj.uoc
  from Course_enrolments as Ce
  join Courses as C on C.id = Ce.course
  join Subjects as Subj on Subj.id = C.subject
  join Terms as T on T.id = C.term
  where Ce.student = %s
  order by T.code, Subj.code
  """
  cur.execute(transcriptQ, [sId])
  gradesL = cur.fetchall()
  cur.close()
  return gradesL

def getProReq(db, code):
  reqsql = """
  select Pro.name, R.name, rtype, min_req, max_req, acadobjs
  from Requirements as R
  join Programs as Pro on R.for_program = Pro.id
  where Pro.code = %s
  """
  cur = db.cursor()
  cur.execute(reqsql, [code])
  reqL = cur.fetchall()
  cur.close()
  return reqL

def getStreamReq(db, code):
  reqsql = """
  select Str.name, R.name, rtype, min_req, max_req, acadobjs
  from Requirements as R
  join Streams as Str on R.for_stream = Str.id
  where Str.code = %s
  """
  cur = db.cursor()
  cur.execute(reqsql, [code])
  reqL = cur.fetchall()
  cur.close()

  return reqL