// Sign in form


function openSignIn() {
    phoneForm.style.display = 'block';
    codeForm.style.display = 'none';

    const signInForm = document.getElementById('sign_in-form');
    const body = document.getElementsByTagName('body')[0];

    if(signInBtn.innerText == 'Регистрация'){
        signInForm.style.display = 'flex';
        signInBtn.innerText = 'Закрыть';
        signInBtn.classList.add('close');
        body.style.overflowY = 'hidden';
    } else {
        signInForm.style.display = 'none';
        signInBtn.innerText = 'Регистрация';
        signInBtn.classList.remove('close');
        body.style.overflowY = 'scroll';
    }
}

function sendCode() { 
    // Вызывается при нажатии "Отправить код" в 1й форме
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const phoneInput = document.getElementById('phone');
    const phone = phoneInput.value; // введенный номер телефона
    const phoneRegex = /^\+\d{11}$/;
    const phone_subs = document.getElementById('phone_subs');

    if (!phoneRegex.test(phone)) {
        phone_subs.textContent = "Номер телефона должен содержать 12 символов и начинаться с '+'";
        this.setAttribute('disabled', '');
        this.style.color = '#4f4db1';
        this.style.backgroundColor = 'white';
        return; // Если номер телефона не прошел валидацию, прекратить выполнение функции
    } else {
        phone_subs.textContent = "Укажите номер телефона для регистрации";
        this.removeAttribute('disabled');
        this.style.color = '';
        this.style.backgroundColor = '';
    }
    
    // Выводить форму подтверждения номера телефона 
    phoneForm.style.display = 'none';
    codeForm.style.display = 'block';
    // Отправить POST-запрос с номером телефона
    fetch('users/phone/' + phone + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ phone: phone })
    })
}

// Создание массива паролей
const passwords = ['830009', '398092', '781964', '861423', '782200', '225356', '824265', '664697', '242403', '518711'];
const confirmBtn = document.getElementById('conf-code-but');
confirmBtn.addEventListener('click', sendConfirmationCode);

function sendConfirmationCode() {
    const subtitle = document.getElementById('subtitle-field');
    // Функция отсылает введенный пользователем код 
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const codeInput = document.getElementById('code');
    const code = codeInput.value;
    

    // Проверка, есть ли введенный код в массиве паролей
    if (passwords.includes(code)) {
        // Если код есть в массиве, выводим новую форму
        subtitle.textContent = "Телефон подтвержден!";
        const closeButton = document.createElement('input'); // создать новую кнопку
        closeButton.type = 'submit';
        closeButton.value = 'Закрыть';
        closeButton.classList.add('confirm-btn'); // добавить класс для стилизации
        closeButton.style.marginTop = '10px'; // добавить отступ сверху
        closeButton.addEventListener('click', openSignIn); // добавить обработчик событий для закрытия формы
        codeForm.appendChild(closeButton); // добавить кнопку в форму
        confirmBtn.setAttribute('disabled', '');
        confirmBtn.style.display = 'none'; // скрыть кнопку подтверждения
    } else {
        // Если кода нет в массиве, выводим сообщение об ошибке
        subtitle.textContent = "Введен неверный код. Попробуйте еще раз.";
    }

    // Отправить POST-запрос с кодом подтверждения
    fetch('users/check/' + code + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ code: code })
    });
}





const signInBtn = document.getElementsByClassName('sign_in-btn')[0];
signInBtn.addEventListener('click', openSignIn);

const codeBtn = document.getElementById('send-code');
codeBtn.addEventListener('click', sendCode);

const phoneForm = document.getElementById('phone-field');
const codeForm = document.getElementById('code-field');

// File form

function highlightDropZone(event) {
    event.preventDefault();
    this.classList.add('drop');
}

function unHighlightDropZone(event) {
    event.preventDefault();
    this.classList.remove('drop');
}

function addFile1(name) {
    const addLogo_1 = document.getElementById('add-file-1');
    const addTitle_1 = document.getElementById('add-file-title-1');

    addLogo_1.style.display = 'none';
    addTitle_1.innerText = name;

    isFile1 = true;

    if(isFile1 && isFile2){
        converterBtn.removeAttribute('disabled');
    }
}

function addFile2(name) {
    const addLogo_2 = document.getElementById('add-file-2');
    const addTitle_2 = document.getElementById('add-file-title-2');

    addLogo_2.style.display = 'none';
    addTitle_2.innerText = name;

    isFile2 = true;

    if(isFile1 && isFile2){
        converterBtn.removeAttribute('disabled');
    }
}

function enableDownload() {
    downloadBtn.removeAttribute('disabled');
}

var isFile1 = false;
var isFile2 = false;

const converterBtn = document.getElementById('converter-btn');
const downloadBtn = document.getElementById('download-btn');
converterBtn.setAttribute('disabled', "");
converterBtn.addEventListener('click', enableDownload);

const dropFile_1 = document.getElementById('file-field-1');
const dropFile_2 = document.getElementById('file-field-2');


if (dropFile_1) {
    const fileInput_1 = document.getElementById('file_1');
    fileInput_1.value = null;

    dropFile_1.addEventListener('dragover', highlightDropZone);
    dropFile_1.addEventListener('dragenter', highlightDropZone);
    dropFile_1.addEventListener('dragleave', unHighlightDropZone);
    dropFile_1.addEventListener('drop', (event) => {
        const file_1 = event.dataTransfer.files;
        unHighlightDropZone.call(dropFile_1, event);
        
        fileInput_1.files = file_1;
        addFile1(file_1[0].name);
    });

    fileInput_1.addEventListener('change', (event) => {
        const file_1 = event.target.files;
        addFile1(file_1[0].name);
    })
}

if (dropFile_2) {
    const fileInput_2 = document.getElementById('file_2'); 
    fileInput_2.value = null;

    dropFile_2.addEventListener('dragover', highlightDropZone);
    dropFile_2.addEventListener('dragenter', highlightDropZone);
    dropFile_2.addEventListener('dragleave', unHighlightDropZone);
    dropFile_2.addEventListener('drop', (event) => {
        const file_2 = event.dataTransfer.files;
        unHighlightDropZone.call(dropFile_2, event)

        fileInput_2.files = file_2;
        addFile2(file_2[0].name);
    });

    fileInput_2.addEventListener('change', (event) => {
        const file_2 = event.target.files;
        addFile2(file_2[0].name);
    })
}




const sendCodeButton = document.getElementById('send-code');
const phoneInput = document.getElementById('phone');
const phone_subs = document.getElementById('phone_subs')

// Валидация номера телефона
phoneInput.addEventListener('input', function() {
    
    const phoneRegex = /^\+\d{11}$/;
    if (!phoneRegex.test(this.value)) {
        phone_subs.textContent = "Номер телефона должен содержать 12 символов и начинаться с '+'";
        sendCodeButton.setAttribute('disabled', '');
        sendCodeButton.style.color = '#4f4db1';
        sendCodeButton.style.backgroundColor = 'white'; // измените цвет фона на желаемый 
    } else {    
        phone_subs.textContent = "Укажите номер телефона для регистрации";
        sendCodeButton.removeAttribute('disabled');
        sendCodeButton.style.color = ''; // сбросить цвет текста
        sendCodeButton.style.backgroundColor = ''; // сбросить цвет фона
    }
});


