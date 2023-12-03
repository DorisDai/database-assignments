-- COMP3311 23T1 Final Exam
-- Q2: ids of people with same name

-- replace this line with any helper views --

create or replace view q2(name,ids)
as
    select given, family, string_agg(id, ',')
    from Customers
    group by given, family
    order by given, family
;

