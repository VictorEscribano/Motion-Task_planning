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

    print(action + " " + rob + " " + obstacle)
    obsName = serve['Obj']  # Object name
    robotIndex = serve['Rob']  # Robot index
    Robot_control = serve['Cont']
    init = serve['InitControls']
    goal = serve['GoalControls']

    # Set robot control
    kautham.kSetRobControlsNoQuery(node, Robot_control)

    # Attach the object at the initial location
    print(f"Attaching object {obsName} at the initial location...")
    kautham.kAttachObject(node, robotIndex, 14, obsName)  # Assuming link 14, update if needed

    # Move from initial to goal location
    print(f"Moving from {init} to {goal} with object {obsName}...")
    kautham.kSetQuery(node, init, goal)
    kautham.kSetPlannerParameter(node, "_Incremental (0/1)", "0")
    path = kautham.kGetPath(node, 1)

    if path:
        print("-------- Path found: Moving to the goal location.")
        info.taskfile.write("\t<Serve>\n")
        k = sorted(list(path.keys()))[-1][1] + 1  # Number of joints
        p = sorted(list(path.keys()))[-1][0] + 1  # Number of points in the path
        for i in range(p):
            tex = ''
            for j in range(0, k):
                tex = tex + str(path[i, j]) + " "
            ktmpb_python_interface.writePath(info.taskfile, tex)
        info.taskfile.write("\t</Serve>\n")
        kautham.kMoveRobot(node, goal)
    else:
        print("**************************************************************************")
        print("Get path Failed! No Serve possible, Infeasible Task Plan")
        print("**************************************************************************")
        return False

    # Detach the object at the goal location
    print(f"Detaching object {obsName} at the goal location...")
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
