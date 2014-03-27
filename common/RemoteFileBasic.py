# coding: gb18030
'''
Created on Oct 13, 2010

@author: caiyifeng@baidu.com
bs相关file编辑的lib
'''

from shutil import copy, move
from os import path
from common.loger import loger

g_AD_TYPES = ('bd', 'fc')

class RemoteFileBasic():
    '''编辑bs数据文件的基类
    
    caiyifeng@baidu.com'''
    
    def __init__(self,  filepath):
        '''初始化
        
        filepath: 文件路径, 字符串类型'''
        self.filepath = filepath
        self.recs = []  # 文件记录的list
        self.isBaked = False   # 还没bak过
        
    def bak_or_revert(self):
        "如果没有bak文件，就备份；如果有bak文件，就用bak文件恢复原文件"
        bak_path = self.filepath + ".ntsbak"
        
        if path.isfile(bak_path):
            # 已经有备份文件了，恢复原文件
            loger.debug("Revert %s", bak_path)
            copy(bak_path, self.filepath)
        else:
            # 还没有备份文件，备份之
            loger.debug("Bak %s", self.filepath)
            copy(self.filepath, bak_path)
            
        # 标记已经备份过了
        self.isBaked = True
        
    def revert(self):
        '恢复被修改的文件'
        if self.isBaked:
            # 已经备份过了，需要恢复文件
            move(self.filepath, self.filepath + '.ntsrun')  # 保存本次运行的文件
            move(self.filepath + '.ntsbak', self.filepath)  # 恢复备份文件
            self.isBaked = False
        
    def addRec(self, *fields):
        '''在文件中增加一条记录
        
        fileds：各个字段的tuple，每个字段都是字符串类型'''
        self.addRecImp(fields)
        
    def addRecImp(self, fields):
        '''在文件中增加一条记录，addRec方法的具体实现
        
        fields: 各个字段的tuple, list or tuple类型, 每个字段都是字符串类型'''
        arec = fields[:]
        self.recs.append(arec)
        
    def setDelim(self):
        '''设置记录中，各个字段的分隔符为\t'''
        self.delim = '\t'
        
    def __str__(self):
        '''将self.recs打印为字符串'''
        self.setDelim()
        
        strLines = []
        for arec in self.recs:
            strLine = self.delim.join(arec)
            strLines.append(strLine)
        return '\n'.join(strLines) + '\n'
    
    def dump(self):
        '''保存到文件, 第一次保存前会先备份'''
        if not self.isBaked:
            # 还没有bak过，需要先备份
            copy(self.filepath, self.filepath + '.ntsbak')
            self.isBaked = True
        
        # 保存文件
        f = file(self.filepath, 'w')
        f.write(str(self))
        f.close()
        
    def write(self, contents, method='a'):
        if not self.isBaked:
            # 还没有bak过，需要先备份
            copy(self.filepath, self.filepath + '.ntsbak')
            self.isBaked = True
        
        # 保存文件
        f = file(self.filepath, str(method))
        f.write(contents)
        f.close()
        
    def read(self):
        f = file(self.filepath, 'r')
        cont = f.read()
        f.close()
        return cont
