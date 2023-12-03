-- COMP3311 20T3 Final Exam
-- Q4: list of long and short songs by each group

-- ... helper views and/or functions (if any) go here ...

drop function if exists q4();
drop type if exists SongCounts;
create type SongCounts as ( "group" text, nshort integer, nlong integer );

create or replace view sLthan3Min(sId3, on_album3) as
	select id, on_album
	from songs
	where length < 180
;

create or replace view sGthan3Min(sId6, on_album6) as
	select id, on_album
	from songs
	where length > 360
;

create or replace view sScount(Gid, Gname, numS) as
	select G.id, G.name, count(S.sId3)
	from sLthan3Min S
	join Albums A on A.id = S.on_album3
	right join Groups G on G.id = A.made_by
	group by G.id, G.name
;

create or replace view lScount(lGid, lGname, numL) as
	select G.id, G.name, count(S.sId6)
	from sGthan3Min S
	join Albums A on A.id = S.on_album6
	right join Groups G on G.id = A.made_by
	group by G.id, G.name
;

create or replace function
	q4() returns setof SongCounts
as $$
declare 
	_result SongCounts;
begin
	
	for _result in 
		select Gname, numS, numL
		from lScount join sScount on Gid = lGid
	loop
		return next _result;
	end loop;

end;
$$ language plpgsql
;
