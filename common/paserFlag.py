#!/bin/python 

class OverflowExecption(Exception):
    def __init__(self,key):
        Exception.__init__(self,key)
        self.field = key

class Flag:
    def __init__(self,language=0,strategy_flag=0,req_type=0,xml=0,prev_flag=0,mid_flag=0,reserved=0):
        
        self.flag = 0

        self.language = language
        self.strategy_flag = strategy_flag
        self.req_type = req_type
        self.xml = xml
        self.prev_flag = prev_flag
        self.mid_flag = mid_flag
        self.reserved = reserved

    def get_language(self,flag):
        self.language = (flag & 0x0000000F)
        return self.language 

    def set_language(self):
        if self.language >= (1<<5) or self.language < 0:
            raise OverflowExecption("language")
        self.flag |= self.language
    
    def get_strategy_flag(self,flag):
        self.strategy_flag = (flag & 0x00000070) >> 4
        return self.strategy_flag

    def set_strategy_flag(self):
        if self.strategy_flag >= (1<<4) or self.strategy_flag < 0:
            raise OverflowExecption("strategy_flag")
        self.flag |= self.strategy_flag << 4
    
    def get_req_type(self,flag): 
        self.req_type = (flag & 0x00000180) >> 7
        return self.req_type

    def set_req_type(self):
        if self.req_type >= (1 << 3) or self.req_type < 0:
            raise OverflowExecption("req_type")
        self.flag |= self.req_type << 7

    def get_xml(self,flag):
        self.xml = (flag & 0x00000200) >> 9
        return self.xml

    def set_xml(self):
        if self.xml >= (1 << 2) or self.xml < 0:
            raise OverflowExecption("xml")
        self.flag |= self.xml << 9

    def get_prev_flag(self,flag): 
        self.prev_flag = (flag & 0x00000400) >> 10
        return self.prev_flag

    def set_prev_flag(self):
        if self.prev_flag >= (1 << 2) or self.prev_flag < 0:
            raise OverflowExecption("prev_flag")
        self.flag |= self.prev_flag << 10
    
    def get_mid_flag(self,flag): 
        self.mid_flag = (flag & 0x00001800) >> 11
        return self.prev_flag

    def set_mid_flag(self):
        if self.mid_flag >= (1 << 3) or self.mid_flag < 0:
            raise OverflowExecption("mid_flag")
        self.flag |= self.mid_flag << 11

    def get_reserved(self,flag):
        self.reserved = (flag & 0xFFFF8000) >> 13
        return self.reserved 

    def set_reserved(self):
        if self.reserved >= (1 << 20) or self.reserved < 0:
            raise OverflowExecption("reserved")
        self.flag |= self.reserved << 13

    def get_content(self,flag):
        self.get_language(flag)
        self.get_strategy_flag(flag)
        self.get_req_type(flag)
        self.get_xml(flag)
        self.get_prev_flag(flag)
        self.get_mid_flag(flag)
        self.get_reserved(flag)
        content = "flag: %d\tlanguage: %d\tstrategy_flag: %d\treq_type: %d\txml: %d\tprev_flag: %d\tmid_flag: %d\treserved: %d\n"%(flag,self.language,self.strategy_flag,self.req_type,self.xml ,self.prev_flag,self.mid_flag,self.reserved)
        print content

    def get_flag(self):
        try:
            self.set_language()
            self.set_strategy_flag()
            self.set_req_type()
            self.set_xml()
            self.set_prev_flag()
            self.set_mid_flag()
            self.set_reserved()  
        except OverflowExecption,e:
            print e.field + " Overflow"
            return
        print "flag: " + str(self.flag) + "\n"

def str2dict(str):
    res = {}
    for index,kv in enumerate(str.split(',')):
        k = kv.split('=')[0].strip()
        v = kv.split('=')[1].strip()
        res[k] = int(v)
    return res


if __name__ == '__main__':
    method = raw_input("Input the method,0 means: parse flag; 1 means: get flag!\n");
    if method == "0":
        Flag1 = Flag()
        while True:
            flag = raw_input("Input the flag you want to parse!\n")
            Flag1.get_content(int(flag))
    else:
        while True:
            content = raw_input("Input the content as: language=0,strategy_flag=0,req_type=1,xml=0,prev_flag=0,mid_flag=0,reserved=0\n")
            content_dict = str2dict(content)
            Flag1 = Flag(**content_dict)
            Flag1.get_flag()

