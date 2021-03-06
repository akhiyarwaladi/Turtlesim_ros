#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import math
from turtlesim.msg import Pose

def callback(data):
  pose = data
  # pose.x = round(pose.x, 4)
  # pose.y = round(pose.y, 4)
  # pose.theta = round(pose.theta, 4)
  pose.x = pose.x
  pose.y = pose.y
  pose.theta = pose.theta

def degrees2radians(angle_in_degrees):
  return angle_in_degrees * math.pi / 180.0

def move_rotate(speed, angle,clockwise):
  velocity_publisher_rotate = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
  vel_msg_rotate = Twist()
  rate = rospy.Rate(10)
  #Converting from angles to radians
  angular_speed = speed * math.pi / 180.0
  relative_angle = angle * math.pi / 180.0
  # Checking if our movement is CW or CCW

  if (clockwise): 
    vel_msg_rotate.angular.z = math.fabs(angular_speed)
    # Setting the current time for distance calculus
  else:
    vel_msg_rotate.angular.z = -math.fabs(angular_speed)

  t0 = rospy.Time.now().to_sec()
  current_angle = 0

  while(current_angle < relative_angle):
    velocity_publisher_rotate.publish(vel_msg_rotate)
    t1 = rospy.Time.now().to_sec()
    current_angle = angular_speed*(t1-t0)
    rate.sleep()


  #Forcing our robot to stop
  vel_msg_rotate.angular.z = 0
  velocity_publisher_rotate.publish(vel_msg_rotate)
  #rospy.spin()
  #rate.sleep()
  
def setDesiredOrientation(desired_angle_radians):
  pose_x, pose_y, pose_theta = turtlePos()
  print(pose_theta)
  relative_angle_radians = desired_angle_radians - pose_theta
  clockwise = True if relative_angle_radians < 0 else False;
  move_rotate(abs(relative_angle_radians), abs(relative_angle_radians), clockwise)


def turtlePos():
  
  pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, callback)
  pose_msg = Pose()
  pose_x = pose_msg.x
  pose_y = pose_msg.y
  pose_theta = pose_msg.theta

  return pose_x, pose_y, pose_theta

def move_straight(speed, distance, isForward):
  velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
  vel_msg = Twist()
  rate = rospy.Rate(10)
  # cek apakah akan pindah lurus maju atau mundur
  if(isForward):
    vel_msg.linear.x = abs(speed)
  else:
    vel_msg.linear.x = -abs(speed)

  # set semua sumbu jadi 0 karena hanya akan gerak di sumbu x
  vel_msg.linear.y = 0
  vel_msg.linear.z = 0
  vel_msg.angular.x = 0
  vel_msg.angular.y = 0
  vel_msg.angular.z = 0

  # set waktu saat ini untuk perhitungan jarak
  t0 = rospy.Time.now().to_sec()
  current_distance = 0

  # ulangi untuk memindahkan kura kura dengan jarak tertentu
  while(current_distance < distance):
    #Publish velocity saat ini
    velocity_publisher.publish(vel_msg)
    # dapatkan waktu saat ini
    t1=rospy.Time.now().to_sec()
    # hitung jarak saat ini yaitu waktu dikali perubahan waktu
    current_distance= speed*(t1-t0)
    rate.sleep()

  #After the loop, stops the robot
  vel_msg.linear.x = 0
  #Force the robot to stop
  velocity_publisher.publish(vel_msg)
  


def move_circle():

  # Create a publisher which can "talk" to Turtlesim and tell it to move
  pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1)
   
  # Create a Twist message and add linear x and angular z values
  move_cmd = Twist()
  move_cmd.linear.x = 1.0
  move_cmd.angular.z = -1.0

  # Save current time and set publish rate at 10 Hz
  now = rospy.Time.now()
  rate = rospy.Rate(10)

  # For the next 6 seconds publish cmd_vel move commands to Turtlesim
  while rospy.Time.now() < now + rospy.Duration.from_sec(6):
      pub.publish(move_cmd)
  rate.sleep()

def move():
  # Starts a new node
  rospy.init_node('robot_cleaner', anonymous=True)
  rate = rospy.Rate(10)
  while not rospy.is_shutdown():

    print("Let's rotate for the first direction")
    #move_rotate (10, 90, 1);
    setDesiredOrientation(degrees2radians(90))
    rate.sleep()
    i = 0
    while(i < 4):

      print("Let's move straight your robot")
      move_straight (5, 4, 1)
      
      print("Let's rotate your robot")
      move_rotate (10, 90, 0)

      i = i+1
       
    print("Let's move circle")
    move_circle()

    print("Let's rotate for adjust direction")
    move_rotate (20, 100, 0)

  rospy.spin()
  
if __name__ == '__main__':
  try:
    #Testing our function
    move()
  except rospy.ROSInterruptException: pass