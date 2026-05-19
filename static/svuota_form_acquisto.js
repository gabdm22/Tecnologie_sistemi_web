window.addEventListener('pageshow', function(event){
    if(event.persisted){
        window.location.reload();
    }
    else{
        const form = document.getElementById('form_acquisto');
        if(form){
            form.reset();
        }
    }
});