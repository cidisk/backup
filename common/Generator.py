# -*- coding: GB18030 -*-
'''
Created on Dec 21, 2010

@author: caiyifeng@baidu.com
'''

import sys
import os
import random

class Generator(object):
    pass

class IdGen(Generator):
    def __init__(self):
        self.id = 1000      # ���Ҫ�õ�id
    
    def gen(self):
        if self.id >= sys.maxint:
            raise StopIteration, 'IdGen Stops Iteration'
        
        ret = self.id
        self.id += 1
        return ret
    
    def genList(self, repeat):
        return [self.gen() for i in range(repeat)]

class Id64Gen(Generator):
    def __init__(self):
        self.id = 1152921504606846976 # ���Ҫ�õ�id

    def gen(self):
        if self.id >= sys.maxint:
            raise StopIteration, 'IdGen Stops Iteration'
        
        ret = self.id
        self.id += 1
        return ret
    
    def genList(self, repeat):
        return [self.gen() for i in range(repeat)]
        
class ItidGen(Generator):
    def __init__(self):
        self.id = 201 # ���Ҫ�õ�id
    
    def gen(self):
        if self.id >= 1024:
            raise StopIteration, 'IdGen Stops Iteration'
        
        ret = self.id
        self.id += 1
        return ret

#add by hubinfeng
class UitidGen(Generator):
    def __init__(self):
        self.id = 1 #��1��ʼgen

    def gen(self):
        if self.id >= 101: #Ĭ��bs���Խ��ܵ����ֵ
            raise StopIteration, 'IdGen Stops Iteration'

        ret = self.id
        self.id += 1
        return ret
 
class SfsidGen(Generator):
    def __init__(self):
        self.id = 1000001

    def gen(self):
        ret = self.id
        self.id += 1
        return ret

class EventidGen(Generator):
    def __init__(self):
        self.id = 0     # �Ѿ��ù���id
        
    def gen(self):
        if self.id >= sys.maxint:
            # �Ѿ��õ�maxint�ˣ��׳��쳣
            raise StopIteration, "EventidGen Stops Iteration"
        
        self.id += 1
        return self.id
        
class CateidGen(Generator):
    def __init__(self):
        self._id =10
        self._idmax = 10000
        self._usedIds = set()
        
    def gen(self, min = None, max = None):
        '''
        1. gen(): ����0-100�е�һ��û���ù���id
        2. gen(val)������val�����val֮ǰ���ù��ˣ��׳��쳣
        3. gen(min, max)������[min, max-1]�е�һ��û���ù���id
        '''
        # ����min��max
        if min is None and max is None:
            # ��1����ʽ
            min = self._id
            max = self._idmax
            isFirst = True   # �ǵ�1����ʽ
        elif min is not None:
            if max is None:
                # ��2����ʽ
                max = min + 1
            else:
                # ��3����ʽ
                pass
            isFirst = False
        else:
            # ����ȷ�ĵ��÷�ʽ
            raise Exception, "Invalid Invoking of CateidGen.gen()"
            
        # �ҵ�ָ����Χ�ڣ���һ��û�б�ʹ�õ�id
        for i in range(min, max):
            if i not in self._usedIds:
                # ��ǰidû�б��ù�
                self._usedIds.add(i)
                break
        else:
            # ���е�id�����ù���
            raise StopIteration, "CateidGen Stops Iteration"
        
        # ��1����ʽ�ĵ��ã���Ҫ����self._id
        if isFirst:  
            self._id = i + 1
            
        return i        

class PlayerGen(Generator):
    def __init__(self):
        self.ver = 12
        
    def gen(self):
        if self.ver >= sys.maxint:
            raise StopIteration, 'PlayerGen Stops Iteration'
        
        ret= self.ver
        self.ver += 1
        return ret
    
    @staticmethod
    def getBDUnitDft():
        return 10
    
    getAsQueryDft = getBDUnitDft

class PlsaidGen(Generator):
    def __init__(self):
        self._id = 11000
        self._idmax = 19000
        self._usedIds = set()
        
    def gen(self, min = None, max = None):
        '''
        1. gen(): ����1w-2w�е�һ��û���ù���id
        2. gen(val)������val�����val֮ǰ���ù��ˣ��׳��쳣
        3. gen(min, max)������[min, max-1]�е�һ��û���ù���id
        '''
        # ����min��max
        if min is None and max is None:
            # ��1����ʽ
            min = self._id
            max = self._idmax
            isFirst = True   # �ǵ�1����ʽ
        elif min is not None:
            if max is None:
                # ��2����ʽ
                max = min + 1
            else:
                # ��3����ʽ
                pass
            isFirst = False
        else:
            # ����ȷ�ĵ��÷�ʽ
            raise Exception, "Invalid Invoking of PlsaidGen.gen()"
            
        # �ҵ�ָ����Χ�ڣ���һ��û�б�ʹ�õ�id
        for i in range(min, max):
            if i not in self._usedIds:
                # ��ǰidû�б��ù�
                self._usedIds.add(i)
                break
        else:
            # ���е�id�����ù���
            raise StopIteration, "PlsaidGen Stops Iteration"
        
        # ��1����ʽ�ĵ��ã���Ҫ����self._id
        if isFirst:  
            self._id = i + 1
            
        return i        

class TradeidGen(Generator):
    "��ҵ���Generator"
    def __init__(self):
        self.id = 5
        self.iddict = {}
        
    def genFir(self):
        "����һ����ҵ���"
        if self.id >= 100:
            raise StopIteration, "Tradeid genFirst stops iteration"
        
        ret = self.id
        self.id += 1
        return ret
    
    def genSec(self, fCate):
        "����һ����ҵid�����ɶ�����ҵ���"
        if fCate not in self.iddict:
            # fcate��û�����ɹ�������ҵ������ʼֵ
            self.iddict[fCate] = fCate * 100 + 1
            
        if self.iddict[fCate] >= (fCate + 1) * 100:
            raise StopIteration, "Tradeid genSec stops iteration"
        
        ret = self.iddict[fCate]
        self.iddict[fCate] += 1
        return ret
class AdclassidGen(Generator):
    "adclassid Generator"
    def __init__(self):
        self.id = 101
        self.iddict = {}
        self.new_id = 9999
        
    def genSec(self):
        "���ɶ������"
        if self.id >= 524200:
            raise StopIteration, "adclassid genSecond stops iteration"
        
        ret = self.id
        self.id += 1
        return ret

    def genThr(self):
        if self.new_id <= 100:
            raise StopIteration, "adclassid genThird stops iteration"
        ret = self.new_id * 100 
        self.new_id -=1
        return ret
    
    def genFir(self, sadclassid):
        "���ݶ�����ҵid������һ����ҵ���"
        if sadclassid not in self.iddict:
            # fcate��û�����ɹ�������ҵ������ʼֵ
            self.iddict[sadclassid] = sadclassid / 100 + 1
            
        if self.iddict[sadclassid] >= (sadclassid + 1) / 100:
            raise StopIteration, "Tradeid genSec stops iteration"
        
        ret = self.iddict[sadclassid]
        self.iddict[sadclassid] += 1
        return ret

# QueryGen�е�query�б�
_queryList = []

def _initQueryList():
    # ��query_list.txt�ж�ȡquery�б�
    global _queryList
    
    # �õ�query_list.txt�ľ���·��
    # ͨ����ǰ�ļ�·����query_list.txt����ڵ�ǰ�ļ���·��������õ� 
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "./query_list.txt")

    # ��ȡ�ļ���ÿһ�У�����queryList
    queryListFile = open(filepath, 'r')
    for aquery in queryListFile:
        aquery = aquery.rstrip()
        if aquery:
            _queryList.append(aquery)
    queryListFile.close()
    
# ִ��query�б�ĳ�ʼ��
_initQueryList()

class QueryGen(Generator):
    def __init__(self):
        self.index = 0
        self.nonsense = self.gen()
        
    def gen(self):
        global _queryList
        
        if self.index >= len(_queryList):
            raise StopIteration, 'QueryGen Stops Iteration'
        
        ret = _queryList[self.index]
        self.index += 1
        return ret
        
class CnGen(Generator):
    def __init__(self):
        self.index = 1000
        
    def gen(self):
        if self.index >= sys.maxint:
            raise StopIteration, 'CnGen Stops Iteration'
        
        ret = 'nts_test_%s_cpr' % self.index
        self.index += 1
        return ret
    
    @staticmethod
    def getAsQueryCnDft():
        return "rd_test_15_cpr"

class TuGen(Generator):
    def __init__(self):
        self.index = 1000
    def gen(self):
        if self.index >= 99999:
            raise StopIteration, 'TuGen Stops Iteration'
        
        self.index += 1
        return self.index
    
    @staticmethod
    def getAsQueryTuDft():
        return "rd_test_15_cpr"

     
class UrlStruct(object):
    "url�ṹ������url, site, domain��������"
    def __init__(self, domain):
        self.domain = domain
        
    def getDomain(self):
        return self.domain

    def getSite(self):
        return "www." + self.domain
    
    site = property(getSite)

    def getFirstpath(self):
        return self.site + "/ntspath/"
    
    firstpath = property(getFirstpath)
    
    def getUrl(self):
        return "http://" + self.firstpath + "ntsurl.html"
    
    def get_SecUrl(self):
        tmp_path = self.firstpath.strip('www.')
        return "http://" + tmp_path + "ntsurl.html"
    
    url = property(getUrl)
    
class UrlGen(Generator):
    def __init__(self):
        self.index = 1000
        
    def gen(self):
        if self.index >= sys.maxint:
            raise StopIteration, 'UrlGen Stops Iteration'
        
        ret = UrlStruct("nts-%s.com" % self.index)
        self.index += 1
        return ret

    def gen_sec(self):
        if self.index >= sys.maxint:
            raise StopIteration, 'UrlGen Stops Iteration'
        
        ret = UrlStruct("second.nts-%s.com" % self.index)
        self.index += 1
        return ret

    def gen_thr(self):
        if self.index >= sys.maxint:
            raise StopIteration, 'UrlGen Stops Iteration'

        ret = UrlStruct("third.second.nts-%s.com" % self.index)
        self.index += 1
        return ret
    
    @staticmethod
    def getBDUnitShowurlDft():
        return UrlStruct("nts-bdunit-showurl.com").url
    
    @staticmethod
    def getBDUnitTargeturlDft():
        return UrlStruct("nts-bdunit-targeturl.com").url
    
    @staticmethod
    def getAsQueryUrlDft():
        return UrlStruct("nts-asquery-url.com").url
    
    @staticmethod
    def getCtrReduceModelSiteDft():
        return UrlStruct("nts-ctr-reduce-model-url.com").site

    @staticmethod
    def getCtrBsQtModelSiteDft():
        return UrlStruct("nts-ctr-bs-qt-model-url.com").site

    @staticmethod
    def getCtrBsPtModelSiteDft():
        return UrlStruct("nts-ctr-bs-pt-model-url.com").site
        
class IpGen(Generator):
    # ip��ΧΪ[1.1.1.10] ~ [254.254.254.254]
    # ÿһλ��Ҫ�ܿ�0��255����ֹ����bs�������߼�
    def __init__(self):
        self.ip = [1, 1, 1, 10]     # ��һ���ù���ip
        
    def ipInc(self, bit):
        '''
        ��bitλ����1��bitλ�����λ��������Ϊ254
        ���������������׳�StopIteration
        '''
        for i in range(bit - 1, -1, -1):
            # �ӵ�ǰλ��ʼ����
            if self.ip[i] < 254:
                # ��ǰλС��254�����Ӻ�����ѭ��
                self.ip[i] += 1
                break
            else:
                # ��ǰλ�Ѿ�Ϊ254�ˣ�������Ϊ1������������ǰһλ
                self.ip[i] = 1
        else:
            # ѭ��Խ�磬��ʾ�޷���������
            raise StopIteration, "IpGen stops iteration"
        
        # ��bit�����λ��������Ϊ254
        for i in range(bit, 4):
            self.ip[i] = 254
    
    def gen(self, bit):
        '''
        ���ض�ռ��ip/ipƬ�Ρ�bit��ʾ�ڵڼ�λ�϶�ռ��ȡֵΪ1-4
        ������˵������gen(3)������һ��3λ��ipƬ�� 'a.b.c'����ʾ��ռ'a.b.c.*'
        '''
        if not 1 <= bit <=4:
            raise Exception, "bit should be 1~4 in IpGen.gen()"
        
        self.ipInc(bit)
        return ".".join([str(i) for i in self.ip[0:bit]])
    
    @staticmethod
    def getAsQueryIpDft():
        return "1.1.1.1"

class CookieGen(Generator):
    # Cookie����ʽΪ32���ַ���ÿ���ַ���16�������֣�Ӣ����ĸ��д
    # ���صķ�ΧΪ'1' + '0' * 31 ~ 'F' * 32
    def __init__(self):
        self.cookie = '1' + '0' * 31
        
    def gen(self):
        if self.cookie == 'F' * 32:
            raise StopIteration, "CookieGen stops iteration"
        
        ret = self.cookie
        self.cookieInc()
        return ret
    
    def cookieInc(self):
        cl = long(self.cookie, 16)
        cl += 1
        self.cookie = "%X" % cl

class SidGen(Generator):
    def __init__(self):
        self.sid = 10000000000

    def gen(self):
        if self.sid >= 2**64:
            raise StopIteration, "Sid stops iteration"

        ret = '%016x' % self.sid
        self.sid += 10
        return ret
    
class WidthHeightGen(Generator):
    def __init__(self):
        self.qianru_pos = 0
        self.xuanfu_pos = 0
        self.tiepian_pos = 0
        
        self.qianru_dict = [(200,    200), \
                            (250,    250),\
                            (300,    250),\
                            (336,    280),\
                            (360,    300),\
                            (460,    60),\
                            (468,    60),\
                            (580,    90),\
                            (640,    60),\
                            (728,    90),\
                            (760,    60),\
                            (760,    75),\
                            (760,    90),\
                            (960,    60),\
                            (960,    90),\
                            (1024,   60),\
                            (120,    600),\
                            (160,    600)]
        self.xuanfu_dict = [(120,    270),\
                            (100,    100),\
                            (120,    120),\
                            (250,    200),\
                            (300,    250)]
        self.tiepian_dict = [(400, 300)]

    def gen(self, type):
        if type.lower() == "qianru":
            if self.qianru_pos == len(self.qianru_dict):
                self.qianru_pos = 0
            self.qianru_pos = self.qianru_pos + 1
            return self.qianru_dict[self.qianru_pos - 1]
        elif type.lower() == "xuanfu":
            if self.xuanfu_pos == len(self.xuanfu_dict):
                self.xuanfu_pos = 0
            self.xuanfu_pos = self.xuanfu_pos + 1
            return self.xuanfu_dict[self.xuanfu_pos - 1]
        elif type.lower() == "tiepian":
            if self.tiepian_pos == len(self.tiepian_dict):
                self.tiepian_pos = 0
            self.tiepian_pos = self.tiepian_pos + 1
            return self.tiepian_dict[self.tiepian_pos - 1]
        else:
            raise Exception("type must be one of qianru, xuanfu, tiepian")

class WeightGen(Generator):
    '''
    ����һmodel�õ�weight
    '''
    def __init__(self):
        self.weight  = 0.01

    def gen(self):
        if self.weight > 0.1 or self.weight < -0.1:
            self.weight = 0.01
            
        if random.random() > 0.5:
            self.weight = -(self.weight + 0.0137)
        else:
            self.weight = -(self.weight - 0.0124)

        return self.weight
            
class SignGen(Generator):
    '''
    ����64λǩ��
    '''
    def __init__(self):
        self.cnt = 0

    def gen(self, sign_prefix=1234):
        self.cnt += 1
        return self.cnt|(sign_prefix<<48)
    
    def genList(self, sign_prefix=1234, num=1):
        return [self.gen(sign_prefix) for i in range(num)]
class StepGen(Generator):
    """
    �����㼶id����
    """
    def __init__(self):
        self.step={}
    def genStep(self,header):
        if not self.step.has_key(header):
            self.step[header] = {}
            self.step[header][id] = 1
        else:
            self.step[header][id] +=1
        return self.step[header][id]


if __name__ == "__main__":
    port_gen = PortGen()
    port_gen2 = PortGen()
    for i in range(10):
        print port_gen.gen()
    for i in range(10):
        print port_gen2.gen()
    for i in range(10):
        print port_gen.gen()
            
    sign_gen = SignGen()
    print sign_gen.gen()
    print sign_gen.gen(61234)
    #weight_gen = WeightGen()
    #for i in range(100):
    #    print weight_gen.gen()
