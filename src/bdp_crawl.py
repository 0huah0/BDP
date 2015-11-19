#!/usr/bin/python
'''
Created on 2015年11月15日

@author: shizh
'''

#1.入口：一个粉丝较多的用户
#2.爬取1用户的个人信息检查本地不存在就保存，爬取共享文件列表及文件信息保存。
#3.爬取1用户的粉丝列表，保存粉丝关系
#4.爬取1用户的订阅列表，保存订阅关系
#5.读取1的粉丝列表，分别执行2-5，直到遇到粉丝为0，订阅为0结束
#6.读取1的订阅列表，分别执行2-5，直到遇到粉丝为0，订阅为0结束

import urllib.request, json
import socket,urllib.parse
import bdp_db

logging = bdp_db.logging

#isExists
def isExists(uk):
    logging.warning("isExists:"+uk)
    return (bdp_db.db_exec("count","select count(*) from user_info where uk=%s;",uk)>0) 


def fetch_data(url,start):
    url=url+"&start="+str(start)
    print("fetching...:"+url);
    logging.debug("fetching...:"+url)
        
    d=None
    try:
        socket.setdefaulttimeout(10)
        req = urllib.request.Request(url)
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1")
        req.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        req.add_header("Accept-Charset","utf-8")
        
        result = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(result.query,True)
        
        if result.path=="/pcloud/feed/getsharelist":    #如果是share则添加req.add_header("Referer",解决start超过500返回errorno=2
            #print(params['query_uk'][0])
            req.add_header("Referer","http://yun.baidu.com/share/home?uk="+params['query_uk'][0]+"&view=share")
        
        d=urllib.request.urlopen(req).read()
        d=str(d.decode('utf-8'))
        d=json.loads(d)
    except urllib.request.HTTPError as err:
        logging.warning("Failed.fetching:")
        logging.warning(err)
    except BaseException as err:
        logging.warning(err)
    
    if d==None:d={}
    return d #反序列化

#crawl_update_user
def crawl_update_user(uk):
    d=fetch_data("http://yun.baidu.com/pcloud/user/getinfo?query_uk="+uk,0)
    d=d.get('user_info',None)
    if d!=None:
        try:
            d=[d['avatar_url'],d['fans_count'],d['follow_count'],d['album_count'],d['intro'],d['uname'],d['uk'],d['pubshare_count'],d['tui_user_count'],d['c2c_user_sell_count'],d['c2c_user_buy_count'],d['c2c_user_product_count'],d['pair_follow_type']]
            bdp_db.db_exec("insert",bdp_db.insert_user,d) #insert new
        except Exception as e:
            logging.warn("skip insert.err:"+str(e))


def crawl_save_share(uk):
    max_limit=100
    start=0
    
    url="http://yun.baidu.com/pcloud/feed/getsharelist?auth_type=1&limit="+str(max_limit)+"&query_uk="+uk
    d=fetch_data(url,start)
    start+=max_limit   #++
    tc=d.get('total_count',0)

    while tc>start:     #by page
        
        ls=d.get('records',[])
        
        for d in ls :
            category_6_cnt=d.get('category_6_cnt',-1)
            if category_6_cnt==-1:category_6_cnt=d.get('category_4_cnt',-1)
            
            try:
                bdp_db.db_exec("insert",bdp_db.insert_share,[d['uk'],d['shareid'],d['feed_type'],d['category'],d['public'],d['data_id'],d['title'],d['third'],d['clienttype'],d['filecount'],d['username'],d['feed_time'],d['desc'],d['avatar_url'],category_6_cnt,d['source_uid'],d['source_id'],d['shorturl'],d['vCnt'],d['dCnt'],d['tCnt'],d['like_status'],d['like_count'],d['comment_count']]) #insert new
            except Exception as e:
                logging.warn("skip insert.err:"+str(e))
            
            #save files
            filelist=d.get('filelist',[])
            
            for f in filelist :
                try:
                    bdp_db.db_exec("insert",bdp_db.insert_file,[d['shareid'],f['server_filename'],f['category'],f['isdir'],f['size'],f['fs_id'],f['path'],f['md5'],f['sign'],f['time_stamp']]) #insert new
                except Exception as e:
                    logging.warn("skip insert.err:"+str(e))
                    
        d=fetch_data(url,start)
        start+=max_limit   #++
        
    print("Success.total_count=" + str(tc))
    
    
    
#crawl_save_follow
def crawl_save_follow(uk):
    max_limit=25
    start=0
    url="http://yun.baidu.com/pcloud/friend/getfollowlist?limit="+str(max_limit)+"&query_uk="+uk
    d=fetch_data(url,0)
    start+=max_limit   #++
    tc=d.get('total_count',0)

    while tc>start:     #by page
        
        ls=d.get('follow_list',[])
        
        for d in ls :
            try:
                bdp_db.db_exec("insert",bdp_db.insert_follow,[uk,d['follow_uk'],d['follow_time']]) #insert new
            except Exception as e:
                logging.warn("skip insert.err:"+str(e))
        
        d=fetch_data(url,start)
        start+=max_limit   #++
        
    print("crawl_save_follow end.total_count=" + str(tc))
    
    
    
#crawl_save_fans
def crawl_save_fans(uk):
    max_limit=25
    start=0
    url="http://yun.baidu.com/pcloud/friend/getfanslist?limit="+str(max_limit)+"&query_uk="+uk
    d=fetch_data(url,0)
    start+=max_limit   #++
    tc=d.get('total_count',0)
    
    while tc>start:     #by page
        ls=d.get('fans_list',[])
        for d in ls :
            try:
                bdp_db.db_exec("insert",bdp_db.insert_fans,[uk,d['fans_uk'],d['follow_time']]) #insert new
            except Exception as e:
                logging.warn("skip insert.err:"+str(e))
        
        
        d=fetch_data(url,start)
        start+=max_limit   #++
    print("crawl_save_follow end.total_count=" + str(tc))
    

#loop_follow
def loop_follow(uk):
    uks=bdp_db.db_exec("list","select follow_uk from follow_list where uk='%s';",uk)
    print(uks)
    if uks!=0:
        for uk in uks:
            do_crawl(uk[0])

#loop_fans
def loop_fans(uk):
    uks=bdp_db.db_exec("list","select fans_uk from fans_list where uk='%s';",uk) 
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
        
        
        
#do_crawl("891489109")
do_crawl("490155926")

#    
# sql="insert into share(uk,shareid,feed_type,category,public,data_id,title,third,clienttype,filecount,username,feed_time,desc_,avatar_url,category_6_cnt,source_uid,source_id,shorturl,vCnt,dCnt,tCnt,like_status,like_count,comment_count) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s);"
#    
# args=[490155926, '908522425', 'share', 6, '1', '6062932482101822284', 'K4_4.0.0_to_4.0.1_版本.rar', 0, 0, 1, '没我找不到的书', 1406610874000, '', 'http://himg.bdimg.com/sys/portrait/item/611d4933.jpg', 1, '860429665', '908522425', '1bnneBUJ', 271, 27, 142, 0, 1, 0]
#    
# bdp_db.db_exec(sql, args);
