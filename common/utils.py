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
     ��������·��
     Ĭ���� ../..
    '''
    DEPLOY_ENV_PATH = os.path.join(os.path.dirname(__file__), "../../")
    DEPLOY_ENV_PATH = os.path.abspath(DEPLOY_ENV_PATH)             
    CONF_XML_PATH = DEPLOY_ENV_PATH +"/lib/conf.xml"
    DATA_XML_PATH = DEPLOY_ENV_PATH +"/lib/dict.xml"

    
class Shell_System(object):
    '''
    @note:��װ������ִ��
    '''
    def __init__(self):
        '''
        @note:todo ������õ�һ��log���� 
        '''
        pass

    def getFile(self,path):
        dirname, filename = os.path.split(inspect.stack()[1][1])
        return dirname + "/" + path

    def shell(self,cmd, output = False, loglevel = None, ignoreWarning=False):
        '''
        ����shell����cmd
        ���cmd����ֵ��Ϊ0����¼warning��־
    
        output = Falseʱ��ֻ����cmd��return code�������������ض���/dev/null
        output = Trueʱ������cmd�� (return code, stdout output, stderr output)
        
        TODO:Ŀǰ����¼log���ȴ��ϲ�robotframe
 
        loglevel����ΪNone, "debug", "info", "warning", "error", "critical"
        loglevel��ΪNoneʱ��cmd��ִ�б�������־
        ignoreWarning=True�� ����ӡwarning��־��Ĭ���Ǵ�ӡ��
        '''
        if loglevel: 
            log_func = getattr(loger, loglevel) 
            log_func("%s: %s", prompt, cmd) 
            
        if output:
            return self.system_output(cmd, ignoreWarning)
        else:
            return self.system_raw(cmd, ignoreWarning)

    def system_output(self,cmd,ignoreWarning=False):
        """����(return code, stdout output, stderr output)
           ignoreWarning=True�� ����ӡwarning��־��Ĭ���Ǵ�ӡ��
        """
        proc = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        outdata, errdata = proc.communicate()
        ret = proc.returncode

        if ret != 0 and ignoreWarning == False:
            # cmdִ���д�
            loger.warning("'%s' return code: %d\nError message: %s", cmd, ret, errdata)
        else:
            loger.warning("'%s' return code: %d", cmd, ret)
        return ret, outdata, errdata
    
    def system_raw(self,cmd, ignoreWarning=False):
        "����return code"
        dev_null = open("/dev/null", "w")
        proc = subprocess.Popen(cmd, shell = True, stdout = dev_null, stderr = dev_null)
        ret = proc.wait()
        dev_null.close()
        if ret != 0 and ignoreWarning == False:
            # cmdִ���д�
            loger.warning("'%s' return code: %d", cmd, ret)
        return ret


def getpids(processpath):
    '''
    @summary: ��ý��̵�id list
    @param processpath: ���̵ľ���·��
    @return: ����id list��û�иý���ʱ�����ؿ�list
    '''
    res = []
    
    processpath = os.path.abspath(processpath)
    processname = os.path.basename(processpath)
    ext = os.path.splitext(processname)[1]
    sys_sh = Shell_System()
    
    if ext == ".py" or ext == ".sh":
        # python or bash script
        
        # ���processpath��Ӧ������id
        cmd = "ps -ef | grep '%s' | grep -v 'grep' | awk '{print $2}'" % processpath
        idlist = sys_sh.shell(cmd, output=True)[1].splitlines()
        res.extend(idlist)
    else:
        # 2���Ƴ���
        # ���processname��Ӧ������id
        cmd = "pgrep -u $USER '^%s$'" % processname
        idlist = sys_sh.shell(cmd, output=True)[1].splitlines()
        
        # �鿴��Щid�Ƿ��Ӧ��processpath
        for id in idlist:
            cmd = "readlink /proc/%s/exe" % id
            idpath = sys_sh.shell(cmd, output=True)[1].rstrip()
            if idpath == processpath:
                # �ҵ��˶�Ӧ�ĳ���path
                res.append(id)
        
    return res


def kill_process(processpath):
    '''
    @summary: ɱ������
    @param processpath: ���̵ľ���·��
    '''
    pids = getpids(processpath)
    sys_sh = Shell_System()
    if pids:
        cmd = "kill -9 " + " ".join(pids)
        sys_sh.shell(cmd)
    
        
def get_relpath(abspath):
    '''
    @summary: �������� <DEPLOY_ENV_PATH>/dts��·��
    '''
    abspath = os.path.abspath(abspath)
    
    if abspath.startswith(EnvGlobal.DEPLOY_ENV_PATH+"/dts/"):
        return abspath[len(EnvGlobal.DEPLOY_ENV_PATH+"/dts/"):]
    else:
        # ����<DEPLOY_ENV_PATH>/dts ��ͷ��ȥ��ͷ�ϵ�'/'
        return abspath.lstrip("/")
    

def rename_cores(path):
    '''@summary: ������path��path/bin/�µ�����core'''
    # path
    sys_sh = Shell_System()
    cmd = "find %s -name 'core.*' -maxdepth 1" % path
    cores = sys_sh.shell(cmd, output=True)[1].splitlines()
    for c in cores:
        dir_str, filename_str = os.path.split(c)        # �ֿ�·�����ļ���
        ext_str = os.path.splitext(filename_str)[1]     # �����չ��
        target_name = dir_str + "/" + "bug" + ext_str
        cmd = "mv %s %s" % (c, target_name)
        sys_sh.shell(cmd)

    # path/bin/
    if not os.path.isdir("%s/bin" % path):
        return
    
    cmd = "find %s/bin -name 'core.*' -maxdepth 1" % path
    cores = sys_sh.shell(cmd, output=True)[1].splitlines()
    for c in cores:
        dir_str, filename_str = os.path.split(c)        # �ֿ�·�����ļ���
        ext_str = os.path.splitext(filename_str)[1]     # �����չ��
        target_name = dir_str + "/" + "bug" + ext_str
        cmd = "mv %s %s" % (c, target_name)
        sys_sh.shell(cmd, loglevel="debug", prompt="Rename Core")


def log_cores(path):
    '''@summary: ��־���path��path/bin/�µ�����core'''
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
    @summary: ���ݻ�ָ�path�ļ���
    @param path: Ŀ���ļ��е�·��
    @note: ���path.dtsbak�����ڣ���path����
    - ���path.dtsbak���ڣ�����path.dtsbak����path
    '''
    bak_path = os.path.abspath(path) + ".robotbak"
        
    if os.path.isdir(bak_path):
        # path.dtsbak���ڣ���������path
        shutil.rmtree(path)
        shutil.copytree(bak_path, path)
        loger.debug("Revert path from %s", bak_path)
    else:
        # path.dtsbak�����ڣ�����
        shutil.copytree(path, bak_path)
        loger.debug("Bak path %s to %s", path, bak_path)

def dict_merge(input_scalar,df_scalar,key_path_stack=[]):
    """
    notes:
         @param:input_scalar �û������dict
         @param:df_scalar ����ģ��req/res ��Ĭ��dict
         @input_scalar �� df_scalar ��key���������ͬ�ı��뷽ʽ���ڲ����豣֤,�ⲿ���ñ�֤
         @����ֵ:input_scalar,��df_scalar ���º��input_scalar
         @summary: ��df_scalar ���dict ȥ�����û������input_scalar
 
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
               #ֱ��ǳ����
               input_scalar[each_key] = df_scalar[each_key]
            else:
               # input_dict ���Ѿ����ڸ�key��
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
    ���ַ�������ǩ������ȡsign1��sign2
    @param _str:Ҫǩ�����ַ���
    @type _str: string
    @param len:�ַ����ĳ���
    @type len: number
    @return: ִ����ȷʱ����(sign1, sign2),ִ��ʧ��ʱ����(0,0)
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
