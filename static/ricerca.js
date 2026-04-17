document.addEventListener('DOMContentLoaded', function(){
    const barra = document.getElementById('barra-ricerca');
    const opere = document.querySelectorAll('.riga_opera');

    barra.addEventListener('input', function(){
        const testo_cercato = barra.value.toLowerCase();    /* prende il testo dalla barra di ricerca (in minuscolo) */

        opere.forEach(function(opera){  /* cicla sulle opere */
            const testo_opera = opera.innerText.toLowerCase();  /* prende il testo dalle opere (in minuscolo) */

            if(testo_opera.includes(testo_cercato)){    // se l'opera contiene il testo_cercato allora non fa nulla
                opera.style.display = '';
            }
            else{                               // altrimenti non la visualizza (display='none')
                opera.style.display = 'none';
            }
        });
    });
});