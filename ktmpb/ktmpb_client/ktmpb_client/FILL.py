import kautham_python_interface as kautham
import ktmpb_python_interface

import xml.etree.ElementTree as ET
from collections import defaultdict

global path
global fill
fill = defaultdict(lambda: defaultdict(dict))


def FILL(node, fill, info, Line):
    print("**************************************************************************")
    print("  FILL ACTION  ")
    print("**************************************************************************")
    action = Line[0]
    rob = Line[1]
    obstacle = Line[2]
    
    print(f"Executing {action} for robot {rob} and object {obstacle}")
    
    # Inicializar variables
    try:
        init = fill['InitControls']
        goal = fill['GoalControls']
        Robot_control = fill['Cont']
    except KeyError as e:
        print(f"Error: Campo faltante en los datos de FILL: {e}")
        return False
    
    print("Init= ", init)
    print("Goal= ", goal)


    info.Robot_move_control= Robot_control
    print("Robot control= ", Robot_control)
    
    # Configurar control del robot
    kautham.kSetRobControlsNoQuery(node, Robot_control)
    
    # Configurar la consulta de movimiento en Kautham
    kautham.kSetQuery(node, init, goal)
    print("Solving Query")
    kautham.kSetPlannerParameter(node, "_Incremental (0/1)", "0")  # Planificación desde cero
    
    path = kautham.kGetPath(node, 1)
    
    if path:
        print("-------- Path found: Filling action ")
        # Escribir el path en el archivo de tareas
        info.taskfile.write("\t<Transit>\n")
        
        k = sorted(list(path.keys()))[-1][1] + 1  # número de articulaciones
        p = sorted(list(path.keys()))[-1][0] + 1  # número de puntos en el path
        for i in range(p):
            tex = ''
            for j in range(0, k):
                tex = tex + str(path[i, j]) + " "
            ktmpb_python_interface.writePath(info.taskfile, tex)
        
        info.taskfile.write("\t</Transit>\n")
        
        # Mover el robot al estado objetivo
        kautham.kMoveRobot(node, goal)
    else:
        print("**************************************************************************")
        print("Get path Failed! No Fill possible, Infeasible Task Plan")
        print("**************************************************************************")
        return False
    

    # Configurar control del robot
    kautham.kSetRobControlsNoQuery(node, Robot_control)
    
    # Configurar la consulta de movimiento en Kautham
    kautham.kSetQuery(node, goal, init)
    print("Solving Query")
    kautham.kSetPlannerParameter(node, "_Incremental (0/1)", "0")  # Planificación desde cero
    
    path = kautham.kGetPath(node, 1)
    
    if path:
        print("-------- Path found: Filling action ")
        # Escribir el path en el archivo de tareas
        info.taskfile.write("\t<Transit>\n")
        
        k = sorted(list(path.keys()))[-1][1] + 1  # número de articulaciones
        p = sorted(list(path.keys()))[-1][0] + 1  # número de puntos en el path
        for i in range(p):
            tex = ''
            for j in range(0, k):
                tex = tex + str(path[i, j]) + " "
            ktmpb_python_interface.writePath(info.taskfile, tex)
        
        info.taskfile.write("\t</Transit>\n")
        
        # Mover el robot al estado objetivo
        kautham.kMoveRobot(node, goal)
        
    else:
        print("**************************************************************************")
        print("Get path Failed! No Fill possible, Infeasible Task Plan")
        print("**************************************************************************")
        return False

    return True

def Fill_read(action_element):  # Leer datos de la configuración
    for val in action_element.attrib:
        globals()[val] = action_element.attrib[val]

    fill = {}

    for el in action_element:
        try:
            globals()[el.tag] = int(el.text)
        except:
            try:
                globals()[el.tag] = [float(f) for f in str(el.text).strip().split()]
            except:
                globals()[el.tag] = str(el.text).strip()
        fill.update({el.tag: globals()[el.tag]})

    return fill
