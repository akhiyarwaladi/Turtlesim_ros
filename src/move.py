#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import math

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

  #After the loop, stops the robot
  vel_msg.linear.x = 0
  #Force the robot to stop
  velocity_publisher.publish(vel_msg)
  rate.sleep()

def move_rotate(speed, angle, clockwise):
  velocity_publisher_rotate = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
  vel_msg_rotate = Twist()
  rate = rospy.Rate(10)
  #Converting from angles to radians
  angular_speed = speed * math.pi / 180.0
  relative_angle = angle * math.pi / 180.0
  # Checking if our movement is CW or CCW

  if clockwise:
    vel_msg_rotate.angular.z = -abs(angular_speed)
  else:
    vel_msg_rotate.angular.z = abs(angular_speed)
  # Setting the current time for distance calculus
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
  rate.sleep()
  
def move_circle():

  # Create a publisher which can "talk" to Turtlesim and tell it to move
  pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1)
   
  # Create a Twist message and add linear x and angular z values
  move_cmd = Twist()
  move_cmd.linear.x = 1.0
  move_cmd.angular.z = 1.0

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

  velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
  vel_msg = Twist()

  rate = rospy.Rate(10)
  while not rospy.is_shutdown():
 
    i = 0
    while(i < 4):

      print("Let's move your robot")
      move_straight (2, 3, 1);
      

      print("Let's rotate your robot")
      move_rotate (20, 90, 1);
      i = i+1
    
    print("Let's move circle")
    move_circle()

  rospy.spin()
  
if __name__ == '__main__':
  try:
    #Testing our function
    move()
  except rospy.ROSInterruptException: pass