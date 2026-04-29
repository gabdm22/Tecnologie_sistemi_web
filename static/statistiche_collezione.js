document.addEventListener('DOMContentLoaded', function(){
    const prezzi = document.querySelectorAll('.prezzo-pagato');
    let somma = 0;

    prezzi.forEach(p => {
        let testo = p.innerText;
        let prezzo_pulito = testo.replace(/[^\d.]/g, '');   //toglie tutto tranne numeri e punti
        let valore = parseFloat(prezzo_pulito);
        if(!isNaN(valore)){
            somma+=valore;
        }
    });

    document.getElementById('numero-opere').innerText = prezzi.length;

    const display_tot = document.getElementById('totale-collezione');
    let valore_iniziale = 0;
    const anim = 300   //durata animazione
    const incremento = somma / (anim/16);
    
    const timer = setInterval(()=>{
        valore_iniziale += incremento;
        if(valore_iniziale>=somma){
            display_tot.innerText = somma.toFixed(2) + '€';
            clearInterval(timer);
        }
        else{
            display_tot.innerText = valore_iniziale.toFixed(2) + '€';
        }
    }, 16);
});