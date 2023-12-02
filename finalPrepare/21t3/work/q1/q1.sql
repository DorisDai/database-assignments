-- COMP3311 21T3 Exam Q1
-- Properties most recently sold; date, price and type of each
-- Ordered by price, then property ID if prices are equal

create or replace view q1(date, price, type)
as
    -- about the most recently sold properties.
    select sold_date, sold_price, ptype
    from Properties
    where sold_date is not null
    order by sold_date DESC
;
