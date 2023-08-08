// Sign in form
const sendCodeButton = document.getElementById('send-code');
const phoneInput = document.getElementById('phone');
const nameInput = document.getElementById('name');

sendCodeButton.setAttribute('disabled', '');

const phone_subs = document.getElementById('phone_subs');
const phone_subs_text = phone_subs.innerText;

function validatePhoneNumber(phoneValue) {
    const phoneRegex = /^\+\d{11,15}$/;
    return phoneRegex.test(phoneValue);
}

function updateValidationState(phoneValue) {
    if (!validatePhoneNumber(phoneValue)) {
        phone_subs.textContent = "Номер телефона должен содержать 12-16 символов и начинаться с '+'";
        sendCodeButton.setAttribute('disabled', '');       
    } else {    
        phone_subs.textContent = phone_subs_text;
        sendCodeButton.removeAttribute('disabled');
    }
}

// Вызываем проверку при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    updateValidationState(phoneInput.value);
});

// Валидация номера телефона при вводе
phoneInput.addEventListener('input', function() {
    updateValidationState(this.value);
});
