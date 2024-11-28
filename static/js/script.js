const socket = io();
const sessionId = sessionStorage.getItem('session_id') || Math.random().toString(36).substr(2, 9);
sessionStorage.setItem('session_id', sessionId);

// Atualiza a lista de usuários na tabela
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

// Atualiza o status do usuário no cabeçalho
socket.on('atualizar_status', (data) => {
    const statusUsuario = document.getElementById('status-usuario');
    const totalUsuarios = document.getElementById('total-usuarios');
    statusUsuario.textContent = `Seu código: ${data.session_id} | Pessoas à sua frente: ${data.pessoas_a_frente}`;
    totalUsuarios.textContent = `Total de usuários logados: ${data.total_usuarios}`;
});

// Atualiza o timer do usuário atual
socket.on('atualizar_timer', (data) => {
    document.getElementById('usuario-atual').textContent = data.usuario_atual;
    document.getElementById('timer').textContent = data.timer;
});

// Atualiza os eventos na tabela
socket.on('atualizar_eventos', (eventos) => {
    const lista = document.getElementById('eventos-lista');
    lista.innerHTML = ''; // Limpa a tabela atual
    eventos.forEach(evento => {
        const row = document.createElement('tr');
        
        const cellNome = document.createElement('td');
        const cellVagas = document.createElement('td');
        
        cellNome.textContent = evento.nome;
        cellVagas.textContent = evento.vagas;

        row.appendChild(cellNome);
        row.appendChild(cellVagas);
        lista.appendChild(row);
    });
});
