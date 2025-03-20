create table if not exists ai_users
(
	userid varchar(10) primary key,
	name varchar(100),
	address varchar (500),
	groupid varchar(20),
	emailid varchar(50),
	password varchar (100),
	Foreign Key (groupid) REFERENCES ai_groups(groupid) on Delete Cascade
)
