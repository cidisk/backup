#! /usr/bin/env python
#coding=gbk

import os
import sys

class DictHandler:
    '''
    �����ֵ����
    �ж�д����
    '''
    def __init__(self, path, seg=""):
        self.path = path
        self.seg = seg
        self.lines = []
    
    def set_seg(self, seg ='\t' ):
        '''
        ���ô������ֵ��м�ָ���
        '''
        self.seg = seg
  
    def clear_dict(self):
        fd_dict = open(self.path, 'w')
        fd_dict.close()
        
       
    def set_dict(self,app_line):
        '''
        �����úõ�list
        '''
        fd_dict = open(self.path, 'a')
        if type(app_line) == type([]) or type(app_line) == type(()):
            app_l = u""
            for i in range(len(app_line)):
                app_l += app_line[i]  + self.seg
            del_len = 0-len(self.seg) 
            app_l = app_l[0:del_len]
        else:
            app_l = app_line
        app_l = app_l.replace(r"\t", "\t")
        print app_l
        app_l = app_l.replace(r"\r", "\r")
        app_l = app_l.replace(r"\n", "\n")
        
        app_l += "\n"    
        fd_dict.write(app_l)
        fd_dict.close()
         
