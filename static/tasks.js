// Fonction pour ajouter une tâche
function addTask() {
    const taskInput = document.getElementById('new-task');
    const taskText = taskInput.value.trim();

    if (taskText) {
        fetch('/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: taskText })
        })
        .then(response => response.json())
        .then(() => {
            loadTasks();
            taskInput.value = '';
        });
    }
}

// Ajouter un écouteur d'événements pour le bouton "Add Task"
document.getElementById('add-task-btn').addEventListener('click', addTask);

// Ajouter un écouteur d'événements pour le bouton "Clear List"
document.getElementById('clear-tasks-btn').addEventListener('click', function() {
    const taskList = document.getElementById('task-list');
    const tasks = taskList.querySelectorAll('li');
    tasks.forEach(task => {
        const taskId = task.getAttribute('data-id');
        deleteTask(taskId);
    });
});

// Ajouter un écouteur d'événements pour le champ de saisie pour la touche "Enter"
document.getElementById('new-task').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Empêche le comportement par défaut du formulaire
        addTask();
    }
});

// Fonction pour charger les tâches
function loadTasks() {
    fetch('/tasks/all')
    .then(response => response.json())
    .then(tasks => {
        const taskList = document.getElementById('task-list');
        taskList.innerHTML = ''; // Vide la liste actuelle
        tasks.forEach(task => {
            const li = document.createElement('li');
            li.textContent = task.title; // Affiche le titre de la tâche
            li.setAttribute('data-id', task.id); // Assigne l'ID de la tâche

            // Ajout du bouton de suppression
            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Delete';
            deleteBtn.addEventListener('click', () => {
                const taskId = li.getAttribute('data-id'); // Récupère l'ID de la tâche
                deleteTask(taskId); // Appelle la fonction pour supprimer la tâche
            });

            li.appendChild(deleteBtn);
            taskList.appendChild(li);
        });
    });
}

// Fonction pour supprimer une tâche
function deleteTask(taskId) {
    if (taskId) { // Assurez-vous que l'ID de la tâche est valide
        fetch(`/tasks/${taskId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(() => {
            loadTasks(); // Recharge la liste des tâches après suppression
        })
        .catch(error => console.error('Error:', error));
    } else {
        console.error('Task ID is null or undefined');
    }
}

// Charger les tâches au chargement de la page
loadTasks();
