# downward_ros2

[downward_ros](https://gitioc.upc.edu/jan.rosell/downward_ros) is a ROS wrapper to [fast-downward](https://www.fast-downward.org/).

## Run setup

### Installing fast-downward (Ubuntu 22.04)

```
$ sudo add-apt-repository ppa:deb-rob/jammy-robotics
$ sudo apt update
$ sudo apt install fast-downward
```

### Installing fast-downward (Debian 11) TO_DO!

```

$ sudo sh -c 'echo "deb [arch=amd64] http://debrob.upc.edu/debian-robotics bullseye-robotics main" > /etc/apt/sources.list.d/debian-robotics.list'
$ curl -s https://debrob.upc.edu/debian-robotics/debian-robotics.gpg.asc | sudo apt-key add
$ sudo apt-get update
$ sudo apt install fast-downward 
```

### Build downward_ros2 & downward_interfaces

```
$ colcon build
$ source install/local_setup.bash
```

## Test

```
$ ros2 launch downward_ros2 downward_service.launch.py test:=true
```

This launch file runs the downward_client and downward_server nodes. 

The downward_server node wraps the downward executable and offers a service, called `downward_service`, with the following request and response:

```
string problem
string domain
string evaluator
string search
---
bool response
string[] plan
```

`problem` and `domain` are the PDDL problem and domain files, and `evaluator` and `search` are the Downward arguments. If they are left void, then the parameters for the FF are set, i.e.:

- evaluator = "hff=ff()"
- search = "lazy_greedy([hff], preferred=[hff])"

The test example is from the blocksworld domain using pickup, putdown, stack, unstack actions. 

The downward_client calls the service both using Fast-forward (FF) and context-enhanced additive heuristic (CEA) options. The solution, printed in the terminal is: ['PICKUP OBJB', 'STACK OBJB OBJA']


