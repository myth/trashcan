create database if not exists testrace;
use testrace;

drop table if exists result;
drop table if exists race;
drop table if exists athlete;

create table athlete(sid int primary key auto_increment not null,
                     name varchar(100) not null,
                     class int not null,
                     birthdate date not null,
                     nationality varchar(100) not null);

create table race(rid int primary key auto_increment not null,
                  start datetime not null,
                  distance int not null);

create table result(rid int not null,
                    sid int not null,
                    place int not null,
                    result time not null,
                    primary key (rid, sid),
                    foreign key (rid) references race (rid) on update cascade on delete cascade,
                    foreign key (sid) references athlete (sid) on update cascade on delete cascade);

insert into athlete values (null, 'Arne', 1, '1987-03-05', 'Norway'),
                           (null, 'Jens', 1, '1988-02-05', 'Sweden'),
                           (null, 'Gottlieb', 2, '1990-01-15', 'Germany'),
                           (null, 'Olaf', 2, '1978-05-19', 'Norway'),
                           (null, 'Frida', 2, '1989-09-19', 'Sweden'),
                           (null, 'Marty', 1, '1993-07-18', 'Netherlands'),
                           (null, 'Emily', 2, '1992-12-24', 'England');

insert into race values (null, '2014-05-08 14:13:18 +01:00', 5000),
                        (null, '2014-05-09 15:00:00 +01:00', 3000);

insert into result values (1, 1, 3, '09:09'),
                          (1, 2, 2, '09:01'),
                          (1, 3, 4, '10:04'),
                          (1, 4, 1, '08:45'),
                          (1, 5, 5, '11:01'),
                          (1, 6, 6, '11:03'),
                          (1, 7, 6, '11:03'),
                          (2, 1, 4, '06:49'),
                          (2, 2, 2, '06:10'),
                          (2, 3, 3, '06:30'),
                          (2, 4, 5, '07:01'),
                          (2, 5, 1, '06:01'),
                          (2, 6, 7, '07:09'),
                          (2, 7, 6, '07:03');

