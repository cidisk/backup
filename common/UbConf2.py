import re,json

class UbConfigParser():
    def __init__(self, path, seg=':'):
        self.seg = seg
        self.wrlines = []
        self.content = {}
        self.lines = []
        self.linedict = {}
        self.path = path
        self.setinfo = {}

    def set_seg(self, seg):
        self.seg=seg
        
    def read_conf(self):
        f = file(self.path)
        self.lines = f.read().splitlines()
        f.close()
        self.linedict['selflinenum'] = -1
        self.linedict['endlinenum']  = len(self.lines) -1
        self.read_unit(self.content, 0, self.lines, self.linedict, 0)

    def dumpconf(self):
         fd = open(self.path, 'w')
         for line in self.lines:
             fd.write(line+"\n")
         fd.close()
    
    def one_dump_info(self, clstype, fun, setdict):
         resdict = {}
         generator_case_info={}
         generator_case_info['node']=''
         generator_case_info['type']=clstype
         generator_case_info['set_fun']=fun
         generator_case_info['serialized']=False
         generator_case_info["dump_fun"] = ''
         resdict['generator_case_value'] = setdict
         resdict['generator_case_info']  = generator_case_info
         return resdict

    def dump_conf_set_info(self, dumpfpath, dumpclsname=-1):
        if dumpclsname==-1:
            clsname =  self.__class__.__name__
        else:
            clsname = dumpclsname
        dumpfd=open(dumpfpath, 'a')
        if self.setinfo.has_key('set'):
            setresdict = self.one_dump_info(clsname, 'set', self.setinfo['set'])
            dumpfd.write(json.dumps(setresdict,encoding='gb18030')+"\n")
        if self.setinfo.has_key('delete'):
            delresdict = self.one_dump_info(clsname, 'delete', self.setinfo['delete'])
            dumpfd.write(json.dumps(delresdict, encoding='gb18030')+"\n")
        dumpfd.close()
        
         
    def read_unit(self, root, level, lines, linedict, startnum):
        idx = 0
        total = len(lines)

        write_idx = idx+startnum     
        while idx < total:
            line = lines[idx].replace(' ', '').replace('\t', '')
            if len(line) == 0 or line[0] == '#':
                idx = idx + 1
                write_idx  += 1
                continue
            if len(line) < 3:
                raise Exception("Format error[%s]!" % line)
            repattern = '(.*?)' + self.seg + '(.*)'
            if line[0] != '[':
                if line[0] != '@':
                    m=re.search(repattern,line)
                    root[m.group(1)] = m.group(2)
                    linedict[m.group(1)] = write_idx
                else:
                    line = line[1:]
                    m=re.search(repattern, line)
                    if root.has_key(m.group(1)):
                        root[m.group(1)].append(m.group(2))
                        linedict[m.group(1)].append(write_idx)
                    else:
                        root[m.group(1)] = [m.group(2)]
                        linedict[m.group(1)] = [write_idx]
                idx = idx + 1
                write_idx += 1 
                continue

            inner_level = line.count('.')
            if inner_level != level:
                raise Exception("Format error[%s]!" % line)

            k = line[1:-1].replace('.', '')
            idx = idx + 1
            write_idx += 1
            start = idx
            while idx < total and (lines[idx] == "" or lines[idx][0] != '[' or lines[idx].count('.') != level):
                idx = idx + 1
                write_idx += 1
            end = idx
            u_start = start + startnum 
            if k[0] != '@':
                v = dict()
                root[k] = v
                idxv= dict()
                linedict[k] = idxv
                linedict[k]['selflinenum'] = u_start-1
                linedict[k]['endlinenum'] = end + startnum -1
                self.read_unit(v, level + 1, lines[start:end], idxv, u_start)
            else:
                k = k[1:]
                v = dict()
                idxv= dict()
                if root.has_key(k):
                    root[k].append(v)
                    linedict[k].append(idxv)
                    linedict[k][-1]['selflinenum']=u_start-1
                    linedict[k][-1]['endlinenum'] = end + startnum -1
                else:
                    root[k] = [v]
                    linedict[k] = [idxv]
                    linedict[k][-1]['selflinenum']=u_start-1
                    linedict[k][-1]['endlinenum'] = end + startnum -1
                self.read_unit(v, level + 1, lines[start:end], idxv, u_start)

    def save(self,path=None):
        self.write_conf(self.content,0,1)
        try:
          if path==None:
             f=open(self.path, 'w')
             f.write("\n".join(self.wrlines))
             f.close()
          else:
             f=open(path, 'w')
             f.write("\n".join(self.wrlines))
             f.close()
        except:
          return 1
        return 0

    def write_conf(self,conf,level,flag,listkey=''):
        """
        flag=1/0..dict/list  level:the number of dot
        """
        if flag==1:
           for keys in conf.keys():
               if type(conf[keys]) is str:
                  self.wrlines.append(keys+self.seg+conf[keys])
           for keys in conf.keys():
               if type(conf[keys]) is dict:
                  self.wrlines.append('['+self.mkdot(level)+keys+']')
                  self.write_conf(conf[keys],level+1,1)
           for keys in conf.keys():
               if type(conf[keys]) is list:
                  self.write_conf(conf[keys],level,0,keys)
        else:
           for item in conf:
               if type(item) is dict:
                  self.wrlines.append('['+self.mkdot(level)+'@'+listkey+']')
                  self.write_conf(item,level+1,1)
               else: 
                  self.wrlines.append('@'+listkey+self.seg+item)                 

    def mkdot(self,num):
        dot=''
        while num>0:
              dot=dot+'.'
              num=num-1
        return dot

    def setvalue(self,dicpath,value):
        if self.content == {}:
           self.read_conf()
        keys=dicpath.split('/')
        self.set=0
        self.set_value(self.content,keys,value)
        return 1-self.set

    def set_value(self, conf, keys, value):
        if type(conf) is dict:
           if conf.has_key(keys[0]):
              if type(conf[keys[0]]) is str:
                 conf[keys[0]]=value
                 self.set=1
              else:
                 self.set_value(conf[keys[0]],keys[1:],value)
        if type(conf) is list:
           idx=0
           while idx < len(conf):
                 if type(conf[idx]) is dict:
                    self.set_value(conf[idx],keys,value)
                    idx=idx+1
                 elif type(conf[idx]) is str:
                      conf[idx]=value
                      self.set=1
                      idx=idx+1
                 else:
                     idx=idx+1

    def set(self, keys, value):
        if not self.setinfo.has_key('set'):
            self.setinfo['set']={}
        self.setinfo['set'][keys] = value
        self.read_conf()
        keyslist = keys.split('#')
        confdict = self.content
        linedict = self.linedict
        level = 0
        for i in range(len(keyslist)):
            key = keyslist[i]
            if key.find('@') != -1:
                keystr = key.split('@')[0]
                num = int(key.split('@')[1])
                if confdict.has_key(keystr):
                   confdict = confdict[keystr]
                   linedict = linedict[keystr]
                   if type(confdict) == type([]):
                       if len(confdict) < num+1:
                           if i < len(keyslist)-1:
                               for i in range(num+1 -len(confdict)):
                                   addline = "["  + "."*level + "@" + keystr + "]"
                                   self.addline(addline, linedict['endlinenum']+1)
                           else:
                                for i in range(num+1 -len(confdict)):
                                    addline = "@" + keystr + self.seg + value
                                    self.addline(addline, linedict['selflinenum']+1)
                       else:
                           confdict=confdict[num]
                           linedict = linedict[num]
                           if i == (len(keyslist)-1):
                               addline = "@" + keystr + self.seg + value
                               self.setline(addline, linedict)
                   else:
                       errorstr = "Add key type is error!"
                       raise AssertError,errorstr
                else:
                    if i < len(keyslist)-1:
                        addline = "["  + "."*level + "@" + keystr + "]"
                        for i in range(num):
                            self.addline(addline, linedict['endlinenum']+1)
                    else:
                        addline = "@" + keystr + self.seg + value
                        for i in range(num):
                            self.addline(addline, linedict['selflinenum']+1)
            else:
                keystr = key
                if confdict.has_key(keystr):
                   confdict = confdict[keystr]
                   linedict = linedict[keystr]
                   if i == (len(keyslist)-1):
                       addline =  keystr + self.seg + value
                       self.setline(addline, linedict)
                else:
                    if i == (len(keyslist)-1):
                        addline =  keystr + self.seg + value
                        self.addline(addline, linedict['selflinenum']+1)
                    else:
                        addline = "["  + "."*level  + keystr + "]"
                        self.addline(addline, linedict['endlinenum']+1)
            level +=1

    def addline(self, line, num):
        self.lines.append("")
        if num >= len(self.lines):
            errorstr = "set line error is error!"
            raise AssertError,errorstr
        self.lines.insert(num, line)  
        self.dumpconf()
        self.read_conf()
        
    def setline(self, line, num):  
        if num >= len(self.lines):
            errorstr = "set line error is error!"
            raise AssertError,errorstr
        self.lines[num] = line
        self.dumpconf()
        self.read_conf()

    def get(self, keys):
        keyslist = keys.split('#')
        confdict = self.content
        try:
            for i in range(len(keyslist)):
                key = keyslist[i]
                if key.find('@') != -1:
                    keystr = key.split('@')[0]
                    num = int(key.split('@')[1])
                    confdict = confdict[keystr][num]
                else:
                    keystr = key
                    confdict = confdict[keystr]
            return  confdict
        except:
            return None
        
    def delelte_conf(self, keys, tag=1):
        if tag != 1:
            return None
        self.delelte_conf(keys)
        
    def delete(self, keys):
        if not self.setinfo.has_key('delete'):
            self.setinfo['delete'] = {}
        self.setinfo['delete'][keys] = 1

        keyslist = keys.split('#')
        confdict = self.linedict
        deldict = None
        try:
             for i in range(len(keyslist)):
                key = keyslist[i]
                if key.find('@') != -1:
                    keystr = key.split('@')[0]
                    num = int(key.split('@')[1])
                    confdict = confdict[keystr][num]
                else:
                    keystr = key
                    confdict = confdict[keystr]
             deldict =  confdict
        except:
             deldict = None
        if deldict is not None:
            print "sd"*45
            if type(deldict) == type({}):
                startline = deldict['selflinenum']
                endline = deldict['endlinenum']
                del self.lines[startline:endline]
            else:
                del self.lines[int(deldict)]
        self.dumpconf()
        self.read_conf()

    def getvalue(self,dicpath):
        if self.content == {}:
           self.read_conf()
        keys=dicpath.split('/')
        self.get=0
        return self.get_value(self.content,keys) 

    def get_value(self,conf,keys):
        if type(conf) is dict:
           if conf.has_key(keys[0]):
              if type(conf[keys[0]]) is str:
                 self.get=1
                 return conf[keys[0]]
              else:
                 return self.get_value(conf[keys[0]],keys[1:])
        if type(conf) is list:
           idx=0
           reslist=[]
           while idx < len(conf):
                 if type(conf[idx]) is dict:
                    res=self.get_value(conf[idx],keys)
                    if res:
                       return res
                    idx=idx+1
                 elif type(conf[idx]) is str:
                      self.get=1
                      reslist.append(conf[idx])
                      idx=idx+1
                 else:
                     idx=idx+1 
           if reslist != []:
              return reslist

    def conf_replace(self,confdict,rp_str,rpd_str):
        if confdict.has_key(rp_str):
           confdict[rp_str]=rpd_str
        for item in confdict:
            if type(confdict[item]) is dict:               
               self.conf_replace(confdict[item],rp_str,rpd_str)

if __name__ == "__main__":
    #conf = UbConfigParser("/home/work/NTS_TASK/uap-str-hct/module_driver/conf/strategy/hct_user_extractor.conf")
    conf = UbConfigParser("/home/work/NTS_TASK/uap-str-hct/module_driver/conf/strategy/extract_behavior_framework.conf")
    #conf = UbConfigParser("/home/work/NTS_TASK/uap-str-hct/module_driver/conf/strategy/gflags.conf.bak")
    #conf.set_seg("=")
    conf.read_conf()
    conf.set('bbbaaa', '222')
    #conf.set('key1', '222')
    #conf.set('extractors#extractor@0#name', 'baozi')
    print conf.get("bbbaaa")
    print conf.content
    print conf.linedict
