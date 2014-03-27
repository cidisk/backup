# -*- coding: GB18030 -*-
'''
Created on Feb 22, 2011

@author: caiyifeng@baidu.com
'''

import time

class Timer(object):
    '''
    @note: 分阶段汇总计时器类
    @note: 使用方法： (start -> ... -> end) -> ... -> (start -> ... -> end)
    @note: totaltime记录所有start/end对之间的时间总和
    '''

    def __init__(self):
        self.totaltime = 0.0      # 总用时，浮点数，单位秒
        self._starttime = 0.0     # 上一次开始计时的时间，浮点数，单位秒
        
    def start(self):
        "@note: 开始计时"
        self._starttime = time.time()
    
    def end(self):
        '''
        @note: 结束计时，并增加总用时
        '''
        endtime = time.time()
        interval = endtime - self._starttime
        self.totaltime += interval
    
    
class Timer2(object):
    '''
    @note: 单阶段计时器类
    @note: 使用方法： (init)start -> ... -> end -> ... -> end
    @note: 返回start到最后一个end之间的时间
    '''
    
    def __init__(self):
        self._starttime = 0.0       # start开始计时的时间，浮点数，单位秒
        
        self.start()    # 默认初始化时，就开始计时
        
    def start(self):
        "@note: 开始计时"
        self._starttime = time.time()
        
    def end(self):
        '''
        @note: 结束计时
        @return: 到start的时间间隔
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

