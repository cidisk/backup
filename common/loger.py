# -*- coding: GB18030 -*-
'''
Created on Feb 18, 2011

@author: caiyifeng@baidu.com

debug: 调试信息
info: 程序执行关键节点的信息
success: 重要的成功信息
warning: 任务有错，可以恢复或忽略
diagnose: 出错诊断信息
error: 任务出错中断（程序含多个任务）
critical: 整个程序出错中断

info以上的日志必须是规整的，可以用来进行信息提取和统计
屏幕输出 info以上级别的日志
日志文件输出 所有级别的日志
wf日志文件输出warning以上级别的日志
'''


import os, sys 
from common import mylogging


class dtslog(object):
    "@note: 单例类"
    def __init__(self):
        self.logger = mylogging.getLogger("dtslog")
        
        # 增加一个SUCCESS层级
        self.SUCCESS = 25   # 高于INFO, 小于WARNING
        mylogging.addLevelName(self.SUCCESS, "SUCCESS")
        
        # 增加一个DIAGNOSE层级
        self.DIAGNOSE = 35  # 高于WARNING, 小于ERROR
        mylogging.addLevelName(self.DIAGNOSE, "DIAGNOSE")
        
        # 设置logger level
        self.logger.setLevel(mylogging.DEBUG)
        
        # 屏幕输出info级别以上的日志
        sh = mylogging.StreamHandler()
        sh.setLevel(mylogging.INFO)
        
        # 屏幕输出日志格式
        fmt_sh = mylogging.Formatter("[\033[1;%(colorcode)sm%(levelname)s\033[0m   %(asctime)s   %(myfn)s:%(mylno)d:%(myfunc)s]   %(message)s", "%m-%d %H:%M:%S")
        sh.setFormatter(fmt_sh)
        
        # 将handler加入logger
        self.logger.addHandler(sh)
        
        self.sh = sh
        
    def set_no_color(self):
        "@note: 不在屏幕上输出有颜色的日志"
        fmt_sh = mylogging.Formatter("[%(levelname)s   %(asctime)s   %(myfn)s:%(mylno)d:%(myfunc)s]   %(message)s", "%m-%d %H:%M:%S")
        self.sh.setFormatter(fmt_sh)
        
    def set_sh_debug(self):
        "@note: 屏幕输出debug日志"
        self.sh.setLevel(mylogging.DEBUG)
        
    def init_logger(self, logpath):
        "@note: 初始化文件日志处理器"
        # 日志文件输出所有级别的日志
        fh = mylogging.FileHandler(logpath, "w")
        fh.setLevel(mylogging.DEBUG)
        
        # 文件输出日志格式
        fmt_fh = mylogging.Formatter("[%(levelname)s   %(asctime)s   %(myfn)s:%(mylno)d:%(myfunc)s]   %(message)s", "%m-%d %H:%M:%S")
        fh.setFormatter(fmt_fh)
        
        # 将handler加入logger
        self.logger.addHandler(fh)
        
        
        # wf日志文件输出warning级别以上的日志
        fh_wf = mylogging.FileHandler(logpath+".wf", "w")
        fh_wf.setLevel(mylogging.WARNING)
        
        # 文件输出日志格式
        fmt_fh_wf = mylogging.Formatter("[%(levelname)s   %(asctime)s   %(myfn)s:%(mylno)d:%(myfunc)s]   %(message)s", "%m-%d %H:%M:%S")
        fh_wf.setFormatter(fmt_fh_wf)
        
        # 将handler加入logger
        self.logger.addHandler(fh_wf)
        
    def update_kwargs(self, kwargs, colorcode):
        '''
        @note: 必须直接被debug等函数调用
        @note: 在kwargs的extra dict中，增加myfn, mylno, myfunc, colorcode
        '''
        try:
            fn, lno, func = self.logger.findCaller()
            fn = os.path.basename(fn)
        except Exception:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
           
        if not "extra" in kwargs:
            # kwargs中没有extra字典，创建它
            kwargs["extra"] = {}
            
        kwargs["extra"]["myfn"] = fn
        kwargs["extra"]["mylno"] = lno
        kwargs["extra"]["myfunc"] = func
        kwargs["extra"]["colorcode"] = colorcode
        
    def indent_msg(self, msg, args):
        '''
        @note: 将msg从第2行开始indent
        '''
        msg = msg % args
        msg = msg.rstrip("\n")
        msg_lines = msg.splitlines(True)
        if not msg_lines:
            msg_lines = [""]
        
        msg_indent_lines = []
        msg_indent_lines.append(msg_lines[0])
        msg_indent_lines.extend(["  > " + line for line in msg_lines[1:]] )
        
        return "".join(msg_indent_lines)
            
    def debug(self, msg, *args, **kwargs):
        msg = self.indent_msg(msg, args)
        self.update_kwargs(kwargs, "0")    # 白色
        self.logger.debug(msg, **kwargs)
        
    def info(self, msg, *args, **kwargs):
        msg = self.indent_msg(msg, args)
        self.update_kwargs(kwargs, "36")   # 浅蓝色
        self.logger.info(msg, **kwargs)
        
    def success(self, msg, *args, **kwargs):
        msg = self.indent_msg(msg, args)
        self.update_kwargs(kwargs, "32")   # 绿色
        self.logger._log(self.SUCCESS, msg, (), **kwargs)
        
    def warning(self, msg, *args, **kwargs):
        msg = self.indent_msg(msg, args)
        self.update_kwargs(kwargs, "33")   # 黄色
        self.logger.warning(msg, **kwargs)
        
    def diagnose(self, msg, *args, **kwargs):
        msg = self.indent_msg(msg, args)
        self.update_kwargs(kwargs, "35")   # 粉红色
        self.logger._log(self.DIAGNOSE, msg, (), **kwargs)
        
    def error(self, msg, *args, **kwargs):
        msg = self.indent_msg(msg, args)
        self.update_kwargs(kwargs, "31")   # 红色
        self.logger.error(msg, **kwargs)
        
    def critical(self, msg, *args, **kwargs):
        msg = self.indent_msg(msg, args)
        self.update_kwargs(kwargs, "41")   # 红底
        self.logger.critical(msg, **kwargs)

# dtslog 全局句柄
dtslog = dtslog()
loger = dtslog


def _test():
    "@note: 单元测试"
    dtslog.init_logger("test.log")
    
    dtslog.debug("debug 日志")
    dtslog.info("info 日志")
    try:
        raise Exception, "except 异常"     # this is a 异常注释 !
    except Exception:
        dtslog.warning("warning %s", "日志", exc_info = True)
    dtslog.error("error 日志")
    dtslog.critical("critical 日志")

if __name__ == "__main__":
    _test()
