document.addEventListener('DOMContentLoaded', function() {
    const pass1 = document.getElementById('pass1');
    const pass2 = document.getElementById('pass2');
    const btn_reg = document.getElementById('registrazione-btn');
    const messaggio = document.getElementById('messaggio');
    
    if(pass1 && pass2 && btn_reg){
        function controllaPassword(){
            if(pass2.value==''){
                pass2.classList.remove('input-errore', 'input-successo');
                messaggio.style.display = 'none';
                btn_reg.disabled = true;
                return;
            }

            if(pass1.value==pass2.value){
                pass2.classList.remove('input-errore');
                pass2.classList.add('input-successo');
                messaggio.style.display = 'none';
                btn_reg.disabled = false;
                btn_reg.style.cursor = 'pointer';
                btn_reg.style.opacity = '1';
            }
            else{
                pass2.classList.remove('input-successo');
                pass2.classList.add('input-errore');
                messaggio.style.display = 'block';
                btn_reg.disabled = true;
                btn_reg.style.cursor = 'not allowed';
                btn_reg.style.opacity = '0.5';
            }
        }

        pass1.addEventListener('input', controllaPassword);
        pass2.addEventListener('input', controllaPassword);
    }
});