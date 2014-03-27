# coding: gb18030
'''
Created on Oct 13, 2010

@author: caiyifeng@baidu.com
bs���file�༭��lib
'''

from shutil import copy, move
from os import path
from common.loger import loger

g_AD_TYPES = ('bd', 'fc')

class RemoteFileBasic():
    '''�༭bs�����ļ��Ļ���
    
    caiyifeng@baidu.com'''
    
    def __init__(self,  filepath):
        '''��ʼ��
        
        filepath: �ļ�·��, �ַ�������'''
        self.filepath = filepath
        self.recs = []  # �ļ���¼��list
        self.isBaked = False   # ��ûbak��
        
    def bak_or_revert(self):
        "���û��bak�ļ����ͱ��ݣ������bak�ļ�������bak�ļ��ָ�ԭ�ļ�"
        bak_path = self.filepath + ".ntsbak"
        
        if path.isfile(bak_path):
            # �Ѿ��б����ļ��ˣ��ָ�ԭ�ļ�
            loger.debug("Revert %s", bak_path)
            copy(bak_path, self.filepath)
        else:
            # ��û�б����ļ�������֮
            loger.debug("Bak %s", self.filepath)
            copy(self.filepath, bak_path)
            
        # ����Ѿ����ݹ���
        self.isBaked = True
        
    def revert(self):
        '�ָ����޸ĵ��ļ�'
        if self.isBaked:
            # �Ѿ����ݹ��ˣ���Ҫ�ָ��ļ�
            move(self.filepath, self.filepath + '.ntsrun')  # ���汾�����е��ļ�
            move(self.filepath + '.ntsbak', self.filepath)  # �ָ������ļ�
            self.isBaked = False
        
    def addRec(self, *fields):
        '''���ļ�������һ����¼
        
        fileds�������ֶε�tuple��ÿ���ֶζ����ַ�������'''
        self.addRecImp(fields)
        
    def addRecImp(self, fields):
        '''���ļ�������һ����¼��addRec�����ľ���ʵ��
        
        fields: �����ֶε�tuple, list or tuple����, ÿ���ֶζ����ַ�������'''
        arec = fields[:]
        self.recs.append(arec)
        
    def setDelim(self):
        '''���ü�¼�У������ֶεķָ���Ϊ\t'''
        self.delim = '\t'
        
    def __str__(self):
        '''��self.recs��ӡΪ�ַ���'''
        self.setDelim()
        
        strLines = []
        for arec in self.recs:
            strLine = self.delim.join(arec)
            strLines.append(strLine)
        return '\n'.join(strLines) + '\n'
    
    def dump(self):
        '''���浽�ļ�, ��һ�α���ǰ���ȱ���'''
        if not self.isBaked:
            # ��û��bak������Ҫ�ȱ���
            copy(self.filepath, self.filepath + '.ntsbak')
            self.isBaked = True
        
        # �����ļ�
        f = file(self.filepath, 'w')
        f.write(str(self))
        f.close()
        
    def write(self, contents, method='a'):
        if not self.isBaked:
            # ��û��bak������Ҫ�ȱ���
            copy(self.filepath, self.filepath + '.ntsbak')
            self.isBaked = True
        
        # �����ļ�
        f = file(self.filepath, str(method))
        f.write(contents)
        f.close()
        
    def read(self):
        f = file(self.filepath, 'r')
        cont = f.read()
        f.close()
        return cont
