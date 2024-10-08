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
    });
}

function loadApartments() {
    fetch('/get_apartments')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
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
        });
}


// Charger les appartements au démarrage
window.onload = loadApartments;
