# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 08:53:37 2021

@author: louqu
"""
import os
import yaml

def get_yaml_load_all(yaml_file):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    all_data = yaml.load_all(file_data,Loader=yaml.FullLoader)
    return all_data      

def walkFile(file):
    for root, dirs, files in os.walk(file):
        for file in files:
            return get_yaml_load_all(root+file)
        


        