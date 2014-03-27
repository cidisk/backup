# coding=gbk
'''
Created on 2014.01.21
@author: wangdongsheng@baidu.com
处理conf 及data接口，由框架调用
'''

import os,json,sys 
from xml.dom.minidom import parse
from lib.common.UbConf2 import *
from lib.common.utils import EnvGlobal

        
def getconfitem(modulepath, modulename, confid):
    xmlpath = EnvGlobal.CONF_XML_PATH
    __root = parse(xmlpath).documentElement
    manager_node_list = __root.getElementsByTagName('module_manager')
    for manager_node in manager_node_list:
        module_type = manager_node.getAttribute("module")
        if module_type == modulename:
            for xconf in manager_node.getElementsByTagName('conf'):
                id = xconf.getAttribute("id")
                if id == confid:
                    seg = xconf.getAttribute("seg")
                    if seg == "":
                        seg = ":"
                    path = xconf.getElementsByTagName('path')[0].firstChild.data
                    path = path.strip()
                    path = os.path.join(modulepath, path)
                    name = xconf.getElementsByTagName('name')[0].firstChild.data
                    name = name.strip()
                    path = os.path.join(path, name)
                    return path,seg
    return None,None
    

def getdictitem(modulename, confid):
    xmlpath = EnvGlobal.DATA_XML_PATH
    print "dict xml path %s"%(xmlpath)
    print "module name is %s"%(modulename)
    print "confid is %s"%(confid)
    __root = parse(xmlpath).documentElement
    manager_node_list = __root.getElementsByTagName('module_manager')
    for manager_node in manager_node_list:
        module_type = manager_node.getAttribute("module")
        if module_type == str(modulename):
            for xconf in manager_node.getElementsByTagName('dict'):
                id = xconf.getAttribute("id")
                if id == confid:
                    seg = xconf.getAttribute("seg")
                    if seg == "":
                        seg = "\t"
                    path = xconf.getElementsByTagName('path')[0].firstChild.data
                    path= path.strip()
                    name = xconf.getElementsByTagName('name')[0].firstChild.data
                    name = name.strip()
                    path = os.path.join(path, name)
                    return path,seg
    return None,None

