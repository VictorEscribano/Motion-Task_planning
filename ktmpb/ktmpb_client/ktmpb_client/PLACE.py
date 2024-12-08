import kautham_python_interface as kautham
import ktmpb_python_interface

#from ktmpb_python_interface  import writePath
#from ktmpb_python_interface  import computeGraspControls

import xml.etree.ElementTree as ET
from collections import defaultdict

global path
global path_r
global place
place = defaultdict(lambda: defaultdict(dict))

def PLACE(node,place,info,Line):  #management of the action on the task plan
    print("**************************************************************************")
    print("  PLACE ACTION  ")
    print("**************************************************************************")
    action=Line[0]
    rob= Line[1]
    obstacle = Line[2]
    toLocation = Line[3]
    
    print(action +" "+rob+" "+obstacle+" "+toLocation)
    obsName = place['Obj'] #Obj_name 
    robotIndex = place['Rob'] #Robot_name 
    init = place['Regioncontrols']
    Robot_control=place['Cont']
    #Set robot control
    kautham.kSetRobControlsNoQuery(node,Robot_control)

    if 'Graspcontrols' in place.keys():
        print(info.graspControlsUsed)
        print(place['Graspcontrols'])
        print(place['Graspcontrols'][info.graspControlsUsed])
        goal = place['Graspcontrols'][info.graspControlsUsed]
        #Set the move query in Kautham
        print("Searching path to Move to the location where object must be placed - using graspcontrols = ", info.graspControlsUsed)
        print("Init= ", init)
        print("Goal= ", goal)
        print("Robot Control=",Robot_control)
        #Set robot control
        kautham.kSetRobControlsNoQuery(node,Robot_control)
        kautham.kSetQuery(node,init,goal)
        #Solve query
        print("Solving query to place object")
        kautham.kSetPlannerParameter(node,"_Incremental (0/1)","0") #to assure a fresh GetPath
        path=kautham.kGetPath(node,1)
        #Write path to task file
        if path:
            print("TASKFILE WRITING ---- ")
            print("-------- Path found: Moving to the location where object must be placed " )
            #finish transfer
            k = sorted(list(path.keys()))[-1][1]+1 #number of joints
            p = sorted(list(path.keys()))[-1][0]+1 #number of points in the path
            for i in range(p): #for i=0 to i=p-1
                tex=''
                for j in range(0,k):
                    tex=tex + str(path[i,j]) + " "
                ktmpb_python_interface.writePath(info.taskfile,tex)
            info.taskfile.write("\t</Transfer>\n")
            kautham.kMoveRobot(node,goal)
            info.graspedobject= False
            #return
        else:
            print("**************************************************************************")
            print("Get Path failed. No MOVE TO PLACE possible. Infeasible TASK PLAN")
            print("**************************************************************************")
            return False
        
    #Set Place query to kautham
    print("Placing object ",obsName)
    kautham.kDetachObject(node,obsName)
    #Move back to the home configuration of the region without the object
    print("-Searching path to Move back to the home configuration of the region")
    print("Init= ", goal)
    print("Goal= ", init)
    print("Robot Control=",Robot_control)
    #Set robot control
    kautham.kSetRobControlsNoQuery(node,Robot_control)
    kautham.kSetQuery(node,goal,init)
    kautham.kSetPlannerParameter(node,"_Incremental (0/1)","0") #to assure a fresh GetPath
    path_r=kautham.kGetPath(node,1)
    if path_r:
        print("-------- Path found: Moving to the home configuration of the region " )
        kautham.kMoveRobot(node,init)
        info.taskfile.write("\t<Transit>\n")
        k = sorted(list(path_r.keys()))[-1][1]+1 #number of joints
        p = sorted(list(path_r.keys()))[-1][0]+1 #number of points in the path
        for i in range(p):
            tex=''
            for j in range(0,k):
                tex=tex + str(path_r[i,j]) + " "
            ktmpb_python_interface.writePath(info.taskfile,tex)
        info.taskfile.write("\t</Transit>\n")
    else:
        print("**************************************************************************")
        print("Get path Failed! No Move possible after Place process, Infeasible Task Plan")
        print("**************************************************************************")
        return False

    return True

def Place_read(action_element): #reading from the tamp configuration file

    for val in action_element.attrib:
        globals()[val] = action_element.attrib[val]

    place = {}
    grasp={}

    for el in action_element:
        try:
            globals()[el.tag] = int(el.text)
        except:
            try:
                globals()[el.tag] = [float(f) for f in str(el.text).strip().split()]
            except:
                globals()[el.tag] = str(el.text).strip()
        if el.tag == 'Graspcontrols': #variables with multiple entries should be added the same way
            grasp_name = el.get('grasp')
            graspcontrol= el.text
            graspcontrol=[float(f) for f in graspcontrol.split()]
            grasp[grasp_name]= graspcontrol
            globals()[el.tag] = grasp

        place.update({el.tag : globals()[el.tag]})

    return place
