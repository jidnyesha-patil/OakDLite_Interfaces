import rclpy
from rclpy.node import Node
from rclpy.serialization import serialize_message
from std_msgs.msg import String
from sensor_msgs.msg import Image, NavSatFix

import rosbag2_py


class BagRecorder(Node):
    def __init__(self):
        super().__init__('bag_recorder')
        self.writer = rosbag2_py.SequentialWriter()

        storage_options = rosbag2_py._storage.StorageOptions(
            uri='sensor_bag',
            storage_id='sqlite3')
        
        converter_options = rosbag2_py._storage.ConverterOptions(input_serialization_format='cdr',
        output_serialization_format='cdr')

        self.writer.open(storage_options, converter_options)

        camera_topic_info = rosbag2_py._storage.TopicMetadata(
            name='OakLite_Camera',
            type='sensor_msgs/msg/Images',
            serialization_format='cdr')
        
        gps_topic_info = rosbag2_py._storage.TopicMetadata(
            name='gps_data',
            type='sensor_msgs/msg/NavSatFix',
            serialization_format='cdr')
        
        self.writer.create_topic(camera_topic_info)
        self.writer.create_topic(gps_topic_info)

        self.subscription_camera = self.create_subscription(
            Image,
            'OakLite_Camera',
            self.camera_callback,
            10)
        self.subscription_camera

        self.subscription_gps = self.create_subscription(
            NavSatFix,
            'gps_data',
            self.gps_callback,
            10)
        self.subscription_gps

    def camera_callback(self, msg):
        self.writer.write(
            'OakLite_Camera',
            serialize_message(msg),
            self.get_clock().now().nanoseconds)

    def gps_callback(self,msg):
        self.writer.write(
            "gps_data",
            serialize_message(msg),
            self.get_clock().now().nanoseconds
        )

def main(args=None):
    rclpy.init(args=args)
    sbr = BagRecorder()
    rclpy.spin(sbr)
    rclpy.shutdown()


if __name__ == '__main__':
    main()