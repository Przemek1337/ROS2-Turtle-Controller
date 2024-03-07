# ROS2-Turtle-Controller
Turtle Controller is an application that allows you to control a turtle on the board by entering the target path in the form of x and y variables
# Usage
1. Install ROS2 on ubuntu
2. Build project by: colcon build --symlink-install
3. Refresh source by: source install/setup.bash
4. In the first console window type: ros2 run turtlesim turtlesim_node
5. In the second console window type: ros2 run [your_name_of_controller from ros2 installation] turtle-controller
