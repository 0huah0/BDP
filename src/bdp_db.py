#!/usr/bin/python
'''
Created on 2015年11月15日

@author: shizh
'''

import mysql.connector
import logging
import datetime

cur_date=datetime.datetime.now().strftime('%Y%m%d%H%M');
#print('bdp_crawl_'+cur_date+'.log')

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name) %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y%m%d-%H:%M:%S',
                filename='bdp_crawl_'+cur_date+'.log',
                filemode='w')

#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(name)-2s: %(levelname)-8s %(message)s'))
logging.getLogger('').addHandler(console)

logger = logging.getLogger('bdp') 

insert_share="insert into share(uk,shareid,feed_type,category,public,data_id,title,third,clienttype,filecount,username,feed_time,desc_,avatar_url,category_6_cnt,source_uid,source_id,shorturl,vCnt,dCnt,\
    tCnt,like_status,like_count,comment_count) values \
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
     %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
     %s,%s,%s,%s);"
    
    
insert_file="insert into filelist(shareid,server_filename,category,isdir,size,fs_id,path,md5,sign,time_stamp) values \
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"


insert_user="insert into user_info(avatar_url,fans_count,follow_count,album_count,intro,uname,\
    uk,pubshare_count,tui_user_count,c2c_user_sell_count,c2c_user_buy_count,c2c_user_product_count,pair_follow_type) values \
    (%s,%s,%s,%s,%s,%s ,%s,%s,%s,%s,%s,%s,%s);"
    
    
insert_follow="insert into follow_list(uk,follow_uk,follow_time) values (%s,%s,%s);"

insert_fans="insert into fans_list(uk,fans_uk,follow_time) values (%s,%s,%s);"    

def db_exec(action,sql,args):
    logging.debug("exec:"+sql)
    
    logger.debug(str(args).encode('utf-8',"ignore"))
    
    results=0
    
    try:
        conn = mysql.connector.connect(host='localhost', user='root', passwd='root', db='bdp', port=3306)
        cur = conn.cursor()
        
        if "insert"==action or "delete"==action:  # INSERT
            cur.execute(sql, args)
            conn.commit()
        elif "count"==action: #COUNT
            cur.execute(sql % (args))
            results=cur.fetchone()[0]
            #print(results)
            if results==None:
                results=0;
        else:   # LIST
            cur.execute(sql % (args))
            results=cur.fetchall()
            
        cur.close()
        conn.close()
    except mysql.connector.Error as err:
        logger.warning("Failed.exec:"+str(err))
    else:
        logger.debug("Success.exec:"+sql)
        cur.close()
        
        
    return results