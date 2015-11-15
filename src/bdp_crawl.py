#!/usr/bin/python
'''
Created on 2015年11月15日

@author: Administrator
'''

#1.入口：一个粉丝较多的用户
#2.爬取1用户的个人信息检查本地不存在就保存，爬取共享文件列表及文件信息保存。
#3.爬取1用户的粉丝列表，保存粉丝关系
#4.爬取1用户的订阅列表，保存订阅关系
#5.读取1的粉丝列表，分别执行2-5，直到遇到粉丝为0，订阅为0结束
#6.读取1的订阅列表，分别执行2-5，直到遇到粉丝为0，订阅为0结束

import urllib.request, json, mysql.connector


def db_exec(sql, args):
    print("exec:"+sql)
    print(args)
    
    results=0
    try:
        conn = mysql.connector.connect(host='localhost', user='root', passwd='root', db='bdp', port=3306)
        cur = conn.cursor()
        
        if args==None:
            cur.execute(sql, args)
            results=cur.fetchall()
            print(results)
        elif "count"==args:
            results=cur.execute(sql)
            if results==None:
                results=0;
            print(results)
        else:
            # cur.execute('insert into test values(%s,%s)',value)
            cur.execute(sql, args)
            conn.commit()
            
        cur.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Failed.exec:")
        print(err)
    else:
        print("Success.exec:"+sql)
        cur.close()
        
        
    return results

#isExists
def isExists(uk):
    print("isExists:"+uk)
    return (db_exec("select count(*) from user_info where uk='"+uk+"'","count")>0) 


def fetch_data(url,start):
    url=url+"&start="+str(start)
    print("fetching...:"+url);
    d=urllib.request.urlopen(url).read()
    d=str(d.decode('UTF-8'))
    return json.loads(d) #反序列化

#crawl_update_user
def crawl_update_user(uk):
    d=fetch_data("http://yun.baidu.com/pcloud/user/getinfo?query_uk="+uk,0)
    d=d['user_info']
    
    #db_exec("delete from user_info where uk='"+uk+"'",None) #delete exist
    
    sql="insert into user_info(avatar_url,fans_count,follow_count,album_count,intro,uname,"
    sql+="uk,pubshare_count,tui_user_count,c2c_user_sell_count,c2c_user_buy_count,c2c_user_product_count,pair_follow_type)values"
    sql+="(%s,%s,%s,%s,%s,%s ,%s,%s,%s,%s,%s,%s,%s)"
    
    d=[d['avatar_url'],d['fans_count'],d['follow_count'],d['album_count'],d['intro'],d['uname'],d['uk'],d['pubshare_count'],d['tui_user_count'],d['c2c_user_sell_count'],d['c2c_user_buy_count'],d['c2c_user_product_count'],d['pair_follow_type']]
    db_exec(sql,d) #insert new
    


def crawl_save_share(uk):
    #max_limit=100
    url="http://yun.baidu.com/pcloud/feed/getsharelist?auth_type=1&limit=100&query_uk="+uk
    d=fetch_data(url,0)
    tc=d['total_count']
    start=10
    
    ls=list(d['records'])
    
    sql="insert into share(uk,shareid,feed_type,category,public,data_id,title,third,clienttype,filecount,"
    sql+="username,feed_time,desc_,avatar_url,category_6_cnt,source_uid,source_id,shorturl,vCnt,dCnt,"
    sql+="tCnt,like_status,like_count,comment_count)values"
    sql+="(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
    sql+="%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
    sql+="%s,%s,%s,%s"
    
    while tc>start:     #by page
        d=fetch_data(url,start)
        start+=10   #++
        
        ls=list(d['records'])
        
        for d in ls :
            #d['uk'],d['shareid'],d['feed_type'],d['category'],d['public'],d['data_id'],d['title'],d['third'],d['clienttype'],d['filecount'],d['username'],d['feed_time'],d['desc_'],d['avatar_url'],d['category_6_cnt'],d['source_uid'],d['source_id'],d['shorturl'],d['vCnt'],d['dCnt'],d['tCnt'],d['like_status'],d['like_count'],d['comment_count']
            db_exec(sql,d) #insert new
    
    print("Success.total_count=" + str(tc))
    
    
    
#crawl_save_follow
def crawl_save_follow(uk):
    #max_limit=25
    url="http://yun.baidu.com/pcloud/friend/getfollowlist?limit=10&query_uk="+uk
    d=fetch_data(url,0)
    ls=list(d['follow_list'])
    tc=d['total_count']
    start=10
    
    sql="insert into follow_list(uk,follow_uk,follow_time)values(%s,%s,%s)"

    while tc>start:     #by page
        d=fetch_data(url,start)
        start+=10   #++
        
        ls=list(d['follow_list'])
        
        for d in ls :
            db_exec(sql,[uk,d['follow_uk'],d['follow_time']]) #insert new
        
    print("crawl_save_follow end.total_count=" + str(tc))
    
    
    
#crawl_save_fans
def crawl_save_fans(uk):
    #max_limit=25
    url="http://yun.baidu.com/pcloud/friend/getfanslist?limit=10&query_uk="+uk
    d=fetch_data(url,0)
    ls=list(d['fans_list'])
    tc=d['total_count']
    start=10
    
    sql="insert into fans_list(uk,fans_uk,follow_time)values(%s,%s,%s)"

    while tc>start:     #by page
        d=fetch_data(url,start)
        start+=10   #++
        
        ls=list(d['fans_list'])
        
        for d in ls :
            db_exec(sql,[uk,d['fans_uk'],d['follow_time']]) #insert new
        
        
    print("crawl_save_follow end.total_count=" + str(tc))
    

#loop_follow
def loop_follow(uk):
    uks=db_exec("select follow_uk from follow_list where uk="+uk,None) #insert new
    print(uks)
    if uks!=0:
        for uk in uks:
            do_crawl(uk[0])

#loop_fans
def loop_fans(uk):
    uks=db_exec("select fans_uk from fans_list where uk="+uk,None) #insert new
    print(uks)
    if uks!=0:
        for uk in uks:
            do_crawl(uk[0])
    
    
    
def do_crawl(uk):
    if isExists(uk):
        print("skip exits uk:"+uk)
    else:
        crawl_update_user(uk)
        crawl_save_share(uk)
        crawl_save_follow(uk)
        crawl_save_fans(uk)
        loop_follow(uk)
        loop_fans(uk)
        
        
        
do_crawl("891489109")


