document.addEventListener('DOMContentLoaded', function(){
    const barra = document.getElementById('barra-ricerca');
    const opere = document.querySelectorAll('.riga_opera');

    barra.addEventListener('input', function(){
        const testo_cercato = barra.value.toLowerCase();

        opere.forEach(function(opera){
            const testo_opera = opera.innerText.toLowerCase();

            if(testo_opera.includes(testo_cercato)){
                opera.style.display = '';
            }
            else{
                opera.style.display = 'none';
            }
        });
    });
});