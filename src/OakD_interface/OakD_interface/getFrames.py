import rclpy
import cv2
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import time
import depthai

pipeline = depthai.Pipeline()
cam_rgb = mono = pipeline.createMonoCamera()
cam_rgb.setBoardSocket(depthai.CameraBoardSocket.LEFT)
cam_rgb.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_480_P)

xout_rgb = pipeline.create(depthai.node.XLinkOut)
xout_rgb.setStreamName("rgb")
cam_rgb.out.link(xout_rgb.input)



bridge = CvBridge()

class ImageNode(Node):
    def __init__(self) -> None:
        super().__init__("ImagePublisherNode")

        self._publisher = self.create_publisher(Image, 'OakLite_Camera', 10)
        self.frameGrabber()

    def frameGrabber(self):
        with depthai.Device(pipeline) as device:

            # Output queues will be used to get the grayscale frames from the outputs defined above
            qLeft = device.getOutputQueue(name="rgb", maxSize=10, blocking=False)
            
            while True:
                inLeft = qLeft.tryGet()
                now = self.get_clock().now().to_msg()
                if inLeft is not None:
                    left_frame = inLeft.getCvFrame()
                    cv2.imshow("cam_out",left_frame)
                    left_frame_ros = bridge.cv2_to_imgmsg(left_frame,'mono8')
                    left_frame_ros.header.stamp = now
                    self._publisher.publish(left_frame_ros)
                time.sleep(0.1)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = ImageNode()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()