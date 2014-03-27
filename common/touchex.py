# -*- coding: GB18030 -*-
'''
Created on Sep 9, 2011

@author: caiyifeng<caiyifeng@baidu.com>

@summary: touch增强版
'''

import os
import time

from common.utils import Shell_System 


def touchex(filepath, *compare_files):
    '''
    @summary: 自适应touch
    @note: 1. 比filepath新
     - 2. 比所有的compare_files新
     - 3. >= 当前时间
    '''
    sh_sys = Shell_System()
    if not os.path.exists(filepath):
        # 文件不存在，需要生成
        # 使用tempfile过渡，避免目标文件被两次更改时间戳（touch + touchex）
        tempfile = filepath + ".dtstemp"
        sh_sys.shell("touch "+tempfile)
        _updatetime(tempfile, *compare_files)
        
        # 将tempfile mv到目标文件
        sh_sys.shell("mv %s %s" % (tempfile, filepath))
    else:
        # 文件/目录 存在，直接更新时间戳
        _updatetime(filepath, *compare_files)
        
    
def _updatetime(filepath, *compare_files):
    '''
    @summary: 更新filepath的时间戳
    @note: 1. 比filepath新
     - 2. 比所有的compare_files新
     - 3. >= 当前时间
    '''
    # 记录所有时间戳
    times = []
    
    # 记录filepath时间戳
    st = os.stat(filepath)
    times.extend([st.st_atime, st.st_mtime, st.st_ctime])
    
    # 记录所有compare_files的时间戳
    for f in compare_files:
        if os.path.exists(f):
            st = os.stat(f)
            times.extend([st.st_atime, st.st_mtime, st.st_ctime])
            
    # 更新时间戳
    max_time = max(times) + 1                   # 比filepath和所有的compare_files都新
    max_time = max(max_time, time.time())       # >=当前时间
    os.utime(filepath, (max_time, max_time))

