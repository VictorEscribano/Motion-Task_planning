import kautham_python_interface as kautham
import ktmpb_python_interface

import xml.etree.ElementTree as ET
from collections import defaultdict

global path
global serve
serve = defaultdict(lambda: defaultdict(dict))


def SERVE(node, serve, info, Line):
    print("**************************************************************************")
    print("  SERVE ACTION  ")
    print("**************************************************************************")
    action = Line[0]
    rob = Line[1]
    obstacle = Line[2]
    destination = Line[3]

    print(f"Executing {action} for robot {rob}, object {obstacle}, to destination {destination}")

    # Inicializar variables
    try:
        obsName = serve['Obj']  # Nombre del objeto
        robotIndex = serve['Rob']  # Índice del robot
        init = serve['InitControls']  # Configuración inicial
        goal = serve['GoalControls']  # Configuración final
        Robot_control = serve['Cont']  # Archivo de control del robot
    except KeyError as e:
        print(f"Error: Campo faltante en los datos de SERVE: {e}")
        return False

    print("Init= ", init)
    print("Goal= ", goal)
    print("Robot control= ", Robot_control)

    # Configurar control del robot
    kautham.kSetRobControlsNoQuery(node, Robot_control)

    # Adjuntar el objeto
    print(f"Acoplando objeto {obsName} al robot...")
    kautham.kAttachObject(node, robotIndex, 14, obsName)

    # Configurar la consulta de movimiento en Kautham
    print(f"Moviendo de {init} a {goal} con el objeto {obsName}.")
    kautham.kSetQuery(node, init, goal)
    kautham.kSetPlannerParameter(node, "_Incremental (0/1)", "0")  # Planificación desde cero
    path = kautham.kGetPath(node, 1)

    if path:
        print("-------- Path encontrado: Realizando movimiento para SERVE.")
        # Escribir el path en el archivo de tareas
        info.taskfile.write("\t<Transfer object = \"%s\" robot = \"%d\" link = \"%d\">\n" % (obsName,robotIndex, 14))
        k = sorted(list(path.keys()))[-1][1] + 1  # Número de articulaciones
        p = sorted(list(path.keys()))[-1][0] + 1  # Número de puntos en el path
        for i in range(p):
            tex = ''
            for j in range(0, k):
                tex = tex + str(path[i, j]) + " "
            ktmpb_python_interface.writePath(info.taskfile, tex)
        info.taskfile.write("\t</Transfer>\n")
        
        # Mover el robot al estado objetivo
        kautham.kMoveRobot(node, goal)

        # Desacoplar el objeto en el destino
        print(f"Desacoplando objeto {obsName} en el destino.")
        kautham.kDetachObject(node, obsName)

        # Volver a la posición inicial (opcional)
        print("Regresando a la configuración inicial.")
        kautham.kSetQuery(node, goal, init)
        path_back = kautham.kGetPath(node, 1)
        if path_back:
            kautham.kMoveRobot(node, init)
            print("Movimiento de retorno completado.")
        else:
            print("No se encontró un camino de retorno.")
        return True
    else:
        print("**************************************************************************")
        print("Get path Failed! No SERVE possible, Infeasible Task Plan")
        print("**************************************************************************")
        return False


def Serve_read(action_element):  # Leer datos de la configuración
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
