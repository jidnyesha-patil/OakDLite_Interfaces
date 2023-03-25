import rclpy
import cv2
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import time
import depthai

bridge = CvBridge()

class ImageNode(Node):
    def __init__(self) -> None:
        super().__init__("ImagePublisherNode")

        self._subscriber = self.create_subscription(Image, 'OakLite_Camera',self.listener_callback, 10)
    
    def listener_callback(self, msg):
        frame = bridge.imgmsg_to_cv2(msg,'mono8')
        cv2.imshow('Camera out',frame)
        cv2.waitKey(1)
    

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = ImageNode()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()