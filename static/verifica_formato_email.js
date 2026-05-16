document.addEventListener('DOMContentLoaded', function(){
    const email = document.getElementById('Email');
    const feedback = document.getElementById('Email-feedback');
    const btn_reg = document.getElementById('registrazione-btn');

    const regex_email = /^[a-z0-9.]+@[a-z0-9.-]+\.[a-z]{2,}$/; // Espressione regolare per il formato email

    email.addEventListener('input', function(){
        const valore = this.value.trim(); // Rimuove spazi bianchi all'inizio e alla fine

        if(!event.isTrusted) return;

        if(valore.length==0){
            feedback.textContent = ""; // Rimuove il messaggio di feedback se il campo è vuoto
            feedback.className = "feedback-text"; 
            return;
        }
        
        if(regex_email.test(valore)){
            feedback.textContent = "";
            feedback.className = "feedback-text disponibile";
        }
        else{
            feedback.textContent = "❌ Formato email non corretto";
            feedback.className = "feedback-text errore";
            btn_reg.disabled = true;
        }
    });
});