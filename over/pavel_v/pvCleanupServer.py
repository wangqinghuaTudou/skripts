'''
import glob
import re
import time
import datetime
import os
import shutil
import fnmatch


rootPath="//renderServer/Project"
stringbuffer=[]
treeMonthLaterReal = datetime.datetime.now() - datetime.timedelta(days = 150)
treeMonthLater = datetime.datetime.now() - datetime.timedelta(days = 45)
oneNedelyaLater = datetime.datetime.now() - datetime.timedelta(days = 5)
treeNedelyaLater = datetime.datetime.now() - datetime.timedelta(days = 10) 
rootPathsArray={"//dataServer/Project":[],"//renderServer/Project":[],"//cacheServer/Project":[]}
projectsArray={"UrfinJuse":[],"UrfinJuse2":[],"Tsarevny":[],"SOBAKI":[],"Luntik":[]}


print("RENDERMAN FROM ASSETS AND SCENES\n")

for rootPath in rootPathsArray.keys():
    for project in projectsArray.keys():
        ppaths=["/assets/*/*","/scenes/*/*"]
        if project != "UrfinJuse" and project != "UrfinJuse2":
            ppaths=["/assets/*/*","/scenes/*/*/*"]
        for pp in ppaths:

            paths=glob.glob(rootPath+"/"+project+pp+"/renderman/*")
            for path in paths:
                if os.path.basename(path)!="ribarchives" and os.path.basename(path)!="textures":
                    if not os.path.isdir(path) and oneNedelyaLater > datetime.datetime.fromtimestamp(os.path.getmtime(path)):
                        stringbuffer.append(path)
                    else:
                        if treeMonthLaterReal > datetime.datetime.fromtimestamp(os.path.getmtime(path)):
                            stringbuffer.append(path)
                        else:
                            if os.path.isdir(path):
                                if os.path.exists(os.path.join(path,"rib")):
                                    if oneNedelyaLater > datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(path,"rib"))):
                                        stringbuffer.append(os.path.join(path,"rib"))
                                if os.path.exists(os.path.join(path,"shaders")):
                                    if oneNedelyaLater > datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(path,"shaders"))):
                                        stringbuffer.append(os.path.join(path,"shaders"))                        
                                if os.path.exists(os.path.join(path,"data")):
                                    if oneNedelyaLater > datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(path,"data"))):
                                        stringbuffer.append(os.path.join(path,"data"))                                                

            paths=glob.glob(rootPath+"/"+project+pp+"/slim/shaders/*")
            for path in paths:
                try:
                    if oneNedelyaLater > datetime.datetime.fromtimestamp(os.path.getmtime(path)):
                        stringbuffer.append(path)
                except:
                    pass

            paths=glob.glob(rootPath+"/"+project+pp+"/arnold/*")
            for path in paths:
                try:
                    if oneNedelyaLater > datetime.datetime.fromtimestamp(os.path.getmtime(path)):
                        stringbuffer.append(path)
                except:
                    pass

            paths=glob.glob(rootPath+"/"+project+pp+"/light/work/arnold/*")
            for path in paths:
                try:
                    if oneNedelyaLater > datetime.datetime.fromtimestamp(os.path.getmtime(path)):
                        stringbuffer.append(path)
                except:
                    pass
            
            paths=glob.glob(rootPath+"/"+project+pp+"/light/work/redshift/*")
            print paths
            for path in paths:
                try:
                    if treeNedelyaLater > datetime.datetime.fromtimestamp(os.path.getmtime(path)):
                        stringbuffer.append(path)
                except:
                    pass

            paths=glob.glob(rootPath+"/"+project+pp+"/redshift/*")
            print paths
            for path in paths:
                try:
                    if treeNedelyaLater > datetime.datetime.fromtimestamp(os.path.getmtime(path)):
                        stringbuffer.append(path)
                except:
                    pass

            paths=glob.glob(rootPath+"/"+project+pp+"/light/redshift/*")
            print paths
            for path in paths:
                try:
                    if treeNedelyaLater > datetime.datetime.fromtimestamp(os.path.getmtime(path)):
                        stringbuffer.append(path)
                except:
                    pass

            paths=glob.glob(rootPath+"/"+project+pp+"/light/work/redshift/*/rs/*")
            print paths
            for path in paths:
                try:
                    if oneNedelyaLater > datetime.datetime.fromtimestamp(os.path.getmtime(path)):
                        stringbuffer.append(path)
                except:
                    pass

            paths=glob.glob(rootPath+"/"+project+pp+"/redshift/*/rs/*")
            print paths
            for path in paths:
                try:
                    if oneNedelyaLater > datetime.datetime.fromtimestamp(os.path.getmtime(path)):
                        stringbuffer.append(path)
                except:
                    pass

            paths=glob.glob(rootPath+"/"+project+pp+"/light/redshift/*/rs/*")
            print paths
            for path in paths:
                try:
                    if oneNedelyaLater > datetime.datetime.fromtimestamp(os.path.getmtime(path)):
                        stringbuffer.append(path)
                except:
                    pass


print("WRITE TO FILE\n")

if os.path.exists("//dataServer/Project/backup_s3d/lib/python/fileToDelete.txt"):
    os.remove("//dataServer/Project/backup_s3d/lib/python/fileToDelete.txt")

fileLog = open("//dataServer/Project/backup_s3d/lib/python/fileToDelete.txt", "w")		
fileLog.write("Papok udaleno: "+str(len(stringbuffer))+"\n")
for item in stringbuffer:
    fileLog.write("%s\n" % item)
fileLog.close()
'''