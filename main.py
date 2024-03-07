import time
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
import threading

class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.cmd_vel_publisher = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.pose_subscriber = self.create_subscription(Pose, 'turtle1/pose', self.pose_callback, 10)
        self.pose = Pose()
        self.destination_x = 5.0  
        self.destination_y = 5.0  
        self.is_moving = False
        self.get_logger().info("Turtle controller has started")

    def pose_callback(self, msg):
        self.pose = msg
        self.move_to_goal()

    def set_goal(self, x, y):
        self.destination_x = x
        self.destination_y = y
        self.is_moving = True  

    def move_to_goal(self):
        if not self.is_moving:
            return

        vel_msg = Twist()
        K_linear = 1.0
        K_angular = 4.0

        
        angle_to_goal = math.atan2(self.destination_y - self.pose.y, self.destination_x - self.pose.x)
        angular_difference = self.normalize_angle(angle_to_goal - self.pose.theta)

        
        distance_to_goal = math.sqrt((self.destination_x - self.pose.x) ** 2 + (self.destination_y - self.pose.y) ** 2)

        
        if abs(angular_difference) > 0.1:  
            vel_msg.angular.z = K_angular * angular_difference
        else:
            vel_msg.angular.z = 0.0
            if distance_to_goal > 0.1:  
                vel_msg.linear.x = K_linear * distance_to_goal
            else:
                vel_msg.linear.x = 0.0
                self.is_moving = False  
                self.get_logger().info("Goal reached")

        self.cmd_vel_publisher.publish(vel_msg)

    def normalize_angle(self, angle):
        
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

def main(args=None):
    rclpy.init(args=args)
    turtle_controller = TurtleControllerNode()

    def user_input():
        while rclpy.ok():
            x_goal = float(input("Enter x goal: "))
            y_goal = float(input("Enter y goal: "))
            turtle_controller.set_goal(x_goal, y_goal)
            while turtle_controller.is_moving:
                
                time.sleep(0.1)

    
    input_thread = threading.Thread(target=user_input)
    input_thread.start()

    rclpy.spin(turtle_controller)

    turtle_controller.destroy_node()
    rclpy.shutdown()
    input_thread.join()

if __name__ == '__main__':
    main()

