window.addEventListener('pageshow', function(event) {
    const form = document.getElementById('login-form, registrazione-form');
    if (form) {
        form.reset(); // Resetta il form, svuotando tutti i campi, incluso quello della password
    }
});