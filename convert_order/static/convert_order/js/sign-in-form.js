// Sign in form

const sendCodeButton = document.getElementById('send-code');
const phoneInput = document.getElementById('phone');

phoneInput.value = null;
sendCodeButton.setAttribute('disabled', '');

const phone_subs = document.getElementById('phone_subs')

// Валидация номера телефона
phoneInput.addEventListener('input', function() {

    const phoneRegex = /^\+\d{11}$/;
    if (!phoneRegex.test(this.value)) {
        phone_subs.textContent = "Номер телефона должен содержать 12 символов и начинаться с '+'";
        sendCodeButton.setAttribute('disabled', '');
        sendCodeButton.style.marginTop = "3%";        
    } else {    
        phone_subs.textContent = "Укажите номер телефона для регистрации";
        sendCodeButton.removeAttribute('disabled');
        sendCodeButton.style.marginTop = "6%";    
    }
});