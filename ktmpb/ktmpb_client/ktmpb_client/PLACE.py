import kautham_python_interface as kautham
import ktmpb_python_interface

import xml.etree.ElementTree as ET
from collections import defaultdict

global path
global serve
serve = defaultdict(lambda: defaultdict(dict))

def SERVE(node, serve, info, Line):  # Management of the action on the task plan
    print("**************************************************************************")
    print("  SERVE ACTION  ")
    print("**************************************************************************")
    action = Line[0]
    rob = Line[1]
    obstacle = Line[2]
    toLocation = Line[3]

    print(action + " " + rob + " " + obstacle + " " + toLocation)
    obsName = serve['Obj']  # Object name
    robotIndex = serve['Rob']  # Robot index
    linkIndex = serve['Link']  # Link index for attachment
    Robot_control = serve['Cont']
    init = serve['Regioncontrols']
    goal = serve['Graspcontrols']

    # Set robot control
    kautham.kSetRobControlsNoQuery(node, Robot_control)

    # Simulate grasping the object
    print(f"Grasping object {obsName} using link {linkIndex}...")
    kautham.kAttachObject(node, robotIndex, linkIndex, obsName)

    # Move to the goal location
    print(f"Moving to {toLocation} with object {obsName}...")
    kautham.kSetQuery(node, init, goal)
    kautham.kSetPlannerParameter(node, "_Incremental (0/1)", "0")
    path = kautham.kGetPath(node, 1)

    if path:
        print("-------- Path found: Moving to the serving location.")
        info.taskfile.write("\t<Transfer>\n")
        k = sorted(list(path.keys()))[-1][1] + 1  # Number of joints
        p = sorted(list(path.keys()))[-1][0] + 1  # Number of points in the path
        for i in range(p):
            tex = ''
            for j in range(0, k):
                tex = tex + str(path[i, j]) + " "
            ktmpb_python_interface.writePath(info.taskfile, tex)
        info.taskfile.write("\t</Transfer>\n")
        kautham.kMoveRobot(node, goal)
    else:
        print("**************************************************************************")
        print("Get path Failed! No Serve possible, Infeasible Task Plan")
        print("**************************************************************************")
        return False

    # Simulate detaching the object
    print(f"Serving object {obsName} at {toLocation} by detaching...")
    kautham.kDetachObject(node, obsName)

    print("SERVE action completed.")
    return True

def Serve_read(action_element):  # Reading from the tamp configuration file
    for val in action_element.attrib:
        globals()[val] = action_element.attrib[val]

    serve = {}
    for el in action_element:
        try:
            globals()[el.tag] = int(el.text)
        except:
            try:
                globals()[el.tag] = [float(f) for f in str(el.text).strip().split()]
            except:
                globals()[el.tag] = str(el.text).strip()
        serve.update({el.tag: globals()[el.tag]})

    return serve
