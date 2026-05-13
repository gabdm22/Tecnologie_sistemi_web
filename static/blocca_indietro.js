document.addEventListener("DOMContentLoaded", function() {
    window.history.pushState(null, document.title, window.location.href);
    // Aggiunge un listener per l'evento "popstate" per bloccare il comportamento predefinito del pulsante indietro
    window.addEventListener("popstate", function(event) {
        // reinserisce la stessa pagina nella cronologia per impedire l'effetto del pulsante indietro
        window.history.pushState(null, document.title, window.location.href);
        window.history.forward();
    });
});