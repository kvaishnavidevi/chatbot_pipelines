--drop table ai_conversations;
create table ai_conversations
(	
	seq_no serial,
	session_id varchar(10),
	conv_id varchar(10),
	conv_role varchar(20),
	conversations varchar,
	conv_date date default current_Date,
	conv_time time,
	conv_userid varchar(10),
	conv_idletime_insec int,
	conv_files varchar(200),
	PRIMARY KEY (seq_no,conv_userid,conv_id,conv_date),
	FOREIGN KEY (conv_userid) REFERENCES ai_users(userid) ON DELETE CASCADE
)
Partition by range (conv_date);