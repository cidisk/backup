# -*- coding: GB18030 -*-
'''
Created on Sep 9, 2011

@author: caiyifeng<caiyifeng@baidu.com>

@summary: touch��ǿ��
'''

import os
import time

from common.utils import Shell_System 


def touchex(filepath, *compare_files):
    '''
    @summary: ����Ӧtouch
    @note: 1. ��filepath��
     - 2. �����е�compare_files��
     - 3. >= ��ǰʱ��
    '''
    sh_sys = Shell_System()
    if not os.path.exists(filepath):
        # �ļ������ڣ���Ҫ����
        # ʹ��tempfile���ɣ�����Ŀ���ļ������θ���ʱ�����touch + touchex��
        tempfile = filepath + ".dtstemp"
        sh_sys.shell("touch "+tempfile)
        _updatetime(tempfile, *compare_files)
        
        # ��tempfile mv��Ŀ���ļ�
        sh_sys.shell("mv %s %s" % (tempfile, filepath))
    else:
        # �ļ�/Ŀ¼ ���ڣ�ֱ�Ӹ���ʱ���
        _updatetime(filepath, *compare_files)
        
    
def _updatetime(filepath, *compare_files):
    '''
    @summary: ����filepath��ʱ���
    @note: 1. ��filepath��
     - 2. �����е�compare_files��
     - 3. >= ��ǰʱ��
    '''
    # ��¼����ʱ���
    times = []
    
    # ��¼filepathʱ���
    st = os.stat(filepath)
    times.extend([st.st_atime, st.st_mtime, st.st_ctime])
    
    # ��¼����compare_files��ʱ���
    for f in compare_files:
        if os.path.exists(f):
            st = os.stat(f)
            times.extend([st.st_atime, st.st_mtime, st.st_ctime])
            
    # ����ʱ���
    max_time = max(times) + 1                   # ��filepath�����е�compare_files����
    max_time = max(max_time, time.time())       # >=��ǰʱ��
    os.utime(filepath, (max_time, max_time))

