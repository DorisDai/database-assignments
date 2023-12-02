-- COMP3311 20T3 Final Exam
-- Q2: group(s) with no albums

-- ... helper views (if any) go here ...

create or replace view no_album(Aid, Acount) as
    select G.id, count(A.made_by)
    from Groups as G 
    left join Albums as A on G.id = A.made_by
    group by G.id
;

create or replace view q2("group")
as
    select name from no_album join Groups as G on G.id = Aid
    where Acount = 0
;

