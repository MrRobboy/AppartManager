function addApartment() {
    const url = document.getElementById('url').value;

    fetch('/add_apartment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        // Optionnel : Rafraîchir la liste des appartements après ajout
        loadApartments();
    })
    .catch(error => {
        console.error('Error adding apartment:', error);
        alert('Erreur lors de l\'ajout de l\'appartement: ' + error.message);
    });
}

function loadApartments() {
    fetch('/get_apartments')
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error('Network response was not ok: ' + response.status + ' - ' + text);
                });
            }
            return response.json();
        })
        .then(data => {
            const container = document.getElementById('appartements-attente');
            container.innerHTML = ''; // Réinitialiser le contenu

            data.forEach(appartement => {
                const card = document.createElement('div');
                card.className = 'appartement-card';
                card.innerHTML = `
                    <h3>${appartement.nom}</h3>
                    <p>Adresse: ${appartement.adresse}</p>
                    <p>Loyer: €${appartement.loyer}</p>
                    <p>Surface: ${appartement.surface} m²</p>
                    <p>Statut: ${appartement.statut}</p>
                `;
                container.appendChild(card);
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            alert('Erreur de chargement des appartements: ' + error.message);
        });
}

// Charger les appartements au démarrage
window.onload = loadApartments;
