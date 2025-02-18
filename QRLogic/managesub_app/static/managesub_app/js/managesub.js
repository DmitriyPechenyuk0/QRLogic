const popup = document.querySelector('.popup')
const choicePlan = document.querySelector('.choice-plan')
const changeButton = document.querySelector('.change-button')
const closePopup = document.querySelector('.close-popup')
const cancelButton = document.querySelector('.cancel-button')
const popupCancel = document.querySelector('.popup-cancel')
const saveSub = document.querySelector('.save-sub')
const killSub = document.querySelector('.kill-sub')

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


function showNotification() {
    let notification = document.getElementById("notification");
    let progressBar = notification.querySelector(".progress-bar");

    progressBar.style.animation = "none";
    void progressBar.offsetWidth;
    progressBar.style.animation = "progress 3s linear forwards";
    

    notification.style.top = "-200px";
    notification.style.display = "flex";
    
    setTimeout(() => {
        notification.style.transition = "top 0.5s cubic-bezier(0.25, 0.1, 0.25, 1)";
        notification.style.top = "100px";
    }, 10);
    
    setTimeout(() => {
        notification.style.top = "-200px";
        setTimeout(() => {
            notification.style.display = "none";
        }, 300);
    }, 3000);
}