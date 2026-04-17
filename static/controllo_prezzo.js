document.addEventListener('DOMContentLoaded', function(){
    const prezzo = document.getElementById('prezzo');
    const mess = document.getElementById('errore-prezzo');

    prezzo = addEventListener('blur', function(){
        let valore = parseFloat(prezzo.value);

        if(!prezzo.value){
            prezzo.classList.remove('input-invalido', 'input-valido');
            mess.classList.remove('attivo');
            return;
        }

        if(isNaN(valore) || valore<=0){
            prezzo.classList.add('input-invalido');
            prezzo.classList.remove('input-valido');
            mess.classList.add('attivo');
            prezzo.value = ''
        }
        else{
            prezzo.value = valore.toFixed(2);
            prezzo.classList.remove('input-invalido');
            prezzo.classList.add('input-valido');
            mess.classList.remove('attivo');
        }
    });

    prezzo.addEventListener('input', function(e){
        if(prezzo.value<0){
            prezzo.value = '';
        }
    });
});