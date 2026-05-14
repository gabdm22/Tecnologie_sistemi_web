window.addEventListener('pageshow', function(event) {
    if(event.persisted){    // se l'utente torna con la freccia indietro ricarica la pagina
        window.location.reload();   // ricaricare la pagina fa scattare il "session.clear()" di flask chiamato l'end point "/form_login.html"
    }
    else {
        const form = document.getElementById('login-form')
        if(form){
            form.reset(); // Resetta il form, svuotando tutti i campi, incluso quello della password
        }
    }
});