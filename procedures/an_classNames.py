#self=AnNames()
#self.getBodyJnt()
#self.rigStructure(make=True)

import maya.cmds as cmds
import re

"""
        AnNames
        
    metods:  
        - divideName ()
        - sfxMinus () 
        - fixNonUniqueName()
        - prefixes()
        - suffixes()
        - general()
        - body()
        - head()
        - neck()
        - bends()
        - getArm()
        - getLeg()
        - getFingers()
        - getWholeBody()
        - getArmJnt()
        - getLegJnt()
        - getBodyJnt()
        - rigStructure()

        AnNamesQuadro ( AnNames ) class for Quadropid
    metods: 
        - getArm()
        - getLeg()
"""

# AnNames().getLeg()
# AnNames().getArm()  
# AnNamesQuadro().getArm() 
# AnNamesQuadro().getLeg()  

class AnNames(object):
    __prefixes = ['l_', 'r_', 'up_', 'dw_', 'fr_', 'bk_', 'mid_'] 
    __suffixes = ['_CT', '_jnt', '_bind', '_grp',  '_ori', '_con', '_geo', \
                  '_nurbs', '_proxy', '_match', '_crv', '_ik', '_mdv', '_scnt', \
                  '_pma', 'adl', 'mdl', 'poci', 'pomi', 'posi', 'uc', 'dcm', \
                  '_set', '_loc', '_clstr', '_lttc', '_bs ', '_space', '_pvcnt', \
                  '_eff', 'skin', 'ffd', 'cls', 'rbs', '_aux', '_bend', \
                  '_soft', '_bsLttc', '_pcnt', '_ocnt', '_parcnt', '_aimcnt', \
                  '_dist', '_distDs', 'vprod', 'rhlp', '_tancnt', '_geocnt', \
                  '_nrmcnt', '_popcnt']
    __general = ['switch', 'general', 'pivotOffset']  
    __body = ['body', 'pelvis', 'waistIk', 'waist', 'torso', 'hip', 'hips', 'shoulders', 'spine']
    __neck = [ 'neck', 'neckAdd' ]          
    __head = [ 'head', 'headAim' ]  
    __arm = ['elbowIk', 'handIk', 'upArm', 'foreArm', 'hand', 'shoulder']  
    __leg = ['kneeIk', 'footIk', 'upLeg', 'knee', 'foot', 'hip']
    __bends = ['upArmBend', 'armMidBend', 'foreArmBend', 'upLegBend', \
               'legMidBend', 'lowLegBend', 'neckBend']
    __fingers = ['handClinch', 'thumb', 'index', 'middle', 'ring', 'pinky']                 
    __armJnt = ['shoulder', 'upArm', 'foreArm', 'hand']    
    __legJnt = ['hip', 'upLeg', 'lowLeg', 'foot', 'toe'] 
    
    def __init__ (self, name=None, pfx=None):
        self.name = name
    
    def divideName (self):
        pref = ''
        suff = ''
        for each in self.__prefixes:          
            size = len(each)
            if each in  self.name[:size]:          
                pref = each
        ferstPart = self.name[len(pref):]        
        
        for each in self.__suffixes:           
            size = len(each)
            if each in  self.name[-size:]:  
                suff = each
        name = ferstPart[:-len(suff)] if  suff else ferstPart 
        return pref, name, suff 
        
    def sfxMinus (self):  
        pfx, name, sfx = self.divideName()
        return  pfx+name  

    def fixNonUniqueName(self, hashes='##'):
        if not cmds.objExists(self.name):  return self.name # if obj Unique return old name
        # 1. Devaid name on:  txt, namber, sfx 
        devName = self.divideName()
        try: num = re.findall('(\d+)',  devName[1])[-1]#get seurs namber string 
        except IndexError: num=""
        txt = devName[0]+ devName[1].replace(num, '')
        sfx = devName[2]
        # 2. Set new num
        newName, num= txt+num+sfx, "0"
        while cmds.objExists(newName):
            num = int(num) + 1
            strNewNum = '0'*(len(hashes)-len(str(int(num))))+str(int(num))
            newName = txt+strNewNum+sfx
        return  newName

    def an_unicName (self, name, sfx , num=False):  #return unik name
        print(name, sfx )
 
        if not num:# ecli nomer ne nuzhen
            if not cmds.objExists(name+sfx): #esli imya v scene otcutstvuet, to mozhno ispol`zovat` ishodnoe
                return name+sfx, '00'
            else: return unicName ( name, sfx , num=True)
        else:# ecli nomer nuzhen
            for i in xrange(1,100): 
                num = '0'+ str(i) if len(str(i))==1 else str(i)
                if not cmds.objExists(name+num+sfx): return name+num+sfx, num 

 
    def prefixes(self):
        return self.__prefixes

    def suffixes(self):
        return self.__suffixes

    def general(self):
        return [self.__general[0] + self.__suffixes[0],		                     # general_CT
            		self.__general[1] + self.__suffixes[0], 		             # pivotOffset_CT
            		self.__general[2] + self.__suffixes[0]]		                 # switch_CT
    def body(self):
        return [self.__body[0] + self.__suffixes[0],		                     # body_CT
            		self.__body[6] + self.__suffixes[0],                         # hips_CT
            		self.__prefixes[3] + self.__body[3] + self.__suffixes[0],    # dw_waist_CT
            		self.__prefixes[2] + self.__body[3] + self.__suffixes[0],    # up_waist_CT
            		self.__body[4] + self.__suffixes[0],                         # torso_CT
                    self.__body[7] + self.__suffixes[0]]                         # shoulders_CT

    def head(self):
        return [    self.__head[0] + self.__suffixes[0],                         # head_CT
                    self.__head[1] + self.__suffixes[0]]                         # headAim_CT

    def neck(self):
        return [    self.__neck[0] + self.__suffixes[0],      	                 # neck_CT
                    self.__neck[1] + self.__suffixes[0]]                         # neckAdd_CT        
         
    def bends(self, side=''):
        return [    side + self.__bends[0] + self.__suffixes[0],                  # *_upArmBend_CT
                    side + self.__bends[1] + self.__suffixes[0],                  # *_armMidBend_CT
                    side + self.__bends[2] + self.__suffixes[0],                  # *_foreArmBend_CT
                    side + self.__bends[3] + self.__suffixes[0],                  # *_upLegBend_CT
                    side + self.__bends[4] + self.__suffixes[0],                  # *_legMidBend_CT        
                    side + self.__bends[5] + self.__suffixes[0]]                  # *_lowLegBend_CT         

    def getArm(self, side=''):
        return [side + self.__arm[0] + self.__suffixes[0],                     # *_elbowIk_CT
              		side + self.__arm[1] + self.__suffixes[0],                 # *_handIk_CT
            		side + self.__arm[2] + self.__suffixes[0],                 # *_upArm_CT
            		side + self.__arm[3] + self.__suffixes[0],                 # *_foreArm_CT
            		side + self.__arm[4] + self.__suffixes[0],                 # *_hand_CT
            		side + self.__arm[5] + self.__suffixes[0]]                 # *_shoulder_CT

    def getLeg(self, side=''):
        return [side + self.__leg[0] + self.__suffixes[0],                     # *_kneeIk_CT
              		side + self.__leg[1] + self.__suffixes[0],                 # *_footIk_CT
            		side + self.__leg[2] + self.__suffixes[0],                 # *_upLeg_CT
            		side + self.__leg[3] + self.__suffixes[0],                 # *_knee_CT
            		side + self.__leg[4] + self.__suffixes[0],                 # *_foot_CT
            		side + self.__leg[5] + self.__suffixes[0]]                 # *_hip_CT

    def getFingers(self, side='', oneList=False):
        all=[]
        lstlst =    [side + self.__fingers[0] + self.__suffixes[0],             # *_handClinch_CT
                    [side + self.__fingers[1] +str(i)+ self.__suffixes[0] for i in xrange(3)],             # *_thumb_CT
              		[side + self.__fingers[2] +str(i)+ self.__suffixes[0] for i in xrange(4)],             # *_index_CT
            		[side + self.__fingers[3] +str(i)+ self.__suffixes[0] for i in xrange(4)],             # *_middle_CT
            		[side + self.__fingers[4] +str(i)+ self.__suffixes[0] for i in xrange(4)],             # *_ring_CT
            		[side + self.__fingers[5] +str(i)+ self.__suffixes[0] for i in xrange(4)],]             # *_pinky_CT
        if oneList:
            for lst in lstlst:
                if type(lst) is list: all.extend(lst)
                else: all.append(lst)
            return all
        else: 
            return lstlst		     

    def getWholeBody(self, isGeneral=False):
        output = self.body + self.neck + self.head + \
                self.getArm('l_') + self.getArm('r_') + \
                self.getLeg('l_') + self.getLeg('r_') + \
                self.getFingers('l_', oneList=True) + self.getFingers('r_', oneList=True) + \
                self.bends('l_') + self.bends('r_')
        if isGeneral:  return self.general+output
        else:  return  output 

    def getArmJnt(self, side=''):
        return [    side + self.__armJnt[0] + self.__suffixes[1],                 # *_shoulder_bind
              		side + self.__armJnt[1] + self.__suffixes[1],                 # *_upArm_jnt
            		side + self.__armJnt[2] + self.__suffixes[1],                 # *_foreArm_jnt
            		side + self.__armJnt[3] + self.__suffixes[2]]                 # *_hand_bind
 
    def getLegJnt(self, side=''):
        return [    side + self.__legJnt[0] + self.__suffixes[1],                 # *l_hip_jnt
              		side + self.__legJnt[1] + self.__suffixes[1],                 # *l_upLeg_jnt
            		side + self.__legJnt[2] + self.__suffixes[1],                 # *l_lowLeg_jnt
            		side + self.__legJnt[3] + self.__suffixes[2],                 # *l_foot_bind
            		side + self.__legJnt[4] + self.__suffixes[2],                 # *l_toe_bind
            		side + self.__legJnt[4] +"1"+ self.__suffixes[1]]             # *l_toe1_jnt

    def getBodyJnt(self):
        return [    self.__body[6]+'01'+ self.__suffixes[2],                 # hips01_bind
              		self.__body[6]+'02'+ self.__suffixes[2],                 # hips02_bind     		
              		self.__body[8]+'01'+ self.__suffixes[2],                 # spine01_bind 
              		self.__body[8]+'02'+ self.__suffixes[2],                 # spine02_bind 
              		self.__body[8]+'03'+ self.__suffixes[2],                 # spine03_bind 
              		self.__body[8]+'04'+ self.__suffixes[2],                 # spine04_bind 
              		self.__neck[0]+ self.__suffixes[2],                      # neck_bind 
              		self.__head[0]+ self.__suffixes[2],                      # head_bind 
              		self.__head[0]+'01'+ self.__suffixes[1], ]               # head01_jnt               		
              		
              		
    def rigStructure(self, query=False, make=False, fold=False, ch=False, p=False, rigFold=False):
        foldStr  = ['*root',                  
        '**'+           'geo',
        '***'+               'geo_low',
        '****'+                   'sProxyBody_grp',
        '****'+                   'sProxyHead_grp',
        '***'+               'geo_middle',
        '****'+                   'proxyBody_grp',
        '*****'+                       'loClothProxyGeo_grp',        
        '*****'+                       'upClothProxyGeo_grp', 
        '****'+                   'proxyHead_grp',    
        '****'+                   'accessoriesProxyGeo_grp',
        '***'+               'geo_normal',
        '***'+               'geo_high',
        '***'+               'geo_ultra',
        '**'+           'rig',
        '***'+               'rigBody',
        '****'+                   'correctiv_grp',
        '*****'+                       'correctivJnt_grp',
        '*****'+                       'bridgeNoneScale_grp',
        '****'+                   'rivets_grp',
        '****'+                   'rigGeoBody',
        '*****'+                       'rigGeoBody_low',
        '*****'+                       'rigGeoBody_middle',
        '****'+                   'rootspaces_grp',
        '***'+               'rigHead',
        '****'+                   'rigGeoHead',
        '*****'+                       'rigGeoHead_low',
        '*****'+                       'rigGeoHead_middle',      
        '**'+           'dyn',
        '***'+               'dyn_geo',
        '***'+               'dyn_nodes',
        '**'+           'ren',]
        
        foldStrLevel = [[x.split('*')[-1], len(x.split('*'))-1] for x in foldStr] #get  name and deep
        foldersList = [x[0] for x in foldStrLevel] 
        if query and fold: return  foldersList ############ query folder names
        
        rigFolders    ={
                        'rigBody':'rigBody',  
                        'correctivJnt':'correctiv_grp',
                        'rivets':'rivets_grp',
                        }
        if query and rigFold: return  rigFolders ############ query rig folders names
        
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
                
        if query and ch and self.name:         ############ query childrens grp
            return dict(zip (foldersList, childList ))[self.name]
         
        if query and p and self.name:        ############ query parent grp
            for index, fld in enumerate(childList):  
                if self.name in fld: return parentList[index]
    

 

class AnNamesQuadro(AnNames):
    def getArm(self, side=''):        #  insert *_elbowIkDw_CT to 2 position
        bipList =    AnNames().getArm(side)      
        dwElboeCt = AnNames(bipList[0]).divideName ()[0]+AnNames(bipList[0]).divideName ()[1]+'Dw'+AnNames(bipList[0]).divideName ()[2]
        bipList.insert(1, dwElboeCt)
        bipList.insert(6, AnNames().getFingers(side)[3][0].replace('0_', '_'))
        return bipList  
        
    def getLeg(self, side=''):        #  insert *_kneeIk_CT to 2 position
        bipList =    AnNames().getLeg(side)      
        dwElboeCt = AnNames(bipList[0]).divideName ()[0]+AnNames(bipList[0]).divideName ()[1]+'Dw'+AnNames(bipList[0]).divideName ()[2]
        bipList.insert(1, dwElboeCt)
        bipList.insert(6, AnNames().getLegJnt(side)[-1].replace('1_jnt', '_CT'))
        return bipList         
       
    
#nn = AnNames().an_unicName ("box", '_geo', num=True ) 
#cmds.polyCube(n=nn[0])

# AnNames().getLeg()
# AnNames().getArm()  
# AnNamesQuadro().getArm() 
# AnNamesQuadro().getLeg()  



