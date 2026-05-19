window.addEventListener('pageshow', function(event){
    if(event.persisted){
        window.location.reload();
    }
    else{
        const form = document.getElementById('form');
        const anteprima = document.getElementById('immagine-anteprima');
        const contenitore = document.getElementById('contenitore-anteprima');
        if(form){
            form.reset();

            if(anteprima && contenitore){
                anteprima.src = '';
                contenitore.style.display = 'none';
            }
        }
    }
});