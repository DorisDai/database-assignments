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
    genereString text := '';
    result GroupGenres;
begin
    for r1 in 
        select G.id as Gid, G.name as Gname, string_agg(A.genre) as gGenre
        from groups G
        left join Albums A
        group by G.id, G.name
    loop
        if r1.genre is not null
            genereString := r1.genre;
        end if;
        result."group" := r1.Gname;
        result.genres := r1.genereString;
        return next result;
    end loop;
end;
$$ language plpgsql
;

