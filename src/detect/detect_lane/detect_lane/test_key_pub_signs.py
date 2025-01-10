import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class KeyboardSubscriber(Node):
    def __init__(self):
        super().__init__('key_signs_subscriber')

        # 訂閱 /detect/signs 主題
        self.signs_subscription = self.create_subscription(
            String,
            '/detect/signs',
            self.signs_callback,
            10
        )
        self.signs_subscription  # 防止被垃圾回收

        # 訂閱 /detect/traffic_light 主題
        self.traffic_light_subscription = self.create_subscription(
            String,
            '/detect/traffic_light',
            self.traffic_light_callback,
            10
        )
        self.traffic_light_subscription  # 防止被垃圾回收

    def signs_callback(self, msg):
        # 處理來自 /detect/signs 的消息
        self.get_logger().info(f'Received sign message: "{msg.data}"')

    def traffic_light_callback(self, msg):
        # 處理來自 /detect/traffic_light 的消息
        self.get_logger().info(f'Received traffic light message: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)

    # 創建並啟動訂閱節點
    keyboard_subscriber = KeyboardSubscriber()

    try:
        rclpy.spin(keyboard_subscriber)
    except KeyboardInterrupt:
        pass

    # 關閉節點
    keyboard_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

