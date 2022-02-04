import maya.cmds as cmds

# this is the function for making window
def makeWindow():
    winName="TreadBuilder"
    if cmds.window(winName,q=True,exists=True):
        cmds.deleteUI(winName)
    #now we are gonna make a window
    cmds.window(winName)
    cmds.columnLayout()
    cmds.text(l="welcome to the treadmaker")
    cmds.separator(w=200)
    makeWindow.initBtn=cmds.button(l="Initialize",c="initFunc()")
    makeWindow.ResetBtn=cmds.button(l="reset",c="ResetLoc()",en=False)
    cmds.separator(w=400)
    makeWindow.MakeCurveBtn=cmds.button(l="Make tread Curve",c="MakeCurve()",vis=False)
    cmds.separator(w=400)
    makeWindow.ObjText=cmds.textFieldButtonGrp(bl="Pick Tread OBJ",bc="PickingObj()",ed=False)
    cmds.separator(w=400)
    makeWindow.CopyNum=cmds.intSliderGrp(min=10,max=500,v=35,f=True,cc="numChange()")
    cmds.button(l="Make Tread",c="MakeTankTread()")
    cmds.showWindow()
    
#we want to make sure either the user knows the direction or not
confirmVar=cmds.confirmDialog(t="before anything",m="please ensure your model in placed along Z axis",b=['yes','no'],db='yes',cb='no')
print (confirmVar)
if confirmVar=='no':
    cmds.confirmDialog(m="then you must reorient your model on Z axis")
else:
    makeWindow()

#start of all functions
def initFunc(): # this function initializes the process by dumping two locators for the user
    initFunc.frontLocator=cmds.spaceLocator(n="CircleLocFront")
    cmds.scale(5,5,5)
    cmds.move(0,0,10,r=True)
    initFunc.backLocator=cmds.spaceLocator(n="CircleLocBack")
    cmds.scale(5,5,5)
    cmds.confirmDialog(m="you now have two locators. place them where you want according to your model need")
    cmds.button(makeWindow.initBtn,edit=True,en=False)
    cmds.button(makeWindow.ResetBtn,edit=True,en=True)
    cmds.button(makeWindow.MakeCurveBtn,edit=True,vis=True)

def ResetLoc(): #this function deletes the two locator created
    cmds.delete([initFunc.frontLocator[0],initFunc.backLocator[0]])
    cmds.delete(MakeCurve.treadCurve)
    cmds.delete("locGroup")
    cmds.button(makeWindow.initBtn,edit=True,en=True)
    cmds.button(makeWindow.ResetBtn,edit=True,en=False)
    cmds.button(makeWindow.MakeCurveBtn,edit=True,vis=False)
    
def MakeCurve(): #this function creates curve based one the two locators
    cmds.select(initFunc.frontLocator)
    FrontLocPos=cmds.getAttr(".translateZ")
    cmds.select(initFunc.backLocator)
    BackLocPos=cmds.getAttr(".translateZ")
    print (FrontLocPos)
    print (BackLocPos)
    LocDistance=abs(FrontLocPos-BackLocPos)
    print ("the total distance is: %s" %LocDistance)
    curveRadius=LocDistance/2
    MakeCurve.treadCurve=cmds.circle(n="TreadCurve",r=curveRadius,nr=(1,0,0))
    cmds.group(initFunc.frontLocator,initFunc.backLocator,n="locGroup")
    cmds.select(MakeCurve.treadCurve,r=True)
    cmds.select("locGroup",add=True)
    cmds.align(z="mid", atl=True)
    cmds.select(MakeCurve.treadCurve)
    cmds.FreezeTransformations()
    
def PickingObj(): #this function identifies the tread object
    global selectedOBJ
    selectedOBJ=cmds.ls(sl=True,o=True)
    print (selectedOBJ[0])
    cmds.textFieldButtonGrp(makeWindow.ObjText,e=True,tx=selectedOBJ[0])
    return selectedOBJ

def numChange(): #this function sends out the numebr of copy set by the user
    if cmds.objExists("TreadFull"):
        cmds.delete("TreadFull")
    if cmds.objExists("_wire"):
        cmds.delete("_wire")
    
    global updateCopyNum
    updateCopyNum=cmds.intSliderGrp(makeWindow.CopyNum,query=True,v=True)
    print (updateCopyNum)
    #animating the picked obj around the path
    cmds.select(selectedOBJ,r=True)
    cmds.select(MakeCurve.treadCurve,add=True)
    cmds.pathAnimation(f=True,fa="z",ua="y",wut="vector",wu=(0,1,0),inverseFront=False,iu=False,b=False,stu=1,etu=updateCopyNum)
    cmds.select(selectedOBJ,r=True)
    cmds.selectKey("motionPath1_uValue",time=(1,updateCopyNum))
    cmds.keyTangent(itt="linear",ott="linear")
    cmds.snapshot(n="TreadSS",i=1,ch=False,st=1,et=updateCopyNum,u="animCurve")
    cmds.DeleteMotionPaths()
    #now we combine all duplicated and delete the Sanpshot
    cmds.select("TreadSSGroup",r=True)
    cmds.polyUnite(n="TreadFull",ch=False)
    cmds.select("TreadSSGroup",r=True)
    cmds.delete()
    def createWireD(geo,wireCRV,dropoffDist=40):
        wire=cmds.wire(geo,w=wireCRV,n="_wire")
        wirenode=wire[0]
        cmds.setAttr(wirenode+".dropoffDistance[0]",dropoffDist)
        
    cmds.select("TreadFull")
    wireObj=cmds.ls(sl=True,o=True)[0]
    cmds.select(MakeCurve.treadCurve)
    wirecurve=cmds.ls(sl=True,o=True)[0]
    createWireD(wireObj,wirecurve)
    
    return updateCopyNum
    

def MakeTankTread(): #this function uses the picked obj and the numebr of copies and makes treads
#animating the picked obj around the path
    cmds.select(selectedOBJ,r=True)
    cmds.select(MakeCurve.treadCurve,add=True)
    cmds.pathAnimation(f=True,fa="z",ua="y",wut="vector",wu=(0,1,0),inverseFront=False,iu=False,b=False,stu=1,etu=updateCopyNum)
    cmds.select(selectedOBJ,r=True)
    cmds.selectKey("motionPath1_uValue",time=(1,updateCopyNum))
    cmds.keyTangent(itt="linear",ott="linear")
    cmds.snapshot(n="TreadSS",i=1,ch=False,st=1,et=updateCopyNum,u="animCurve")
    cmds.DeleteMotionPaths()
    #now we combine all duplicated and delete the Sanpshot
    cmds.select("TreadSSGroup",r=True)
    cmds.polyUnite(n="TreadFull",ch=False)
    cmds.select("TreadSSGroup",r=True)
    cmds.delete()
    def createWireD(geo,wireCRV,dropoffDist=40):
        wire=cmds.wire(geo,w=wireCRV,n="_wire")
        wirenode=wire[0]
        cmds.setAttr(wirenode+".dropoffDistance[0]",dropoffDist)
        
    cmds.select("TreadFull")
    wireObj=cmds.ls(sl=True,o=True)[0]
    cmds.select(MakeCurve.treadCurve)
    wirecurve=cmds.ls(sl=True,o=True)[0]
    createWireD(wireObj,wirecurvew)
    













