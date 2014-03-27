# -*- coding: GB18030 -*-
'''
Created on Aug 16, 2011

@author: caiyifeng<caiyifeng@baidu.com>
'''

import re
import os,sys
from common.utils import Shell_System
from common.utils import getpids

#��ʼ��һ������
dtssystem = Shell_System()


def check_process_exist(processpath):
    '''
    @summary: �����̴���
    @param processpath: ���̵ľ���·��
    '''
    pids = getpids(processpath)
    
    if pids:
        return True
    else:
        return False

    
def check_port_exist(port):
    '''
    @summary: ���˿ڱ�ռ��
    @param port: �˿ں�
    '''
    cmd="netstat -nl | grep ':%s '" % port
    output = dtssystem.shell(cmd, output=True)[1]
    
    if output:
        return True
    else:
        return False
    
    
def check_process_started(processpath, *ports):
    '''
    @summary: ����������
    @param processpath: ���̵ľ���·��
    @param ports: ���̶˿ں��б�
    '''
    if not check_process_exist(processpath):
        return False
    
    for p in ports:
        if not check_port_exist(p):
            return False
        
    return True
    

def check_str_contain_multi(string, regex=[]):
    '''@summary: ���string�к�������regex'''
    res = True
    for rel in regex:
        match = re.search(rel, string)
        if not match:
            res = False
            break
    return res

def check_str_contain(string, regex):
    '''@summary: ���string�к�������regex'''
    match = re.search(regex, string)
    if match:
        return True
    else:
        return False
    
def check_lines_contain_multi(lines,ignore_list=[],regex=[]):
    '''
    @summary: ���lines�е�ÿһ�У��Ƿ�������regex
    @param ignore_list: ���Է���ignore regex����
    '''
    # ѡ������δ�����Ե���
    f_lines = []
    for l in lines:
        for ig in ignore_list:
            if check_str_contain(l, ig):
                # ������
                break
        else:
            # δ������
            f_lines.append(l)

    # ���ʣ�µ��У��Ƿ����regex
    for l in f_lines:
        if check_str_contain_multi(l, regex):
            return True
    else:
        return False
    
def check_lines_contain(lines, regex, ignore_list=[]):
    '''
    @summary: ���lines�е�ÿһ�У��Ƿ�������regex
    @param ignore_list: ���Է���ignore regex����
    '''
    # ѡ������δ�����Ե���
    f_lines = []
    for l in lines:
        for ig in ignore_list:
            if check_str_contain(l, ig):
                # ������
                break
        else:
            # δ������
            f_lines.append(l)
            
    # ���ʣ�µ��У��Ƿ����regex
    for l in f_lines:
        if check_str_contain(l, regex):
            return True
    else:
        return False
   
def check_log_contain_multi(log_reader, ignore_list=[],regex=[]):
    '''
    @summary: ���log_readerָ������־���Ƿ���regex��������Ϊ��λ
    @param log_reader: LogReader����
    @param ignore_list: ���Է���ignore regex����
    '''
    # ��log_reader�ж�ȡ
    string = log_reader.read()
    lines = string.splitlines()

    return check_lines_contain_multi(lines, ignore_list, regex) 
    
def check_log_contain(log_reader, regex, ignore_list=[]):
    '''
    @summary: ���log_readerָ������־���Ƿ���regex��������Ϊ��λ
    @param log_reader: LogReader����
    @param ignore_list: ���Է���ignore regex����
    '''
    # ��log_reader�ж�ȡ
    string = log_reader.read()
    lines = string.splitlines()
    
    return check_lines_contain(lines, regex, ignore_list)


def check_path_contain(dirpath, filename, r=False):
    '''
    @summary: ���dirpathĿ¼�У��Ƿ���filename�ļ�orĿ¼
    @param filename: ���Ժ�����չ����*, ?
    @param r: �Ƿ�ݹ���ҡ�Ĭ��False
    '''
    cmd = "find %s -name '%s'" % (dirpath, filename)
    if not r:
        # �ǵݹ�
        cmd += " -maxdepth 1"
    
    output = dtssystem.shell(cmd, output=True)[1]
    if output:
        return True
    else:
        return False
    

def test_check_lines_contain():
    lines = ["line1, feature", "line2, hudson", "line3, nts", "line4, npat"]
    ignore_list = [",.*d", ", nts"]
    
    print check_lines_contain(lines, "[mn]", ignore_list)
    print check_lines_contain(lines, "[sk]")
    print check_lines_contain(lines, "[sk]", ignore_list)
    
if __name__ == "__main__":
    test_check_lines_contain()

