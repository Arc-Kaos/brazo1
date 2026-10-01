import time
import threading

class Pedido:
    def __init__(self, goal_handle, client_id, priority, joint_positions):
        self.goal_handle = goal_handle
        self.client_id = client_id
        self.priority = priority
        self.joint_positions = joint_positions
        self.goal_id = bytes(goal_handle.goal_id.uuid).hex()[:12]
        self.t_llegada = time.time()
        self.t_inicio_ejec = None
        self.fin = threading.Event()

    @property
    def espera_s(self):
        return time.time() - self.t_llegada

class PoliticaFIFO:
    nombre = 'fifo'
    def siguiente(self, pendientes):
        # Retorna siempre el primer elemento que llegó (índice 0)
        return 0 if pendientes else None
       
    def atendido(self, pedido):
        pass

class PoliticaPrioridad:
    nombre = 'prioridad'
    def __init__(self, tau_envejecimiento_s=8.0):
        self.tau = tau_envejecimiento_s

    def siguiente(self, pendientes):
        if not pendientes:
            return None
       
        mejor_idx = 0
        mejor_p = -float('inf')
        ahora = time.time()
       
        # Recorre la cola y calcula la prioridad efectiva (prioridad + envejecimiento)
        for idx, p in enumerate(pendientes):
            p_efectiva = p.priority + ((ahora - p.t_llegada) / self.tau)
            if p_efectiva > mejor_p:
                mejor_p = p_efectiva
                mejor_idx = idx
               
        return mejor_idx

    def atendido(self, pedido):
        pass

POLITICAS = {
    'fifo': PoliticaFIFO,
    'prioridad': PoliticaPrioridad
}