document.addEventListener('DOMContentLoaded', function(){
    const form = document.getElementById('form_acquisto');
    const nome = document.getElementById('nome_cognome');
    const titolare = document.getElementById('titolare');
    const indirizzo = document.getElementById('indirizzo'); 
    const carta = document.getElementById('numero_carta');
    const scadenza = document.getElementById('scadenza');
    const cvv = document.getElementById('cvv');
    const btn_acq = document.getElementById('acquista');

    if(form && carta && cvv && btn_acq){
        function controllaPagamento(){
            let soloNumeri = carta.value.replace(/\D/g, '');

            carta.value = soloNumeri.replace(/(.{4})/g, '$1 ').trim();


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

            
            let nomeValido = nome.checkValidity();
            let titolareValido = titolare.checkValidity();
            let indirizzoValido = indirizzo.checkValidity();
            let scadenzaValida = scadenza.checkValidity();

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