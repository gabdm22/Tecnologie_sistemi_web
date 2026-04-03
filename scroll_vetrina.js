document.addEventListener('DOMContentLoaded', function(){
    const navbar = document.querySelector('.navbar');

    if(navbar){
        window.addEventListener('scroll', function(){
            if(this.window.scrollY>50){
                navbar.classList.add('scrolled');
            }
            else{
                navbar.classList.remove('scrolled');
            }
        });
    }
});