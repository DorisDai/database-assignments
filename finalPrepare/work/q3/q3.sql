-- COMP3311 20T3 Final Exam
-- Q3:  performer(s) who play many instruments

-- ... helper views (if any) go here ...

create or replace view noGuitarC(num) as
    select count(distinct instrument)
    from PlaysOn
    where (instrument not like '%guitar%') and (instrument not like 'vocals')
;

create or replace view GuitarC(Gnum) as
    select count(distinct instrument)
    from PlaysOn
    where instrument like '%guitar%'
;

create or replace view ins(total) as
    select num + 1
    from noGuitarC, GuitarC
    where Gnum != 0
;

create or replace view prINoGC(id, num) as
    select performer, count(distinct instrument)
    from PlaysOn as Pr
    where (instrument not like '%guitar%') and (instrument not like 'vocals')
    group by performer
;

create or replace view prIGC(id, Gnum) as
    select performer, count(distinct instrument)
    from PlaysOn as Pr
    where instrument like '%guitar%'
    group by performer
;

create or replace view PrIC(id, num) as
    select N.id, num + 1
    from prINoGC as N join prIGC as Y on N.id = Y.id
    where Gnum != 0
;

create or replace view q3(performer,ninstruments)
as
    select Pr.name, num
    from PrIC 
    join performers as Pr on Pr.id = Po.id
    where num > (select total from ins) / 2
;

