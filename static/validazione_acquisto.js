document.addEventListener('DOMContentLoaded', function(){
    const form = document.getElementById('form_acquisto');
    const nome = document.getElementById('nome_cognome');
    const titolare = document.getElementById('titolare');
    const indirizzo = document.getElementById('indirizzo'); 
    const carta = document.getElementById('numero_carta');
    const scadenza = document.getElementById('scadenza');
    const feedback = document.getElementById('feedback-scadenza');
    const cvv = document.getElementById('cvv');
    const btn_acq = document.getElementById('acquista');

    if(form && carta && cvv && btn_acq){
        function controllaPagamento(){
            let soloNumeri = carta.value.replace(/\D/g, '');// rimuove tutti i caratteri non numerici

            carta.value = soloNumeri.replace(/(.{4})/g, '$1 ').trim();  // inserisce spaziatura ogni 4 caratteri


            let cartaValida = (soloNumeri.length==16);
            let cvvValido = (cvv.value.length==3 && !isNaN(cvv.value)); 

            //contro validità carta dal numero
            if(soloNumeri==''){
                carta.classList.remove('input-successo', 'input-errore'); 
            }
            else if(cartaValida){
                carta.classList.remove('input-errore'); 
                carta.classList.add('input-successo');
            }
            else{
                carta.classList.remove('input-successo');
                carta.classList.add('input-errore');
            }


            //controllo validità carta dal cvv
            if(cvv.value==''){
                cvv.classList.remove('input-successo', 'input-errore');
            }
            else if(cvvValido){
                cvv.classList.remove('input-errore');
                cvv.classList.add('input-successo');
            }
            else{
                cvv.classList.remove('input-successo');
                cvv.classList.add('input-errore');
            }

            let scadenzaValida = false;
            let valore_scad = scadenza.value;
            if(valore_scad!=''){
                const scad = valore_scad.split('-');
                const anno = parseInt(scad[0], 10);
                const mese = parseInt(scad[1], 10);

                const oggi = new Date();
                const anno_curr = oggi.getFullYear();
                const mese_curr = oggi.getMonth() + 1;

                if(anno>anno_curr || anno==anno_curr && mese>=mese_curr){
                    scadenzaValida = true;
                }
            }

            if(valore_scad==''){
                scadenza.classList.remove('input-successo', 'input-errore');
                if(feedback){
                    feedback.textContent = '';
                    feedback.className = 'feedback-text'
                }
            }
            else if(scadenzaValida){
                scadenza.classList.remove('input-errore');
                scadenza.classList.add('input-successo');
                if(feedback){
                    feedback.textContent = '';
                    feedback.className = 'feedback-text disponibile'
                }
            }
            else{
                scadenza.classList.remove('input-successo');
                scadenza.classList.add('input-errore');
                if(feedback){
                    feedback.textContent = '❌ La carta è scaduta';
                    feedback.className = 'feedback-text errore'
                }
            }

            let nomeValido = nome.checkValidity(); //controllo validità nome e cognome
            let titolareValido = titolare.checkValidity();//controllo validità titolare
            let indirizzoValido = indirizzo.checkValidity();//controllo validità indirizzo

            //sblocco l'acquisto se entrambi rispettano il formato
            if(nomeValido && titolareValido && indirizzoValido && scadenzaValida && cartaValida && cvvValido){
                btn_acq.disabled = false;
                btn_acq.style.cursor = 'pointer';
                btn_acq.style.opacity = '1';
            }
            else{
                btn_acq.disabled = true;
                btn_acq.style.cursor = 'not-allowed';
                btn_acq.style.opacity = '0.5'
            }
        }

        form.addEventListener('input', controllaPagamento);
    }
});