# -*- coding: utf-8 -*-

'日志封装'

__auth__ = '杨斌'

import logging.handlers

LOG_FILE = r'robot.log'

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')  # 实例化handler
fmt = '%(message)s'

formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter

sh = logging.StreamHandler()#往屏幕上输出
sh.setFormatter(formatter) #设置屏幕上显示的格式

log = logging.getLogger()  # 获取logger
log.addHandler(handler)  # 为logger添加handler
log.addHandler(sh) 
log.setLevel(logging.INFO)

class logger(object):

    def info(self,*pstr):  
        global log 
        s1 = ''
        for s in pstr:
            s1 = s1 + str(s)
        log.info(s1)

if __name__ == '__main__':
    logger.info('测试','测试哈哈')




