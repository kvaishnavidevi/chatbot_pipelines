create table if not exists ai_groups
(
	groupid varchar(20) primary key,
	groupname varchar(200),
	groupemail varchar(50),
	isschool char(5)
)