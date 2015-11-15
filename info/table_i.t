insert into user_info(avatar_url,fans_count,follow_count,album_count,intro,uname,uk,pubshare_count,tui_user_count,c2c_user_sell_count,c2c_user_buy_count,c2c_user_product_count,pair_follow_type)values(d['avatar_url'],d['fans_count'],d['follow_count'],d['album_count'],d['intro'],d['uname'],d['uk'],d['pubshare_count'],d['tui_user_count'],d['c2c_user_sell_count'],d['c2c_user_buy_count'],d['c2c_user_product_count'],d['pair_follow_type'])
insert into share(uk,shareid,feed_type,category,public,data_id,title,third,clienttype,filecount,username,feed_time,desc_,avatar_url,category_6_cnt,source_uid,source_id,shorturl,vCnt,dCnt,tCnt,like_status,like_count,comment_count)values(d['uk'],d['shareid'],d['feed_type'],d['category'],d['public'],d['data_id'],d['title'],d['third'],d['clienttype'],d['filecount'],d['username'],d['feed_time'],d['desc'],d['avatar_url'],d['category_6_cnt'],d['source_uid'],d['source_id'],d['shorturl'],d['vCnt'],d['dCnt'],d['tCnt'],d['like_status'],d['like_count'],d['comment_count'])
insert into filelist(shareid,server_filename,category,isdir,size,fs_id,path,md5,sign,time_stamp)values(d['shareid'],d['server_filename'],d['category'],d['isdir'],d['size'],d['fs_id'],d['path'],d['md5'],d['sign'],d['time_stamp'])
insert into fans_list(uk,fans_uk,follow_time)values(d['uk'],d['fans_uk'],d['follow_time'])
insert into follow_list(uk,follow_uname,follow_time)values(d['uk'],d['follow_uname'],d['follow_time'])

delete from user_info;
delete from share;
delete from filelist;
delete from fans_list;
delete from follow_list;


select 'user_info',count(1) from user_info union select 'share',count(1) from share union select 'filelist',count(1) from filelist union select 'fans_list',count(1) from fans_list union select 'follow_list',count(1) from follow_list;


