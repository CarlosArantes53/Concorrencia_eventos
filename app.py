from flask import Flask, render_template, session, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room
from fila import Fila
import threading
import time

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"
socketio = SocketIO(app)

fila = Fila()
eventos = []  # Lista para armazenar os eventos no formato: {"nome": str, "vagas": int}

def atualizar_timer():
    while True:
        if fila.usuarios:
            for segundos in range(30, -1, -1):
                socketio.emit('atualizar_timer', {'usuario_atual': fila.usuarios[0][0], 'timer': segundos})
                time.sleep(1)
            fila.mover_para_fim()
            socketio.emit('atualizar_lista', fila.obter_usuarios())

threading.Thread(target=atualizar_timer, daemon=True).start()

@app.route('/')
def index():
    session_id = request.remote_addr + ":" + str(request.environ.get('REMOTE_PORT'))
    session['id'] = session_id
    fila.adicionar_usuario(session_id)
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/eventos', methods=['GET', 'POST'])
def gerenciar_eventos():
    if request.method == 'POST':
        novo_evento = request.json
        nome = novo_evento.get('nome')
        vagas = novo_evento.get('vagas')
        if nome and isinstance(vagas, int) and vagas > 0:
            evento = {"nome": nome, "vagas": vagas}
            eventos.append(evento)
            socketio.emit('atualizar_eventos', eventos)
            return jsonify({'status': 'success', 'evento': evento}), 200
        return jsonify({'status': 'error', 'message': 'Dados inválidos'}), 400
    return jsonify(eventos)

@socketio.on('connect')
def conectar():
    session_id = session.get('id')
    join_room(session_id)
    socketio.emit('atualizar_lista', fila.obter_usuarios())
    socketio.emit('atualizar_eventos', eventos)

@socketio.on('disconnect')
def desconectar():
    session_id = session.get('id')
    leave_room(session_id)
    fila.remover_usuario(session_id)
    socketio.emit('atualizar_lista', fila.obter_usuarios())

if __name__ == '__main__':
    socketio.run(app, debug=True)
