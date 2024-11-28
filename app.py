from flask import Flask, render_template, session, request, jsonify
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
            atualizar_todos_usuarios()

# Thread para o timer da fila
threading.Thread(target=atualizar_timer, daemon=True).start()

@app.route('/')
def index():
    """Rota principal para usuários."""
    session_id = request.remote_addr + ":" + str(request.environ.get('REMOTE_PORT'))
    session['id'] = session_id
    fila.adicionar_usuario(session_id)
    return render_template('index.html')
reservas = []  # Lista para armazenar reservas no formato {"evento": str, "nome": str, "telefone": str}

@app.route('/reservar', methods=['POST'])
def reservar():
    """Rota para processar reservas de eventos."""
    data = request.json
    evento = data.get('evento')
    nome = data.get('nome')
    telefone = data.get('telefone')

    if not all([evento, nome, telefone]):
        return jsonify({'status': 'error', 'message': 'Dados incompletos'}), 400

    reserva = {"evento": evento, "nome": nome, "telefone": telefone}
    reservas.append(reserva)
    return jsonify({'status': 'success', 'reserva': reserva}), 200

@socketio.on('connect')
def conectar():
    """Lida com conexões de novos clientes."""
    session_id = session.get('id')
    join_room(session_id)
    atualizar_todos_usuarios()

@socketio.on('disconnect')
def desconectar():
    """Lida com a desconexão de clientes."""
    session_id = session.get('id')
    leave_room(session_id)
    fila.remover_usuario(session_id)
    atualizar_todos_usuarios()

def atualizar_todos_usuarios():
    """Atualiza todos os usuários com as informações da fila."""
    usuarios = fila.obter_usuarios()
    total_usuarios = len(usuarios)

    # Atualizar o status individual de cada usuário
    for i, u in enumerate(usuarios):
        session_id = u['id']
        pessoas_a_frente = i  # Posição na lista é igual ao número de pessoas à frente
        socketio.emit('atualizar_status', {
            'session_id': session_id,
            'total_usuarios': total_usuarios,
            'pessoas_a_frente': pessoas_a_frente,
        }, room=session_id)

    # Atualizar a lista para todos os usuários
    socketio.emit('atualizar_lista', usuarios)

def atualizar_status_usuario(session_id):
    """Envia informações do status do usuário atual."""
    usuarios = fila.obter_usuarios()
    posicao = next((i for i, u in enumerate(usuarios) if u['id'] == session_id), None)
    total_usuarios = len(usuarios)
    pessoas_a_frente = posicao if posicao is not None else -1
    socketio.emit('atualizar_status', {
        'session_id': session_id,
        'total_usuarios': total_usuarios,
        'pessoas_a_frente': pessoas_a_frente,
    }, room=session_id)

if __name__ == '__main__':
    socketio.run(app, debug=True)
