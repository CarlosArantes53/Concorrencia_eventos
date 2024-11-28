document.getElementById('adicionar-evento').addEventListener('click', () => {
    const nome = document.getElementById('evento-nome').value.trim();
    const vagas = parseInt(document.getElementById('evento-vagas').value, 10);

    if (nome && vagas > 0) {
        fetch('/eventos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, vagas }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.getElementById('evento-nome').value = '';
                document.getElementById('evento-vagas').value = '';
                carregarEventos();
            }
        });
    }
});

function carregarEventos() {
    fetch('/eventos')
        .then(response => response.json())
        .then(eventos => {
            const lista = document.getElementById('eventos-lista');
            lista.innerHTML = '';
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
}

window.onload = carregarEventos;
