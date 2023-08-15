////////////////////////////////////////////////
//// Файл JS для главного шаблона base.html ////
////////////////////////////////////////////////

// Форма для выбора языка сайта //
document.addEventListener('DOMContentLoaded', function () {
    const languageForm = document.getElementById('language-form');
    const languageSelect = document.getElementById('language-select');

    languageSelect.addEventListener('change', function () {
        languageForm.submit();
    });
});
//////////////////////////////////

////// Блок с cookies //////
const cookiePopup = document.getElementById('cookie-popup');
document.addEventListener('DOMContentLoaded', function () {
    const cookiePopup = document.getElementById('cookie-popup');
    const cookieConfirmButton = document.getElementById('cookie-confirm');

    // Проверяем, была ли сохранена метка в локальном хранилище
    const isCookieConfirmed = localStorage.getItem('cookieConfirmed');

    if (isCookieConfirmed) {
        // Если метка есть, скрываем форму
        cookiePopup.style.display = 'none';
    } else {
        // Добавляем обработчик события нажатия на кнопку "Ясно"
        cookieConfirmButton.addEventListener('click', function () {
            // Деактивируем форму
            cookiePopup.style.display = 'none';
            // Сохраняем метку в локальное хранилище
            localStorage.setItem('cookieConfirmed', true);
        });
    }
});
////////////////////////////