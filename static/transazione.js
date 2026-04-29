document.addEventListener('DOMContentLoaded', function(){
    const form_acquisto = document.getElementById('form_acquisto');
    const btn_acquista = document.getElementById('acquista');

    if(form_acquisto){
        form_acquisto.addEventListener('submit', function(evento){
            evento.preventDefault();
            btn_acquista.innerHTML = 'Elaborazione in corso...';
            btn_acquista.style.backgroundColor = '#7f8c8d';
            btn_acquista.style.cursor = 'not-allowed';
            btn_acquista.disabled = true;

            setTimeout(function(){
                btn_acquista.innerHTML = 'Transazione approvata!';
                btn_acquista.style.backgroundColor = '#2e7d32';
            }, 1500);

            setTimeout(function(){
                form_acquisto.submit();
            }, 2500);
        });
    }
});