#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os as os
import maya.cmds as mc
from an_classNames import AnNames as chn

'''
dir='//renderServer/Project/Tsarevny/assets/chars/'
char=['Mulat', 'LyagushkaVasilisa', 'Belka','Kot', 'Ptichka', 'BabaYaga', 'Pchelka', 'Pryanichek', 'Koschey', 'LyagushkaLivan', 'Drakon', 'Kloun', 'Drakoniha', 'Lyaguha', 'LyagushkaVasko', 'Lyagushka', 'Alyonka', 'Marlen', 'Mishka', 'Snegovik', 'PticaPoyun', 'Pilesos', 'Strekoza', 'Medved', 'Smile', 'Vasilisa', 'Sova', 'LyagushkaVarya', 'Shestilapyy', 'Pauk', 'Babochka', 'Voron', 'Varvara', 'Sonya', 'Dasha', 'Aziat', 'SovaSvyazanaya', 'Alyosha',  'Vorona',  'PrinceVeter', 'Grunvald', 'IzbushkaBabiYagi']
errorsFiles=[]
for chars in char:
    for files in [x for x in os.listdir(dir+chars+'/maya/') if not 'Middle' in x and not 'middle' in x and not 'OLD' in x and not '.js' in x and not '.preload' in x and not '.html' in x and '.mb' in x ]:
        mc.file(dir+chars+'/maya/'+files,f=True,options="v=0;",ignoreVersion=True,typ="mayaBinary",o=True)
        try:
            cleanConstrainsBody()               
            cleanConstrainsEyes()
        
        except Exception as e:
            print e
            errorsFiles.append('D:/tsarevny/'+chars+'/maya/'+files)      
        if not os.path.exists('D:/tsarevny/'+chars+'/maya/'):
            os.makedirs('D:/tsarevny/'+chars+'/maya/')
        mc.file(rename='D:/tsarevny/'+chars+'/maya/'+files)
        mc.file(typ="mayaBinary",save=True)
print   errorsFiles      

'''
  
def cleanConstrainsBody():
    const=[x for x in mc.listRelatives('geo_normal',c=True,ad=True,type='constraint') if not 'eye' in x] #нахожу все констрейны в папке geo_normal
    
    #mc.select(const)
    
    if const:
        for i in const:
            obj=mc.listConnections(i+'.target[0].targetParentMatrix')[0]             #нахожу обьект откуда идёт кострейн
            conObj=mc.listRelatives(i,p=True)[0]                                     #нахожу чем упровляет кострейн
            mesh=[x for x in mc.listRelatives(conObj,c=True,ad=True,type='mesh') if not 'Orig' in x]  #нахжу все меши которыми управляет данный констрейн (так как контрейн может управлять группой в которой есть меши)
            if mc.nodeType(obj)!='joint':                                                                        #создание костей в обьектах откуда идёт кострейн
                if not mc.ls(conObj.replace('_geo','_bind').replace('_grp','_bind').replace('_loc','_bind')):                  #если эта кость уже создана(если из одного обьекта констерйн шёл на несколько мешей, то кость может уже существовать)
                    mc.select(cl=True)
                    jnt=mc.joint(n=conObj.replace('_geo','_bind').replace('_grp','_bind').replace('_loc','_bind'))
                    mc.setAttr(jnt+'.v',0)
                    mc.delete(mc.parentConstraint(obj,jnt,mo=False))
                    mc.parent(jnt,obj)
                    mc.delete(i)
                    for a in mesh:
                        if not mc.ls(mc.listHistory(a),type='skinCluster'):                                                    #провека на скин, скин может появиться на обьекте если к обьекту шёл парент кострейн и скейл констрейн (по идее скейлы не нужно обрабатывать, скел нужно кидать на созданную кость от 'pivotOffset_CT')
                            mc.skinCluster(a,jnt,tsb=True)
                else:
                    for a in mesh: 
                        if not mc.ls(mc.listHistory(a),type='skinCluster'):
                            mc.skinCluster(a,conObj.replace('_geo','_bind').replace('_grp','_bind').replace('_loc','_bind'),tsb=True)
                    mc.delete(i)
            else:                                    #если обьекты были приконстрейнины к кости, то без содания кости новыой автоматически назначается скин
                mc.delete(i)
                for a in mesh:
                    if not mc.ls(mc.listHistory(a),type='skinCluster'):
                        mc.skinCluster(a,obj,tsb=True)
                            
 
        
        
'''      
eyeGeo = cmds.ls(sl=True)
     
eyeGrp = cmds.group(n='eyeGeo_grp',em=True)

for eye in eyeGeo:
    renam = cmds.rename(eye , eye.replace('_geo', 'Driver_geo'))
    cmds.duplicate(renam, n= eye)
    cmds.parent(eye, eyeGrp)
    cmds.makeIdentity (apply=True, t=1, r=1, s=1, n=0, pn=1)
    cmds.blendShape(renam, eye, w=[(0, 1)], o="world")

     
cmds.parent(eyeGrp, 'geo_normal')     

'''



#mc.select(mesh)


i = cmds.ls(sl=True)[0]   # get кострейн
obj=mc.listConnections(i+'.target[0].targetParentMatrix')[0]             #нахожу обьект откуда идёт кострейн
conObj=cmds.listRelatives(i,p=True)[0]                                     #нахожу чем упровляет кострейн

mesh=[x for x in cmds.listRelatives(conObj,c=True,ad=True,type='mesh') if not 'Orig' in x]  #нахжу все меши 
mesh=[cmds.listRelatives( x, p=True)[0] for x in  mesh  ]


if cmds.nodeType(obj)== 'joint':
    for geo in mesh:
        cmds.skinCluster(geo, obj ,tsb=True)
else:
    jn = cmds.joint(n=chn(obj).sfxMinus()+'_jnt')
    cmds.parent(jn,  obj) 
    cmds.skinCluster(mesh, jn ,tsb=True)

cmds.delete(i)









        