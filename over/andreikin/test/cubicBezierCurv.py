import maya.cmds as cmds


def cubicBezierCurv( point0=(0,0),  point1=(1,1), point2=(2,2), point3=(3,3), vertexNumber=4): # make linear Bezier Curve in 2d space
    tList = [x/float(vertexNumber)  for x in xrange(0,vertexNumber)]   #define list of t values
    tList.append(1.0)
    xCoord = [pow((1-t),3)*point0[0] + 3*pow((1-t),2)*t*point1[0] + 3*(1-t)*pow(t,2)*point2[0] + pow(t,3)*point3[0] for t in tList ] 
    yCoord = [pow((1-t),3)*point0[1] + 3*pow((1-t),2)*t*point1[1] + 3*(1-t)*pow(t,2)*point2[1] + pow(t,3)*point3[1] for t in tList ]
    return zip (xCoord, yCoord)    
 
 
def getValFromBezierCurv ( xVal, points=[(0,0), (0,1), (2,2), (3,3)], vNumber=20):

    if xVal>points[3][0]: return points[3][1]
    if xVal<points[0][0]: return points[0][1]
    tList = [x/float(vNumber)  for x in xrange(0,vNumber)]   #define list of t values
    tList.append(1.0)
    xCoord = [pow((1-t),3)*points[0][0] + 3*pow((1-t),2)*t*points[1][0] + 3*(1-t)*pow(t,2)*points[2][0] + pow(t,3)*points[3][0] for t in tList ] 
    yCoord = [pow((1-t),3)*points[0][1] + 3*pow((1-t),2)*t*points[1][1] + 3*(1-t)*pow(t,2)*points[2][1] + pow(t,3)*points[3][1] for t in tList ]
    cord = zip (xCoord, yCoord) #define Bezier Curve points
    if xVal in xCoord: return dict(cord)[xVal]
    #cmds.curve (p=[ (x[0], 0, x[1]) for x in cord], d=1 ) 
    xMaxVal=min([x[0] for x  in cord if x[0]>xVal ])#get 
    xMinVal=max([x[0] for x  in cord if x[0]<xVal ])
    yMaxVal= dict(cord)[xMaxVal]
    yMinVal= dict(cord)[xMinVal]
    koff=  (xVal-xMinVal)/(xMaxVal-xMinVal)
    return ((yMaxVal-yMinVal)* koff)+yMinVal #return y value


"""
cmds.delete ('out_input1Y')
for coord in cubicBezierCurv( point0=(1,0),   point1=(1.07, 0.05),   point2=(1.065, 1.05),   point3=(1.25,  1), vertexNumber=20):
    cmds.setDrivenKeyframe ('out.input1Y', cd='in1.outputY', dv=coord[0], v=coord[1]) # mack anim curve





getValFromBezierCurv (0.18, points=[(0,0), (0,2), (3,0), (3,2)], vNumber=20)


 




v1= 10
v2= 5
mix = 0
output = v1*mix+v2*(1-mix)
print output
"""