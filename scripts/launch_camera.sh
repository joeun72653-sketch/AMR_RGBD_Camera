#!/usr/bin/env bash

# ============================================================
# Orbbec Gemini 335L RGB-D Camera Launch Script
#
# Environment : Ubuntu 24.04 / ROS2 Jazzy
# Camera      : Orbbec Gemini 335L
# RGB         : 1280 x 720 @ 30 FPS
# Depth       : 848 x 480 @ 30 FPS
# RMW         : Cyclone DDS
# ============================================================


# ROS2 Jazzy 환경 설정
source /opt/ros/jazzy/setup.bash

# AMR Workspace 환경 설정
source ~/amr_ws/install/setup.bash


# ------------------------------------------------------------
# ROS2 Middleware 설정
# Fast DDS 환경에서 RGB/Depth frame drop이 발생하여
# Cyclone DDS를 사용하도록 설정
# ------------------------------------------------------------

export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp


# ------------------------------------------------------------
# Gemini 335L 실행
# ------------------------------------------------------------

ros2 launch orbbec_camera gemini_330_series.launch.py \
  enable_color:=true \
  enable_depth:=true \
  enable_accel:=false \
  enable_gyro:=false \
  enable_point_cloud:=false \
  enable_colored_point_cloud:=false \
  color_width:=1280 \
  color_height:=720 \
  color_fps:=30 \
  depth_width:=848 \
  depth_height:=480 \
  depth_fps:=30 \
  color_qos:=SENSOR_DATA \
  depth_qos:=SENSOR_DATA \
  color_qos_history:=KEEP_LAST \
  color_qos_depth:=5 \
  depth_qos_history:=KEEP_LAST \
  depth_qos_depth:=5
