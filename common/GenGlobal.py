# -*- coding: GB18030 -*-
'''
Created on Dec 29, 2010

@author: caiyifeng@baidu.com
'''

from lib.common import Generator

class GenGlobal(object):
    '''
    单例类，直接使用g_genGlobal对象
    '''
    
    def __init__(self):
        self.initGen()

    def initGen(self):
        "初始化Generator对象"
        self.reinitGen()
        
    def reinitGen(self):
        # reload中的rollback调用。除了eventidGen，其他都重置
        self.idGen = Generator.IdGen()
        self.id64Gen = Generator.Id64Gen()
        self.eventidGen = Generator.EventidGen()
        self.cateidGen = Generator.CateidGen()
        self.playerGen = Generator.PlayerGen()
        self.plsaidGen = Generator.PlsaidGen()
        self.tradeidGen = Generator.TradeidGen()
        self.uitidGen = Generator.UitidGen()

        self.queryGen = Generator.QueryGen()
        self.cnGen = Generator.CnGen()
        self.tuGen = Generator.TuGen()
        self.urlGen = Generator.UrlGen()
        self.ipGen = Generator.IpGen()
        self.cookieGen = Generator.CookieGen()
        self.adclassidGen = Generator.AdclassidGen()

        self.dimGen = Generator.WidthHeightGen()
        self.weightGen = Generator.WeightGen()
        self.sidGen = Generator.SidGen()
        self.itidGen = Generator.ItidGen()
        self.sfsidGen = Generator.SfsidGen()
        self.signGen = Generator.SignGen()
        self.stepGen = Generator.StepGen()
                
    def genId(self):
        return self.idGen.gen()

    def genId64(self):
        return self.id64Gen.gen()

    def genUitId(self):
        return self.uitidGen.gen()
    
    def genIdList(self, repeat):
        return self.idGen.genList(repeat)
    
    def genEventid(self):
        return self.eventidGen.gen()
    
    def genCateid(self,min = None, max = None):
        return self.cateidGen.gen(min, max)
    
    def genPlayer(self):
        return self.playerGen.gen()
    
    def genPlsaid(self, min = None, max = None):
        return self.plsaidGen.gen(min, max)
    
    def genFcate(self):
        return self.tradeidGen.genFir()
    
    def genScate(self, fcate):
        return self.tradeidGen.genSec(fcate)
    
    def genSadclassid(self):
        return self.adclassidGen.genSec()

    def genTadclassid(self):
        return self.adclassidGen.genThr()
    
    def genQuery(self):
        return self.queryGen.gen()
    
    def genCn(self):
        return self.cnGen.gen()
    
    def genTu(self):
        return self.tuGen.gen()
    
    def genUrl(self):
        return self.urlGen.gen()

    def genSecondUrl(self):
        return self.urlGen.gen_sec()

    def genThirdUrl(self):
        return self.urlGen.gen_thr()
    
    def genIp(self, bit = 4):
        return self.ipGen.gen(bit)
    
    def genCookie(self):
        return self.cookieGen.gen()

    def genIntentid(self):
        return self.intentidGen.gen()
    
    def genDim(self, type = "qianru"): 
        return self.dimGen.gen(type)
    def reinitIntentid(self):
        self.intentidGen = Generator.IntentidGen()
        
    def genEntityid(self):
        return self.entityidGen.gen()
    
    def reinitEntityid(self):
        self.entityidGen = Generator.EntityidGen()

    def genPort(self,min=61000,max=65000):
        return self.portGen.gen(min,max)

    def genWeight(self):
        return self.weightGen.gen()
    
    def genSid(self):
        return self.sidGen.gen()
    def genItid(self):
        return self.itidGen.gen()

    def genSfsid(self):
        return self.sfsidGen.gen()
    
    def genSign(self, sign_prefix=1234, num = 1):
        if num == 1:
            return self.signGen.gen(sign_prefix)
        
        return self.signGen.genList(sign_prefix, num)
    def genStep(self,header):
        return self.stepGen.genStep(header)

g_genGlobal = GenGlobal()
