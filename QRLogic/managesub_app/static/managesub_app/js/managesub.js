const popup = document.querySelector('.popup')
const choicePlan = document.querySelector('.choice-plan')
const changeButton = document.querySelector('.change-button')
const closePopup = document.querySelector('.close-popup')
const cancelButton = document.querySelector('.cancel-button')
const popupCancel = document.querySelector('.popup-cancel')

const saveSub = document.querySelector('.save-sub')
const killSub = document.querySelector('.kill-sub')

const PopupEntercardFree = document.querySelector('.free-entercard')
const PopupEntercardStandart = document.querySelector('.standart-entercard')
const PopupEntercardPro = document.querySelector('.pro-entercard')
const PopupEntercardCommerce = document.querySelector('.commerce-entercard')

const buttonFree = document.querySelector('.free-sub')
const buttonStandart = document.querySelector('.standart-sub')
const buttonPro = document.querySelector('.pro-sub')
const buttonCommerce = document.querySelector('.commerce-sub')

const freeCardNumber = document.querySelector('.cardnumber-free')
const standartCardNumber = document.querySelector('.cardnumber-standart')
const proCardNumber = document.querySelector('.cardnumber-pro')

const expirationFree = document.getElementById('expiration-date-free')
const expirationStandart = document.getElementById('expiration-date-standart')
const expirationPro = document.getElementById('expiration-date-pro')

const slotsOpener = document.querySelector('.buy-slots-button')
const overlay = document.querySelector('.overlay-slots')
const overlayDiv = document.querySelector('.slots-div')
const slotsClose = document.querySelector('.slots-close')
const offers = document.querySelectorAll('.offer-input')
let slotsInput = document.querySelector('.input-slots')
let slotsBuyButton = document.querySelector('.slots-buy-button')


let listExpiration = [expirationFree, expirationStandart, expirationPro]
let listCards = [freeCardNumber, standartCardNumber, proCardNumber]

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

buttonFree.addEventListener('click', () => {
    PopupEntercardFree.classList.toggle('popup-entercard-opened')
})

buttonStandart.addEventListener('click', () => {
    PopupEntercardStandart.classList.toggle('popup-entercard-opened')
})

buttonPro.addEventListener('click', () => {
    PopupEntercardPro.classList.toggle('popup-entercard-opened')
})

buttonCommerce.addEventListener('click', () => {
    PopupEntercardCommerce.classList.toggle('popup-entercard-opened')
})

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && popupCancel.classList.contains('popup-cancel-opened')) {
        popupCancel.classList.remove('popup-cancel-opened');
    }
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && popup.classList.contains('popup-opened')) {
        popup.classList.remove('popup-opened');
    }
});

listCards.forEach((input) => {
    if (input) {
        input.addEventListener('input', (event) => {
            let value = event.target.value.replace(/[^\d-]/g, '');

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
    }
});
listExpiration.forEach((input) => {
    if (input) {
        input.addEventListener('input', (event) => {
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
    }
});

slotsInput.addEventListener('input', () => {
    let slotsDollar = slotsInput.value * 0.10
    slotsBuyButton.innerHTML = `Buy ${slotsInput.value} for <b>${slotsDollar.toFixed(2)}$</b>`
})
slotsOpener.addEventListener('click', () => {
    overlay.classList.toggle('slots-opened')
    overlayDiv.classList.toggle('slots-opened')
})

slotsClose.addEventListener('click', () => { 
    overlay.classList.toggle('slots-opened')
    overlayDiv.classList.toggle('slots-opened')
})

offers.forEach((offer) => {
    offer.addEventListener('click', () => {
        slotsInput.value = offer.value;
        slotsInput.dispatchEvent(new Event('input'));
    });
});