const signInButton = document.querySelector('#sign_in');

// Only listen for clicks if user is not yet signed in
if (signInButton) {
    const modalBg = document.querySelector('.login.modal-background');
    const modal = document.querySelector('.login.modal');
    const modalButton = document.querySelector('.login.modal-close');

    signInButton.addEventListener('click', () => {
        modal.classList.add('is-active');
    });
    modalBg.addEventListener('click', () => {
        modal.classList.remove('is-active');
    });
    modalButton.addEventListener('click', () => {
        modal.classList.remove('is-active');
    });
}