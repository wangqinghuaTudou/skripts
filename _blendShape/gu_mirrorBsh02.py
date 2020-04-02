import maya.cmds as mc
import math as mat


def gu_mirrorBsh02():

	wind=mc.window(title='mirror Bsh point to point',iconName='mirrorBsh',widthHeight=(300,80))
	mc.columnLayout( adjustableColumn=True )
	mc.text('select geometry for get points ')
	mc.separator ( h=10)
	mc.separator (st="none", h=10)
	mc.button( label='get points', command=('get_points(mc.ls(sl=True))') )
	mc.button( label='mirror geo', command=('gu_mirrorBsh(mc.ls(sl=True))') )

	mc.showWindow(wind)
	vert=[]
	vertexes=[]
	similarPoints=[]

##############################################################################################################
def get_points(selGeo):
	vert=mc.getAttr(mc.listRelatives(selGeo[0],c=True,type='mesh')[0]+'.vrts',mi=True) #getPuints on object
	dobjPoz=mc.xform(selGeo[0],t=True,ws=True,q=True)
	mc.xform(selGeo[0],t=(0,0,0),ws=True)
	pozPoints=mc.xform(selGeo[0]+'.vtx[*]',q=True,t=True,ws=True) #get Puints position in world
	pozPointsX=pozPoints[::3]
	pozPointsY=pozPoints[1::3]
	pozPointsZ=pozPoints[2::3]
	for i in vert:     #exclude negative to X vertexes. and search "brotherly" points
		if pozPointsX[i] > -0.1:
			tempSize=[]
			tempVrt=[]
			for a in vert:
				if pozPointsX[a] < 0.1:
					tempSize.append(mat.sqrt(mat.pow(pozPointsX[i]-(-1*pozPointsX[a]),2)+ mat.pow(pozPointsY[i]-pozPointsY[a],2)+ mat.pow(pozPointsZ[i]-pozPointsZ[a],2)))
					tempVrt.append([i,a])
			if tempSize:
				vertexes.append(tempVrt[tempSize.index(min(tempSize))])
	mc.xform(selGeo[0],t=(dobjPoz[0],dobjPoz[1],dobjPoz[2]),ws=True)
##################################################################################################
def gu_mirrorBsh(sel):
	for i in sel:
		pref=[]
		if i[:2]=='r_':
			pref='l_'
		else:
			if i[:2]=='R_':
				pref='L_'
			else:
				if i[:2]=='l_':
					pref='r_'
				else:
					if i[:2]=='L_':
						pref='R_'
					else:
						pref='new_'
		new=mc.duplicate(i,n=pref+i[2:])
		poz=mc.xform(new[0],t=True,q=True,ws=True)
		mc.xform(new[0],t=(0,0,0),ws=True)
		getPoz=mc.xform(new[0]+'.vtx[*]',t=True,q=True,ws=True)
		getPozX=getPoz[::3]
		getPozY=getPoz[1::3]
		getPozZ=getPoz[2::3]
		for i in vertexes:
			mc.xform(new[0]+'.vtx['+str(i[1])+']',t=(getPozX[i[0]]*-1,getPozY[i[0]],getPozZ[i[0]]),ws=True)
			mc.xform(new[0]+'.vtx['+str(i[0])+']',t=(getPozX[i[1]]*-1,getPozY[i[1]],getPozZ[i[1]]),ws=True)
		mc.xform(new[0],t=(poz[0]*-1,poz[1],poz[2]),ws=True)