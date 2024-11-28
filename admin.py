from flask import Blueprint, render_template, request, jsonify
from flask_socketio import SocketIO

admin_bp = Blueprint('admin', __name__)
socketio = None 

eventos = []


@admin_bp.route('/admin')
def admin_page():
    return render_template('admin.html')


@admin_bp.route('/eventos', methods=['GET', 'POST'])
def gerenciar_eventos():
    if request.method == 'POST':
        novo_evento = request.json
        nome = novo_evento.get('nome')
        vagas = novo_evento.get('vagas')
        if nome and isinstance(vagas, int) and vagas > 0:
            evento = {"nome": nome, "vagas": vagas}
            eventos.append(evento)
            if socketio:
                socketio.emit('atualizar_eventos', eventos)
            return jsonify({'status': 'success', 'evento': evento}), 200
        return jsonify({'status': 'error', 'message': 'Dados inválidos'}), 400
    return jsonify(eventos)




def init_socketio(sio):
    global socketio
    socketio = sio
