# -*- encoding: utf-8 -*-
import json

#文字や形態素⇔インデックス間の返還を行うクラス
class UnitTable:
    def __init__(self,filename):
        with open(filename,'r') as f:
            unit_list = json.load(f)
        self.dic_unit2index = dict((v,int(n)) for n,v in unit_list.items())
        self.dic_index2unit = dict((int(n),v) for n,v in unit_list.items())
        self.typenum = len(unit_list)
        
    def unit2index(self,unit):
        return self.dic_unit2index[unit]
    
    def index2unit(self,index):
        return self.dic_index2unit[index]
    
    def ret_typenum(self):
        return self.typenum