# -*- coding: GB18030 -*-
'''
Created on Feb 28, 2014
@author: tifeifei <tifeifei@baidu.com>
'''

from lib.common.loger import loger
from lib.common.asserts import *
from lib.common import autosleep
from lib.common.BaseModule import *
from lib.common.utils import * 
from lib.common import checker 
from lib.bslib.bslibModule import bslibModule
from lib.common.GenGlobal import g_genGlobal
from lib.common.logreader import LogReader 
from google.protobuf.descriptor import FieldDescriptor as FD
from google.protobuf.descriptor import Descriptor as DD
import json
import os

class BsModule(baseModule):
    '''
    @summary: bs ģ����ܿ���
    '''
    def __init__(self):
        baseModule.__init__(self)
        self.path = os.path.join(EnvGlobal.DEPLOY_ENV_PATH ,"bs_run_env/bs")
        self.bin_path = self.path + "/bin"
        self.bin = "bs"
        self.bs_port = 0
        self.log_path = self.path + "/log"
        self.wflogname = "bs.log.wf"
        self.ntlogname = "bs.log"
        #���ڱ�ʾģ����
        self.type="bs"
        #���ڱ�������ģ��
        self.module_rel_set = []
        #���ڱ�ʾ��ģ����Ҫ���õĶ˿�
        self.port_num=2
        #���ڴ洢������õ��Ķ˿�
        self.port=[]
        self.libmodule = bslibModule()
        nt_log_path = os.path.join(self.log_path, self.ntlogname)
        self.nt_logreader = LogReader(nt_log_path)
        wf_log_path = os.path.join(self.log_path, self.wflogname)
        self.wf_logreader = LogReader(wf_log_path)

    def common_check(self):
        #basemodule ��common_check ����,�����������������ڴ����
        #baseModule.common_check(self)
        #���core
        log_cores(self.path)
        #���FATAL

        if checker.check_log_contain(self.wf_logreader, "^FATAL.*"):
            raise AssertionError("There FATAL in module[%s]"%(self.type))

        
    def start(self):
        #TODO: check �Ƿ�����
        loger.info("Start bs")
        rename_cores(self.path)
        assert_process_not_started(self.path, str(self.bs_port))        
        # dump das to file
        self.dump_das() 
        # localize 
        self.localize()

        wf_log_path = os.path.join(self.log_path, self.wflogname)
        wf_logreader = LogReader(wf_log_path)

        # TODO: bs �����ɹ���־������
        cmd = "cd %s && nohup ./bin/%s &" % (self.path, self.bin)
        self.sys.shell(cmd)
        #ͨ���������鿴�����Ƿ����� TODO---- checker ��������time����
        checker.check_process_exist(self.bin_path + self.bin)
        #checker.check_port_exist(self.bs_port)
        #autosleep.sleeptill_startprocess(ggEnvGlobal.UI_BIN_PATH,EnvGlobal.UI_PORT,30)
        #ͨ��������־�鿴�����Ƿ����� TODO --- checker ���������
        autosleep.sleeptill_haslog(wf_logreader, "BS server is running...")
        self.common_check()

    def dump_index(self):
        #����bslib �ṩ��dump ��������
        print self.sys.shell('pstree work',  output = True)
        self.libmodule.dump_req()
        
    def kill(self):
        loger.debug("Kill bs")
        kill_process(os.path.join(self.bin_path, self.bin))
        autosleep.sleeptill_killprocess(self.bin_path, self.bs_port)
        
    def restart(self):
        self.kill()
        self.start()

    def stop(self):
        self.kill()
        
    def get_ip_port_set(self):
        """
        @note: ���ظ�����port��Ϣ
        """
        return self.listen_port

    def set_listen_port(self):
        """
        @note:�������ñ�ģ���listen_port
                   ��env������������
        """
        self.set_conf("ub_conf","_svr_newdsp_bs_port",str(self.port[0]))
        self.set_conf("ub_monitor_conf","ubmonitor_socket_port",str(self.port[1]))
        self.listen_port = str(self.port[0])
        return 0

    def localize(self):
        """
        @note: ���ػ���������Ҫ������conf
        """
        # �޸��߳���Ϊ1
        self.set_conf("ub_conf","_svr_newdsp_bs_threadnum",str(1))
        self.set_conf("bs_conf","reload_interval",str(2))
        return 0

    def check(self,table_name, key, attr, value):
        """
        @note: check bdlib ����: res_js Ϊ������������eg.{"table_name":"user_status_table","key":[key1,key2..],"attr":"status","value":0}
        �� ��ʵdump���������бȽ�
        """
        #TODO: ���bdlib �ṩ��check ����
        ret = self.libmodule.check(table_name,key,attr,value)
        if ret == False:
            raise AssertionError("module [bs] check %s[%s].%s = %s error!"%(table_name, key, attr, value))

    def checkNotExist(self, table_name, key):
        ret = self.libmodule.checkNotExist(table_name,key)
        if ret == False:
            raise AssertionError("module [bs] checkNotExist %s[%s] error!"%(table_name, key))

    def set(self,current_obj,objPath_or_attrPath,value):
        try: 
            value = int(value)
        except:
            value = str(value)

        exec_cmd = "current_obj.%s = value"%objPath_or_attrPath
        exec(exec_cmd)

    def get(self,current_obj,objPath_or_attrPath):
        #ret
        exec_cmd = "ret = current_obj.%s"%objPath_or_attrPath
        exec(exec_cmd)
        return ret
            
    def add_base(self,current_obj,objPath_or_attrPath):
        '''
                        ����һ��base�㼶
        '''
        exec_cmd = "ret = current_obj.%s.SmartAdd()"%objPath_or_attrPath
        exec(exec_cmd)
        return ret
    
    def add_inc(self,current_obj,objPath_or_attrPath):
        '''
        ����һ�����������㼶
        '''
        exec_cmd = "obj = current_obj.%s.SmartAdd();obj.event_id =g_genGlobal.genEventid()"%objPath_or_attrPath
        exec(exec_cmd)
        return obj

    def del_inc(self, current_obj, path):
        '''
        ����һ��ɾ�������㼶
        '''
        if not path.endswith(']'):
            raise Exception("U set the wrong path")
        
        instance_ori = self.get(current_obj, path)
        instance_new = None

        _list_name = path.split('[')[0]
        exec_cmd = "instance_new = current_obj.%s.SmartAdd(); instance_new.event_id =g_genGlobal.genEventid()"%_list_name
        exec(exec_cmd)
        instance_new.MergeFrom(instance_ori)
        instance_new.type = 1

    def mod_inc(self, current_obj, path, kv_json):
        '''
        ����һ���޸������㼶
        '''
        kv_dict = json.loads(kv_json)
        if path == "":
            old_obj = current_obj
            parent_instance = current_obj._listener._parent_message_weakref
            for field in parent_instance.DESCRIPTOR.fields:
                if field.message_type.name == current_obj.DESCRIPTOR.name:
                    parent_obj_list = getattr(parent_instance, field.name)
                    break
        else:
            _list_name = path.rstrip('[0-9]')
            parent_obj_list = self.get(current_obj, _list_name)
            old_obj = self.get(current_obj, path)  

        new_obj = parent_obj_list.SmartAdd()
        #new_obj.MergeFrom(old_obj)
        #*********modified by caiduo02 to adapt only one level modify***********
        for field in new_obj.DESCRIPTOR.fields:
            if field.label != FD.LABEL_REPEATED:
				exec("new_obj.%s = old_obj.%s"%(field.name,field.name))
        #************************************************************
        new_obj.type = 2
        new_obj.event_id = g_genGlobal.genEventid() 
        for k, v in kv_dict.items():
            try:
                v = int(v)
            except:
                v = str(v)
            setattr(new_obj, k, v)
            
    def create_kt_das(self):
        self.libmodule.branch.add_valid_kt_ad()
        return self.libmodule.branch.__protobuf_obj__

    def create_rt_das(self):
        self.libmodule.branch.add_valid_rt_ad()
        return self.libmodule.branch.__protobuf_obj__

    def create_act_das(self):
        self.libmodule.branch.add_valid_act_ad()
        return self.libmodule.branch.__protobuf_obj__

    def dump_das(self):
        self.libmodule.dump()
