// Assurez-vous d'attendre que le DOM soit chargé
$(document).ready(function () {
    // Obtenez la référence vers l'image
    var videoFeed = document.getElementById('video-feed');

    // Créez une fonction pour mettre à jour l'image
    function updateImage() {
        // Modifiez l'URL de l'image pour forcer le rafraîchissement
        videoFeed.src = "{{ url_for('webcam') }}?" + new Date().getTime();
    }

    // Définissez l'intervalle de rafraîchissement en millisecondes
    var refreshInterval = 1000; // par exemple, rafraîchir toutes les secondes

    // Mettez à jour l'image périodiquement
    var intervalId = setInterval(updateImage, refreshInterval);

    // Ajoutez le gestionnaire d'événements pour le bouton d'arrêt
    $("#stop-button").click(function () {
        // Arrêtez la mise à jour de l'image en désactivant l'intervalle
        clearInterval(intervalId);
    });
});
