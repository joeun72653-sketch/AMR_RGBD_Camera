import rclpy
from rclpy.node import Node
from rclpy.qos import (
    QoSProfile,
    ReliabilityPolicy,
    HistoryPolicy,
    DurabilityPolicy
)

from sensor_msgs.msg import Image
import numpy as np


class FrontDistanceNode(Node):
    """
    Orbbec Gemini 335L의 Depth 영상을 이용하여
    카메라 전방 물체까지의 거리를 측정하는 ROS2 Node.

    Topic:
        /camera/depth/image_raw

    Method:
        - Depth 영상 중앙의 60 x 60 ROI 사용
        - 유효하지 않은 Depth 값 제거
        - 유효 Depth 값의 Median 계산
        - 최종 거리를 meter 단위로 출력
    """

    def __init__(self):
        super().__init__('front_distance_node')

        # Gemini 335L Depth Publisher와 호환되는 QoS
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=5
        )

        # Depth Image 구독
        self.subscription = self.create_subscription(
            Image,
            '/camera/depth/image_raw',
            self.depth_callback,
            qos_profile
        )

        # 영상 중앙에서 거리 측정에 사용할 ROI 크기
        self.roi_width = 60
        self.roi_height = 60

        # 사용할 Depth 범위
        self.min_distance_m = 0.1
        self.max_distance_m = 10.0

        self.get_logger().info(
            'Front distance node started.'
        )

    def depth_callback(self, msg):

        # 16-bit unsigned Depth Image
        if msg.encoding == '16UC1':

            depth_image = np.frombuffer(
                msg.data,
                dtype=np.uint16
            ).reshape(
                msg.height,
                msg.width
            )

            # millimeter -> meter
            depth_image = (
                depth_image.astype(np.float32)
                / 1000.0
            )

        # 32-bit floating-point Depth Image
        elif msg.encoding == '32FC1':

            depth_image = np.frombuffer(
                msg.data,
                dtype=np.float32
            ).reshape(
                msg.height,
                msg.width
            )

        else:
            self.get_logger().warning(
                f'Unsupported depth encoding: {msg.encoding}'
            )
            return

        height, width = depth_image.shape

        # Depth 영상 중앙 좌표
        center_x = width // 2
        center_y = height // 2

        half_w = self.roi_width // 2
        half_h = self.roi_height // 2

        # 중앙 ROI 추출
        roi = depth_image[
            center_y - half_h:center_y + half_h,
            center_x - half_w:center_x + half_w
        ]

        # 0, NaN, Inf 및 측정 범위 밖의 값 제거
        valid_depths = roi[
            np.isfinite(roi)
            & (roi > self.min_distance_m)
            & (roi < self.max_distance_m)
        ]

        # 유효한 Depth 값이 없는 경우
        if valid_depths.size == 0:

            self.get_logger().warning(
                'Front distance: no valid depth'
            )
            return

        # Depth 노이즈의 영향을 줄이기 위해 Median 사용
        distance = np.median(valid_depths)

        # 전방 거리 출력
        self.get_logger().info(
            f'Front distance: {distance:.2f} m'
        )


def main(args=None):

    rclpy.init(args=args)

    node = FrontDistanceNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
