// Obsługa logowania użytkownika
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;

    // Żądanie do endpointu logowania
    fetch('http://localhost:8000/voteapp/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password, login }),
    })
    .then(response => {
        if (!response.ok) {
            // Jeśli status odpowiedzi nie jest OK (np. 401 Unauthorized)
            return response.json().then(errData => {
                throw new Error(errData.error || "Nieprawidłowy login lub hasło");
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.UID) {
            // Jeśli logowanie się powiodło, przejdź do strony głównej
            alert("Zalogowano pomyślnie!");
            window.location.href = "./vote.html";
        }
    })
    .catch(error => {
        console.error('Błąd:', error);
        alert(error.message);
    });
});