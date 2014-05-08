====
Løsningsforslag
====

* `select name, nationality from athlete a join result r on r.sid=a.sid join race ra on r.rid=ra.rid where ra.distance=5000;`

* `select name, distance, place, result from result r join athlete a on r.sid=a.sid join race ra on r.rid=ra.rid where a.nationality='Norway' order by distance, result asc;`

* `select nationality, count(r.sid) as amount from result r join athlete a on r.sid = a.sid join race ra on r.rid=ra.rid where distance=5000 and result < '10:30' group by nationality order by amount desc;`

* `select distinct nationality from athlete a where sid not in (select sid from result r where place <= 3);`

* `select count(*) medaljer from result r join athlete a on r.sid=a.sid where place <= 3 and a.nationality = 'Norway';`
