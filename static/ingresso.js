document.addEventListener('DOMContentLoaded', function(){
    const elem = document.querySelectorAll('.elemento-animato');    // elemento che deve essere animato
    
    elem.forEach(function(elemento, indice){
        const ritardo = indice*200; // ritardo di 200ms tra un elemento e l'altro

        setTimeout(function(){
            elemento.classList.add('elemento-visibile')
        }, ritardo);
    });
});