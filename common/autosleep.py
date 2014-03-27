# -*- coding: GB18030 -*-
'''
Created on May 26, 2011

@author: caiyifeng@baidu.com

@note: ����Ӧsleep
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

    # ����Ѱ��
    loger.debug("Sleep until finding '%s' in '%s'", regstr, logreader.logpath)

    while t.end() < maxwait:
        if checker.check_log_contain_multi(logreader, [],regstr):
            # �ҵ�
            loger.debug("Sleep Ends")
            return
        else:
            # û�ҵ�
            time.sleep(0.1)

    else:
        # �������ʱ��
        raise AssertionError("'%s' has no log pattern '%s' during %s second(s)" % (logreader.logpath, regstr, maxwait))

   
def sleeptill_haslog(logreader, regstr, maxwait=10):
    '''
    @summary: �ȴ�log�г���ĳ������
    @param logreader: LogReader����
    @param regstr: �����ַ���
    @param maxwait: ��ȴ�ʱ�䣬��λ��
    @raise AutosleepException: ������ȴ�ʱ��
    '''
    # ��ʼ��ʱ
    t = Timer2()
    
    # ����Ѱ��
    loger.debug("Sleep until finding '%s' in '%s'", regstr, logreader.logpath)
    
    while t.end() < maxwait:
        if checker.check_log_contain(logreader, regstr):
            # �ҵ�
            loger.debug("Sleep Ends")
            return
        else:
            # û�ҵ�
            time.sleep(0.1)
            
    else:
        # �������ʱ��
        raise AssertionError("'%s' has no log pattern '%s' during %s second(s)" % (logreader.logpath, regstr, maxwait))


def sleeptill_hasprocess(processpath, maxwait=10):
    '''
    @summary: �ȴ����̴���
    @param processpath: ���̵ľ���·��
    @param maxwait: ��ȴ�ʱ�䣬��λ��
    @raise AutosleepException: ������ȴ�ʱ��
    '''
    t = Timer2()
    
    loger.debug("Sleep until Process '%s' exists", processpath)
    
    while t.end() <maxwait:
        # �жϽ����Ƿ����
        if checker.check_process_exist(processpath):
            # ����
            loger.debug("Sleep Ends")
            return
        else:
            # ������
            time.sleep(0.1)
    else:
        #�������ʱ��
        raise AssertionError("Process '%s' never exists during %s second(s)" % (processpath, maxwait))


def sleeptill_noprocess(processpath, maxwait=10):
    '''
    @summary: �ȴ����̲�����
    @param processpath: ���̵ľ���·��
    @param maxwait: ��ȴ�ʱ�䣬��λ��
    @raise AutosleepException: ������ȴ�ʱ��
    '''
    t = Timer2()
    
    loger.debug("Sleep until Process '%s' NOT Exists", processpath)
    
    while t.end() <maxwait:
        # �жϽ����Ƿ����
        if checker.check_process_exist(processpath):
            # ����
            time.sleep(0.1)
        else:
            # ������
            loger.debug("Sleep Ends")
            return
            
    else:
        #�������ʱ��
        raise AssertionError("Process '%s' always exists during %s second(s)" % (processpath, maxwait))


def sleeptill_hasport(port, maxwait=10):
    '''
    @summary: �ȴ��˿ڱ�ռ��
    @param port: �˿ں�
    @param maxwait: ��ȴ�ʱ�䣬��λ��
    @raise AutosleepException: ������ȴ�ʱ��
    '''
    t = Timer2()
    
    loger.debug("Sleep until Port '%s' exists", port)
    
    while t.end() <maxwait:
        # �ж϶˿��Ƿ�ռ��
        if checker.check_port_exist(port):
            # ��ռ��
            loger.debug("Sleep Ends")
            return
        else:
            # ���ͷ�
            time.sleep(0.1)
    else:
        #�������ʱ��
        raise AssertionError("Port '%s' never exists during %s second(s)" % (port, maxwait))
    
    
def sleeptill_noport(port, maxwait=10):
    '''
    @summary: �ȴ��˿ڱ��ͷ�
    @param port: �˿ں�
    @param maxwait: ��ȴ�ʱ�䣬��λ��
    @raise AutosleepException: ������ȴ�ʱ��
    '''
    t = Timer2()
    
    loger.debug("Sleep until Port '%s' Free", port)
    
    while t.end() <maxwait:
        # �ж϶˿��Ƿ�ռ��
        if checker.check_port_exist(port):
            # ��ռ��
            time.sleep(0.1)
        else:
            # ���ͷ�
            loger.debug("Sleep Ends")
            return
    else:
        #�������ʱ��
        raise AssertionError("Port '%s' always exists during %s second(s)" % (port, maxwait))
        

def sleeptill_startprocess(processpath, port, maxwait=10):
    '''@param port: ������һ��int��Ҳ������һ��int list'''
    sleeptill_hasprocess(processpath, maxwait)
    if isinstance(port, int):
        sleeptill_hasport(port, maxwait)
    else:
        for p in port:
            sleeptill_hasport(p, maxwait)
    
    
def sleeptill_killprocess(processpath, port, maxwait=10):
    '''@param port: ������һ��int��Ҳ������һ��int list'''
    sleeptill_noprocess(processpath, maxwait)
    if isinstance(port, int):
        sleeptill_noport(port, maxwait)
    else:
        for p in port:
            sleeptill_noport(p, maxwait)

def sleep_till_dir_exist(dirpath,maxwait=10):
    '''
    @note: �ȴ��ļ��д���
    @param file:�ȴ����ļ���
    @param maxwait: ��ȴ�ʱ�䣬��λ�룬�������ӡwarning��־
    '''
    t = Timer2()
    t.start()

    loger.debug("Sleep until Dir %s exist"%dirpath)

    while t.end() <maxwait:
        # �жϽ����Ƿ����
        if os.path.isdir(dirpath):
            # ����
            loger.debug("Sleep Ends")
            return
        else:
            # ������
            time.sleep(0.1)

    else:
        #�������ʱ��
        raise Exception, "Dir '%s' never exist during %s second(s)" % (dirpath, maxwait)  
    
def sleep_till_files_stable(path, maxwait=50, timeInterval = 0.5):
    '''
    @note: �ȴ��ļ���С�ȶ�
    @param file: �ȴ����ļ�
    @param maxwait: ��ȴ�ʱ�䣬��λ�룬�������ӡwarning��־
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
            #�������ʱ��
            raise Exception, "File '%s' never become stable during %s second(s)" % (file, maxwait)
        