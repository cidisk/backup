# coding: GB18030 -*-
'''
Created on Aug 17, 2011

@author: caiyifeng<caiyifeng@baidu.com>
'''

import os
import shutil
import subprocess
from common.loger import loger
import string
import traceback
from ctypes import *

so_path=os.path.join(os.path.dirname(__file__), "") + "/util.so"

class EnvGlobal(object):
    '''
     环境部署路径
     默认在 ../..
    '''
    DEPLOY_ENV_PATH = os.path.join(os.path.dirname(__file__), "../../")
    DEPLOY_ENV_PATH = os.path.abspath(DEPLOY_ENV_PATH)             
    CONF_XML_PATH = DEPLOY_ENV_PATH +"/lib/conf.xml"
    DATA_XML_PATH = DEPLOY_ENV_PATH +"/lib/dict.xml"

    
class Shell_System(object):
    '''
    @note:封装命令行执行
    '''
    def __init__(self):
        '''
        @note:todo 从外面得到一个log对象 
        '''
        pass

    def getFile(self,path):
        dirname, filename = os.path.split(inspect.stack()[1][1])
        return dirname + "/" + path

    def shell(self,cmd, output = False, loglevel = None, ignoreWarning=False):
        '''
        调用shell命令cmd
        如果cmd返回值不为0，记录warning日志
    
        output = False时，只返回cmd的return code。命令的输出被重定向到/dev/null
        output = True时，返回cmd的 (return code, stdout output, stderr output)
        
        TODO:目前不记录log，等待合并robotframe
 
        loglevel可以为None, "debug", "info", "warning", "error", "critical"
        loglevel不为None时，cmd的执行被记入日志
        ignoreWarning=True， 不打印warning日志，默认是打印的
        '''
        if loglevel: 
            log_func = getattr(loger, loglevel) 
            log_func("%s: %s", prompt, cmd) 
            
        if output:
            return self.system_output(cmd, ignoreWarning)
        else:
            return self.system_raw(cmd, ignoreWarning)

    def system_output(self,cmd,ignoreWarning=False):
        """返回(return code, stdout output, stderr output)
           ignoreWarning=True， 不打印warning日志，默认是打印的
        """
        proc = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        outdata, errdata = proc.communicate()
        ret = proc.returncode

        if ret != 0 and ignoreWarning == False:
            # cmd执行有错
            loger.warning("'%s' return code: %d\nError message: %s", cmd, ret, errdata)
        else:
            loger.warning("'%s' return code: %d", cmd, ret)
        return ret, outdata, errdata
    
    def system_raw(self,cmd, ignoreWarning=False):
        "返回return code"
        dev_null = open("/dev/null", "w")
        proc = subprocess.Popen(cmd, shell = True, stdout = dev_null, stderr = dev_null)
        ret = proc.wait()
        dev_null.close()
        if ret != 0 and ignoreWarning == False:
            # cmd执行有错
            loger.warning("'%s' return code: %d", cmd, ret)
        return ret


def getpids(processpath):
    '''
    @summary: 获得进程的id list
    @param processpath: 进程的绝对路径
    @return: 进程id list。没有该进程时，返回空list
    '''
    res = []
    
    processpath = os.path.abspath(processpath)
    processname = os.path.basename(processpath)
    ext = os.path.splitext(processname)[1]
    sys_sh = Shell_System()
    
    if ext == ".py" or ext == ".sh":
        # python or bash script
        
        # 获得processpath对应的所有id
        cmd = "ps -ef | grep '%s' | grep -v 'grep' | awk '{print $2}'" % processpath
        idlist = sys_sh.shell(cmd, output=True)[1].splitlines()
        res.extend(idlist)
    else:
        # 2进制程序
        # 获得processname对应的所有id
        cmd = "pgrep -u $USER '^%s$'" % processname
        idlist = sys_sh.shell(cmd, output=True)[1].splitlines()
        
        # 查看这些id是否对应了processpath
        for id in idlist:
            cmd = "readlink /proc/%s/exe" % id
            idpath = sys_sh.shell(cmd, output=True)[1].rstrip()
            if idpath == processpath:
                # 找到了对应的程序path
                res.append(id)
        
    return res


def kill_process(processpath):
    '''
    @summary: 杀死进程
    @param processpath: 进程的绝对路径
    '''
    pids = getpids(processpath)
    sys_sh = Shell_System()
    if pids:
        cmd = "kill -9 " + " ".join(pids)
        sys_sh.shell(cmd)
    
        
def get_relpath(abspath):
    '''
    @summary: 获得相对于 <DEPLOY_ENV_PATH>/dts的路径
    '''
    abspath = os.path.abspath(abspath)
    
    if abspath.startswith(EnvGlobal.DEPLOY_ENV_PATH+"/dts/"):
        return abspath[len(EnvGlobal.DEPLOY_ENV_PATH+"/dts/"):]
    else:
        # 不以<DEPLOY_ENV_PATH>/dts 开头，去除头上的'/'
        return abspath.lstrip("/")
    

def rename_cores(path):
    '''@summary: 重命名path和path/bin/下的所有core'''
    # path
    sys_sh = Shell_System()
    cmd = "find %s -name 'core.*' -maxdepth 1" % path
    cores = sys_sh.shell(cmd, output=True)[1].splitlines()
    for c in cores:
        dir_str, filename_str = os.path.split(c)        # 分开路径和文件名
        ext_str = os.path.splitext(filename_str)[1]     # 获得扩展名
        target_name = dir_str + "/" + "bug" + ext_str
        cmd = "mv %s %s" % (c, target_name)
        sys_sh.shell(cmd)

    # path/bin/
    if not os.path.isdir("%s/bin" % path):
        return
    
    cmd = "find %s/bin -name 'core.*' -maxdepth 1" % path
    cores = sys_sh.shell(cmd, output=True)[1].splitlines()
    for c in cores:
        dir_str, filename_str = os.path.split(c)        # 分开路径和文件名
        ext_str = os.path.splitext(filename_str)[1]     # 获得扩展名
        target_name = dir_str + "/" + "bug" + ext_str
        cmd = "mv %s %s" % (c, target_name)
        sys_sh.shell(cmd, loglevel="debug", prompt="Rename Core")


def log_cores(path):
    '''@summary: 日志输出path和path/bin/下的所有core'''
    # path
    sys_sh = Shell_System()
    cmd = "find %s -name 'core.*' -maxdepth 1" % path
    cores = sys_sh.shell(cmd, output=True)[1]
    if cores:
        loger.diagnose("Find Cores in %s:\n%s", path, cores)
        raise AssertionError("Find Cores in %s:\n%s", path, cores)    
    # path/bin/
    if not os.path.isdir("%s/bin" % path):
        return
    
    cmd = "find %s/bin -name 'core.*' -maxdepth 1" % path
    cores = sys_sh.shell(cmd, output=True)[1]
    if cores:
        loger.diagnose("Find Cores in %s/bin/:\n%s", path, cores)
        raise AssertionError("Find Cores in %s/bin/:\n%s", path, cores)

def bak_or_revert(path):
    '''
    @summary: 备份或恢复path文件夹
    @param path: 目标文件夹的路径
    @note: 如果path.dtsbak不存在，则将path备份
    - 如果path.dtsbak存在，则用path.dtsbak覆盖path
    '''
    bak_path = os.path.abspath(path) + ".robotbak"
        
    if os.path.isdir(bak_path):
        # path.dtsbak存在，用它覆盖path
        shutil.rmtree(path)
        shutil.copytree(bak_path, path)
        loger.debug("Revert path from %s", bak_path)
    else:
        # path.dtsbak不存在，备份
        shutil.copytree(path, bak_path)
        loger.debug("Bak path %s to %s", path, bak_path)

def dict_merge(input_scalar,df_scalar,key_path_stack=[]):
    """
    notes:
         @param:input_scalar 用户输入的dict
         @param:df_scalar 各个模块req/res 的默认dict
         @input_scalar 和 df_scalar 的key必须采用相同的编码方式，内部不予保证,外部调用保证
         @返回值:input_scalar,用df_scalar 更新后的input_scalar
         @summary: 用df_scalar 这个dict 去更新用户输入的input_scalar
 
    """
    if type(input_scalar) != type(df_scalar) and \
            ( type(input_scalar) not in (int, bool) and type(df_scalar) not in (int,bool)) :
       key_path = string.join(key_path_stack, r'.') if len(key_path_stack) > 0 else ""
       loger.error("input key %s type:[%s] is not equal df type:[%s]" %(key_path, type(input_scalar), type(df_scalar)))
       return -1
    elif type(df_scalar) == dict:
        for each_key in df_scalar.keys():
            key_path_stack.append(str(each_key))
            key_path = string.join(key_path_stack, r'.')
            if not input_scalar.has_key(each_key):
               loger.info("add key:[%s] to input_scalar from  default dict" % key_path)
               #直接浅拷贝
               input_scalar[each_key] = df_scalar[each_key]
            else:
               # input_dict 里已经存在该key了
               ret = dict_merge(input_scalar[each_key], df_scalar[each_key], key_path_stack)
               key_path_stack.pop()
               if ret != 0:
                  return -1
    elif type(df_scalar) == list:
         key_path = string.join(key_path_stack, r'.') if len(key_path_stack) > 0 else ""
         loger.info("update array key:[%s] with df_scalar"%(key_path)) 
         if len(df_scalar) > 0:
            for i in range(0, len(input_scalar)):
                ret = dict_merge(input_scalar[i], df_scalar[0], key_path_stack)
                if ret != 0:
                   return -1
    elif type(df_scalar) in (int, float, long, bool, str, unicode):
         return 0
    return 0

def creat_sign_fs64(_str, len):
    """
    对字符串进行签名，获取sign1和sign2
    @param _str:要签名的字符串
    @type _str: string
    @param len:字符串的长度
    @type len: number
    @return: 执行正确时返回(sign1, sign2),执行失败时返回(0,0)
    @rtype: tuple
    """
    global so_path
    if _str is None:
        print _str, "is none!"
        return ""
    if os.path.exists(so_path):
        try:
            so = CDLL(so_path)
            sign64 = so._creat_sign_fs64
            t1 = c_ulong(0)
            t2 = c_ulong(0)    
            ret = sign64(_str, len, byref(t1), byref(t2))
        except:
            print "catch exception." 
            print traceback.print_exc() 
        if ret != 1:
            print "error in ", so_path
            return (0, 0)
        res = (t1.value, t2.value)
        return res
    else:
        print so_path , 'is not exists!'
        return (0, 0)

if __name__=="__main__":
    tuple1 = creat_sign_fs64("www.autotest.com",16)
    tuple2 = creat_sign_fs64("autotest.com",12)
    print tuple1
    print tuple2
