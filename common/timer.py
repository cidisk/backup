# -*- coding: GB18030 -*-
'''
Created on Feb 22, 2011

@author: caiyifeng@baidu.com
'''

import time

class Timer(object):
    '''
    @note: �ֽ׶λ��ܼ�ʱ����
    @note: ʹ�÷����� (start -> ... -> end) -> ... -> (start -> ... -> end)
    @note: totaltime��¼����start/end��֮���ʱ���ܺ�
    '''

    def __init__(self):
        self.totaltime = 0.0      # ����ʱ������������λ��
        self._starttime = 0.0     # ��һ�ο�ʼ��ʱ��ʱ�䣬����������λ��
        
    def start(self):
        "@note: ��ʼ��ʱ"
        self._starttime = time.time()
    
    def end(self):
        '''
        @note: ������ʱ������������ʱ
        '''
        endtime = time.time()
        interval = endtime - self._starttime
        self.totaltime += interval
    
    
class Timer2(object):
    '''
    @note: ���׶μ�ʱ����
    @note: ʹ�÷����� (init)start -> ... -> end -> ... -> end
    @note: ����start�����һ��end֮���ʱ��
    '''
    
    def __init__(self):
        self._starttime = 0.0       # start��ʼ��ʱ��ʱ�䣬����������λ��
        
        self.start()    # Ĭ�ϳ�ʼ��ʱ���Ϳ�ʼ��ʱ
        
    def start(self):
        "@note: ��ʼ��ʱ"
        self._starttime = time.time()
        
    def end(self):
        '''
        @note: ������ʱ
        @return: ��start��ʱ����
        '''
        endtime = time.time()
        interval = endtime - self._starttime
        return interval
    
    
def test_timer():
    print "test_timer"
    t = Timer()
    
    t.start()
    time.sleep(1)
    t.end()
    
    t.start()
    time.sleep(2)
    t.end()
    
    print t.totaltime

def test_timer2():
    print "test_timer2"
    t = Timer2()
    
    time.sleep(1)
    print t.end()
    
    time.sleep(2)
    print t.end()

if __name__ == "__main__":
    test_timer()
    print
    test_timer2()

