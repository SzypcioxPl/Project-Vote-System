// Zmienna globalna na przechowywanie listy projektów
let projects = [];
let currentProjectIndex = 0; // Indeks aktualnie wyświetlanego projektu

// Pobranie projektów z serwera
function loadProjects() {
    fetch('http://localhost:8000/voteapp/get_project_data/all')  // Użyj pełnego adresu URL
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
    const userId = 7; // Zakładamy przykładowe UID użytkownika, powinien być pobrany z sesji

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
