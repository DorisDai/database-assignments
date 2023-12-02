-- COMP3311 21T3 Exam Q3
-- Unsold house(s) with the lowest listed price
-- Ordered by property ID

create or replace view q3(id,price,street,suburb)
as
    -- gives the cheapest unsold house(s).
    select Pr.id, list_price, street_no || ' ' || St.name || ' ' || stype, Su.name
    from Properties Pr
    join Streets St on St.id = Pr.street
    join suburbs Su on Su.id = St.suburb
    where sold_price is null 
    and ptype = 'House'
    and list_price = (select min(list_price) from Properties where ptype = 'House' and sold_price is null)
    order by Pr.id
;
