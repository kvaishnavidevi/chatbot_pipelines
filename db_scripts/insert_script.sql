-- Create Partition for month of march
CREATE TABLE ai_conversations_2025_03
PARTITION OF ai_conversations
FOR VALUES FROM ('2025-03-01') TO ('2025-04-01');

--create partition for month of April
CREATE TABLE ai_conversations_2025_04
PARTITION OF ai_conversations
FOR VALUES FROM ('2025-04-01') TO ('2025-05-01');

--insert into ai_groups table
insert into ai_groups values ('group1', 'school1', 'abc@xyz.com','Y');

--insert into ai_users table
insert into ai_users (userid) values ('user1');
insert into ai_users (userid) values ('user2');
insert into ai_users (userid) values ('user3');
insert into ai_users (userid) values ('user4');
insert into ai_users (userid) values ('user5');
insert into ai_users (userid) values ('user6');
insert into ai_users (userid) values ('user7');
insert into ai_users (userid) values ('user8');
insert into ai_users (userid) values ('user9');
insert into ai_users (userid) values ('user10');





