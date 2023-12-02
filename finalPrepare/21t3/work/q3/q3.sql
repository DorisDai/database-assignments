-- COMP3311 21T3 Exam Q3
-- Unsold house(s) with the lowest listed price
-- Ordered by property ID

create or replace view q3(id,price,street,suburb)
as
    -- gives the cheapest unsold house(s).
    select Pr.id, list_price, St.name, Su.name
    from Properties as Pr
    join Streets as St on St.id = Pr.street
    join suburbs as Su on Su.id = St.suburb
    where sold_price is null 
    and list_price = (select min(list_price) from Properties)
    order by Pr.id
;
