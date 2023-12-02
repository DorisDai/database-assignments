-- Q12
select sname 
from Suppliers as Su
join Catalog as Ca on Su.sid = Ca.sid
join Parts as P on P.pid = Ca.pid
where colour = 'red'

-- Q13
select sid 
from Catalog as C
join Parts as P on C.pid = P.pid
where colour = 'red' or 'green';
-- Q14
-- Q15
-- way1:
select sid
from Catalog as C
join Parts as P on C.pid = P.pid
where sid = (select sid from Catalog as C join Parts as P on C.pid = P.pid where colour = 'red') and colour = 'green'
-- way2:
select sid
from Catalog as C
join Parts as P on C.pid = P.pid
join Catalog as C2 on C.sid = C2.sid
join Parts as P2 on C2.pid = P2.pid
where P.color = 'red' and P2.color = 'green'
-- Q16
-- Q17
-- Q18
-- Q19
-- Q20
-- Q21
-- Q22
-- Q23