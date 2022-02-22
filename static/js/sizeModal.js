const sizeGuideButton = document.querySelector('#size-guide-btn');

// Only listen for clicks if product has size variants
if (sizeGuideButton) {
    const sizeModalBg = document.querySelector('.size.modal-background');
    const sizeModal = document.querySelector('.size.modal');
    const sizeModalButton = document.querySelector('.size.modal-close');

    sizeGuideButton.addEventListener('click', (e) => {
        e.preventDefault();
        sizeModal.classList.add('is-active');
    });
    sizeModalBg.addEventListener('click', (e) => {
        e.preventDefault();
        sizeModal.classList.remove('is-active');
    });
    sizeModalButton.addEventListener('click', (e) => {
        e.preventDefault();
        sizeModal.classList.remove('is-active');
    });
}