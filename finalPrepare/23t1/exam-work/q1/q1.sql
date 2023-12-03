-- COMP3311 23T1 Final Exam
-- Q1: suburbs with the most customers

create or replace view subC(suburb,nPeople)
as
    select lives_in, count(id)
    from Customers group by lives_in
;

create or replace view q1(suburb,ncust)
as
    select suburb, nPeople
    from subC
    where nPeople = 
    (select max(nPeople) from subC)
;
