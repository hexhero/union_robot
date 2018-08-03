#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'1.5 最新版本外挂 单用户 15068181441'

__author__ = '杨斌'

import requests
import json
import hashlib
import schedule
import time
import argparse

from collections import namedtuple
from datetime import datetime
from logger import logger
from sendmail import sendmail

logger = logger()

# 请求头
headers = {'User-Agent':'okhttp/3.8.1','Content-Type':'text/plain;charset=utf-8','Cookie':'JSESSIONID=6C56894B79314A4B256444DFC0DB3123'}

def login():
    global headers
    loginUrl = 'http://app.hzgh.org:8002/unionApp/interf/front/U/U005'
    param = r'{"channel":"02","dec_key":"EJsHG0\/+uWn1hSoMqfQ9SqUdnEA9eiqIGHbHeylgxI8eD19eH\/0SPQ3GNLNw3AzjkuU2A1TEKx50rXX1vYOmQm1PYRv71QKQ+iWX\/p9Ewr3vhF4gHk9fyBgdPWqV\/N5C3AMSPgD0A8Abzc8MFy\/sxjeFQtqQnmVxN7CxDEbm6sY=","app_ver_no":"2.1.5","ses_id":"3bbbf8b55dcb455ba0456b87ac3f48e5","login_name":"RsTxzNDVHq4=","key":"channel,dec_key,app_ver_no,ses_id,login_name","sign":"27AF9ED1558232580E31B482DFDE9333007D6DE1"}'
    r = requests.post(loginUrl,data=param,headers=headers)
    if r.status_code == requests.codes.ok:
        result = r.json()
        logger.info(result['mobile'],'登录积分')
        return result

def readNews():
    newsUrl = 'http://app.hzgh.org:8002/unionApp/interf/front/U/U042'
    param = r'{"channel":"02","dec_key":"Xk0mpHO5FMMVa4TlxALTS24Pl0uqbT8P7quUAw36DRvfLiRfrrV90f3lhXNNWZD\/GLYSBxZqqm1gu0cUTx0AJiBbmK8Xjsg+M9+QG2H5yVg3Qsnb3Mjn\/ZkH4kWWN\/obYrgVeaLkBnEAczRG6vLXQ9ueEtTNCrAoWnkODr2a+xs=","ses_id":"eea475bfcaba4df19caad26e3308e66e","type":"5","login_name":"9lUQ3qiRRIY=","key":"channel,dec_key,ses_id,type,login_name","sign":"C93F2562B0E89187973B1044069ED23D09A83EF1"}'
    for n in range(0,4):
        r = requests.post(newsUrl,data=param,headers=headers)
        if r.status_code == requests.codes.ok:
            result = r.json()
            logger.info('阅读新闻: ',result['msg'])
        time.sleep(3)

shareUrl = 'http://app.hzgh.org:8002/unionApp/interf/front/U/U042'

def shareApp():
    param = r'{"channel":"02","dec_key":"h5h8\/ko4jF+99HL9zwdeYCtxIBlIC1j5RH\/SIkUyYgW\/2iyevBymKGlqDotyzw0Uh7w0U8h1UD79g2kdKSBrVJdcNpIHFdOGTUtLwLrpSnL4mzqZTKq9qFInrMSknnhLXNP7\/VWM025JjdohsBITM4IgX5kUuWujBbMLRkE5DPw=","ses_id":"eea475bfcaba4df19caad26e3308e66e","type":"7","login_name":"oaib6bqqosE=","key":"channel,dec_key,ses_id,type,login_name","sign":"B05855F52699AD55239E0E4DA3F494CEF256FF76"}'
    r = requests.post(shareUrl,data=param,headers=headers)
    if r.status_code == requests.codes.ok:
        result = r.json()
        logger.info('分享APP: ',result['msg'])
        return result

def shareActivity():
    param = r'{"channel":"02","dec_key":"lLNZ977une5LKzz9GlNkN7q7rI88l4DIm0eJUy5DAfDAg6TiTyRWa5kXr+T+fV6j0bSIG4g4\/1dJkbS+U7O5nycpXmw4G35KivXLfVosL5IvnJjDa+W1lRidHYPO\/MHjc1os0s+S5vjBLHUScHpK6\/niBepVYeyH0iHIZ30tfXg=","ses_id":"eea475bfcaba4df19caad26e3308e66e","type":"8","login_name":"NE+T7kZPKjM=","key":"channel,dec_key,ses_id,type,login_name","sign":"4F462EA72E862B6A086A0CDC82F5BB333441BA84"}'
    r = requests.post(shareUrl,data=param,headers=headers)
    if r.status_code == requests.codes.ok:
        result = r.json()
        logger.info('分享活动: ',result['msg'])
        return result

def myGrade():
    gradeUrl = 'http://app.hzgh.org:8002/unionApp/interf/front/U/U043'
    param = r'{"channel":"02","dec_key":"W\/Jo3t\/qfY8ZE8gqEeULpw7muxw4rO6xRuU4JcZSQVaNey6ce3XnFtl1\/tKcGXKqCec24b+tHp8twb8N5wW20UOukxtDh0zZNSfi3n6SrC8\/3tqwULOl+v94rEW\/YvXFaavFMAZsFluja0Bmy0EUg1D65sezSGR4OFaQQRP+Vmk=","ses_id":"eea475bfcaba4df19caad26e3308e66e","login_name":"iRiXrlXL3jc=","key":"channel,dec_key,ses_id,login_name","sign":"04E66F6601804F7B5CD7C4B9792D2797F9F98C2B"}'
    r = requests.post(gradeUrl,data=param,headers=headers)
    if r.status_code == requests.codes.ok:
        result = r.json()
        logger.info('我的积分: ',result['remain_integral'])
        return result['remain_integral']

def work():
    try:
        oldGradeCount = int(myGrade())
        
        login() # +1
        readNews() # +4
        shareApp() # +1
        shareActivity() # +1
        
        newGradeCount = int(myGrade())

        sendmail('杭工e家 积分信息', '现在积分: %s <br/> 之前积分: %s <br/> 今日新增: %s' % (newGradeCount,oldGradeCount,newGradeCount-oldGradeCount))
    except Exception as e:
        sendmail('杭工e家 刷分系统异常',e)
    
    logger.info('-----------------邮件已发送-----------------')

def main(run=False):
    logger.info('-----------------程序启动-----------------')
    if run:
        work()
    logger.info('-----------------每天早上9点执行-----------------')
    schedule.every().day.at('09:00').do(work)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--run', type=bool, default = False)
    args = parser.parse_args()
    print(args.run)
    main(args.run)
    