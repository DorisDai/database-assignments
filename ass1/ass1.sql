-- COMP3311 23T3 Assignment 1
--
-- Fill in the gaps ("...") below with your code
-- You can add any auxiliary views/function that you like
-- but they must be defined in this file *before* their first use
-- The code in this file *MUST* load into an empty database in one pass
-- It will be tested as follows:
-- createdb test; psql test -f ass1.dump; psql test -f ass1.sql
-- Make sure it can load without error under these conditions

-- Put any views/functions that might be useful in multiple questions here



---- Q1
--
create or replace view Q1(state, nbreweries)as 
    select region as state, count(B.id) as nbreweries
    from Breweries B right join Locations L on B.located_in = L.id
    where L.country = 'Australia'
    group by region;
--
---- Q2
create or replace view Q2(style,min_abv,max_abv) as
-- name: double qupte single quote?
    select name, min_abv, max_abv
    from Styles
    where max_abv - min_abv = (select max(max_abv - min_abv) from Styles );
;
--
---- Q3
--
--create or replace view Q3(...)
--as
--...
--;
--
---- Q4
--
--create or replace view Q4(...)
--as
--...
--;
--
---- Q5
--
--create or replace function
--    Q5(...) returns ...
--as $$
--...
--$$
--language sql ;
--
---- Q6
--
--create or replace function
--    Q6(...) returns ...
--as $$
--...
--$$
--language sql ;
--
---- Q7
--
--create or replace function
--    Q7(...) returns ...
--as $$
--...
--$$
--language plpgsql ;
--
---- Q8
--
--create or replace function
--    Q8(...) returns ...
--as $$
--...
--$$
--language plpgsql ;
--
---- Q9
--
--create or replace function
--    Q9(...) returns ...
--as $$
--...
--$$
--language plpgsql ;
--
