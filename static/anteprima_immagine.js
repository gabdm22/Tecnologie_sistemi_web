document.addEventListener('DOMContentLoaded', function(){
    const img_input = document.getElementById('file');
    const box_anteprima = document.getElementById('contenitore-anteprima');
    const img_anteprima = document.getElementById('immagine-anteprima');
    
    img_input.addEventListener('change', function(){
        if(this.files && this.files[0]){
            const file = this.files[0];
            const url_temp = URL.createObjectURL(file);
            img_anteprima.src = url_temp;
            box_anteprima.classList.add('attivo');

        }
        else{
            img_anteprima.src = '';
            box_anteprima.classList.remove('attivo');
        }
    });
});