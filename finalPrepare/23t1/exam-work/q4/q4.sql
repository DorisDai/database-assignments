-- COMP3311 23T1 Final Exam
-- Q4: Check whether account balance is consistent with transactions

-- replace this line with any helper views or functions --

create or replace function q4(_acctID integer)
	returns text
as $$
declare
	_id integer;
	_sum integer := 0;
	_rtrans record;
	_aBalance integer;
begin
	select id, balance into _id, _aBalance from Accounts where id = _acctID;
	if (not found) then
		return 'No such account';
	end if;

	for _rtrans in 
		select * 
		from transactions
		where dest = _acctID or source = _acctID
	loop
		if _rtrans.dest is not null and _rtrans.dest = _acctID then
			_sum = _sum + _rtrans.amount;
		elsif _rtrans.source is not null and _rtrans.source = _acctID
		then
			_sum = _sum - _rtrans.amount;
		end if;
	end loop;

	if _sum = _aBalance then
		return 'OK';
	else
		return format('Mismatch: calculated balance %s, stored balance %s', _sum, _aBalance);
	end if;
end;
$$ language plpgsql;
