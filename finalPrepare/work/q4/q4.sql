-- COMP3311 20T3 Final Exam
-- Q4: list of long and short songs by each group

-- ... helper views and/or functions (if any) go here ...

drop function if exists q4();
drop type if exists SongCounts;
create type SongCounts as ( "group" text, nshort integer, nlong integer );

create or replace view sScount(Gid, Gname, numS) as
	select G.id, G.name, count(S.id)
	from Songs S
	join Albums A on A.id = S.on_album
	right join Groups G on G.id = A.made_by
	where S.length < 180 or S.length is null
	group by G.id, G.name
;

create or replace view lScount(lGid, lGname, numL) as
	select G.id, G.name, count(S.id)
	from Songs S
	join Albums A on A.id = S.on_album
	right join Groups G on G.id = A.made_by
	where S.length > 360 or S.length is null
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
		from lScount full join sScount on Gid = lGid
	loop
		return next _result;
	end loop;

end;
$$ language plpgsql
;
