CREATE DATABASE `bdp`  
CHARACTER SET 'utf8'  
COLLATE 'utf8_general_ci'; 


create table share(
	uk varchar(100),
	shareid varchar(100),
	feed_type varchar(100),
	category int,
	public int,
	data_id varchar(100),
	title varchar(1000),
	third int,
	clienttype int,
	filecount int,
	username varchar(100),
	feed_time varchar(100),
	desc_ varchar(1000),
	avatar_url varchar(1000),
	category_6_cnt int,
	source_uid varchar(100),
	source_id varchar(100),
	shorturl varchar(100),
	vcnt int,
	dcnt int,
	tcnt int,
	like_status int,
	like_count int,
	comment_count int,
	create_dt timestamp default now()
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table filelist(
	shareid varchar(100),	#!!
	server_filename varchar(1000),
	category int,
	isdir int,
	size int(15),
	fs_id varchar(100),
	path varchar(1000),
	md5 varchar(100),
	sign varchar(100),
	time_stamp varchar(100),
	create_dt timestamp default now()
)ENGINE=InnoDB DEFAULT CHARSET=utf8; 

create table user_info(
	avatar_url varchar(1000),
	fans_count int,
	follow_count int,
	album_count int,
	intro varchar(1000),
	uname varchar(100),
	uk varchar(100),
	pubshare_count int,
	tui_user_count int,
	c2c_user_sell_count int,
	c2c_user_buy_count int,
	c2c_user_product_count int,
	pair_follow_type int,
	create_dt timestamp default now()
)ENGINE=InnoDB DEFAULT CHARSET=utf8; 


create table fans_list(
	uk varchar(100),	#!!
	fans_uk varchar(100),
	follow_time varchar(100),
	create_dt timestamp default now()
)ENGINE=InnoDB DEFAULT CHARSET=utf8; 



create table follow_list(
	uk varchar(100),	#!!
	follow_uk varchar(100),
	follow_time varchar(100),
	create_dt timestamp default now()
)ENGINE=InnoDB DEFAULT CHARSET=utf8; 

create table bdp_new_uk(
	uk varchar(100)
)ENGINE=InnoDB DEFAULT CHARSET=utf8; 

