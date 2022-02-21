const signInButton = document.querySelector('#sign_in');
const modalBg = document.querySelector('.modal-background');
const modal = document.querySelector('.modal');
const modalButton = document.querySelector('.modal-close');

signInButton.addEventListener('click', () => {
    modal.classList.add('is-active');
});
modalBg.addEventListener('click', () => {
    modal.classList.remove('is-active');
});
modalButton.addEventListener('click', () => {
    modal.classList.remove('is-active');
});