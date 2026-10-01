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

def fk(q):
    dh_params = [
        (q[0],             131.56,  0,       math.pi/2),
        (q[1] - math.pi/2, 0,      -110.4,   0),
        (q[2],             0,      -96.0,    0),
        (q[3] - math.pi/2, 63.20,   0,       math.pi/2),
        (q[4] + math.pi/2, 71.44,   0,      -math.pi/2),
        (q[5],             53.60,   0,       0)
    ]
   
    T = np.eye(4)
    for theta, d, a, alpha in dh_params:
        T = T @ dh_matrix(theta, d, a, alpha)
       
    x = T[0, 3]
    y = T[1, 3]
    z = T[2, 3]
   
    return float(x), float(y), float(z)

def dentro_de_limites(q):
    limite = math.radians(165)
    for i, angulo in enumerate(q):
        if abs(angulo) > limite:
            return False, f"Articulacion {i+1} excede limite"
    return True, ""

def dentro_del_workspace(q):
    x, y, z = fk(q)
    if z < 15.0:
        return False, f"Colision mesa: z={z:.1f}"
    if math.hypot(x, y) < 60.0 and z < 120.0:
        return False, "Auto-colision base"
    return True, ""

def paso_articular(desde, q):
    return max(abs(a - b) for a, b in zip(desde, q))
