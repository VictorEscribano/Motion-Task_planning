import kautham_python_interface as kautham
import ktmpb_python_interface

import xml.etree.ElementTree as ET
from collections import defaultdict

global path
global fill
fill = defaultdict(lambda: defaultdict(dict))

def FILL(node, fill, info, Line):  # Management of the action on the task plan
    print("**************************************************************************")
    print("  FILL ACTION  ")
    print("**************************************************************************")
    action = Line[0]
    rob = Line[1]
    obstacle = Line[2]
    region = Line[3]

    print(action + " " + rob + " " + obstacle + " " + region)
    obsName = fill['Obj']  # Object name
    Robot_control = fill['Cont']
    init = fill['Regioncontrols']

    # Set robot control
    kautham.kSetRobControlsNoQuery(node, Robot_control)

    if 'Graspcontrols' in fill.keys():
        grasp_control = fill['Graspcontrols']
        for grasp in grasp_control.keys():
            goal = grasp_control[str(grasp)]
            print(f"Attempting grasp for {obsName} with configuration: {grasp}")
            print("Init= ", init)
            print("Goal= ", goal)

            # Set the move query in Kautham
            kautham.kSetQuery(node, init, goal)
            kautham.kSetPlannerParameter(node, "_Incremental (0/1)", "0")  # Ensure fresh query
            path = kautham.kGetPath(node, 1)

            if path:
                print(f"-------- Path found: Performing the fill action for {obsName}.")
                info.taskfile.write("\t<Filling>\n")
                k = sorted(list(path.keys()))[-1][1] + 1  # Number of joints
                p = sorted(list(path.keys()))[-1][0] + 1  # Number of points in the path
                for i in range(p):
                    tex = ''
                    for j in range(0, k):
                        tex = tex + str(path[i, j]) + " "
                    ktmpb_python_interface.writePath(info.taskfile, tex)
                info.taskfile.write("\t</Filling>\n")
                kautham.kMoveRobot(node, goal)
                print(f"Filling action completed for {obsName} at {region}.")
                break
            else:
                print(f"**************************************************************************")
                print(f"Get path Failed! Unable to fill {obsName} with grasp {grasp}. Trying next grasp configuration.")
                print(f"**************************************************************************")
        else:
            print(f"No valid grasp configuration found for {obsName}. FILL action aborted.")
            return False
    else:
        print("No grasp controls found in configuration for FILL action.")
        return False

    return True

def Fill_read(action_element):  # Reading from the tamp configuration file
    for val in action_element.attrib:
        globals()[val] = action_element.attrib[val]

    fill = {}
    grasp = {}

    for el in action_element:
        try:
            globals()[el.tag] = int(el.text)
        except:
            try:
                globals()[el.tag] = [float(f) for f in str(el.text).strip().split()]
            except:
                globals()[el.tag] = str(el.text).strip()
        if el.tag == 'Graspcontrols':  # Variables with multiple entries should be added the same way
            grasp_name = el.get('grasp')
            graspcontrol = el.text
            graspcontrol = [float(f) for f in graspcontrol.split()]
            grasp[grasp_name] = graspcontrol
            globals()[el.tag] = grasp

        fill.update({el.tag: globals()[el.tag]})

    return fill
