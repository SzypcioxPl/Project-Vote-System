

// Obsługa tworzenia projektu
document.getElementById('projectForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const date_start = document.getElementById('date_start').value;
    const date_end = document.getElementById('date_end').value;
    const vote_scale = document.querySelector('input[name="vote_scale"]:checked').value;
    const status = document.getElementById('status').value;

    // Żądanie do endpointu tworzenia projektu
    fetch('/voteapp/create_project/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, date_start, date_end, vote_scale, status }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.PID) {
            alert("Projekt został pomyślnie utworzony!");
            // Możesz tutaj dodać przekierowanie lub inną akcję
        } else {
            alert("Wystąpił błąd podczas tworzenia projektu.");
        }
    })
    .catch(error => {
        console.error('Błąd:', error);
        alert("Wystąpił błąd. Spróbuj ponownie później.");
    });
});

// Pobieranie raportu dla konkretnego projektu
function downloadReport() {
    const pid = 1; // Przykładowy PID projektu, zmień na odpowiednie ID projektu
    window.location.href = `/voteapp/get_report/${pid}`;
}

