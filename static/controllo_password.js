document.addEventListener('DOMContentLoaded', function(){
    const pass1 = document.getElementById('pass1');
    const reg_btn = document.getElementById('registrazione-btn');
    const avviso = document.getElementById('avviso-password'); // Prende l'elemento già esistente!

    pass1.addEventListener('input', function(){
        const password = pass1.value;
        const requisiti = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

        if (password.length > 0 && !requisiti.test(password)){
            avviso.style.display = 'block';
            reg_btn.disabled = true;
            reg_btn.style.opacity = '0.5';
            reg_btn.style.cursor = 'not-allowed';
        } else {
            avviso.style.display = 'none';
            /*reg_btn.disabled = false;
            reg_btn.style.opacity = '1';
            reg_btn.style.cursor = 'pointer';*/
        }
    });
});
function toggleVisibility(inputId, spanElement) {
    const inputField = document.getElementById(inputId);
    const iconImg = spanElement.querySelector('img');
    if (inputField.type === "password") {
        inputField.type = "text";
        iconImg.src = "/static/occhio_sbarrato.svg"; 
        iconImg.alt = "Nascondi password"; 
    } else {
        inputField.type = "password";
        iconImg.src = "/static/occhio.svg"; 
        iconImg.alt = "Mostra password";
    }
}