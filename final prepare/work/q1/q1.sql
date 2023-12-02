-- COMP3311 20T3 Final Exam
-- Q1: longest album(s)

-- ... helper views (if any) go here ...

create or replace view albumsLT("group",album,year, aL)
as
    select G.name, A.title, A.year, sum(S.length)
    from Songs as s
    join Albums as A on A.id = S.on_album
    join Groups as G on G.id = A.made_by
    group by G.name, A.title, A.year
;

create or replace view q1("group",album,year)
as
    select "group",album,year
    from albumsLT
    where al = (select max(al) from albumsLT)
;

