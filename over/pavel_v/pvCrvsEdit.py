source, dest = ls(sl=True)
for i in range(10,4,-1):
    tx = getAttr (source + '.controlPoints[%s].xValue'%i)
    setAttr (dest + '.controlPoints[%s].xValue'%i, tx)
    ty = getAttr (source + '.controlPoints[%s].yValue'%i)
    setAttr (dest + '.controlPoints[%s].yValue'%i, ty)
    tz = getAttr (source + '.controlPoints[%s].zValue'%i)
    setAttr (dest + '.controlPoints[%s].zValue'%i, tz)

lSide = ls(sl=True)[0]
rSide = lSide.replace('l_','r_')
chLs = listRelatives(lSide, c=True)
chRs = listRelatives(rSide, c=True)
for cl,cr in zip(chLs, chRs):
    if 'cheek' in cl:
        for i in range(0, 9):
            tx = getAttr (cl + '.controlPoints[%s].xValue'%i)
            setAttr (cr + '.controlPoints[%s].xValue'%i, -tx)
            ty = getAttr (cl + '.controlPoints[%s].yValue'%i)
            setAttr (cr + '.controlPoints[%s].yValue'%i, ty)
            tz = getAttr (cl + '.controlPoints[%s].zValue'%i)
            setAttr (cr + '.controlPoints[%s].zValue'%i, tz)
    if 'lip' in cl:
        for i,j in zip(range(0, 11), range(10,-1,-1)):
            print i, j
            tx = getAttr (cl + '.controlPoints[%s].xValue'%i)
            setAttr (cr + '.controlPoints[%s].xValue'%j, -tx)
            ty = getAttr (cl + '.controlPoints[%s].yValue'%i)
            setAttr (cr + '.controlPoints[%s].yValue'%j, ty)
            tz = getAttr (cl + '.controlPoints[%s].zValue'%i)
            setAttr (cr + '.controlPoints[%s].zValue'%j, tz)

source, dest = ls(sl=True)
for i in range(0,6):
    tx = getAttr (source + '.controlPoints[%s].xValue'%i)
    setAttr (dest + '.controlPoints[%s].xValue'%i, tx)
    ty = getAttr (source + '.controlPoints[%s].yValue'%i)
    setAttr (dest + '.controlPoints[%s].yValue'%i, ty)
    tz = getAttr (source + '.controlPoints[%s].zValue'%i)
    setAttr (dest + '.controlPoints[%s].zValue'%i, tz)

source, dest = ls(sl=True)
if 'cheek' in source:
    for i in range(0, 5):
        tx = getAttr (source + '.controlPoints[%s].xValue'%i)
        setAttr (dest + '.controlPoints[%s].xValue'%i, tx)
        ty = getAttr (source + '.controlPoints[%s].yValue'%i)
        setAttr (dest + '.controlPoints[%s].yValue'%i, ty)
        tz = getAttr (source + '.controlPoints[%s].zValue'%i)
        setAttr (dest + '.controlPoints[%s].zValue'%i, tz)
if 'lip' in source:
    for i in range(0, 11):
        tx = getAttr (source + '.controlPoints[%s].xValue'%i)
        setAttr (dest + '.controlPoints[%s].xValue'%i, tx)
        ty = getAttr (source + '.controlPoints[%s].yValue'%i)
        setAttr (dest + '.controlPoints[%s].yValue'%i, ty)
        tz = getAttr (source + '.controlPoints[%s].zValue'%i)
        setAttr (dest + '.controlPoints[%s].zValue'%i, tz)

cl = mc.ls(sl=True)[0]
cr = cl.replace('l_','r_')
if 'cheek' in cl:
    for i in range(0, 9):
        tx = mc.getAttr (cl + '.controlPoints[%s].xValue'%i)
        mc.setAttr (cr + '.controlPoints[%s].xValue'%i, -tx)
        ty = mc.getAttr (cl + '.controlPoints[%s].yValue'%i)
        mc.setAttr (cr + '.controlPoints[%s].yValue'%i, ty)
        tz = mc.getAttr (cl + '.controlPoints[%s].zValue'%i)
        mc.setAttr (cr + '.controlPoints[%s].zValue'%i, tz)
if 'lip' in cl:
    for i,j in zip(range(0, 11), range(10,-1,-1)):
        print i, j
        tx = mc.getAttr (cl + '.controlPoints[%s].xValue'%i)
        mc.setAttr (cr + '.controlPoints[%s].xValue'%j, -tx)
        ty = mc.getAttr (cl + '.controlPoints[%s].yValue'%i)
        mc.setAttr (cr + '.controlPoints[%s].yValue'%j, ty)
        tz = mc.getAttr (cl + '.controlPoints[%s].zValue'%i)
        mc.setAttr (cr + '.controlPoints[%s].zValue'%j, tz)