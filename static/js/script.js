const socket = io();
const sessionId = sessionStorage.getItem('session_id') || Math.random().toString(36).substr(2, 9);
sessionStorage.setItem('session_id', sessionId);

socket.on('atualizar_lista', (usuarios) => {
    const lista = document.getElementById('lista-usuarios');
    lista.innerHTML = ''; // Limpa a tabela atual
    usuarios.forEach(usuario => {
        const row = document.createElement('tr');

        const cellIndice = document.createElement('td');
        const cellUsuario = document.createElement('td');
        const cellHorario = document.createElement('td');
        
        cellIndice.textContent = usuario.indice;
        cellUsuario.textContent = usuario.id;
        cellHorario.textContent = usuario.horario;

        row.appendChild(cellIndice);
        row.appendChild(cellUsuario);
        row.appendChild(cellHorario);

        if (usuario.id === sessionId) {
            row.classList.add('current-session');
        }

        lista.appendChild(row);
    });
});

socket.on('atualizar_timer', (data) => {
    document.getElementById('usuario-atual').textContent = data.usuario_atual;
    document.getElementById('timer').textContent = data.timer;
});

socket.on('atualizar_eventos', (eventos) => {
    const lista = document.getElementById('eventos-lista');
    lista.innerHTML = '';
    eventos.forEach(evento => {
        const li = document.createElement('li');
        li.textContent = evento;
        lista.appendChild(li);
    });
});
