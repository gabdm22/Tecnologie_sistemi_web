document.addEventListener('DOMContentLoaded', function(){
    const navbar = document.querySelector('.navbar');

    if(navbar){
        window.addEventListener('scroll', function(){
            if(this.window.scrollY>60){
                navbar.classList.add('scrolled');
            }
            else if(this.window.scrollY<=10){
                navbar.classList.remove('scrolled');
            }
        });
    }
});