document.getElementById('adicionar-evento').addEventListener('click', () => {
    const eventoInput = document.getElementById('evento-input');
    const evento = eventoInput.value.trim();
    if (evento) {
        fetch('/eventos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ evento }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                eventoInput.value = '';
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
                const li = document.createElement('li');
                li.textContent = evento;
                lista.appendChild(li);
            });
        });
}

window.onload = carregarEventos;
