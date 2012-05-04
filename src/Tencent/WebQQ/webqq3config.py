# -*- coding: utf-8 -*-
"""
webqq得配置信息
"""
from ConfigParser import ConfigParser
cfg=ConfigParser()
cfg.read('webqq3.ini')
sections=cfg.sections()
configs={}
for s in sections:
    dic={}
    for k, v in cfg.items(s):
        dic[k]=v
    configs[s]=dic

def getURL(name=None):
    return configs['url'].get(name)
    
def getHeader(name=None):
    return configs['header'].get(name)
