document.addEventListener('DOMContentLoaded', function(){
    const lightbox = document.getElementById('lightbox');
    const lightbox_img = document.getElementById('lightbox-img');
    const btn_chiudi = document.querySelector('.chiudi-lightbox');

    /* seleziona tutte le immagini delle opere */
    const immagini_opere = document.querySelectorAll('.immagine_opera img');

    /* applica a tutte le immagini questo evento, se cliccate si attiva la lightbox (che aveva display='none') */
    immagini_opere.forEach(img=>{
        img.addEventListener('click', function(){
            lightbox_img.src = this.src;
            lightbox.style.display = 'flex';
        });
    });

    /* quando clicco sulla X in alto a destra si chiude lo zoom */
    btn_chiudi.addEventListener('click', function(){
        lightbox.style.display = 'none';
    });

    /* quando clicco al di fuori dell'immagine si chiude lo zoom, cioè se clicco sullo sfondo nero */
    lightbox.addEventListener('click', function(event){
        if(event.target===lightbox){
            lightbox.style.display = 'none';
        }
    })
});