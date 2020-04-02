import maya.cmds as cmds

def propsStructure( query=False, make=False, fold=False, ch=False, p=False, rigFold=False):
        foldStr  = ['*root',                  
        '**'+           'geo',
        '***'+               'geo_normal',
        '**'+           'rig',]
        
        foldStrLevel = [[x.split('*')[-1], len(x.split('*'))-1] for x in foldStr] #get  name and deep
        foldersList = [x[0] for x in foldStrLevel] 
        if query and fold: return  foldersList ############ query folder names
         
        ##  childrens list
        childList=[]
        for index, fld in enumerate(foldStrLevel): #chek all grp
            childrens =[]
            for child in foldStrLevel[index+1:]:
                if child[1]-1==fld[1]:
                    childrens.append(child[0])
                if child[1]-1<fld[1]:break
            childList.append(childrens)
            
        ## parent list
        parentList=[]
        for index, fld in enumerate(foldStrLevel): #chek all grp
            for each in list(reversed(foldStrLevel[:index+1]))[1:]:  #search parent
                if each[1]<fld[1]:
                    parentList.append (each[0])        
                    break
        
        ##  create folders
        if make:
            for fld in foldStrLevel:  
                if not cmds.objExists(fld[0]):  cmds.group(n=fld[0], em=True
            )   
            for par, childs  in zip ([ x[0] for x in  foldStrLevel], childList):
                if childs: 
                    for each in childs: 
                        if not  cmds.listRelatives(each, p=True): cmds.parent (each, par)
            return [x[0] for x in foldStrLevel]

def an_propsFolders():
    propsStructure(make=True)
    cmds.select( 'geo_normal' )
    cmds.createDisplayLayer (name="geo_layer", number=1)
    cmds.setAttr ("geo_layer.displayType", 2)
