# AMR RGB-D Camera

Orbbec Gemini 335L RGB-D 카메라를 ROS2 Jazzy 환경에서 연동하고,
RGB/Depth 영상 수신 및 전방 거리 측정을 구현한 프로젝트입니다.

## 개발 환경

- OS: Ubuntu 24.04
- ROS2: Jazzy
- Camera: Orbbec Gemini 335L
- Orbbec SDK: 2.10.6
- ROS Wrapper: 2.10.6
- USB: USB 3.2
- DDS: Cyclone DDS

## 구현 기능

- Gemini 335L ROS2 연동
- RGB 영상 수신
- Depth 영상 수신
- RGB 1280×720 @ 30 FPS
- Depth 848×480 @ 30 FPS
- Cyclone DDS 기반 영상 스트림 안정화
- Depth 기반 전방 물체 거리 측정
- 중앙 60×60 ROI 기반 거리 계산
- BEST_EFFORT QoS 적용

## 주요 ROS2 Topics

RGB:

/camera/color/image_raw

Depth:

/camera/depth/image_raw

Camera Info:

/camera/depth/camera_info

Point Cloud:

/camera/depth/points

## 성능 확인

Cyclone DDS 적용 후:

- RGB: 약 30 Hz
- Depth: 약 30 Hz
- RGB + Depth 동시 스트리밍 정상 동작

## 향후 구현

1. RGB 영상 + 전방 거리 동시 표시
2. Point Cloud 시각화
3. YOLO 객체 인식
4. YOLO + Depth 결합
5. 객체별 거리 측정
6. AMR 감속/정지 제어 연동
