# Task\_and\_motion\_planning2

This meta-repository contains:

module **downward\_ros**: package that wraps the Fast-Downward set of task planners - (using **ros2** branch)

module **kautham\_interfaces**: package that wraps the calls to the Kautham services

module **ktmpb**: package that uses the Fast-Downward and Katham services to plan at task and motion levels - (using **ros2** branch)

## Clone and build

```
$ mkdir -p colcon_ws/src
$ cd colcon_ws/src
$ git clone  https://github.com/VictorEscribano/Motion-Task_planning.git
$ cd ..
$ colcon build
```

## Test

The **ktmpb** package has a demo folder called _task\_and\_motion\_planning2/ktmpb/ktmpb\_interfaces/demos/_ that is installed in _install/ktmpb\_interfaces/share/ktmpb\_interfaces/demos/_.

To test the task and motion planning client launch the following file:

```
$ ros2 launch ktmpb_client tiago_kitchen_no_pose_right.launch.py
```

This example uses the task and motion planning configuration file **tampconfig\_no\_pose\_right.xml** where the following PDDL files and Kautham files to be used are defined:

```
- pddldomain file: "ff-domains/manipulationdomain.pddl"
- pddlproblem file "ff-domains/manipulation_problem_redcan"
- kautham file: "tiago_mobile_counterA_counterB_right.xml"
```

The resulting file (in the folder _install/ktmpb\_interfaces/share/ktmpb\_interfaces/demos/_) is called:

```
- taskfile_tampconfig_pose_no_graspit_right.xml
```