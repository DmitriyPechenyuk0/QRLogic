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



document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.querySelector(".input-file-upload");
    const logoImage = document.querySelector(".logo-icon");

    fileInput.addEventListener("change", function () {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                logoImage.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.querySelector(".input-file-upload");
    const deleteButton = document.querySelector(".button-delete-logo");
    const logoImage = document.querySelector(".logo-icon");

    deleteButton.addEventListener("click", function (event) {
        event.preventDefault();
        fileInput.value = "";
        logoImage.src = "{% static '/images/No-Logo.png' %}";
    });
});