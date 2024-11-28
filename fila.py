from threading import Lock
from time import time, strftime, localtime

class Fila:
    def __init__(self):
        self.lock = Lock()
        self.usuarios = []  # Lista de tuplas (session_id, last_moved_time, horario_login)

    def adicionar_usuario(self, session_id):
        with self.lock:
            if session_id not in [u[0] for u in self.usuarios]:
                horario_atual = strftime("%H:%M:%S", localtime())
                self.usuarios.append((session_id, time(), horario_atual))
    
    def remover_usuario(self, session_id):
        with self.lock:
            self.usuarios = [u for u in self.usuarios if u[0] != session_id]
    
    def mover_para_fim(self):
        with self.lock:
            if self.usuarios:
                user = self.usuarios.pop(0)
                horario_atual = strftime("%H:%M:%S", localtime())
                self.usuarios.append((user[0], time(), horario_atual))
    
    def obter_usuarios(self):
        with self.lock:
            return [
                {"indice": idx + 1, "id": u[0], "tempo_ativo": int(time() - u[1]), "horario": u[2]}
                for idx, u in enumerate(self.usuarios)
            ]
