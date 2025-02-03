const InputSubstrate = document.querySelector('.input-substrate');
const inputPrimary = document.querySelector('.input-primary');
const pSubstrate = document.querySelector('.p-substrate');
const pPrimary = document.querySelector('.p-primary');

InputSubstrate.addEventListener('input', () => {
    pSubstrate.textContent = InputSubstrate.value;
});
inputPrimary.addEventListener('input', () => {
    pPrimary.textContent = inputPrimary.value;
});