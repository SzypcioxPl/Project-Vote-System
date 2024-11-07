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

// Zmienna globalna na przechowywanie listy projektów
let projects = [];
let currentProjectIndex = 0; // Indeks aktualnie wyświetlanego projektu

// Pobranie projektów z serwera
function loadProjects() {
    fetch('/voteapp/get_project_data/all')  // Endpoint pobierający wszystkie projekty
        .then(response => response.json())
        .then(data => {
            projects = Object.values(data);  // Konwertowanie obiektu na tablicę
            displayProject(currentProjectIndex);  // Wyświetlenie pierwszego projektu
        })
        .catch(error => console.error('Błąd przy pobieraniu projektów:', error));
}

// Wyświetlanie projektu na podstawie indeksu
function displayProject(index) {
    const project = projects[index];
    const projectCard = document.getElementById('projectCard');

    projectCard.innerHTML = `
        <h3>${index + 1}. ${project.name}</h3>
        <p>${project.description}</p>
        <p>OCENA: <span class="stars">${generateStars(project.vote_scale)}</span></p>
        <p>LICZBA ODDANYCH GŁOSÓW: ${project.votes}</p>
    `;
}

// Funkcja generująca gwiazdki na podstawie skali głosów
function generateStars(voteScale) {
    return '★'.repeat(voteScale / 5);
}

// Przewijanie do poprzedniego projektu
function showPreviousProject() {
    if (currentProjectIndex > 0) {
        currentProjectIndex--;
        displayProject(currentProjectIndex);
    }
}

// Przewijanie do następnego projektu
function showNextProject() {
    if (currentProjectIndex < projects.length - 1) {
        currentProjectIndex++;
        displayProject(currentProjectIndex);
    }
}

// Oddawanie głosu
function submitVote() {
    const projectId = projects[currentProjectIndex].PID;
    const userId = 1; // Zakładamy przykładowe UID użytkownika, powinien być pobrany z sesji

    fetch('/voteapp/vote/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ PID: projectId, UID: userId, value: 1 }),  // Zakładamy wartość głosu 1
    })
    .then(response => response.json())
    .then(data => {
        if (data.VID) {
            alert("Głos został oddany!");
            loadProjects();  // Odświeżenie listy projektów po oddaniu głosu
        } else {
            alert("Wystąpił błąd przy oddawaniu głosu.");
        }
    })
    .catch(error => console.error('Błąd:', error));
}

// Funkcja uruchamiana po załadowaniu strony
window.onload = loadProjects;
