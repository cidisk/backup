# -*- coding: GB18030 -*-
'''
Created on May 26, 2011

@author: caiyifeng@baidu.com

@note: 自适应sleep
'''

import time
import os, sys 
from common.timer import Timer2
from common.loger import loger
from common import checker


class AutosleepException(Exception):
    pass


def sleeptill_haslog_multi(logreader, maxwait=10,regstr=[]):

    t = Timer2()

    # 不断寻找
    loger.debug("Sleep until finding '%s' in '%s'", regstr, logreader.logpath)

    while t.end() < maxwait:
        if checker.check_log_contain_multi(logreader, [],regstr):
            # 找到
            loger.debug("Sleep Ends")
            return
        else:
            # 没找到
            time.sleep(0.1)

    else:
        # 超过最大时间
        raise AssertionError("'%s' has no log pattern '%s' during %s second(s)" % (logreader.logpath, regstr, maxwait))

   
def sleeptill_haslog(logreader, regstr, maxwait=10):
    '''
    @summary: 等待log中出现某个正则
    @param logreader: LogReader对象
    @param regstr: 正则字符串
    @param maxwait: 最长等待时间，单位秒
    @raise AutosleepException: 超过最长等待时候
    '''
    # 开始计时
    t = Timer2()
    
    # 不断寻找
    loger.debug("Sleep until finding '%s' in '%s'", regstr, logreader.logpath)
    
    while t.end() < maxwait:
        if checker.check_log_contain(logreader, regstr):
            # 找到
            loger.debug("Sleep Ends")
            return
        else:
            # 没找到
            time.sleep(0.1)
            
    else:
        # 超过最大时间
        raise AssertionError("'%s' has no log pattern '%s' during %s second(s)" % (logreader.logpath, regstr, maxwait))


def sleeptill_hasprocess(processpath, maxwait=10):
    '''
    @summary: 等待进程存在
    @param processpath: 进程的绝对路径
    @param maxwait: 最长等待时间，单位秒
    @raise AutosleepException: 超过最长等待时候
    '''
    t = Timer2()
    
    loger.debug("Sleep until Process '%s' exists", processpath)
    
    while t.end() <maxwait:
        # 判断进程是否存在
        if checker.check_process_exist(processpath):
            # 存在
            loger.debug("Sleep Ends")
            return
        else:
            # 不存在
            time.sleep(0.1)
    else:
        #超过最大时间
        raise AssertionError("Process '%s' never exists during %s second(s)" % (processpath, maxwait))


def sleeptill_noprocess(processpath, maxwait=10):
    '''
    @summary: 等待进程不存在
    @param processpath: 进程的绝对路径
    @param maxwait: 最长等待时间，单位秒
    @raise AutosleepException: 超过最长等待时候
    '''
    t = Timer2()
    
    loger.debug("Sleep until Process '%s' NOT Exists", processpath)
    
    while t.end() <maxwait:
        # 判断进程是否存在
        if checker.check_process_exist(processpath):
            # 存在
            time.sleep(0.1)
        else:
            # 不存在
            loger.debug("Sleep Ends")
            return
            
    else:
        #超过最大时间
        raise AssertionError("Process '%s' always exists during %s second(s)" % (processpath, maxwait))


def sleeptill_hasport(port, maxwait=10):
    '''
    @summary: 等待端口被占用
    @param port: 端口号
    @param maxwait: 最长等待时间，单位秒
    @raise AutosleepException: 超过最长等待时候
    '''
    t = Timer2()
    
    loger.debug("Sleep until Port '%s' exists", port)
    
    while t.end() <maxwait:
        # 判断端口是否被占用
        if checker.check_port_exist(port):
            # 被占用
            loger.debug("Sleep Ends")
            return
        else:
            # 被释放
            time.sleep(0.1)
    else:
        #超过最大时间
        raise AssertionError("Port '%s' never exists during %s second(s)" % (port, maxwait))
    
    
def sleeptill_noport(port, maxwait=10):
    '''
    @summary: 等待端口被释放
    @param port: 端口号
    @param maxwait: 最长等待时间，单位秒
    @raise AutosleepException: 超过最长等待时候
    '''
    t = Timer2()
    
    loger.debug("Sleep until Port '%s' Free", port)
    
    while t.end() <maxwait:
        # 判断端口是否被占用
        if checker.check_port_exist(port):
            # 被占用
            time.sleep(0.1)
        else:
            # 被释放
            loger.debug("Sleep Ends")
            return
    else:
        #超过最大时间
        raise AssertionError("Port '%s' always exists during %s second(s)" % (port, maxwait))
        

def sleeptill_startprocess(processpath, port, maxwait=10):
    '''@param port: 可以是一个int，也可以是一个int list'''
    sleeptill_hasprocess(processpath, maxwait)
    if isinstance(port, int):
        sleeptill_hasport(port, maxwait)
    else:
        for p in port:
            sleeptill_hasport(p, maxwait)
    
    
def sleeptill_killprocess(processpath, port, maxwait=10):
    '''@param port: 可以是一个int，也可以是一个int list'''
    sleeptill_noprocess(processpath, maxwait)
    if isinstance(port, int):
        sleeptill_noport(port, maxwait)
    else:
        for p in port:
            sleeptill_noport(p, maxwait)

def sleep_till_dir_exist(dirpath,maxwait=10):
    '''
    @note: 等待文件夹存在
    @param file:等待的文件夹
    @param maxwait: 最长等待时间，单位秒，超过则打印warning日志
    '''
    t = Timer2()
    t.start()

    loger.debug("Sleep until Dir %s exist"%dirpath)

    while t.end() <maxwait:
        # 判断进程是否存在
        if os.path.isdir(dirpath):
            # 存在
            loger.debug("Sleep Ends")
            return
        else:
            # 不存在
            time.sleep(0.1)

    else:
        #超过最大时间
        raise Exception, "Dir '%s' never exist during %s second(s)" % (dirpath, maxwait)  
    
def sleep_till_files_stable(path, maxwait=50, timeInterval = 0.5):
    '''
    @note: 等待文件大小稳定
    @param file: 等待的文件
    @param maxwait: 最长等待时间，单位秒，超过则打印warning日志
    '''
    t = Timer2()
    t.start()

    loger.debug("Sleep untill Path %s stable"%path)
   
    for file in os.listdir(path):
        size_0 = os.path.getsize(path+'/'+file)
        size_1 = -1

        time.sleep(timeInterval)
        while t.end() < maxwait:
            size_1 = size_0
            size_0 = os.path.getsize(path+'/'+file)

            if size_0 == size_1:
                return
            else:
                time.sleep(timeInterval)
    
        else:
            #超出最大时间
            raise Exception, "File '%s' never become stable during %s second(s)" % (file, maxwait)
        