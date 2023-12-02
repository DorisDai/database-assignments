-- COMP3311 21T3 Exam Q2
-- Number of unsold properties of each type in each suburb
-- Ordered by type, then suburb

create or replace view q2(suburb, ptype, nprops)
as
    --  gives a list of how many unsold properties of each type are in each suburb.
    select Su.name, Pr.ptype, count(Pr.id)
    from properties as Pr
    join Streets as St on St.id = Pr.street
    join suburbs as Su on Su.id = St.suburb
    where Pr.sold_date is null
    group by Su.name, Pr.ptype
    order by ptype, Su.name

;
