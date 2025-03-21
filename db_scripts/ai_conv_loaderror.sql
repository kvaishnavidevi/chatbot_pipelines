create table if not exists ai_conv_loaderror
(
	filename varchar(50),
	error_message varchar(100),
	conv_date date,
	fileuploadtime timestamp
					
)
