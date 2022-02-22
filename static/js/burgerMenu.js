const burgerMenu = document.querySelector('#burger-menu');
const navbar = document.querySelector('#main-navbar');

burgerMenu.addEventListener('click', () => {
    burgerMenu.classList.toggle('is-active');
    navbar.classList.toggle('is-active');
});