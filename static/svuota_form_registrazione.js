window.addEventListener('pageshow', function(event){
    if(event.persisted){
        window.location.reload();
    }
    else{
        const form = document.getElementById('registrazione-form');
        if(form){
            form.reset();
        }
    }
});