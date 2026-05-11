const form = document.querySelector('#login-form'); // Seleziona il form di login
const errorBox = document.getElementById('error-box'); 

form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Impedisce il ricaricamento della pagina

    const formData = new FormData(form); // Crea un oggetto FormData con i dati del form
    
    // Invio asincrono
    const response = await fetch('/login', {  //chimata al server per il login
        method: 'POST',
        body: formData
    });

    const data = await response.json(); 

    if (data.success) {
        // Se il login è OK, reindirizziamo manualmente
        window.location.href = data.redirect;
    } else {
        // Se c'è un errore, lo mostriamo dinamicamente
        errorBox.textContent = data.message;
        errorBox.style.display = 'block';
        document.querySelector('input[name="password"]').value = ''; // Pulisce il campo password
    }
});