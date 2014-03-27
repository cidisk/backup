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
        #模块bin 路径
        self.bin_path = None
        #模块配置路径
        self.conf_path = None
        #模块字典路径
        self.dict_path = None
        #log路径
        self.log_path = None
        #用于存储被分配得到的端口
        self.port=[]
        #用于表示本模块需要设置的端口数目
        self.port_num = 0
        #用于表示模块名
        self.type=None
        #是否进行conf 备份flag
        self.conf_bak_flag = False
        #是否进行dict备份
        self.dict_back_flag = False
        #以下变量根据需要在各个module中初始化
        #notice 日志名称
        self.ntlogname = None
        #WF日志名称
        self.wflogname = None
        self.nt_logreader = None
        self.wf_logreader = None
            
    def add_relation(self,module):
        """
        @note: 参数传递的是已经生成的其他module的实例
        具体关联关系的建立
        """
        self.module_rel_set.append(module)
        loger.info("Topology is  %s ----> %s",self.type,getattr(module,"type"))
        return 0

    def build_relation(self):
        """
        @note: 如果有下游模块必须实现改方法
        建本模块和下游模块关系
        """
        pass
       
    def get_port(self):
        """
        @note: 返回本模块申请的端口list
        """
        return self.port

    def set_listen_port(self):
        """
        @note:各模块实现设置对用的conf
        """
        pass

    def start(self):
        """
        @note: 启动模块
        注意可通过端口或进程是否存在判断是否启动成功
        checker.check_process_exist(processpath)
        checker.check_port_exist(port)
        """
        pass

    def stop(self):
        """
        @note:停止运行
        默认通过self.bin_path实现
        """
        if self.bin_path <> None and os.path.exists(self.bin_path):
            kill_process(self.bin_path)
            loger.debug("kill process %s"%(self.bin_path))
        else:
            loger.warning("module [%s] has not bin_path!"%(self.type))

    def bak_or_revert_env(self):
        """
        @note：根据bakflag 进行bak 操作
        默认进行两项bak conf dict
        如果path.robotbak不存在，则将path备份
        - 如果path.dtsbak存在，则用path.robotbak覆盖path
        """
        #清理log目录
        if self.log_path is not None:
            cmd = "rm -rf " + self.log_path
            loger.debug(cmd)
            self.sys.shell(cmd)
        # 重命名core
        rename_cores(self.path)
        #备份恢复conf
        if  self.conf_bak_flag:
            bak_or_revert(self.conf_path)
        #备份恢复dict
        if self.dict_back_flag:
            bak_or_revert(self.dict_path)
        return 0
        
    def __conf_op(self, optype, confid, k, v=None):
        """
        @note: 封装 获取，删除、设置3种conf操作方法
        optype为操作类型 0:设置、1:获取、2：删除
        对外接口由 set_conf、get_conf、delete_conf
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
        @note:设置conf
        confid为conf.xml中注册id
        """
        return self.__conf_op(0, confid, str(k), str(v)) 

    def get_conf(self, confid, k):
        return self.__conf_op(1, confid, str(k))

    def delete_conf(self, confid, k):
        return self.__conf_op(2, confid, str(k))
    
    def set_dict(self, dictid, *line_item):
        """
        @note:设置字典数据 将数据设置进不同的列中
        """
        path, seg = getdictitem(self.type, dictid) 
        real_path = os.path.join(self.path, path)
        dicth = DictHandler(real_path, seg)
        dicth.set_dict(line_item)

    def clear_dict(self, dictid):
        """
        @note:清理字典
        """
        path, seg = getdictitem(self.type, dictid) 
        real_path = os.path.join(self.path, path)
        dicth = DictHandler(self, real_path, seg)
        dicth.clear_dict()

    #以下接口为测试接口
    def check_notice_log_has(self, regex):
        """
        @note:检查 notice log中是否包含某项
        regex为匹配正则表达式
        return： 包含返回True、否则为False 
        """
        if self.nt_logreader == None:
            nt_log_path = os.path.join(self.log_path, self.ntlogname)
            self.nt_logreader = LogReader(nt_log_path)
        return checker.check_log_contain(self.nt_logreader,regex)
    
    def check_wf_log_has(self, regex):
        """
        检查wf日志包含某项
        regex为匹配正则表达式
        return： 包含返回True、否则为False 
        """
        if self.wf_logreader == None:
            wf_log_path = os.path.join(self.log_path, self.wflogname)
            self.wf_logreader = LogReader(wf_log_path)
        return checker.check_log_contain(self.wf_logreader, regex)
    
    def check_fatal(self):
        """
        @note:检查结果中是否包含fatal
        return: 包含fatal 返回 True， 否则返回false
        """
        regex="^FATAL.*"
        return self.check_wf_log_has(regex)

        
    def set_req(self, reqresjs=None, *agrs):
        """
        @note:设置请求
        注意不是字典设置
        """
        pass

    def set_res():
        """
        @note:设置返回
        """
        pass

    def common_check(self):
        """
        通用commoncheck接口
        该接口无传入参数
        一般用作fatal、core等检查
        """
        #将log打印出
        if self.nt_logreader == None:
           nt_log_path = os.path.join(self.log_path, self.ntlogname)
           self.nt_logreader = LogReader(nt_log_path)
        if self.wf_logreader == None:
            wf_log_path = os.path.join(self.log_path, self.wflogname)
            self.wf_logreader = LogReader(wf_log_path)
        loger.diagnose("Module[%s] wf logs:\n%s"%(self.type, self.wf_logreader.read_fatal_and_last_lines(10)))
        loger.diagnose("Module[%s] notice logs:\n%s"%(self.type, self.nt_logreader.read_last_lines(10)))
        #检查core
        log_cores(self.path)
        #检查FATAL
        if self.check_fatal():
            raise AssertionError("There FATAL in module[%s]"%(self.type))
        
    def check(self, checkjs=None):
        """
        @note:check接口
        """
        pass
        
    def reqdata(self):
        '''
        @note: 将各个模块的req形成json赋值给内部变量
        '''
        pass

    def get_used_port(self):
        """
        @note:获得该模块所在机器的空闲端口号 
        """
        used_port_list = self.sys.shell("netstat -na 2>/dev/null|grep \":\"|awk -F \"[ :]\" '{print $17}'",output = "true")[1].splitlines()
        return used_port_list

def test_system():
    "单元测试"
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
