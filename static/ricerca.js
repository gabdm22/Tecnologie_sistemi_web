document.addEventListener('DOMContentLoaded', function(){
    const barra = document.getElementById('barra-ricerca');
    const filtro = document.getElementById('filtro-categoria');
    const opere = document.querySelectorAll('.riga_opera');

    function aggiornaVetrina(){
        const testo_cercato = barra.value.toLowerCase();    /* prende il testo dalla barra di ricerca (in minuscolo) */
        const cat_cercata = filtro.value.toLowerCase();

        opere.forEach(function(opera){  /* cicla sulle opere */
            const titolo = opera.querySelector('.nome_opera').innerText.toLowerCase();  /* prende il testo dalle opere (in minuscolo) */

            const dettagli = opera.querySelectorAll('.dettaglio');  // i dettagli sono autore [0], categoria [1], dimensioni[2]
            const autore = dettagli[0].innerText.toLowerCase();
            const categoria = dettagli[1].innerText.toLowerCase();

            const testo_ok = (testo_cercato==='') || titolo.includes(testo_cercato) || autore.includes(testo_cercato);
            const categoria_ok = (cat_cercata==='tutte') || categoria.includes(cat_cercata);

            if(testo_ok && categoria_ok){    // se l'opera contiene il testo_cercato allora non fa nulla
                opera.style.display = '';
            }
            else{                               // altrimenti non la visualizza (display='none')
                opera.style.display = 'none';
            }
        });
    }
    
    barra.addEventListener('input', aggiornaVetrina);
    filtro.addEventListener('change', aggiornaVetrina);
});