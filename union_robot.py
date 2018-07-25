#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'杭工e家 刷积分机器人'

__author__ = '杨斌'

import requests
import json
import hashlib
import schedule
import time

from collections import namedtuple
from datetime import datetime
from logger import logger

User = namedtuple('User',['username','password'])
# 用户名和密码
users = [User('你的用户名','你的密码'),
        User('你的用户名','你的密码')]

# 登录url
loginUrl = 'http://app.hzgh.org:8002/unionApp/interf/front/U/U004'

# 新闻加积分
newsUrl = 'http://app.hzgh.org:8002/unionApp/interf/front/U/U042'

# sign 盐
salt = '123456'

# 请求头
headers = {'User-Agent':'okhttp/3.8.1','Content-Type': 'text/plain;charset=utf-8'}
# 登录
def login(username, password):
    global loginUrl
    global headers
    param = {'app_verno':'2.1.4',
        'channel':'02',
        'login_name':username,
        'pwd':password,
        'model':'Android SDK built for x86_64',
        'key':'channel,term_id,term_sys,app_ver_no,term_sys_ver,pwd,root,login_name,model',
        'root':'0',
        'term_id':'000000000000000',
        'sign':'536C57614E1D6195E661BF1F7C87D0AD96648599',
        'term_sys':'2',
        'term_sys_ver':'7.0'}
    r = requests.post(loginUrl,data=json.dumps(param),headers=headers)
    if r.status_code == requests.codes.ok:
        result = r.json()
        result['cookies'] = r.cookies['JSESSIONID']
        headers['cookies']='JSESSIONID=%s' % r.cookies['JSESSIONID']
        logger.info(result['msg'],'积分+1')
        return result
    pass

def readNews(loginInfo):
    global headers
    param = {"channel":"02","ses_id":loginInfo['ses_id'],"type":"5","login_name":loginInfo['login_name'],"key":"channel,ses_id,type,login_name","sign":"69EC28F56311300262521FAD7B14E5C8E89DB9BC"}
    #param['sign'] = sign(str(param['login_name'])+str(param['type'])+str(param['ses_id'])+str(param['channel']))
    param['sign'] = sign(str(param['channel'])+str(param['ses_id'])+str(param['type'])+str(param['login_name']))
    r = requests.post(newsUrl, data=json.dumps(param),headers=headers)
    if r.status_code == requests.codes.ok:
        result = r.json()       
        logger.info(result['msg']+'积分+1')
    
def sign(paramStr):
    paramStr = paramStr + salt
    md5 = hashlib.md5()
    md5.update(paramStr.encode('utf-8'))
    md5str = md5.hexdigest().upper()
    sha1 = hashlib.sha1()
    sha1.update(md5str.encode('utf-8'))
    return sha1.hexdigest().upper()
    #{"channel":"02","id":"4801","key":"channel,id","sign":"66050623BBCAEA1A89C63D768C4C823B890A3CE4"}

def main():
    logger.info('-----------------机器人 开始工作-----------------')
    for user in users:
        logger.info(user.username,'开始登录>>>>>>>>>')
        loginInfo = login(user.username,user.password)
        for n in range(0,4): #点击新闻4次 每天查看新闻最多能够获取4个积分
            readNews(loginInfo)
            time.sleep(3) #每次刷分后暂停3秒
        logger.info(user.username,'<<<<<<<<<<<<操作结束')

if __name__ == '__main__':
    logger.info('-----------------程序启动成功 每天早上9点刷分-----------------')
    schedule.every().day.at('09:00').do(main) #定时任务 每天早上9点刷票
    while True:
        schedule.run_pending()
        time.sleep(1)
