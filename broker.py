import math
import numpy as np

JOINT_NAMES = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']

def dh_matrix(theta, d, a, alpha):
    c_th = math.cos(theta)
    s_th = math.sin(theta)
    c_al = math.cos(alpha)
    s_al = math.sin(alpha)
    return np.array([
        [c_th, -s_th*c_al,  s_th*s_al, a*c_th],
        [s_th,  c_th*c_al, -c_th*s_al, a*s_th],
        [0,     s_al,       c_al,      d],
        [0,     0,          0,         1]
    ])
cd ~/jetcobot_ws
colcon build --packages-select arm_broker
source install/setup.bash
python3 src/herramientas/verificar_fk.py