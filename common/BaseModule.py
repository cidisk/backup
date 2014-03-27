# -*- coding: GB18030 -*-
import inspect
import os,sys
import subprocess
from lib.common.utils import *
from lib.common.loger import loger
from lib.common import checker
from lib.common.logreader import LogReader
import shutil
from lib.common.XmlHandler import *
from lib.common.Dict import *

class baseModule(object):
    def __init__(self):
        self.sys = Shell_System()
        self.path =None
        #ģ��bin ·��
        self.bin_path = None
        #ģ������·��
        self.conf_path = None
        #ģ���ֵ�·��
        self.dict_path = None
        #log·��
        self.log_path = None
        #���ڴ洢������õ��Ķ˿�
        self.port=[]
        #���ڱ�ʾ��ģ����Ҫ���õĶ˿���Ŀ
        self.port_num = 0
        #���ڱ�ʾģ����
        self.type=None
        #�Ƿ����conf ����flag
        self.conf_bak_flag = False
        #�Ƿ����dict����
        self.dict_back_flag = False
        #���±���������Ҫ�ڸ���module�г�ʼ��
        #notice ��־����
        self.ntlogname = None
        #WF��־����
        self.wflogname = None
        self.nt_logreader = None
        self.wf_logreader = None
            
    def add_relation(self,module):
        """
        @note: �������ݵ����Ѿ����ɵ�����module��ʵ��
        ���������ϵ�Ľ���
        """
        self.module_rel_set.append(module)
        loger.info("Topology is  %s ----> %s",self.type,getattr(module,"type"))
        return 0

    def build_relation(self):
        """
        @note: ���������ģ�����ʵ�ָķ���
        ����ģ�������ģ���ϵ
        """
        pass
       
    def get_port(self):
        """
        @note: ���ر�ģ������Ķ˿�list
        """
        return self.port

    def set_listen_port(self):
        """
        @note:��ģ��ʵ�����ö��õ�conf
        """
        pass

    def start(self):
        """
        @note: ����ģ��
        ע���ͨ���˿ڻ�����Ƿ�����ж��Ƿ������ɹ�
        checker.check_process_exist(processpath)
        checker.check_port_exist(port)
        """
        pass

    def stop(self):
        """
        @note:ֹͣ����
        Ĭ��ͨ��self.bin_pathʵ��
        """
        if self.bin_path <> None and os.path.exists(self.bin_path):
            kill_process(self.bin_path)
            loger.debug("kill process %s"%(self.bin_path))
        else:
            loger.warning("module [%s] has not bin_path!"%(self.type))

    def bak_or_revert_env(self):
        """
        @note������bakflag ����bak ����
        Ĭ�Ͻ�������bak conf dict
        ���path.robotbak�����ڣ���path����
        - ���path.dtsbak���ڣ�����path.robotbak����path
        """
        #����logĿ¼
        if self.log_path is not None:
            cmd = "rm -rf " + self.log_path
            loger.debug(cmd)
            self.sys.shell(cmd)
        # ������core
        rename_cores(self.path)
        #���ݻָ�conf
        if  self.conf_bak_flag:
            bak_or_revert(self.conf_path)
        #���ݻָ�dict
        if self.dict_back_flag:
            bak_or_revert(self.dict_path)
        return 0
        
    def __conf_op(self, optype, confid, k, v=None):
        """
        @note: ��װ ��ȡ��ɾ��������3��conf��������
        optypeΪ�������� 0:���á�1:��ȡ��2��ɾ��
        ����ӿ��� set_conf��get_conf��delete_conf
        """
        if self.path is None:
            raise AssertionError("get modulepath error[%s]"%(self.path))
        path, seg = getconfitem(self.path, self.type, confid)
        if path is None:
            raise AssertionError("set conf error[%s][%s][%s][%s]"%(self.type, confid, k , v))
        conf = UbConfigParser(path, seg)
        if optype == 0:
            conf.set(k , v)
            return 
        if optype == 1:
            return conf.get(k)
        if optype == 2:
            conf.delete(k)
            return
        
    def set_conf(self, confid, k, v):
        """
        @note:����conf
        confidΪconf.xml��ע��id
        """
        return self.__conf_op(0, confid, str(k), str(v)) 

    def get_conf(self, confid, k):
        return self.__conf_op(1, confid, str(k))

    def delete_conf(self, confid, k):
        return self.__conf_op(2, confid, str(k))
    
    def set_dict(self, dictid, *line_item):
        """
        @note:�����ֵ����� ���������ý���ͬ������
        """
        path, seg = getdictitem(self.type, dictid) 
        real_path = os.path.join(self.path, path)
        dicth = DictHandler(real_path, seg)
        dicth.set_dict(line_item)

    def clear_dict(self, dictid):
        """
        @note:�����ֵ�
        """
        path, seg = getdictitem(self.type, dictid) 
        real_path = os.path.join(self.path, path)
        dicth = DictHandler(self, real_path, seg)
        dicth.clear_dict()

    #���½ӿ�Ϊ���Խӿ�
    def check_notice_log_has(self, regex):
        """
        @note:��� notice log���Ƿ����ĳ��
        regexΪƥ��������ʽ
        return�� ��������True������ΪFalse 
        """
        if self.nt_logreader == None:
            nt_log_path = os.path.join(self.log_path, self.ntlogname)
            self.nt_logreader = LogReader(nt_log_path)
        return checker.check_log_contain(self.nt_logreader,regex)
    
    def check_wf_log_has(self, regex):
        """
        ���wf��־����ĳ��
        regexΪƥ��������ʽ
        return�� ��������True������ΪFalse 
        """
        if self.wf_logreader == None:
            wf_log_path = os.path.join(self.log_path, self.wflogname)
            self.wf_logreader = LogReader(wf_log_path)
        return checker.check_log_contain(self.wf_logreader, regex)
    
    def check_fatal(self):
        """
        @note:��������Ƿ����fatal
        return: ����fatal ���� True�� ���򷵻�false
        """
        regex="^FATAL.*"
        return self.check_wf_log_has(regex)

        
    def set_req(self, reqresjs=None, *agrs):
        """
        @note:��������
        ע�ⲻ���ֵ�����
        """
        pass

    def set_res():
        """
        @note:���÷���
        """
        pass

    def common_check(self):
        """
        ͨ��commoncheck�ӿ�
        �ýӿ��޴������
        һ������fatal��core�ȼ��
        """
        #��log��ӡ��
        if self.nt_logreader == None:
           nt_log_path = os.path.join(self.log_path, self.ntlogname)
           self.nt_logreader = LogReader(nt_log_path)
        if self.wf_logreader == None:
            wf_log_path = os.path.join(self.log_path, self.wflogname)
            self.wf_logreader = LogReader(wf_log_path)
        loger.diagnose("Module[%s] wf logs:\n%s"%(self.type, self.wf_logreader.read_fatal_and_last_lines(10)))
        loger.diagnose("Module[%s] notice logs:\n%s"%(self.type, self.nt_logreader.read_last_lines(10)))
        #���core
        log_cores(self.path)
        #���FATAL
        if self.check_fatal():
            raise AssertionError("There FATAL in module[%s]"%(self.type))
        
    def check(self, checkjs=None):
        """
        @note:check�ӿ�
        """
        pass
        
    def reqdata(self):
        '''
        @note: ������ģ���req�γ�json��ֵ���ڲ�����
        '''
        pass

    def get_used_port(self):
        """
        @note:��ø�ģ�����ڻ����Ŀ��ж˿ں� 
        """
        used_port_list = self.sys.shell("netstat -na 2>/dev/null|grep \":\"|awk -F \"[ :]\" '{print $17}'",output = "true")[1].splitlines()
        return used_port_list

def test_system():
    "��Ԫ����"
    npatSys = Shell_System()
    npatSys.shell("echo '12345' > a.txt")
    npatSys.shell("rm b.txt")
    npatSys.shell("cat a.txt b.txt", output = True)
    npatSys.shell("ttt")
    npatSys.shell("ttt", output = True)
    used_port_list = npatSys.shell("netstat -na 2>/dev/null|grep \":\"|awk -F \"[ :]\" '{print $17}'",output = "true")[1].splitlines()
    print used_port_list

if __name__ == '__main__':
    mm = baseModule()
    print type(mm.sys)
