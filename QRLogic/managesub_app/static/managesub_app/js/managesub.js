const popup = document.querySelector('.popup')
const choicePlan = document.querySelector('.choice-plan')
const changeButton = document.querySelector('.change-button')
const closePopup = document.querySelector('.close-popup')
const cancelButton = document.querySelector('.cancel-button')
const popupCancel = document.querySelector('.popup-cancel')
const saveSub = document.querySelector('.save-sub')
const killSub = document.querySelector('.kill-sub')
const PopupEntercard = document.querySelector('.popup-entercard')
const buybuttons = document.querySelectorAll('.buy-now')

changeButton.addEventListener('click', () => {
    popup.classList.toggle('popup-opened')
})

closePopup.addEventListener('click', () => {
    popup.classList.toggle('popup-opened')
})

cancelButton.addEventListener('click', () => {
    popupCancel.classList.toggle('popup-cancel-opened')
} )

saveSub.addEventListener('click', () => {
    popupCancel.classList.toggle('popup-cancel-opened')
} )

killSub.addEventListener('click', () => {
    popupCancel.classList.toggle('popup-cancel-opened')
    
})

buybuttons.forEach(button => {
    button.addEventListener('click', () => {
        PopupEntercard.classList.toggle('popup-entercard-opened');
        popup.classList.toggle('popup-opened')
    });
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && popupCancel.classList.contains('popup-cancel-opened')) {
        popupCancel.classList.remove('popup-cancel-opened');
    }
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && PopupEntercard.classList.contains('popup-entercard-opened')) {
        PopupEntercard.classList.remove('popup-entercard-opened');
    }
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && popup.classList.contains('popup-opened')) {
        popup.classList.remove('popup-opened');
    }
});

document.getElementById('cardnumber').addEventListener('input', (event) => {
    let value = event.target.value;

    value = value.replace(/[^\d-]/g, '');

    let digitsOnly = value.replace(/\D/g, '');

    let formattedValue = '';
    for (let i = 0; i < digitsOnly.length; i++) {
        formattedValue += digitsOnly[i];

        if ((i + 1) % 4 === 0 && i + 1 < digitsOnly.length) {
            formattedValue += '-';
        }
    }
    if (formattedValue.length > 19) {
        formattedValue = formattedValue.slice(0, 19);
    }

    event.target.value = formattedValue;
});

document.getElementById('expiration-date').addEventListener('input', (event) => {
    let value = event.target.value;

    value = value.replace(/\D/g, '');

    let formattedValue = '';

    for (let i = 0; i < value.length; i++) {
        formattedValue += value[i];
        if (i === 1 && value.length > 2) {
            formattedValue += '/';
        }
    }
    if (formattedValue.length > 5) {
        formattedValue = formattedValue.slice(0, 5);
    }

    event.target.value = formattedValue;
});