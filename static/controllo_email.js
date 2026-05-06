function attivaControllo(idInput, nomeColonna) {
    const elemento = document.getElementById(idInput);
    const feedback = document.getElementById(idInput + '-feedback');

    elemento.addEventListener('blur', function() {
        const valoreInviato = this.value;

        if (valoreInviato.length > 0) {
            fetch('/verifica-unicita', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                // Qui mandiamo sia il nome del campo che il valore
                body: JSON.stringify({ campo: nomeColonna, valore: valoreInviato })
            })
            .then(res => res.json()) 
            .then(data => { 
                if (data.disponibile) {
                    feedback.textContent = "✅ Disponibile"; 
                    feedback.className = "feedback-text disponibile"; // classe css
                } else {
                    feedback.textContent = "❌ Già in uso";
                    feedback.className = "feedback-text errore"; 
                }
            });
        }
    });
}

attivaControllo('Email', 'email');
attivaControllo('Username', 'username');