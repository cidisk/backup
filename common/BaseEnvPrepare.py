# -*- coding: UTF-8* -*-
import os, sys
#from lib.bfpmodule import BfpModule #自lib中import一个module
import json
from lib.common.loger import loger

class BaseEnvPrepare(object):
    def __init__(self):
        self.module_set = []
        #self.bc=BfpClient()
       
    def build_env(self):
        """
        @note:建立模块的关联关系，负责模块的启动
        """
        #step 1: build topo  @使用中必须添加
        #self.bc.add_relation(self.bm)
    
        #step 2: register module @使用中必须添加
        #self.register_module(self.bc)
        
        #step 3: port adaptive
        self.port_adaptive()
        #step 4: build relations
        self.build_relations()
        #conf\dict环境备份或者更新
        self.bak_or_revert_env()

    def __del__(self):
        pass
    
    def __deal_module_method(self, modulename, method, *args):
        """
        @notice:私有方法,调用各个module的方法
        """
        for module_dict in self.module_set:
            if module_dict["module"].type !=  modulename or (not  hasattr(module_dict["module"], method)):
                continue
            getattr(module_dict["module"], method)(*args)
             
    def register_module(self, module, excute_method="build"):
        """
        @note: 添加需要搭建的模块对象
        """
        self.module_set.append({"module":module, "method":excute_method})

    def port_adaptive(self,start_port = 1024):
        """
        @note: 端口自适应,分成三步，收集占用端口，计算可用端口，分配可用端口
        注意这个需要你注册了模块才可以使用，如果你一个模块都没有注册的话，程序将会hang住哦！！！
        """
        used_port_list = []
        port_num = 0
        ret = 0
        #收集各个模块所在机器所占用的端口号以及所需要使用的端口数目
        for module_dict in self.module_set:
            used_port = getattr(module_dict["module"], "get_used_port")()
            used_port_list += used_port
            port_num += getattr(module_dict["module"], "port_num")

        #下面这段代码的意思是去重
        used_port_list = list(set(used_port_list))
        used_port_list = [x for x in used_port_list if x.isdigit() == True]

        #用简单的算法寻找一段连续的空闲端口号
        free_port_list = []
        min_port = start_port
        go_flag = "true"
        num = 0
        while (go_flag == "true" and min_port < 65535):
            max_port = min_port + port_num
            num = 0
            for port in used_port_list:
                if (int(port) > min_port and int(port) < max_port):
                    min_port = max_port + 1
                    break
                num += 1
                if( num == len(used_port_list)):
                    go_flag = "false"

        for i in range(0,port_num):
            free_port_list.append(min_port+i)
        loger.info("free_port_list :%s",str(free_port_list))

        #将free_port_list按照各个模块所需要的端口数，分配下去
        j = 0
        while j < port_num:
            for module_dict in self.module_set:
                for k in range(0,getattr(module_dict["module"], "port_num")):
                    getattr(module_dict["module"], "port").append(free_port_list[j])
                    k += 1
                    j += 1
                #分配完之后就set_listen_port
                if getattr(module_dict["module"],"set_listen_port")() != 0:
                    ret += 1
                loger.info("set %s port : %s" ,str(getattr(module_dict["module"],"type")),str(getattr(module_dict["module"],"get_port")()))
        return ret

    def build_relations(self):
        """
        @note: 设置各个模块的关联关系,收集各个模块的ip+listenport,然后调用方法统一设置
        """
        for module_dict in self.module_set:
            self.__deal_module_method(module_dict["module"].type, "build_relation")

    
    def start(self, ignore_modle_list=[]):
        """
        @note: 设置各个模块的关联关系,收集各个模块的ip+listenport,然后调用方法统一设置
        input: ignore_modle_list 为list类型,统一启动中忽略的模块
        注意：请在各个module start方法种通过判断
        """
        loger.info("xinglin:module_set:%s"%(str(self.module_set)))
        for module_dict in self.module_set:
            
            if hasattr(module_dict["module"],"start") and module_dict["module"].type not in ignore_modle_list:
                getattr(module_dict["module"], "start")()
    
    def bak_or_revert_env(self):
        """
        @note:备份或者还原环境 使用场景 搭建环境后第一次备份，此后运行还原
        打开方式是对应modle 的两个flage打开，或者重载module的bak_or_revert_env方法
        """
        for module_dict in self.module_set:
            self.__deal_module_method(module_dict["module"].type, "bak_or_revert_env")

    def set_dict(self, modulename, dictid, *args):
        """
        @note:设置字典 编辑时字典的一行数据可以放一起，也可以按列填写
        """
        self.__deal_module_method(modulename, "set_dict", dictid, *args)

    def clear_dict(self, modulename, dictid):
        """
        @note将某个指定字典清理
        """
        self.__deal_module_method(modulename, "clear_dict", dictid)
        
    def set_req(self, modulename, reqresjs, *args):
        """
        @note: 设置各个模块的接口数据
           目前设置接收到的上游数据                       
           todo：下游数据也通过这个方法设置
           本质均为将数据统一放入内部结构体
        """
        loger.info("set  req modulename:%s,reqjson:%s",modulename,reqresjs)
        self.__deal_module_method(modulename, "set_req", reqresjs, *args)

    def set_res(self, modulename, reqresjs, *args):
        """
        @note: 设置返回结果
        """
        loger.info("set  res modulename:%s,reqjson:%s",modulename,reqresjs)
        self.__deal_module_method(modulename, "set_res", reqresjs, *args)
        

    def do_req(self):
        """
         @note: send one request
        """
        pass

    def stop(self, modulename=None):
        """
        @note: 默认 stop all module
        modulename有内容时停止对应module的
        """
        ret = 0
        try:
            if modulename!=None:
               return self.__deal_module_method(modulename, "stop")
            for module_dict in self.module_set:
                self.__deal_module_method(module_dict["module"].type, "stop")
        # fianlly,must clear module_set,it's very important
        finally:
            self.module_set=[]
            
    def check_notice_log_has(self, modulename,  regex):
        """
        @notice: 检查某个module notice中是否包含正则中内容
        """
        ret = self.__deal_module_method(modulename, "check_notice_log_has", regex)
        if ret <> True:
            raise AssertionError("module [%s] not has expect notice log[%s] !"%(modulename, regex))
    
    def check_wf_log_has(self, modulename,  regex):
        """
        @notice: 检查某个module notice中是否包含正则中内容
        """
        ret = self.__deal_module_method(modulename, "check_wf_log_has", regex)
        if ret <> True:
            raise AssertionError("module [%s] not has expect wf log[%s] !"%(modulename, regex))

    def check_notice_log_not_has(self, modulename,  regex):
        ret = self.__deal_module_method(modulename, "check_notice_log_has", regex)
        if ret <> False:
            raise AssertionError("module [%s]  has expect notice log[%s] !"%(modulename, regex))

    def check_wf_log_not_has(self, modulename,  regex):
        ret = self.__deal_module_method(modulename, "check_wf_log_has", regex)
        if ret <> False:
            raise AssertionError("module [%s] has expect wf log[%s] !"%(modulename, regex))
            
    def common_check(self):
        """
        @note: common check of every module
        """
        ret = 0
        for module_dict in self.module_set:
            self.__deal_module_method(module_dict["module"].type, "common_check")

    def check(self, modulename, checkjs, *args):
        """
        @note: check of any module
        """
        self.__deal_module_method( modulename, "check", checkjs, *args)
   
    def check_not_equal(self,modulename, excludejs, *args):
        """
        @note: check of any module
        """
        self.__deal_module_method( modulename, "check_not_equal", excludejs, *args)

    def set_conf(self,  modulename, confid, k , v):
        self.__deal_module_method(modulename, "set_conf", confid, k , v) 
                
    def get_conf(self,  modulename, confid, k):
        return self.__deal_module_method(modulename, "get_conf", confid, k)     
    
    def delete_conf(self, modulename, confid, k):
        return self.__deal_module_method(modulename, "delete_conf", confid, k)
               
        
if __name__ == '__main__':
    bc=BfpClient()
    bm=BfpModule()
    adxSt=AdxStub()
    rankSt=RankStub()

    bc.add_relation(bm)
    bm.add_relation(adxSt)
    bm.add_relation(rankSt)

    env=EnvPrapare()
    env.register_module(bc)
    env.register_module(bm)
    env.register_module(adxSt)
    env.register_module(rankSt)
    
    env.port_adaptive(60000)
    env.build_relations()

    slot_dict = {"level":3}
    js=json.dumps(slot_dict)
    env.create_das("createClbNewSlot", js)
    
    #env.stop()
