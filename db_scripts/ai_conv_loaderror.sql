create table if not exists ai_conv_loaderror
(
	session_id varchar(10),
	conv_id varchar(10),
	conv_userid varchar(10),
	error_message varchar(100),
	conv_date date,
	conv_time time
					
)