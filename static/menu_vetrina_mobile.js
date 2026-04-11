document.addEventListener('DOMContentLoaded', function(){
    const hamburger = document.getElementById('hamburger');
    const menu = document.getElementById('menu');

    if(hamburger && menu){
        hamburger.addEventListener('click', function(){
            menu.classList.toggle('aperto')     /*toggle aggiunge la classe se non c'è, la toglie se c'è*/
        });
    }
});