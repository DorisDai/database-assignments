-- COMP3311 20T3 Final Exam
-- Q5: find genres that groups worked in

-- ... helper views and/or functions go here ...

drop function if exists q5();
drop type if exists GroupGenres;

create type GroupGenres as ("group" text, genres text);

create or replace function
    q5() returns setof GroupGenres
as $$
declare
    r1 record;
    genereString text;
    result GroupGenres;
begin
    for r1 in 
        select G.id as Gid, G.name as Gname, string_agg(distinct A.genre, ',' order by A.genre) as gGenre
        from groups G
        left join Albums A on G.id = A.made_by
        group by Gid, Gname
    loop
        genereString := '';
        if r1.gGenre is not null then
            genereString := r1.gGenre;
        end if;
        result."group" := r1.Gname;
        result.genres := genereString;
        return next result;
    end loop;
end;
$$ language plpgsql
;

