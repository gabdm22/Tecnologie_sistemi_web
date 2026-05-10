document.addEventListener('DOMContentLoaded', function(){
    const input = document.querySelectorAll('form input[type="text"], form input[type="email"], form input[type="password"]');
    const btn_reg = document.getElementById('registrazione-btn');

    const err_req = document.getElementById('avviso-password'); //errore di requisiti sulla password
    const err_coinc = document.getElementById('messaggio'); //errore di coincidenza tra password e conferma-password

    function checkGenerale(){
        let pieni = true;

        input.forEach(i=>{
            if(i.value.trim() ===''){
                pieni = false;
            }
        });

        // controlla se ci sono messaggi di errore. se è "none" allora è ok
        let req_ok = window.getComputedStyle(err_req).display=='none';
        let pass_ok = window.getComputedStyle(err_coinc).display=='none';

        if(pieni && req_ok && pass_ok){
            btn_reg.disabled = false;
            btn_reg.style.cursor = 'pointer';
            btn_reg.style.opacity = '1';
        }
        else{
            btn_reg.disabled = true;
            btn_reg.style.cursor = 'not-allowed';
            btn_reg.style.opacity = '0.5';
        }
    }

    // controlla tutto ad ogni inserimento
    input.forEach(i=>{
        i.addEventListener('input', checkGenerale);
    });


    // blocca tutto all'avvio
    if(btn_reg){
        checkGenerale();
    }
});