-- COMP3311 23T1 Final Exam
-- Q4: Check whether account balance is consistent with transactions

-- replace this line with any helper views or functions --

create or replace function q4(_acctID integer)
	returns text
as $$
declare
	_id integer;
	_sum integer;
	_rdeposit record;
begin
	select id into _id from Accounts where id = _acctID;
	if (not found) then
		return 'No such account';
	end if;
	-- ??select muliple resul into a var?
	select amount into _sum from transactions where id = (
		select min(id) from transactions where id = _acctID
	);

	for _rdeposit in select amoun from 


end;
$$ language plpgsql;
