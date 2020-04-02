

import maya.cmds as cmds 
import maya.mel as mm 
from CharacterNames import CharacterNames as chn


class An_Controllers():
    def __init__ (self, name=None):
        self.name = name
        self.conGrp = None
        self.oriGrp = None
        self.color = 17
        self.defColor = {'cntrIk': 20 , 'cntrFk': 17 , 'left':18 , 'right':13 , 'add':20}
        
    def addDevideAttr (self, attrName='_'):
        while cmds.objExists(self.name+'.'+attrName):
            attrName = attrName+'_' 
             
        cmds.addAttr   (self.name, ln=attrName,  keyable=True)
        cmds.setAttr (self.name+'.'+attrName, lock=True)

    def gropeCT(self):   #made ori and con groups and place controller to it whith zero transforms 
        #names = chn.An_CharNames(self.name).devideName()
        names = chn(self.name).divideName()
        self.conGrp = cmds.group(em=True, n=names[0]+names[1]+'_con')
        self.oriGrp = cmds.group(self.conGrp, n=names[0]+names[1]+'_ori' ) 
        cmds.delete(cmds.parentConstraint(self.name, self.oriGrp))
        cmds.parent(self.name, self.conGrp)
        return [self.name, self.conGrp, self.oriGrp]
        
    def pointList (self): ##Returns a list of vertices in several lists, corresponding to the number of shapes .
        vShapes = cmds.listRelatives(self.name, s=True)
        prefix = vShapes if len(vShapes)>1 else [self.name]
        rez = []
        for pfx, shape in zip(prefix, vShapes) :  
            vPointsNum = cmds.getAttr (shape+'.spans')+cmds.getAttr (shape+'.degree')
            if cmds.getAttr (shape+'.form'): vPointsNum = vPointsNum-3 #if curve is closed 
            rez.append([pfx+'.cv['+str(id)+']' for id in range(vPointsNum)] )
        return  rez 

    def addShape(self, newCurve):
        child = cmds.listRelatives (newCurve, s=True )
        for eachCurve  in child: cmds.parent (eachCurve, self.name, s=True, r=True)
        cmds.delete (newCurve)
        
    def shapePresets(self, type):  ## points coordinates puts in tuple for several curves !!!!!!!!!
        if type=='switch': return  {'degree':1, 'point':[[[0.0, 0.04, 0.0], [0.0, 1.94, -0.63], [0.63, 1.94, 0.0], [0.0, 0.04, 0.0], [-0.63, 1.94, 0.0], 
            [0.0, 1.94, -0.63], [-0.63, 1.94, 0.0], [0.0, 1.94, 0.63], [0.0, 0.04, 0.0], [0.0, 1.94, 0.63], [0.63, 1.94, 0.0], [0.0, 3.84, 0.0], 
            [0.0, 1.94, 0.63], [-0.63, 1.94, 0.0], [0.0, 3.84, 0.0], [0.0, 1.94, -0.63]]]}

        elif type=='sphere': return {'degree':3, 'point':[[[0, 0.0, -0.475], [0, -0.12, -0.47], [0, -0.27, -0.39], [0, -0.43, -0.24], [0, -0.5, 0.03], 
            [0, -0.36, 0.36], [0, 0.0, 0.51], [0, 0.36, 0.36], [0, 0.5, 0.03], [0, 0.42, -0.23], [0, 0.28, -0.39], [0, 0.11, -0.47], [0, 0.0, -0.47]], 
            [[0.0, 0.475, 0.0], [-0.12, 0.47, 0], [-0.27, 0.39, 0], [-0.43, 0.24, 0], [-0.5, -0.03, 0], [-0.36, -0.36, 0], [0.0, -0.51, 0.0], [0.36, -0.36, 0], 
            [0.5, -0.03, 0], [0.42, 0.23, 0], [0.28, 0.39, 0], [0.11, 0.47, 0], [0.0, 0.47, 0.0]], [[0.0, 0, -0.475], [-0.12, 0, -0.47], [-0.27, 0, -0.39], 
            [-0.43, 0, -0.24], [-0.5, 0, 0.03], [-0.36, 0, 0.36], [0.0, 0, 0.51], [0.36, 0.0, 0.36], [0.5, 0, 0.03], [0.42, 0, -0.23], [0.28, 0, -0.39], 
            [0.11, 0, -0.47], [0.0, 0, -0.47]]]}
        
        elif type=='head': return {'degree':3, 'point':[[[0, 3.779, 0.751], [-0.22, 3.769, 0.751], [-0.85, 3.666, 0.751], [-1.30, 3.356, 0.752], [-1.66, 3.051, 0.531], 
            [-1.94, 2.677, 0.531], [-2.19, 1.954, 0.531], [-2.21, 1.817, 0.597], [-2.21, 1.511, 0.996], [-2.21, 0.755, 1.160], [-2.21, 0.063, 0.758], [-2.21, -0.20, 0], 
            [-2.21, 0.063, -0.75], [-2.21, 0.755, -1.16], [-2.21, 1.511, -0.99], [-2.21, 1.817, -0.59], [-2.19, 1.954, -0.53], [-1.94, 2.677, -0.53], [-1.66, 3.051, -0.53], 
            [-1.30, 3.356, -0.75], [-0.85, 3.666, -0.75], [0, 3.779, -0.75], [0.859, 3.666, -0.75], [1.309, 3.356, -0.75], [1.667, 3.051, -0.53], [1.942, 2.677, -0.53], 
            [2.192, 1.954, -0.53], [2.210, 1.817, -0.59], [2.210, 1.511, -0.99], [2.211, 0.755, -1.16], [2.211, 0.063, -0.75], [2.211, -0.20, 0], [2.211, 0.063, 0.758], 
            [2.211, 0.755, 1.160], [2.210, 1.511, 0.996], [2.210, 1.817, 0.597], [2.192, 1.954, 0.531], [1.942, 2.677, 0.531], [1.667, 3.051, 0.531], [1.309, 3.356, 0.752], 
            [0.859, 3.666, 0.751], [0.222, 3.769, 0.751], [0, 3.779, 0.751]]] }

        elif type=='headAim': return {'degree':3, 'point':[[[0.001, -0.32, 0.0], [0.066, -0.32, 0.0], [0.030, -0.39, 0.0], [0.030, -0.45, 0.0], [0.053, -0.48, 0.0], 
            [0.368, -0.36, 0.0], [0.486, -0.05, 0.0], [0.458, -0.03, 0.0], [0.396, -0.03, 0.0], [0.354, -0.05, 0.0], [0.322, 0.000, 0.0], [0.354, 0.055, 0.0], 
            [0.396, 0.030, 0.0], [0.458, 0.030, 0.0], [0.486, 0.053, 0.0], [0.367, 0.368, 0.0], [0.053, 0.486, 0.0], [0.030, 0.458, 0.0], [0.030, 0.396, 0.0], 
            [0.055, 0.354, 0.0], [0.002, 0.321, 0.0], [-0.05, 0.354, 0.0], [-0.03, 0.396, 0.0], [-0.03, 0.458, 0.0], [-0.05, 0.486, 0.0], [-0.36, 0.367, 0.0], 
            [-0.48, 0.053, 0.0], [-0.45, 0.030, 0.0], [-0.39, 0.030, 0.0], [-0.35, 0.055, 0.0], [-0.32, -0.00, 0.0], [-0.35, -0.05, 0.0], [-0.39, -0.03, 0.0], 
            [-0.45, -0.03, 0.0], [-0.48, -0.05, 0.0], [-0.36, -0.36, 0.0], [-0.05, -0.48, 0.0], [-0.03, -0.45, 0.0], [-0.03, -0.39, 0.0], [-0.06, -0.32, 0.0], 
            [0.001, -0.32, 0.0]]] }

        elif type=='fk': return {'degree':3, 'point': [ [[0.353, 0, 0.853], [0.530, 0, 0.780], [0.707, 0, 0.707], [0.780, 0, 0.530], [0.926, 0, 0.176], [1.0, 0, 0.0], 
            [0.926, 0, -0.17], [0.780, 0, -0.53], [0.707, 0, -0.70], [0.530, 0, -0.78], [0.176, 0.0, -0.92], [0.0, 0.0, -0.99], [-0.17, 0.0, -0.92], [-0.53, 0, -0.78], [-0.70, 0, -0.70], 
            [-0.78, 0, -0.53], [-0.92, 0, -0.17], [-0.99, 0, 0.0], [-0.92, 0, 0.176], [-0.78, 0, 0.530], [-0.70, 0, 0.707], [-0.53, 0, 0.780], [-0.17, 0.0, 0.926], [0.0, 0.0, 0.999], 
            [0.176, 0.0, 0.926], [0.353, 0, 0.853]]] }

        elif type=='handIk': return {'degree':3, 'point':[[[-0.09, 0, -0.28], [-0.09, -0.03, -0.28], [-0.09, -0.07, -0.28], [-0.29, -0.07, -0.18], [-0.32, -0.07, 0.113], 
            [-0.19, -0.07, 0.220], [-0.17, -0.10, 0.242], [-0.17, -0.12, 0.242], [-0.07, -0.14, 0.293], [0.075, -0.14, 0.293], [0.175, -0.12, 0.242], [0.175, -0.10, 0.242], 
            [0.197, -0.07, 0.220], [0.320, -0.07, 0.113], [0.295, -0.07, -0.18], [0.092, -0.07, -0.28], [0.092, -0.03, -0.28], [0.092, 0, -0.28], [0.092, 0.038, -0.28], 
            [0.092, 0.076, -0.28], [0.295, 0.076, -0.18], [0.320, 0.076, 0.113], [0.197, 0.076, 0.219], [0.175, 0.103, 0.242], [0.175, 0.125, 0.242], [0.075, 0.140, 0.293], 
            [-0.07, 0.140, 0.293], [-0.17, 0.125, 0.242], [-0.17, 0.103, 0.242], [-0.19, 0.076, 0.221], [-0.32, 0.076, 0.113], [-0.29, 0.076, -0.18], [-0.09, 0.076, -0.28], 
            [-0.09, 0.038, -0.28], [-0.09, 0, -0.28]]]   }

        elif type=='axis': return {'degree':1, 'point':[[[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], [[0.0, 0.0, 0.0], [0.0, 1.0, 0.0]], [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]]}

        elif type=='kross': return {'degree':1, 'point':[  [[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]], [[0.0, 1.0, 0.0], [0.0, -1.0, 0.0] ], [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0] ] ]}
        
        elif type=='torso': return {'degree':3, 'point':[[[0, -0.52, 0.620], [0.387, -0.50, 0.617], [0.759, -0.19, 0.455], [0.877, 0, 0], [0.759, -0.15, -0.40], 
            [0.438, -0.41, -0.58], [0, -0.52, -0.61], [-0.43, -0.41, -0.58], [-0.75, -0.15, -0.40], [-0.87, 0, 0], [-0.75, -0.19, 0.455], [-0.38, -0.50, 0.617], [0, -0.52, 0.620]], 
            [[0, -0.64, 0.628], [0.441, -0.62, 0.629], [0.866, -0.24, 0.501], [1.0, 0, 0], [0.866, -0.19, -0.44], [0.5, -0.51, -0.61], [0, -0.64, -0.61], [-0.5, -0.51, -0.61], 
            [-0.86, -0.19, -0.44], [-1.0, 0, 0], [-0.86, -0.24, 0.501], [-0.44, -0.62, 0.629], [0, -0.64, 0.628]]]     }

        elif type=='shoulder': return {'degree':3, 'point': [[[-2.0, 0.0, 0], [-2.0, -0.24, 0], [-2.0, -0.49, 0], [-1.90, -0.49, 0.617], [-1.30, -0.49, 1.670], [0, -0.49, 2.102], 
            [1.294, -0.49, 1.670], [1.882, -0.49, 0.617], [2.0, -0.49, 0], [2.0, -0.24, 0], [2.0, 0.0, 0], [2.0, 0.235, 0], [2.0, 0.470, 0], [1.882, 0.470, 0.617], [1.294, 0.470, 1.670], 
            [0, 0.470, 2.102], [-1.30, 0.470, 1.670], [-1.90, 0.470, 0.617], [-2.0, 0.470, 0], [-2.0, 0.235, 0], [-2.0, 0.0, 0]]] }

        elif type=='body': return {'degree':3, 'point':[ [[4.155, 0, 4.155], [2.493, 0, 5.817], [0.831, 0, 7.479], [0, 0, 8.31], [-0.831, 0, 7.479], [-4.155, 0.0, 4.155], 
            [-7.479, 0, 0.831], [-8.31, 0, 0], [-7.479, 0, -0.831], [-4.155, 0, -4.155], [-0.831, 0, -7.479], [0, 0, -8.310], [0.831, 0, -7.479], [4.155, 0.0, -4.155], 
            [7.479, 0, -0.831], [8.31, 0, 0], [7.47, 0, 0.831], [4.155, 0, 4.155]], [[0.0, 0, 5.878], [2.869, 0, 5.669], [5.472, 0, 3.054], [6.144, 0, -0.018], [5.32, 0, -3.09], 
            [3.072, 0, -5.338], [0.0, 0, -6.162], [-3.072, 0, -5.338], [-5.320, 0, -3.090], [-6.144, 0, -0.018], [-5.472, 0, 3.0541], [-2.869, 0, 5.669], [0.0, 0, 5.878]]] }

        elif type=='fkBody': return {'degree':3, 'point':[  [[3.098, 0.235, 0.0], [3.098, 0.103, 0.0], [3.098, -0.076, 0.0], [3.098, -0.226, 0.0]], [[0.0, -0.244, 3.113], 
            [1.515, -0.244, 3.003], [2.889, -0.244, 1.622], [3.244, -0.242, 0.0], [2.809, -0.154, -1.622], [1.622, -0.088, -2.809], [0.0, -0.065, -3.244], [-1.622, -0.088, -2.809], 
            [-2.809, -0.154, -1.622], [-3.244, -0.242, 0.0], [-2.889, -0.244, 1.622], [-1.515, -0.244, 3.003], [0.0, -0.244, 3.113]], [[0.0, 0.252, 3.113], [1.515, 0.252, 3.003], 
            [2.889, 0.252, 1.622], [3.244, 0.251, 0.0], [2.809, 0.159, -1.622], [1.622, 0.092, -2.809], [0.0, 0.067, -3.244], [-1.622, 0.092, -2.809], [-2.809, 0.159, -1.622], 
            [-3.244, 0.251, 0.0], [-2.889, 0.252, 1.622], [-1.515, 0.252, 3.003], [0.0, 0.252, 3.113]], [[0.0, 0.252, 3.112], [0.0, 0.11, 3.304], [0.0, -0.082, 3.304], 
            [0.0, -0.244, 3.112]], [[-3.098, 0.235, 0.0], [-3.098, 0.103, 0.0], [-3.098, -0.076, 0.0], [-3.098, -0.226, 0.0]], [[0.0, 0.075, -3.098], [0.0, 0.033, -3.098], 
            [0, -0.024, -3.098], [0.0, -0.075, -3.098]]]  }
		
        elif type=='general': return {'degree':3, 'point':[[[0.0, 0.1, 0.8], [0.12, 0.1, 0.8], [0.24, 0.1, 0.8], [0.37, 0.0, 0.86], [0.49, 0.0, 0.86], 
            [0.56, 0.0, 0.75], [0.57, 0.1, 0.62], [0.63, 0.1, 0.51], [0.76, 0.1, 0.29], [0.82, 0.1, 0.18], [0.93, 0.0, 0.1], 
            [1.0, 0.0, 0.0], [0.93, 0.0, -0.1], [0.82, 0.1, -0.18], [0.76, 0.1, -0.29], [0.63, 0.1, -0.51], [0.57, 0.1, -0.62], 
            [0.56, 0.0, -0.75], [0.5, 0.0, -0.86], [0.37, 0.0, -0.86], [0.24, 0.1, -0.80], [0.12, 0.1, -0.80], [-0.12, 0.1, -0.80], 
            [-0.24, 0.1, -0.80], [-0.37, 0.0, -0.86], [-0.49, 0.0, -0.86], [-0.56, 0.0, -0.75], [-0.57, 0.1, -0.62], [-0.63, 0.1, -0.51], 
            [-0.76, 0.1, -0.29], [-0.82, 0.1, -0.18], [-0.93, 0.0, -0.1], [-1.0, 0.0, 0.0], [-0.93, 0.0, 0.1], [-0.82, 0.1, 0.18], 
            [-0.76, 0.1, 0.29], [-0.63, 0.1, 0.51], [-0.57, 0.1, 0.62], [-0.56, 0.0, 0.75], [-0.49, 0.0, 0.86], [-0.37, 0.0, 0.86], 
            [-0.24, 0.1, 0.8], [-0.12, 0.1, 0.8], [0.0, 0.1, 0.8]]]}
            
        elif type=='legIk': return {'degree':3, 'point': [[[1.0, 0.0, 1.0], [1.0, 0, 1.7], [1.0, 0.75, 1.7], [0.5, 0.94, 1.71], [0.14, 0.94, 1.71], [0.11, 0.77, 2.40], 
            [0.43, 0.77, 2.39], [0.99, 0.58, 2.27], [1.0, 0.0, 2.0], [1.0, 0.0, 2.29], [0.65, 0.0, 2.83], [0.0, 0.0, 3.0], [-0.65, 0.0, 2.83], [-1.0, 0.0, 2.3], 
            [-1.0, 0.0, 2.0], [-0.99, 0.58, 2.27], [-0.43, 0.77, 2.39], [-0.11, 0.77, 2.4], [-0.14, 0.94, 1.71], [-0.49, 0.94, 1.71], [-0.99, 0.75, 1.71], 
            [-1.0, 0.0, 1.71], [-1.0, 0.0, 1.0], [-1.0, 0.0, 0.30], [-0.9, 0.0, -0.69], [-0.43, 0.0, -1.0], [-0.16, 0.47, -1.0], [-0.57, 0.49, -0.78], 
            [-0.57, 0.69, -0.78], [0.0, 0.83, -1.0], [0.57, 0.69, -0.78], [0.57, 0.49, -0.78], [0.16, 0.47, -1.0], [0.43, 0.0, -1.0], [1.0, 0.0, -0.69], 
            [1.0, 0.0, 0.30], [1.0, 0.0, 1.0]]]}
            
        elif type=='curvedArrow': return {'degree':3, 'point': [[[3.725, 0.000, 0], [3.712, 0.315, 0], [3.672, 0.630, 0], [3.606, 0.940, 0], [3.514, 1.244, 0], 
        [3.397, 1.539, 0], [3.217, 1.504, 0], [2.822, 1.403, 0], [3.021, 2.099, 0], [2.794, 2.932, 0], [2.827, 2.966, 0], [3.708, 2.469, 0], [4.460, 2.202, 0], 
        [4.145, 1.931, 0], [4.004, 1.810, 0], [4.142, 1.463, 0], [4.250, 1.105, 0], [4.327, 0.740, 0], [4.374, 0.370, 0], [4.390, -0.00, 0], [4.374, -0.37, 0], 
        [4.327, -0.74, 0], [4.250, -1.10, 0], [4.142, -1.46, 0], [4.004, -1.81, 0], [4.145, -1.93, 0], [4.460, -2.20, 0], [3.708, -2.46, 0], [2.827, -2.96, 0], 
        [2.794, -2.93, 0], [3.021, -2.09, 0], [2.822, -1.40, 0], [3.217, -1.50, 0], [3.397, -1.53, 0], [3.514, -1.24, 0], [3.606, -0.94, 0], [3.672, -0.63, 0], 
        [3.712, -0.31, 0], [3.725, 0.000, 0]]]}

        elif type=='circle': return {'degree':3, 'point': [[[0, 0.0, 1.000], [-0.36, 0.0, 0.989], [-0.84, 0.0, 0.668], [-1.09, 0.0, -0.01], [-0.77, 0.0, -0.79], [0, 0.0, -1.11], 
            [0.776, 0.0, -0.79], [1.098, 0.0, -0.01], [0.844, 0.0, 0.668], [0.354, 0.0, 0.992], [0, 0.0, 1.000]]]}
            
        elif type=='skelCT': return {'degree':3, 'point': [[[0.0, 0.0, 0.0], [0.333, 0.0, 0.0], [0.667, 0.0, 0.0], [1.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [0.0, 0.333, 0.0], 
        [0.0, 0.667, 0.0], [0.0, 1.0, 0.0]], [[0.0, 0.0, 0.0], [0.0, 0.0, 0.333], [0.0, 0.0, 0.667], [0.0, 0.0, 1.0]], [[0.0, 0.0, -0.475], [0.0, -0.12, -0.47], [0.0, -0.27, -0.39], 
        [0.0, -0.43, -0.24], [0.0, -0.5, 0.03], [0.0, -0.36, 0.36], [0.0, 0.0, 0.51], [0.0, 0.36, 0.36], [0.0, 0.5, 0.03], [0.0, 0.42, -0.23], [0.0, 0.28, -0.39], [0.0, 0.11, -0.47], 
        [0.0, 0.0, -0.47]], [[0.0, 0.475, 0.0], [-0.12, 0.47, 0.0], [-0.27, 0.39, 0.0], [-0.43, 0.24, 0.0], [-0.5, -0.03, 0.0], [-0.36, -0.36, 0.0], [0.0, -0.51, 0.0], [0.36, -0.36, 0.0], 
        [0.5, -0.03, 0.0], [0.42, 0.23, 0.0], [0.28, 0.39, 0.0], [0.11, 0.47, 0.0], [0.0, 0.47, 0.0]], [[0.0, 0.0, -0.475], [-0.12, 0.0, -0.47], [-0.27, 0.0, -0.39], [-0.43, 0.0, -0.24], 
        [-0.5, 0.0, 0.03], [-0.36, 0.0, 0.36], [0.0, 0.0, 0.51], [0.36, 0.0, 0.36], [0.5, 0.0, 0.03], [0.42, 0.0, -0.23], [0.28, 0.0, -0.39], [0.11, 0.0, -0.47], [0.0, 0.0, -0.47]]] }         

    def hideAttr(self, attrs):        
	    for attr in attrs:  
	        cmds.setAttr ( self.name+"."+attr, lock=True, keyable=False)      
     
    def showTransAttrs(self):
        for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']:
	        cmds.setAttr (self.name+"."+attr, lock=False, keyable=True)
	        
    def moveCt (self, coord): # ofset controller (shape)  
        claster = cmds.cluster(self.name)   
        cmds.move   (coord[0], coord[1], coord[2], claster)
        cmds.delete (self.name, ch=True) 

    def makeController (self, type, size=1, offset = [0, 0, 0], orient="Y"): #Make controller, set size, make shape ofset
        ctrl = cmds.curve (n= self.name, d= self.shapePresets(type)['degree'], p = self.shapePresets(type)['point'][0]) # Make first curve 
        if len(self.shapePresets(type)['point'])>1:  #if the point list is array, built  more curves
            for pList in self.shapePresets(type)['point'][1:]:
                crv = cmds.curve ( d= self.shapePresets(type)['degree'], p = pList) 
                child = cmds.listRelatives (crv, c=True )[0]
                cmds.parent (child, ctrl, s=True, r=True)
                cmds.delete (crv)
        if orient == 'Z': self.rotateCt ([-90, 0, 0])
        if orient == 'X': self.rotateCt ([-90, -90, 0])        
        self.setCtSize (size)
        self.moveCt (offset)
        if not type=='axis': self.addColor ( color=self.color)
        
    def setCtSize(self, size=1): # cet size of coordinates
        Len = max(cmds.getAttr (self.name+".boundingBoxMaxX") - cmds.getAttr (self.name+".boundingBoxMinX"), 
                    cmds.getAttr (self.name+".boundingBoxMaxY") - cmds.getAttr (self.name+".boundingBoxMinY"), 
                    cmds.getAttr (self.name+".boundingBoxMaxZ") - cmds.getAttr (self.name+".boundingBoxMinZ"))
        claster = cmds.cluster(self.name)   
        cmds.move   (0.0, 0.0, 0.0,  claster[1]+'.scalePivot' )
        cmds.scale   (size/Len, size/Len, size/Len,  claster[1], r=True )
        cmds.delete (self.name, ch=True)

    def addColor (self, switch=None, color='cntrFk'): # add color atributes to switch, connect  it to controller
        shape = cmds.listRelatives (self.name, s=True)
        if switch:     # if switch specify
            for each in self.defColor.keys()  :  
                if not  mm.eval("attributeExists \""+each+'_color'+"\""+switch):           
                    cmds.addAttr   (switch, ln=each+'_color', dv=self.defColor[each], min=0, max=32,   keyable = False) 
            for eachShape in shape:
            	cmds.setAttr (eachShape +".overrideEnabled", 1)
                cmds.connectAttr ( switch+'.'+color+'_color', eachShape +".overrideColor", f=True)
        else:      # if switch not specify
            if type(color) is str: 
                self.color = self.defColor[color]     
            else: 
                self.color = color 
            for eachShape in shape:
                cmds.setAttr (eachShape +".overrideEnabled", 1)
                cmds.setAttr (eachShape +".overrideColor", self.color ) 

    def rotateCt (self, coord): # ofset controller (shape)  
        claster = cmds.cluster(self.name) 
        cmds.xform (claster[1], os=True,  piv=(0, 0, 0) )
        cmds.rotate (coord[0], coord[1], coord[2], claster)       
        cmds.delete (self.name, ch=True) 

    def makeOrientAxis (self, size=1):  
        type = 'axis'
        self.makeController (type, size)
        shape = cmds.listRelatives (self.name, s=True)
        for eachShape, colorN in ((shape[0],6), (shape[1],14), (shape[2],13)):  # colors blue, green, red
            cmds.setAttr (eachShape +".overrideEnabled", 1)
            cmds.setAttr (eachShape +".overrideColor", colorN)
            
    def makeSpherAndOrientAxis (self, size=1):  
            type = 'skelCT'
            self.makeController (type, size)
            shape = cmds.listRelatives (self.name, s=True)
            
            for eachShape, colorN in ((shape[0],13), (shape[1],14), (shape[2],6), (shape[3],17) , (shape[4],17) , (shape[5],17)):  # colors blue, green, red
                cmds.setAttr (eachShape +".overrideEnabled", 1)
                cmds.setAttr (eachShape +".overrideColor", colorN) 
                
            for attr in ['axisVisibility',  'sphereVisibility' ]:
                cmds.addAttr(self.name, longName=attr, defaultValue=1.0, minValue=0.0, maxValue=1.0, k=True)               
                connect= ['axisVisibility',0,1,2] if attr=='axisVisibility' else ['sphereVisibility', 3,4,5]
                for i in connect[1:]:
                    cmds.connectAttr ( self.name+'.'+connect[0] , shape[i] +".visibility", f=True)
                
                        
            
                 
    def mirrorShape(self, target): # copy ct shape by X axis 
        sourseShape = cmds.listRelatives(self.name, s=True)     # get curve shape
        targShape = cmds.listRelatives(target, s=True)
        for i in xrange(len(sourseShape)):
            vPointsNum = cmds.getAttr (sourseShape[i]+'.spans')+cmds.getAttr (sourseShape[i]+'.degree')   # get curve points number
            for pn in xrange(vPointsNum): 
                pos =cmds.xform(sourseShape[i]+'.controlPoints['+str(pn)+']',  q=True, t=True, ws=True )
                cmds.xform(targShape[i]+'.controlPoints['+str(pn)+']', t=[pos[0]*-1, pos[1], pos[2] ], ws=True )  
                

    def placeCT (self, target, tape = "parent", aimAndAp = []):
        """ 
        @param[in] tape    - you specify one of placment tapes: "parent", "point", "orient", "polyVector"
        """
        if tape == "parent":  cmds.delete (cmds.parentConstraint (target, self.oriGrp))
        elif tape == "point":	cmds.delete (cmds.pointConstraint (target, self.oriGrp)) 
        elif tape == "orient"  :	cmds.delete (cmds.orientConstraint (target, self.oriGrp))      
        else:                                                                               #place polyVector controller, target - root ik jnt (shoulder)
            tmpJnt = cmds.duplicate(target , rc=True) 
            ikHandl = cmds.ikHandle (shf=False,  sol="ikRPsolver", sj=tmpJnt[0], ee=tmpJnt[2])
             
            posStart = cmds.xform (tmpJnt[0],  q=True, t=True, ws=True) 
            pozEnd = cmds.xform (tmpJnt[2],  q=True, t=True, ws=True)   
            valPv = cmds.getAttr (ikHandl[0]+".poleVector") [0]
            posIkDef =  [posStart[0]+valPv[0], posStart[1]+valPv[1], posStart[2]+valPv[2]]
            pozMiddl=[(posStart[0]+pozEnd[0])/2, (posStart[1]+pozEnd[1])/2, (posStart[2]+pozEnd[2])/2]
              
            posIkDefJnt = cmds.joint (p=posIkDef, children=False) 
            jntPV = cmds.joint (p=pozMiddl)
            jntPVEnd = cmds.joint (p=pozMiddl)
            
            cmds.aimConstraint (target, jntPV, aim =[1, 0, 0], u =[0, 0, 1], wut="object", wuo= posIkDefJnt )
            cmds.setAttr (jntPVEnd+'.translateZ', abs(cmds.getAttr (tmpJnt[1]+".tx")))
            cmds.delete (cmds.pointConstraint (jntPVEnd, self.oriGrp),tmpJnt, posIkDefJnt)
            
    def an_setRotOrder(self):
        def setOrder(contr, rOrd):
            rotOrdVal = {"xyz":0, "yzx":1, "zxy":2, "xzy":3, "yxz":4, "zyx":5}
            if cmds.objExists(contr): cmds.setAttr( contr+'.rotateOrder', rotOrdVal[rOrd] )
    
        setOrder (chn('').general[1],       "zxy")            # general_CT                 
        setOrder (chn('').general[2],       "zxy")            # pivotOffset_CT
        setOrder (chn('').body[0],          "zxy")            # body_CT
        setOrder (chn('').body[1],          "zxy")            # hips_CT 
        setOrder (chn('').body[2],          "zxy")            # dw_waist_CT
        setOrder (chn('').body[3],          "zxy")            # up_waist_CT  
        setOrder (chn('').body[4],          "zxy")            # torso_CT 
        setOrder (chn('').body[5],          "zxy")            # shoulders_CT
        setOrder (chn('').neck[0],          "zxy")            # neck_CT
        setOrder (chn('').head[0],          "zxy")            # head_CT
        
        for side in ('l_', 'r_'):
            setOrder (side+chn('').getArm()[5],       "zxy")            # shoulder_CT  
            setOrder (side+chn('').getArm()[1],       "yxz")            # handIk_CT                   
            setOrder (side+chn('').getArm()[2],       "xzy")            # upArm_CT
            setOrder (side+chn('').getArm()[3],       "xyz")            # foreArm_CT
            setOrder (side+chn('').getArm()[4],       "yzx")            # hand_CT
            
            setOrder (side+chn('').getLeg()[1],       "zxy")            # footIk_CT                     
            setOrder (side+chn('').getLeg()[2],       "xyz")            # upLeg_CT
            setOrder (side+chn('').getLeg()[3],       "xyz")            # knee_CT
            setOrder (side+chn('').getLeg()[4],       "zxy")            # foot_CT
            
            [ setOrder (side+x,  "zxy") for x in chn('').getFingers()[1]] # thumb_CT   
            [ setOrder (side+x,  "zxy") for x in chn('').getFingers()[2]] # index_CT
            [ setOrder (side+x,  "zxy") for x in chn('').getFingers()[3]] # middle_CT
            [ setOrder (side+x,  "zxy") for x in chn('').getFingers()[4]] # ring_CT
            [ setOrder (side+x,  "zxy") for x in chn('').getFingers()[5]] # pinky_CT
        
    def pointCordList (self):  # return coor
        vLisr = self.pointList() 
        def an_pointCoord(vPoint):   #get point coordinates 
            return [ round((cmds.getAttr (vPoint+'.'+vEacchCord+'Value')), 3)for vEacchCord in  ('x', 'y', 'z')] 
        rez = []
        for eachList in vLisr: rez.append ([an_pointCoord(vVertx) for vVertx in  eachList])
        return rez

    """
    def an_convertPointList (self): #print short list of point coord
    
        rez = []
        for  eachList in  self.pointCordList ():
            curvRez= []
            for each in eachList:
                pointCor = []
                for val in each:
                    if 'e' in str(val):pointCor.append('0')
                    else: pointCor.append(str(val)[:5])
                curvRez.append(pointCor)    
            rez.append(curvRez)         
        print rez
    """
   

 
#a = ['fds', 'fgsdaf', 10]
#print ('%s'%a)
 
 
              
#ctrl('').an_setRotOrder()
################################################################################################################################################################################## 
#an_distans('l_ggg1', 'l_ggg3', act='tt')


#ff =  An_Controllers('jjj2')
#ff.makeSpherAndOrientAxis()


#ff.an_setRotOrder( )
#ff.gropeCT()
 
#ff.placeCT ('r_ggg1', tape = "polyVector")




#ff.makeOrientAxis(3)
 
#  ff.addColor ( color='left')


#ff.pointCordList ()


 


#  ff.makeController( 'headAim' ) 

 


#ff.rotateCt ([-90, -90, 0])

 
 
