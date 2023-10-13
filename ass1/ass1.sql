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
create or replace view Q1(state, nbreweries) 
as 
    select region as state, count(B.id) as nbreweries
    from Breweries B right join Locations L on B.located_in = L.id
    where L.country = 'Australia'
    group by region;

---- Q2
create or replace view Q2(style,min_abv,max_abv) 
as
-- name should be double qupte single quote or no quotes?
-- Answer:no single quotes, the other 2 are all good
    select name, min_abv, max_abv
    from Styles
    where max_abv - min_abv = (select max(max_abv - min_abv) from Styles );
;
--
---- Q3
--
create or replace view beerStyleRange(styleId, lo_abv, hi_abv) 
as
    select style, min(ABV), max(ABV)
    from Beers 
    group by style;

create or replace view Q3(style, lo_abv, hi_abv, min_abv, max_abv)
as
    select name, lo_abv, hi_abv, min_abv, max_abv
    -- when attribute names not same, no need to use Table.attribute
    from Styles join beerStyleRange on id = styleId
    where (lo_abv < min_abv or hi_abv > max_abv) and min_abv != max_abv;
;
--
---- Q4
--
create or replace view breweryRating(validBreweryId,avgRating)
as
    select brewery, avg(rating::float)::numeric(3,1)
    from Brewed_by join Beers on beer = id
    group by brewery
    -- difference between having and where:
    -- use where to check wheather each tuple should be included to be grouped(before grouping)
    -- use have to filter already grouped result tuple.
    having count(rating) > 4;

create or replace view Q4(brewery,rating)
as
    select name, avgRating
    from breweryRating join Breweries on validBreweryId = id
    where avgRating = (select max(avgRating) from breweryRating);

;
--
---- Q5
--
create or replace function
   Q5(pattern text) returns table(beer text, container text, std_drinks numeric)
as $$
    select name, volume || 'ml ' || sold_in, (volume * ABV * 0.0008)::numeric(2,1)
    from Beers
    where name ~* ('.*' || pattern || '.*');
$$
language sql ;
--
---- Q6
--
create or replace function
   Q6(pattern text) returns
       table(country text, first integer, nbeers integer, rating numeric)
as $$
    select country, min(brewed), count(Beers.id), avg(rating)::numeric(3,1)
    from Beers 
    join Brewed_by on Beers.id = beer
    join Breweries on brewery = Breweries.id
    join Locations on Locations.id = located_in
    group by country
    having country ~* ('.*' || pattern || '.*');
$$
language sql ;
--
---- Q7
--
create or replace function
   Q7(_beerID integer) returns text
as $$
declare
    _result text;
    _beerName text;
    _beer record;
    _noI boolean;
begin
    select name into _beerName from Beers where id = _beerID;
    if (not found) then
        return format('No such beer (%s)', _beerID);
    else 
        -- \n is not useable in format string
        _result := format('"%s"', _beerName);

        for _beer in 
            select itype, I.name
            from Contains join Ingredients I on ingredient = id
            where beer = _beerID
            order by I.name
        loop
            _noI := false
            _result := _result || E'\n  contains\n' || format('    %s (%s)', _beer.name, _beer.itype);
        end loop;

        if _noI then
            _result := _result || E'\n  contains';
        end if;

        return _result;
    end if;
end;
$$
language plpgsql ;
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
