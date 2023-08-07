// Sign in form

const sendCodeButton = document.getElementById('send-code');
const phoneInput = document.getElementById('phone');

phoneInput.value = '+';
sendCodeButton.setAttribute('disabled', '');

const phone_subs = document.getElementById('phone_subs');
const phone_subs_text = phone_subs.innerText;

// Валидация номера телефона
phoneInput.addEventListener('input', function() {

    const phoneRegex = /^\+\d{11,15}$/;
    if (!phoneRegex.test(this.value)) {
        phone_subs.textContent = "Номер телефона должен содержать 12-16 символов и начинаться с '+'";
        sendCodeButton.setAttribute('disabled', '');       
    } else {    
        phone_subs.textContent = phone_subs_text;
        sendCodeButton.removeAttribute('disabled');
    }
});