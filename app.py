from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, join_room, leave_room
from fila import Fila
from admin import admin_bp, init_socketio
import threading
import time

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"
socketio = SocketIO(app)

# Inicializar a fila de usuários
fila = Fila()

# Importar e registrar o blueprint de administração
app.register_blueprint(admin_bp)
init_socketio(socketio)

def atualizar_timer():
    """Função para gerenciar o timer de movimentação da fila."""
    while True:
        if fila.usuarios:
            for segundos in range(30, -1, -1):
                socketio.emit('atualizar_timer', {'usuario_atual': fila.usuarios[0][0], 'timer': segundos})
                time.sleep(1)
            fila.mover_para_fim()
            socketio.emit('atualizar_lista', fila.obter_usuarios())

# Thread para o timer da fila
threading.Thread(target=atualizar_timer, daemon=True).start()

@app.route('/')
def index():
    """Rota principal para usuários."""
    session_id = request.remote_addr + ":" + str(request.environ.get('REMOTE_PORT'))
    session['id'] = session_id
    fila.adicionar_usuario(session_id)
    return render_template('index.html')

@socketio.on('connect')
def conectar():
    """Lida com conexões de novos clientes."""
    session_id = session.get('id')
    join_room(session_id)
    socketio.emit('atualizar_lista', fila.obter_usuarios())

@socketio.on('disconnect')
def desconectar():
    """Lida com a desconexão de clientes."""
    session_id = session.get('id')
    leave_room(session_id)
    fila.remover_usuario(session_id)
    socketio.emit('atualizar_lista', fila.obter_usuarios())

if __name__ == '__main__':
    socketio.run(app, debug=True)
