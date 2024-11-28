const socket = io();
const sessionId = sessionStorage.getItem('session_id') || Math.random().toString(36).substr(2, 9);
sessionStorage.setItem('session_id', sessionId);

let pessoasAFrenete = -1;

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
socket.on('atualizar_status', (data) => {
    const statusUsuario = document.getElementById('status-usuario');
    const totalUsuarios = document.getElementById('total-usuarios');
    pessoasAFrenete = data.pessoas_a_frente;

    // Adicionando estilo inline
    statusUsuario.innerHTML = `<span style="font-weight: bold; color: blue;">Seu código:</span> ${data.session_id} | <span style="color: green;">Pessoas à sua frente:</span> ${data.pessoas_a_frente}`;
    totalUsuarios.innerHTML = `<span style="color: red;">Total de usuários logados:</span> ${data.total_usuarios}`;

    // Atualiza os botões de reserva
    atualizarBotaoReserva();
});

// // Atualiza o timer do usuário atual
// socket.on('atualizar_timer', (data) => {
//     document.getElementById('usuario-atual').textContent = data.usuario_atual;
//     document.getElementById('timer').textContent = data.timer;
// });


socket.on('atualizar_timer', (data) => {
    const usuarioAtual = document.getElementById('usuario-atual');
    const timer = document.getElementById('timer');

    // Atualiza o usuário atual com estilos
    usuarioAtual.innerHTML = `<span style="font-weight: bold; color: blue;"></span> ${data.usuario_atual}`;

    // Atualiza o timer com estilos animados
    timer.innerHTML = `
        <span style="font-size: 1.5rem; font-weight: bold; color: green; text-shadow: 0 0 5px #00ff00;">
            ${data.timer}
        </span>
    `;
});


// Atualiza os eventos na tabela e adiciona botões de reserva
socket.on('atualizar_eventos', (eventos) => {
    const lista = document.getElementById('eventos-lista');
    lista.innerHTML = ''; // Limpa a tabela atual
    eventos.forEach(evento => {
        const row = document.createElement('tr');

        const cellNome = document.createElement('td');
        const cellVagas = document.createElement('td');
        const cellAcao = document.createElement('td');

        cellNome.textContent = evento.nome;
        cellVagas.textContent = evento.vagas;

        // Criação do botão de reserva
        const botaoReserva = document.createElement('button');
        botaoReserva.textContent = 'Reservar';
        botaoReserva.dataset.evento = evento.nome; // Associar evento ao botão
        botaoReserva.disabled = true; // Desabilitado inicialmente
        botaoReserva.addEventListener('click', () => reservarEvento(evento.nome));

        cellAcao.appendChild(botaoReserva);

        row.appendChild(cellNome);
        row.appendChild(cellVagas);
        row.appendChild(cellAcao);
        lista.appendChild(row);
    });

    atualizarBotaoReserva();
});





// Atualiza o estado dos botões de reserva com base na posição do usuário na fila
function atualizarBotaoReserva() {
    const botoes = document.querySelectorAll('#eventos-lista button');
    botoes.forEach(botao => {
        botao.disabled = pessoasAFrenete > 2; // Habilita somente se houver 2 ou menos pessoas na frente
    });
}

// Lida com o processo de reserva
function reservarEvento(evento) {
    const nome = prompt('Digite seu nome:');
    const telefone = prompt('Digite seu telefone:');
    if (nome && telefone) {
        fetch('/reservar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({evento, nome, telefone}),
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(`Reserva feita para o evento "${evento}"!`);
                } else {
                    alert(`Erro ao fazer a reserva: ${data.message}`);
                }
            });
    }
}
