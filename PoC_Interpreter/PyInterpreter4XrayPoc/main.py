# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 09:03:16 2021

@author: louqu
"""
import loadYaml
import performRule

MyPath="pocs/"

allYamls=loadYaml.walkFile(MyPath)

for PoC in allYamls:
    for rule in PoC['rules']:
        res=loadYaml.actRule(rule,"http://152.136.116.14")        
print(res)