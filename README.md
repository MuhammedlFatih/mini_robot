# 🤖 Robot Vacuum — ROS 2 Simulation Package

<div align="center">

![ROS 2](https://img.shields.io/badge/ROS_2-Humble-22314E?style=for-the-badge&logo=ros&logoColor=white)
![Gazebo](https://img.shields.io/badge/Gazebo-Classic-FF6B35?style=for-the-badge&logoColor=white)
![SLAM](https://img.shields.io/badge/SLAM-Toolbox-4A90D9?style=for-the-badge&logoColor=white)
![Cartographer](https://img.shields.io/badge/Cartographer-ROS-34A853?style=for-the-badge&logoColor=white)
![License](https://img.shields.io/badge/License-Apache_2.0-22C55E?style=for-the-badge)

**A complete ROS 2 simulation package for a differential-drive robot vacuum.**  
Gazebo simulation · SLAM mapping · Localization · LiDAR · Camera · IMU

[Overview](#-overview) · [Features](#-features) · [Installation](#-installation) · [Usage](#-usage) · [Package Structure](#-package-structure)

</div>

---

## 📖 Overview

`robot_vacuum` is a full-featured ROS 2 package that simulates a circular differential-drive robot (Roomba-like) in Gazebo Classic. The robot is equipped with a 2D LiDAR, RGB camera, and IMU, and supports both **SLAM mapping** (slam_toolbox & Cartographer) and **localization** on a pre-built map.

The robot model, sensor configurations, controllers, and world environments are all included out of the box.

---

## ✨ Features

- 🟣 **Custom robot URDF/Xacro** — circular base, two drive wheels, two caster wheels
- 📡 **2D LiDAR** — 360° scan, 20m range via `libgazebo_ros_ray_sensor`
- 📷 **RGB Camera** — 640×480, 10 Hz, forward-facing
- 🧭 **IMU** — Gaussian noise model, 100 Hz
- 🚗 **Differential Drive** — Gazebo plugin with odometry and TF publishing
- 🗺️ **SLAM Mapping** — slam_toolbox (async) and Google Cartographer (2D)
- 📍 **Localization** — slam_toolbox localization mode on serialized maps
- 🌍 **Multiple Gazebo worlds** — empty, TurtleBot3 world, custom obstacle world
- 🎛️ **RViz config** — pre-configured with robot model, TF, LaserScan, camera image

---

## 🛠️ Prerequisites

| Dependency | Version |
|------------|---------|
| ROS 2 | Humble Hawksbill |
| Gazebo | Classic (11) |
| slam_toolbox | `ros-humble-slam-toolbox` |
| cartographer_ros | `ros-humble-cartographer-ros` |
| nav2 | `ros-humble-navigation2` |
| ros2_control | `ros-humble-ros2-control` |

---

## 📦 Installation

### 1. Clone into your workspace

```bash
cd ~/robot_ws/src
git clone https://github.com/your-username/robot_vacuum.git
```

### 2. Install dependencies

```bash
cd ~/robot_ws
rosdep install --from-paths src --ignore-src -r -y
```

### 3. Build

```bash
colcon build --symlink-install
source install/setup.bash
```

---

## 🚀 Usage

### Launch Simulation (Gazebo + RViz)

```bash
ros2 launch robot_vacuum sim_launch.py
```

This spawns the robot in the TurtleBot3 world with RViz pre-configured.

---

### SLAM Mapping

**Option A — slam_toolbox (recommended)**

```bash
ros2 launch slam_toolbox online_async_launch.py \
  slam_params_file:=src/robot_vacuum/config/mapper_params_online_async.yaml \
  use_sim_time:=true
```

**Option B — Google Cartographer**

```bash
ros2 launch robot_vacuum cartographer.py
```

**Save the map (slam_toolbox)**

```bash
# Serialize (for localization later)
ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph \
  "{filename: '/home/$USER/robot_ws/src/robot_vacuum/maps/my_serialize_map'}"

# Save as PNG + YAML (for nav2 map_server)
ros2 run nav2_map_server map_saver_cli -f ~/robot_ws/src/robot_vacuum/maps/my_save_map
```

---

### Localization on a Saved Map

```bash
ros2 launch robot_vacuum sim_launch.py   # start Gazebo first

# Then run slam_toolbox in localization mode
ros2 launch slam_toolbox localization_launch.py \
  slam_params_file:=src/robot_vacuum/config/localization.yaml \
  use_sim_time:=true
```

> Make sure `map_file_name` in `config/localization.yaml` points to your serialized map.

---

### Teleoperation

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args --remap cmd_vel:=/diff_cont/cmd_vel_unstamped
```

---

## 🤖 Robot Specifications

| Property | Value |
|----------|-------|
| Base shape | Cylinder (r = 0.175 m, h = 0.09 m) |
| Wheel separation | 0.36 m |
| Wheel radius | 0.03 m |
| Drive type | Differential drive |
| Caster wheels | 2 (front + back, r = 0.015 m) |
| Base mass | 0.5 kg |

### Sensor Specs

| Sensor | Topic | Rate | Notes |
|--------|-------|------|-------|
| LiDAR | `/scan` | 10 Hz | 360°, 0.3–20 m |
| Camera | `/camera/image_raw` | 10 Hz | 640×480, FOV 62° |
| IMU | `/imu` | 100 Hz | Gaussian noise |
| Odometry | `/odom` | 50 Hz | From diff_drive plugin |

---

## 📂 Package Structure

```
robot_vacuum/
├── config/
│   ├── mapper_params_online_async.yaml  # slam_toolbox mapping config
│   ├── localization.yaml                # slam_toolbox localization config
│   ├── my_2d.lua                        # Cartographer config (with odometry)
│   ├── my_new_2d.lua                    # Cartographer config (no odometry)
│   ├── backpack_2d.lua                  # Cartographer backpack config
│   ├── my_controllers.yaml              # ros2_control diff drive controller
│   ├── twist_mux.yaml                   # Velocity multiplexer config
│   └── odometry_config.yaml             # Odometry parameters
│
├── launch/
│   ├── sim_launch.py                    # Main launch: Gazebo + RSP + RViz
│   ├── cartographer.py                  # Cartographer SLAM launch
│   ├── cart.py                          # Cartographer + occupancy grid launch
│   ├── occupancy_grid.launch.py         # Occupancy grid node
│   └── cartt.py                         # AMCL localization (nav2)
│
├── urdf/
│   ├── main.xacro                       # Top-level xacro (includes all below)
│   ├── robot.urdf.xacro                 # Base link, wheels, casters
│   ├── diff.xacro                       # Gazebo diff drive plugin + materials
│   ├── lidar.xacro                      # LiDAR link + Gazebo sensor plugin
│   ├── camera.xacro                     # Camera link + Gazebo sensor plugin
│   ├── imu.xacro                        # IMU link + Gazebo sensor plugin
│   ├── inertial.xacro                   # Inertia macros (box, cylinder, sphere)
│   └── ros2_control.xacro               # ros2_control hardware interface
│
├── world/
│   ├── turtlebot3_world.world           # TurtleBot3 maze (default)
│   ├── base.world                       # Open world with colored obstacle boxes
│   ├── new.world                        # Simple box obstacle world
│   └── empty.world                      # Empty world for testing
│
├── maps/
│   ├── my_save_map.pgm                  # Saved occupancy grid image
│   ├── my_save_map.yaml                 # Map metadata (resolution, origin)
│   ├── my_serialize_map.data            # slam_toolbox serialized map
│   └── my_serialize_map.posegraph       # slam_toolbox pose graph
│
├── rviz/
│   └── base_rviz.rviz                   # Pre-configured RViz layout
│
├── CMakeLists.txt
└── package.xml
```

---

## 🗺️ Worlds

| World | Description |
|-------|-------------|
| `turtlebot3_world.world` | Classic TurtleBot3 maze — great for SLAM demos |
| `base.world` | Open arena with 10 colored obstacle boxes |
| `new.world` | Minimal world with 4 boxes for quick testing |
| `empty.world` | Flat ground plane only |

---

## ⚙️ Configuration Notes

### Switching SLAM backends

The package supports two SLAM backends. Key differences:

| | slam_toolbox | Cartographer |
|--|---|---|
| Config format | YAML | Lua |
| Localization mode | ✅ Built-in | ❌ Separate setup |
| Real-time performance | Very good | Good |
| Loop closure | ✅ | ✅ |
| Recommended for this robot | ✅ | ✅ |

### Cartographer Lua configs

| File | Use case |
|------|----------|
| `my_2d.lua` | With wheel odometry (`use_odometry: true`) |
| `my_new_2d.lua` | No odometry, `provide_odom_frame: true` |
| `backpack_2d.lua` | Multi-echo LiDAR (reference config) |

### Controller

The robot uses `diff_drive_controller` from `ros2_control`. Velocity commands go to:
```
/diff_cont/cmd_vel_unstamped   (geometry_msgs/Twist)
```

---

## 📡 Key ROS 2 Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/scan` | `sensor_msgs/LaserScan` | Published |
| `/camera/image_raw` | `sensor_msgs/Image` | Published |
| `/imu` | `sensor_msgs/Imu` | Published |
| `/odom` | `nav_msgs/Odometry` | Published |
| `/diff_cont/cmd_vel_unstamped` | `geometry_msgs/Twist` | Subscribed |
| `/map` | `nav_msgs/OccupancyGrid` | Published (SLAM) |
| `/robot_description` | `std_msgs/String` | Published (RSP) |

---

## 🔧 TF Tree

```
map
 └── odom
      └── base_footprint
           └── base_link
                ├── left_wheel
                ├── right_wheel
                ├── front_caster_wheel
                ├── back_caster_wheel
                ├── laser_frame
                ├── camera_link
                └── imu_link
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-sensor`)
3. Commit your changes (`git commit -m 'Add: new sensor integration'`)
4. Push to the branch (`git push origin feature/new-sensor`)
5. Open a Pull Request

---

## 📄 License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

---

<div align="center">

**Built with ROS 2 · Gazebo · slam_toolbox · Cartographer 🚀**

</div>
