# -*- coding: GB18030 -*-
'''
Created on Feb 20, 2014

@author: wangdongsheng<wangdongsheng@baidu.com>
'''

import os, sys 
from common import checker
from common.loger import loger
import string

class AssertException(Exception):
    pass


def assert_equal(lhs, rhs, errmsg=None):
    '''
    @summary: 断言lhs和rhs相等
    @param errmsg: 断言失败时显示的信息
    '''
    if errmsg is None:
        errmsg = "%s doesn't equal to: %s" % (lhs, rhs)
    
    if lhs != rhs:
        raise AssertException, errmsg
    

def assert_not_equal(lhs, rhs, errmsg=None):
    '''
    @summary: 断言lhs和rhs不想等
    @param errmsg: 断言失败时显示的信息
    '''
    if errmsg is None:
        errmsg = "%s equals to: %s" % (lhs, rhs)
        
    if lhs == rhs:
        raise AssertException, errmsg

def assert_gt(lhs, rhs, errmsg=None):
    '''
    @summary: 断言lhs大于rhs
    @param errmsg: 断言失败时显示的信息
    '''
    if errmsg is None:
        errmsg = "%s is less than or equal to %s" % (lhs, rhs)
    
    if lhs <= rhs:
        raise AssertException, errmsg

def assert_bound(value, lb, hb, errmsg=None):
    '''
    @summary: 断言value介于lb和hb之间
    @param errmsg: 断言失败时显示的信息
    @param lb: 下限
    @param hb: 上限
    '''
    if errmsg is None:
        errmsg = "%s is not in [%s, %s]" % (value, lb, hb)
    
    if value < lb or value > hb:
        raise AssertException, errmsg

def assert_in_list(ele, lis, errmsg=None):
    '''
    @summary: 断言element是list中的一个元素
    '''
    if errmsg is None:
        errmsg = "%s is not in %s" % (ele, lis)
    
    if ele not in lis:
        raise AssertException, errmsg
    

def assert_process_started(processpath, *ports):
    '''
    @summary: 断言进程启动
    @param processpath: 进程的绝对路径
    @param ports: 进程端口号列表
    '''
    if not checker.check_process_started(processpath, *ports):
        ports_str = ",".join([str(p) for p in ports])
        raise AssertException, "Process is not started: %s [%s]" % (processpath, ports_str)


def assert_process_not_started(processpath, *ports):
    '''
    @summary: 断言进程未启动
    @param processpath: 进程的绝对路径
    @param ports: 进程端口号列表
    '''
    if checker.check_process_started(processpath, *ports):
        ports_str = ",".join([str(p) for p in ports])
        raise AssertException, "Process is started: %s [%s]" % (processpath, ports_str)


def assert_path_not_contain(dirpath, filename, r=False):
    '''
    @summary: 断言路径中不含有文件
    @param filename: 可以含有扩展符号*, ?
    @param r: 是否递归查找。默认False
    '''
    if checker.check_path_contain(dirpath, filename, r):
        raise AssertException, "File '%s' in path: %s" % (filename, dirpath)
    

def assert_log_not_contain(log_reader, regex, ignore_list=[]):
    '''
    @summary: 断言日志中不含有正则字符串
    @param log_reader: LogReader对象
    @param regex: 正则字符串
    @param ignore_list: 忽略符合ignore regex的行
    '''
    if checker.check_log_contain(log_reader, regex, ignore_list):
        raise AssertException, "Regex '%s' in log '%s' from pos %d" % (regex, log_reader.logpath, log_reader.pos)



'''
以下是scalar equal实现
'''
def comma(_str):
    if _str <> "":
        _str += ','
    return _str

def key_name(name):
    if str(name) <> "":
        return  '"'+str(name)+'"'+":"
    return ""

def which2json(_str, name, item):
    ret = 0
    if type(item) == int or type(item) == float or type(item) == bool:
        _str=numeral2json(_str, name, item)
    elif type(item) == str:
          _str=str2json(_str, name, item)
    elif type(item) == list:
        _str=list2json(_str, name, item)
    elif type(item) == dict:
        _str=dict2json(_str, [], item)
    elif hasattr(item,'tojson'):
        if hasattr(item,'needname') and item.needname() and name <> "":
            _str+='"'+name+'"'+":"
        _str+=item.tojson()
    else:
        ret = -1
        parall_log.autoParLog.warning('unknown type'+str(type(item)))
    return _str,ret
                    
def numeral2json(_str, name, value):
    if value <> "":
        #_str=comma(_str)
        value=str(value)
        if value == "False":
            value='false'
        if value == 'True':
            value='true'
        if name == '':
            _str += value
        else:
            _str += key_name(name)+value
        
    return _str

def str2json(_str, name, value):
    if value <> "":
        #_str=comma(_str)
        _str +=  key_name(name)+'"'+str(value)+'"'
    return _str

def list2json(_str, name, _list, isopt=False):
    llen=len(_list)
    if llen == 0 and isopt == True:
        return _str
    #_str=comma(_str)
    ret = 0
    tmp_str=""
    for inx in range(0, llen):
        item=_list[inx]
        if inx > 0:
            tmp_str=comma(tmp_str)
        tmp_str,ret = which2json(tmp_str, '', item)
    if ret == 0:
        _str +=  key_name(name)+"["+tmp_str+"]"
    return _str
    
def dict2json(_str, name, dict):
    if len(dict) == 0:
        return _str
    itemname=[]
    if len(name) <> 0:
        itemname=name
    else:
        itemname=dict.keys()
    tmp_str=""
    ret = 0
    for inx in range(0, len(itemname)):
        name=itemname[inx]
        if dict.has_key(name):
            if dict[name] == '':
                continue
            tmp_str=comma(tmp_str)
            tmp_str, ret=which2json(tmp_str, name, dict[name])
    if ret == 0:
        _str += '{'+tmp_str+'}'
    return _str

def scalar_equal(src_scalar, dst_scalar, key_path_stack=[]):
    """
    @note:compare src_scalar to dst_scalar variable 
          means, it will compare each item in src_scalar to dst_scalar recursively 
    @param src_scalar: expect scalar
    @param dst_scalar: real   scalar
    @key_path_stack: for recrode key_path 
    """
    if type(src_scalar) != type(dst_scalar) and \
            ( type(src_scalar) not in (int, bool) and type(dst_scalar) not in (int,bool) ) : 
        key_path = string.join(key_path_stack, r'.') if len(key_path_stack) > 0 else ""
        loger.error("src key %s type:[%s] is not equal dst type:[%s]" %(key_path, type(src_scalar), type(dst_scalar)))
        return False
    elif type(src_scalar) == dict:
        for each_key in src_scalar.keys():
            key_path_stack.append(str(each_key))
            key_path = string.join(key_path_stack, r'.')
            if not dst_scalar.has_key(each_key):
                loger.error( "src key:%s does not exists in dst" % key_path)
                return False
            ret = scalar_equal(src_scalar[each_key], dst_scalar[each_key], key_path_stack)
            key_path_stack.pop()
            if not ret:
                return False
    elif type(src_scalar) == list:
        key_path = string.join(key_path_stack, r'.') if len(key_path_stack) > 0 else ""
        if len(src_scalar) != len(dst_scalar):
            loger.error("src key:%s scalar list length %d is not equal dst %d" %(key_path, len(src_scalar), len(dst_scalar)))
        for i in range(0, len(src_scalar)):
            ret = scalar_equal(src_scalar[i], dst_scalar[i], key_path_stack)
            if not ret:
                loger.error("src key:%s[%d]->%s not equal dst value%s" %(key_path, i, src_scalar[i], dst_scalar[i]))
                return False
    elif type(src_scalar) in (int, float, long, bool, str, unicode):
        key_path = string.join(key_path_stack, r'.') if len(key_path_stack) > 0 else ""
        if src_scalar != dst_scalar:
            loger.error("src key %s->%s is not equal dst value %s" %(key_path, src_scalar, dst_scalar))
            return False
    return True
    
