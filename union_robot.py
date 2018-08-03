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
users = [User('15068181441','Admin1992'),
        User('17557285523','cdh65432125'),
        User('15867192953','zsr911'),
        User('15868100796','zxcvbnm1994'),
        User('15888809203','080268lcq'),
        User('15270238857','wg123456789'),
        User('15757178794','z314581947')]



# 登录url
loginUrl = 'http://app.hzgh.org:8002/unionApp/interf/front/U/U004'

# 积分接口
gradeUrl = 'http://app.hzgh.org:8002/unionApp/interf/front/U/U042'

# sign 盐
salt = '123456'

# 请求头
headers = {'User-Agent':'okhttp/3.8.1','Content-Type': 'text/plain;charset=utf-8'}
# 登录
def login(username, password):
    global loginUrl
    global headers
    param = {'app_ver_no':'2.1.4',
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
    param['sign'] = sign(str(param['channel'])+str(param['term_id'])+str(param['term_sys'])+
        str(param['app_ver_no'])+str(param['term_sys_ver'])+str(param['pwd'])+str(param['root'])+
        str(param['login_name'])+str(param['model']))
    r = requests.post(loginUrl,data=json.dumps(param),headers=headers)
    if r.status_code == requests.codes.ok:
        result = r.json()
        result['cookies'] = r.cookies['JSESSIONID']
        headers['cookies']='JSESSIONID=%s' % r.cookies['JSESSIONID']
        logger.info(result['msg'],'+1')
        return result
    pass

# 阅读新闻积分申请
def readNews(loginInfo):
    global headers
    for n in range(0,4):
        param = {"channel":"02",
                "ses_id":loginInfo['ses_id'],
                "type":"5",
                "login_name":loginInfo['login_name'],
                "key":"channel,ses_id,type,login_name",
                "sign":"69EC28F56311300262521FAD7B14E5C8E89DB9BC"}
        param['sign'] = sign(str(param['channel'])+str(param['ses_id'])+str(param['type'])+str(param['login_name']))
        r = requests.post(gradeUrl, data=json.dumps(param),headers=headers)
        if r.status_code == requests.codes.ok:
            result = r.json()       
            logger.info(result['msg']+'+1')
    
# 其他一天只能获取一次的积分接口
def otherObtainGrade(loginInfo):
    global headers
    for tp in [8,2,7]:
        param = {"channel":"02",
                "ses_id":loginInfo['ses_id'],
                "type":tp,
                "login_name":loginInfo['login_name'],
                "key":"channel,ses_id,type,login_name",
                "sign":"69EC28F56311300262521FAD7B14E5C8E89DB9BC"}
        param['sign'] = sign(str(param['channel'])+str(param['ses_id'])+str(param['type'])+str(param['login_name']))
        r = requests.post(gradeUrl, data=json.dumps(param),headers=headers)
        if r.status_code == requests.codes.ok:
            result = r.json()       
            logger.info(result['msg']+'+1')
        pass

# 举报积分接口
def informGrade(loginInfo):
    global headers
    for n in range(0,4):
        param = {"channel":"02",
                "ses_id":loginInfo['ses_id'],
                "type":'9',
                "login_name":loginInfo['login_name'],
                "key":"channel,ses_id,type,login_name",
                "sign":"69EC28F56311300262521FAD7B14E5C8E89DB9BC"}
        param['sign'] = sign(str(param['channel'])+str(param['ses_id'])+str(param['type'])+str(param['login_name']))
        r = requests.post(gradeUrl, data=json.dumps(param),headers=headers)
        if r.status_code == requests.codes.ok:
            result = r.json()       
            logger.info(result['msg']+'+1')
        pass

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
        readNews(loginInfo)           
        otherObtainGrade(loginInfo)
        informGrade(loginInfo)
        logger.info(user.username,'<<<<<<<<<<<<操作结束')

if __name__ == '__main__':
    logger.info('-----------------首次启动执行-----------------')
    main()
    logger.info('-----------------定时器_每天早上9点刷分-----------------')
    schedule.every().day.at('09:00').do(main) #定时任务 每天早上9点刷票
    while True:
        schedule.run_pending()
        time.sleep(1)
