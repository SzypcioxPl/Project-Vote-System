document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const surname = document.getElementById('surname').value;
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;

    // Wysłanie danych do endpointu rejestracji
    fetch('/voteapp/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, surname, login, password, role }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.UID) {
            alert("Rejestracja zakończona sukcesem!");
            window.location.href = "/login"; // Przekierowanie na stronę logowania po rejestracji
        } else {
            alert("Wystąpił błąd przy rejestracji: " + JSON.stringify(data));
        }
    })
    .catch(error => {
        console.error('Błąd:', error);
        alert("Wystąpił błąd. Spróbuj ponownie później.");
    });
});
