#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
План:
    1. СоРабота с файлом динверсий и рендерверсий (создается список путей)
    2. Постановка персонажей в Т позу.
    3. Просчет кешей и плейбластов.
    4. Разработка динверсий и механизм подгрузки в рендер версию. Разработка геометрической т позы
 
"""
class DynObject():
    def __init__(self):
        self.solver=''
        self.collider=''
        self.cloth='' 
        self.outGeoList=[]
        self.tPositions=[] # словарь вершин и координат для т позы
        self.cashPath =''
        
    def getConnectedObj(self, cloth): 
        pass


    def solv():
        pass

    def loadSettings(self):
        pass
        
class DynScene():
    def __init__(self):
        self.DynObjectsList=[]
        self.sceneSettings={}
        
    def dynSceneUi():
        pass
