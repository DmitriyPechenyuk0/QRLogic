const InputSubstrate = document.querySelector('.input-substrate');
const inputPrimary = document.querySelector('.input-primary');
const pSubstrate = document.querySelector('.p-substrate');
const pPrimary = document.querySelector('.p-primary');
let labelPrimary = document.querySelector('.label-primary')
let labelSubstrate = document.querySelector('.label-substrate')
const fileInput = document.querySelector(".input-file-upload");
const logoImage = document.querySelector(".logo-icon");
const deleteButton = document.querySelector(".button-delete-logo");
const defaultColor = InputSubstrate.value;
const defaultColor2 = inputPrimary.value;
const rangeInput = document.querySelector('.sizeqr');
const label = document.querySelector('.sizeqrlabel');

labelSubstrate.style.backgroundColor = defaultColor;
pSubstrate.textContent = defaultColor;

labelPrimary.style.backgroundColor = defaultColor2;
pPrimary.textContent = defaultColor2;

rangeInput.addEventListener('input', () => {
  label.textContent = rangeInput.value;
});

InputSubstrate.addEventListener('input', () => {
    pSubstrate.textContent = InputSubstrate.value;
    labelSubstrate.style.backgroundColor = InputSubstrate.value;
});
inputPrimary.addEventListener('input', () => {
    pPrimary.textContent = inputPrimary.value;
    labelPrimary.style.backgroundColor = inputPrimary.value;
});

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            logoImage.style.border = "1px solid black"
            logoImage.style.borderRadius = "2px"
            logoImage.src = event.target.result;
        };
        reader.readAsDataURL(file);
    }
});

deleteButton.addEventListener("click", (event) => {
    event.preventDefault();
    fileInput.value = "";
    logoImage.style.border = "none"
    logoImage.style.borderRadius = "0px"
    logoImage.src = logoImage.dataset.noLogo;
});
