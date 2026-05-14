function attivaControllo(idInput, nomeColonna) {
    const elemento = document.getElementById(idInput); // query al dom per prendere l'input
    const feedback = document.getElementById(idInput + '-feedback'); // query al dom per prendere il div del feedback

    elemento.addEventListener('blur', function() {
        const valoreInviato = this.value.trim(); // prendo il valore dell'input

        if (valoreInviato.length > 0) {
            fetch('/verifica-unicita', { //chiamata al server per verificare l'unicità tramite fetch api nativa js
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }, // specifica che stiamo inviando json
                // Qui mandiamo sia il nome del campo che il valore
                body: JSON.stringify({ campo: nomeColonna, valore: valoreInviato })
            })
            .then(res => res.json()) // convertiamo la risposta in json
            .then(data => {     // data è l'oggetto restituito dal server, che contiene la proprietà "disponibile"
                if (data.disponibile) {
                    feedback.textContent = "✅ Disponibile"; 
                    feedback.className = "feedback-text disponibile"; // classe css
                } else {
                    feedback.textContent = "❌ Già in uso";
                    feedback.className = "feedback-text errore"; 
                }
            });
        }
        else{
            feedback.textContent = "";
            feedback.className = "feedback-test";
        }
    });
}

attivaControllo('Email', 'email');
attivaControllo('Username', 'username');