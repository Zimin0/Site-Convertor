window.onload = function() {
    const codeField = document.getElementById('code');
    const errorMessage = document.querySelector('.subtitle');
    
    codeField.addEventListener('keyup', function() {
        // Регулярное выражение для проверки на 6 цифр
        const regex = /^\d{6}$/;
        const isCodeValid = regex.test(codeField.value);
        
        if (isCodeValid) {
            errorMessage.innerText = 'Код валиден!';
            errorMessage.style.color = 'green';
        } else {
            errorMessage.innerText = 'Код должен содержать ровно 6 цифр!';
            errorMessage.style.color = 'red';
        }
    });
}
