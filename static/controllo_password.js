document.addEventListener('DOMContentLoaded', function(){
    const pass1 = document.getElementById('pass1');
    const reg_btn = document.getElementById('registrazione-btn');

    const avviso = document.createElement('div');
    avviso.style.color = '#e67e22';
    avviso.style.fontSize = '0.85rem';
    avviso.style.marginTop = '-18px';
    avviso.style.marginBottom = '25px';
    avviso.style.display = 'none';
    avviso.innerText = 'La password deve avere: min 8 caratteri di cui 1 maiuscola, 1 minuscola, 1 numero';

    pass1.parentNode.insertBefore(avviso, pass1.nextSibling);

    pass1.addEventListener('input', function(){
        const password = pass1.value;
        const requisiti = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

        if (password.length>0 && !requisiti.test(password)){
            avviso.style.display = 'block';
            reg_btn.disabled = true;
            reg_btn.style.opacity = '0.5';
            reg_btn.style.cursor = 'not-allowed';
        }
        else{
            avviso.style.display = 'none';
            reg_btn.disabled = false;
            reg_btn.style.opacity = '1';
            reg_btn.style.cursor = 'pointer';
        }
    });
});