#!/usr/bin/env python
import os, sys

# Must config ****************************************
os.environ['ROS_MASTER_URI'] = 'http://localhost:11311'
# Must config ****************************************

src_root = os.path.join('..', '..', '..', '..')
ros_package_path = os.path.abspath(os.path.join(src_root, 'ros', 'kinetic', 'share'))
src_dir_abs = os.path.abspath(os.path.join(src_root, 'my_ws', 'src'))
os.environ['ROS_PACKAGE_PATH'] = src_dir_abs + os.pathsep + ros_package_path
os.environ['ROS_LOG_DIR'] = os.path.abspath('log')

lib_paths = [os.path.join(src_root, 'ros', 'kinetic', 'dist-packages'),
             os.path.join(src_root, 'ros', 'python2', 'dist-packages')]
sys.path.extend(lib_paths)
