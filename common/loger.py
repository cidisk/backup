# -*- coding: GB18030 -*-
'''
Created on Feb 18, 2011

@author: caiyifeng@baidu.com

debug: ������Ϣ
info: ����ִ�йؼ��ڵ����Ϣ
success: ��Ҫ�ĳɹ���Ϣ
warning: �����д����Իָ������
diagnose: ���������Ϣ
error: ��������жϣ����򺬶������
critical: ������������ж�

info���ϵ���־�����ǹ����ģ���������������Ϣ��ȡ��ͳ��
��Ļ��� info���ϼ������־
��־�ļ���� ���м������־
wf��־�ļ����warning���ϼ������־
'''


import os, sys 
from common import mylogging


class dtslog(object):
    "@note: ������"
    def __init__(self):
        self.logger = mylogging.getLogger("dtslog")
        
        # ����һ��SUCCESS�㼶
        self.SUCCESS = 25   # ����INFO, С��WARNING
        mylogging.addLevelName(self.SUCCESS, "SUCCESS")
        
        # ����һ��DIAGNOSE�㼶
        self.DIAGNOSE = 35  # ����WARNING, С��ERROR
        mylogging.addLevelName(self.DIAGNOSE, "DIAGNOSE")
        
        # ����logger level
        self.logger.setLevel(mylogging.DEBUG)
        
        # ��Ļ���info�������ϵ���־
        sh = mylogging.StreamHandler()
        sh.setLevel(mylogging.INFO)
        
        # ��Ļ�����־��ʽ
        fmt_sh = mylogging.Formatter("[\033[1;%(colorcode)sm%(levelname)s\033[0m   %(asctime)s   %(myfn)s:%(mylno)d:%(myfunc)s]   %(message)s", "%m-%d %H:%M:%S")
        sh.setFormatter(fmt_sh)
        
        # ��handler����logger
        self.logger.addHandler(sh)
        
        self.sh = sh
        
    def set_no_color(self):
        "@note: ������Ļ���������ɫ����־"
        fmt_sh = mylogging.Formatter("[%(levelname)s   %(asctime)s   %(myfn)s:%(mylno)d:%(myfunc)s]   %(message)s", "%m-%d %H:%M:%S")
        self.sh.setFormatter(fmt_sh)
        
    def set_sh_debug(self):
        "@note: ��Ļ���debug��־"
        self.sh.setLevel(mylogging.DEBUG)
        
    def init_logger(self, logpath):
        "@note: ��ʼ���ļ���־������"
        # ��־�ļ�������м������־
        fh = mylogging.FileHandler(logpath, "w")
        fh.setLevel(mylogging.DEBUG)
        
        # �ļ������־��ʽ
        fmt_fh = mylogging.Formatter("[%(levelname)s   %(asctime)s   %(myfn)s:%(mylno)d:%(myfunc)s]   %(message)s", "%m-%d %H:%M:%S")
        fh.setFormatter(fmt_fh)
        
        # ��handler����logger
        self.logger.addHandler(fh)
        
        
        # wf��־�ļ����warning�������ϵ���־
        fh_wf = mylogging.FileHandler(logpath+".wf", "w")
        fh_wf.setLevel(mylogging.WARNING)
        
        # �ļ������־��ʽ
        fmt_fh_wf = mylogging.Formatter("[%(levelname)s   %(asctime)s   %(myfn)s:%(mylno)d:%(myfunc)s]   %(message)s", "%m-%d %H:%M:%S")
        fh_wf.setFormatter(fmt_fh_wf)
        
        # ��handler����logger
        self.logger.addHandler(fh_wf)
        
    def update_kwargs(self, kwargs, colorcode):
        '''
        @note: ����ֱ�ӱ�debug�Ⱥ�������
        @note: ��kwargs��extra dict�У�����myfn, mylno, myfunc, colorcode
        '''
        try:
            fn, lno, func = self.logger.findCaller()
            fn = os.path.basename(fn)
        except Exception:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
           
        if not "extra" in kwargs:
            # kwargs��û��extra�ֵ䣬������
            kwargs["extra"] = {}
            
        kwargs["extra"]["myfn"] = fn
        kwargs["extra"]["mylno"] = lno
        kwargs["extra"]["myfunc"] = func
        kwargs["extra"]["colorcode"] = colorcode
        
    def indent_msg(self, msg, args):
        '''
        @note: ��msg�ӵ�2�п�ʼindent
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
        self.update_kwargs(kwargs, "0")    # ��ɫ
        self.logger.debug(msg, **kwargs)
        
    def info(self, msg, *args, **kwargs):
        msg = self.indent_msg(msg, args)
        self.update_kwargs(kwargs, "36")   # ǳ��ɫ
        self.logger.info(msg, **kwargs)
        
    def success(self, msg, *args, **kwargs):
        msg = self.indent_msg(msg, args)
        self.update_kwargs(kwargs, "32")   # ��ɫ
        self.logger._log(self.SUCCESS, msg, (), **kwargs)
        
    def warning(self, msg, *args, **kwargs):
        msg = self.indent_msg(msg, args)
        self.update_kwargs(kwargs, "33")   # ��ɫ
        self.logger.warning(msg, **kwargs)
        
    def diagnose(self, msg, *args, **kwargs):
        msg = self.indent_msg(msg, args)
        self.update_kwargs(kwargs, "35")   # �ۺ�ɫ
        self.logger._log(self.DIAGNOSE, msg, (), **kwargs)
        
    def error(self, msg, *args, **kwargs):
        msg = self.indent_msg(msg, args)
        self.update_kwargs(kwargs, "31")   # ��ɫ
        self.logger.error(msg, **kwargs)
        
    def critical(self, msg, *args, **kwargs):
        msg = self.indent_msg(msg, args)
        self.update_kwargs(kwargs, "41")   # ���
        self.logger.critical(msg, **kwargs)

# dtslog ȫ�־��
dtslog = dtslog()
loger = dtslog


def _test():
    "@note: ��Ԫ����"
    dtslog.init_logger("test.log")
    
    dtslog.debug("debug ��־")
    dtslog.info("info ��־")
    try:
        raise Exception, "except �쳣"     # this is a �쳣ע�� !
    except Exception:
        dtslog.warning("warning %s", "��־", exc_info = True)
    dtslog.error("error ��־")
    dtslog.critical("critical ��־")

if __name__ == "__main__":
    _test()
