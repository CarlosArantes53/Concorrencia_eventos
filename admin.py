from flask import Blueprint, render_template, request, jsonify
from flask_socketio import SocketIO

# Criação do blueprint para administração
admin_bp = Blueprint('admin', __name__)
socketio = None  # Referência ao SocketIO será atribuída pelo app principal

# Lista para armazenar eventos
# eventos = [
#     {"nome": "Conhecendo Java", "vagas": 5},
#     {"nome": "IA Redragon", "vagas": 10},
#     {"nome": "Programação Reativa", "vagas": 5},
#     {"nome": "Privacidade e Segurança", "vagas": 10},
#     {"nome": "SAP Estrutural", "vagas": 40}
# ]

eventos = []


@admin_bp.route('/admin')
def admin_page():
    """Rota para a página de administração."""
    return render_template('admin.html')


@admin_bp.route('/eventos', methods=['GET', 'POST'])
def gerenciar_eventos():
    """Rota para gerenciar eventos."""
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
