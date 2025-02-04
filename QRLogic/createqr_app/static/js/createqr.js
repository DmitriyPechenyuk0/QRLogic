const InputSubstrate = document.querySelector('.input-substrate');
const inputPrimary = document.querySelector('.input-primary');
const pSubstrate = document.querySelector('.p-substrate');
const pPrimary = document.querySelector('.p-primary');
let labelPrimary = document.querySelector('.label-primary')
let labelSubstrate = document.querySelector('.label-substrate')


const defaultColor = InputSubstrate.value;
labelSubstrate.style.backgroundColor = defaultColor;
pSubstrate.textContent = defaultColor;

const defaultColor2 = inputPrimary.value;
labelPrimary.style.backgroundColor = defaultColor2;
pPrimary.textContent = defaultColor2;



InputSubstrate.addEventListener('input', () => {
    pSubstrate.textContent = InputSubstrate.value;
    labelSubstrate.style.backgroundColor = InputSubstrate.value;
});
inputPrimary.addEventListener('input', () => {
    pPrimary.textContent = inputPrimary.value;
    labelPrimary.style.backgroundColor = inputPrimary.value;
});