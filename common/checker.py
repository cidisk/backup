# -*- coding: GB18030 -*-
'''
Created on Aug 16, 2011

@author: caiyifeng<caiyifeng@baidu.com>
'''

import re
import os,sys
from common.utils import Shell_System
from common.utils import getpids

#初始化一个对象
dtssystem = Shell_System()


def check_process_exist(processpath):
    '''
    @summary: 检查进程存在
    @param processpath: 进程的绝对路径
    '''
    pids = getpids(processpath)
    
    if pids:
        return True
    else:
        return False

    
def check_port_exist(port):
    '''
    @summary: 检查端口被占用
    @param port: 端口号
    '''
    cmd="netstat -nl | grep ':%s '" % port
    output = dtssystem.shell(cmd, output=True)[1]
    
    if output:
        return True
    else:
        return False
    
    
def check_process_started(processpath, *ports):
    '''
    @summary: 检查进程启动
    @param processpath: 进程的绝对路径
    @param ports: 进程端口号列表
    '''
    if not check_process_exist(processpath):
        return False
    
    for p in ports:
        if not check_port_exist(p):
            return False
        
    return True
    

def check_str_contain_multi(string, regex=[]):
    '''@summary: 检查string中含有正则regex'''
    res = True
    for rel in regex:
        match = re.search(rel, string)
        if not match:
            res = False
            break
    return res

def check_str_contain(string, regex):
    '''@summary: 检查string中含有正则regex'''
    match = re.search(regex, string)
    if match:
        return True
    else:
        return False
    
def check_lines_contain_multi(lines,ignore_list=[],regex=[]):
    '''
    @summary: 检查lines中的每一行，是否含有正则regex
    @param ignore_list: 忽略符合ignore regex的行
    '''
    # 选出所有未被忽略的行
    f_lines = []
    for l in lines:
        for ig in ignore_list:
            if check_str_contain(l, ig):
                # 被忽略
                break
        else:
            # 未被忽略
            f_lines.append(l)

    # 检查剩下的行，是否符合regex
    for l in f_lines:
        if check_str_contain_multi(l, regex):
            return True
    else:
        return False
    
def check_lines_contain(lines, regex, ignore_list=[]):
    '''
    @summary: 检查lines中的每一行，是否含有正则regex
    @param ignore_list: 忽略符合ignore regex的行
    '''
    # 选出所有未被忽略的行
    f_lines = []
    for l in lines:
        for ig in ignore_list:
            if check_str_contain(l, ig):
                # 被忽略
                break
        else:
            # 未被忽略
            f_lines.append(l)
            
    # 检查剩下的行，是否符合regex
    for l in f_lines:
        if check_str_contain(l, regex):
            return True
    else:
        return False
   
def check_log_contain_multi(log_reader, ignore_list=[],regex=[]):
    '''
    @summary: 检查log_reader指定的日志，是否含有regex正则。以行为单位
    @param log_reader: LogReader对象
    @param ignore_list: 忽略符合ignore regex的行
    '''
    # 从log_reader中读取
    string = log_reader.read()
    lines = string.splitlines()

    return check_lines_contain_multi(lines, ignore_list, regex) 
    
def check_log_contain(log_reader, regex, ignore_list=[]):
    '''
    @summary: 检查log_reader指定的日志，是否含有regex正则。以行为单位
    @param log_reader: LogReader对象
    @param ignore_list: 忽略符合ignore regex的行
    '''
    # 从log_reader中读取
    string = log_reader.read()
    lines = string.splitlines()
    
    return check_lines_contain(lines, regex, ignore_list)


def check_path_contain(dirpath, filename, r=False):
    '''
    @summary: 检查dirpath目录中，是否含有filename文件or目录
    @param filename: 可以含有扩展符号*, ?
    @param r: 是否递归查找。默认False
    '''
    cmd = "find %s -name '%s'" % (dirpath, filename)
    if not r:
        # 非递归
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

