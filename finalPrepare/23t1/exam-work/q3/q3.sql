-- COMP3311 23T1 Final Exam
-- Q3: show branches where
-- *all* customers who hold accounts at that branch
-- live in the suburb where the branch is located

-- replace this line with any helper views --

create or replace view q3(branch)
as  
    select location
    from Branches
    except
    (select B.location
    from Held_by H
    join Customers C on H.customer = C.id
    join Accounts A on A.id = H.account
    join Branches B on B.id = A.held_at
    where C.lives_in != B.location)
;
