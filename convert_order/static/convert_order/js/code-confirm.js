window.onload = function() {
    const codeField = document.getElementById('code');
    const errorMessage = document.querySelector('.subtitle');
    const confirmCodeButton = document.getElementById('conf-code-but');

    codeField.value = null;
    confirmCodeButton.setAttribute('disabled', '');
    
    codeField.addEventListener('keyup', function() {
        // Регулярное выражение для проверки на 6 цифр
        const regex = /^\d{4}$/;
        const isCodeValid = regex.test(codeField.value);
        
        if (isCodeValid) {
            errorMessage.innerText = 'Код валиден!';
            errorMessage.style.color = 'green';

            confirmCodeButton.removeAttribute('disabled');
        } else {
            errorMessage.innerText = 'Код должен содержать ровно 4 цифры!';
            errorMessage.style.color = 'red';

            confirmCodeButton.setAttribute('disabled', '');
        }
    });
}